from django.shortcuts import render
from django.utils import timezone
from django.shortcuts import get_object_or_404, redirect, render
from .models import (
    Attivita,
    Cliente,
    Contatto,
    Offerta,
    Progetto,
    RuoloDipendente,
    StatoAttivita,
    StatoOfferta,
    StatoProgetto,
)
from decimal import Decimal, InvalidOperation
from django.urls import reverse

# get_object_or_404 cerca il contatto. Se non esiste, o è eliminato, risponde 404.


# filter(eliminato=False) tiene fuori i contatti segnati come eliminati. render consegna quell’elenco al template.#
def elenco_contatti(request):
    contatti = Contatto.objects.filter(eliminato=False).order_by("cognome", "nome")
    # render legge il template, ci mette l'elenco e restituisce la pagina HTML.
    # ids_clienti serve a non mostrare Rendi cliente se il collegamento esiste già.
    ids_clienti = Cliente.objects.values_list("contatto_id", flat=True)
    return render(
        request,
        "contatti/elenco.html",
        {"contatti": contatti, "ids_clienti": ids_clienti},
    )


# Elenco dei clienti non eliminati. Il cliente nasce dal contatto, non da questa pagina.
def elenco_clienti(request):
    clienti = Cliente.objects.filter(eliminato=False).order_by("nome", "cognome")
    return render(
        request,
        "contatti/elenco_clienti.html",
        {"clienti": clienti},
    )


def scheda_contatto(request, contatto_id):
    contatto = get_object_or_404(Contatto, pk=contatto_id, eliminato=False)
    # first() restituisce il cliente collegato, oppure None se il contatto non lo è.
    cliente = Cliente.objects.filter(contatto=contatto, eliminato=False).first()
    return render(
        request,
        "contatti/scheda.html",
        {"contatto": contatto, "cliente": cliente},
    )


# Segna il contatto come eliminato. La riga resta nel database.
def elimina_contatto(request, contatto_id):
    contatto = get_object_or_404(Contatto, pk=contatto_id, eliminato=False)
    if request.method == "POST":
        contatto.eliminato = True
        contatto.eliminato_il = timezone.now()
        contatto.save()
    return redirect("elenco_contatti")


# Il POST della finestra di conferma crea il cliente una sola volta.
def rendi_cliente(request, contatto_id):
    contatto = get_object_or_404(Contatto, pk=contatto_id, eliminato=False)
    if (
        request.method == "POST"
        and not Cliente.objects.filter(contatto=contatto).exists()
    ):
        Cliente.objects.create(
            contatto=contatto,
            nome=contatto.nome,
            cognome=contatto.cognome,
            email=contatto.email,
            telefono=contatto.telefono,
            indirizzo="",
            citta="",
            provincia="",
            cap="",
        )
    return redirect("elenco_contatti")


# Un solo salvataggio: senza contatto_id crea, con contatto_id aggiorna.
def salva_contatto(request):
    if request.method != "POST":
        return redirect("elenco_contatti")
    nome = request.POST.get("nome", "").strip()
    cognome = request.POST.get("cognome", "").strip()
    if not nome or not cognome:
        return redirect("elenco_contatti")
    dati = {
        "nome": nome,
        "cognome": cognome,
        "email": request.POST.get("email", "").strip(),
        "telefono": request.POST.get("telefono", "").strip(),
        "note": request.POST.get("note", "").strip(),
    }
    contatto_id = request.POST.get("contatto_id", "").strip()
    if contatto_id:
        contatto = get_object_or_404(Contatto, pk=contatto_id, eliminato=False)
        for campo, valore in dati.items():
            setattr(contatto, campo, valore)
        contatto.save()
    else:
        Contatto.objects.create(**dati)
    return redirect("elenco_contatti")


# Scheda cliente: dati a sinistra, progetti offerte e attività a destra.
def scheda_cliente(request, cliente_id):
    cliente = get_object_or_404(Cliente, pk=cliente_id, eliminato=False)
    # progetto__cliente risale dal progetto fino a questo cliente.
    progetti = Progetto.objects.filter(cliente=cliente, eliminato=False).select_related(
        "stato"
    )
    offerte = Offerta.objects.filter(
        progetto__cliente=cliente, eliminato=False
    ).select_related("stato", "progetto")
    attivita = Attivita.objects.filter(
        progetto__cliente=cliente, eliminato=False
    ).select_related("stato", "progetto", "dipendente")
    return render(
        request,
        "contatti/scheda_cliente.html",
        {
            "cliente": cliente,
            "progetti": progetti,
            "offerte": offerte,
            "attivita": attivita,
            "stati_offerta": StatoOfferta.objects.order_by("nome"),
        },
    )


# Crea un progetto per questo cliente. Lo stato iniziale è sempre 1, In corso.
def salva_progetto(request, cliente_id):
    cliente = get_object_or_404(Cliente, pk=cliente_id, eliminato=False)
    if request.method == "POST":
        titolo = request.POST.get("titolo", "").strip()
        if titolo:
            Progetto.objects.create(
                cliente=cliente,
                titolo=titolo,
                descrizione=request.POST.get("descrizione", "").strip(),
                stato_id=1,
            )
    return redirect("scheda_cliente", cliente_id=cliente.pk)


# Crea l'offerta sul progetto scelto. Lo stato iniziale è sempre 1, Bozza.
def salva_offerta(request, cliente_id):
    cliente = get_object_or_404(Cliente, pk=cliente_id, eliminato=False)
    if request.method == "POST":
        progetto = get_object_or_404(
            Progetto,
            pk=request.POST.get("progetto_id"),
            cliente=cliente,
            eliminato=False,
        )
        titolo = request.POST.get("titolo", "").strip()
        try:
            # La virgola diventa punto, così 1000,50 è un importo valido.
            importo = Decimal(request.POST.get("importo", "").strip().replace(",", "."))
        except InvalidOperation:
            importo = None
        if titolo and importo is not None:
            Offerta.objects.create(
                progetto=progetto,
                titolo=titolo,
                importo=importo,
                stato_id=1,
            )
    destinazione = reverse("scheda_cliente", args=[cliente.pk])
    return redirect(f"{destinazione}?tab=offerte")


# Aggiorna lo stato. Se il nome è Accettata e l'attività non c'è ancora, la crea una volta sola.
def aggiorna_stato_offerta(request, cliente_id, offerta_id):
    cliente = get_object_or_404(Cliente, pk=cliente_id, eliminato=False)
    offerta = get_object_or_404(
        Offerta,
        pk=offerta_id,
        progetto__cliente=cliente,
        eliminato=False,
    )
    if request.method == "POST":
        stato = get_object_or_404(StatoOfferta, pk=request.POST.get("stato_id"))
        offerta.stato = stato
        offerta.save()
        if (
            stato.nome == "Accettata"
            and not Attivita.objects.filter(offerta=offerta).exists()
        ):
            Attivita.objects.create(
                offerta=offerta,
                progetto=offerta.progetto,
                titolo=offerta.titolo,
                descrizione="",
                stato_id=1,
            )
    destinazione = reverse("scheda_cliente", args=[cliente.pk])
    tab = "attivita" if offerta.stato.nome == "Accettata" else "offerte"
    return redirect(f"{destinazione}?tab={tab}")


# Pagina iniziale. I riquadri con i numeri si aggiungono dopo.
def dashboard(request):
    return render(request, "contatti/dashboard.html")


# Pagina provvisoria per una voce di menu che non ha ancora l'elenco.
def sezione(request, titolo):
    return render(request, "contatti/sezione.html", {"titolo": titolo})

    # Ruoli e stati hanno solo il nome: una vista basta per le quattro pagine.


IMPOSTAZIONI = {
    "ruoli": (RuoloDipendente, "Ruoli dipendenti"),
    "stati-progetto": (StatoProgetto, "Stati progetto"),
    "stati-offerta": (StatoOfferta, "Stati offerta"),
    "stati-attivita": (StatoAttivita, "Stati attività"),
}


def elenco_impostazione(request, chiave):
    modello, titolo = IMPOSTAZIONI[chiave]
    if request.method == "POST":
        nome = request.POST.get("nome", "").strip()
        voce_id = request.POST.get("voce_id", "").strip()
        if nome and voce_id:
            # voce_id presente: aggiorna la riga già salvata.
            voce = get_object_or_404(modello, pk=voce_id)
            voce.nome = nome
            voce.save()
        elif nome:
            modello.objects.create(nome=nome)
        return redirect(request.path)
    voci = modello.objects.order_by("nome")
    return render(
        request,
        "contatti/impostazioni.html",
        {"titolo": titolo, "voci": voci},
    )

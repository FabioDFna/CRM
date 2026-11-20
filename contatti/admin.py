from django.contrib import admin

#importazione dei modelli



# Register your models here.
from .models import Contatto, RuoloDipendente, Dipendente, Cliente, StatoProgetto, Progetto, StatoOfferta, Offerta, StatoAttivita, Attivita
from django.utils import timezone
from django.contrib.auth import get_user_model #per ottenere il modello di utente
from django.core.mail import send_mail #per inviare email
from django.db import transaction #per eseguire transazioni
from django.utils.crypto import get_random_string #per generare stringhe casuali
from django.contrib import messages
from django.http import Http404
from django.middleware.csrf import get_token
from django.shortcuts import redirect
from django.urls import path, reverse
from django.utils.html import format_html, format_html_join


#classe per le impostazioni. has_module_permission decide se il modello compare nell’indice. Restituendo False sparisce dal riquadro Contatti e anche dalla barra a sinistra.
class ImpostazioneAdmin(admin.ModelAdmin):
    def has_module_permission(self, request):
        return False

admin.site.register(RuoloDipendente, ImpostazioneAdmin)
admin.site.register(StatoProgetto, ImpostazioneAdmin)
admin.site.register(StatoOfferta, ImpostazioneAdmin)
admin.site.register(StatoAttivita, ImpostazioneAdmin)

#classe per il tracciamento dei cambiamenti
class TracciamentoAdmin(admin.ModelAdmin):
    exclude = (
        "creato_il",
        "modificato_il",
        "eliminato_il",
        "creato_da",
        "modificato_da",
        "eliminato_da",
        "eliminato",
    )
    #metodo per salvare il modello
    def save_model(self, request, obj, form, change):
        if not change:
            obj.creato_da = request.user
        obj.modificato_da = request.user
        super().save_model(request, obj, form, change)

    #metodo per eliminare il modello
    def delete_model(self, request, obj):
        obj.eliminato=True
        obj.eliminato_il=timezone.now()
        obj.eliminato_da=request.user
        obj.save()
        
    
    def delete_queryset(self, request, queryset):
        queryset.update(
            eliminato=True,
            eliminato_il=timezone.now(),
            eliminato_da=request.user,
        )

    #metodo per ottenere il queryset
    def get_queryset(self, request):
        return super().get_queryset(request).filter(eliminato=False)

#classe per la creazione dell'utente e l'invio dell'email di accesso
#if not change vale solo per l'inserimento. In modifica non si crea un secondo account e non si cambia la password. create_user scrive la riga in auth_user. obj.utente = user mette l'id nel dipendente. transaction.atomic annulla anche l'utente se il salvataggio del dipendente fallisce. send_mail parte dopo, così l'email non esce se il salvataggio non è riuscito#

class DipendenteAdmin(TracciamentoAdmin):
    exclude = TracciamentoAdmin.exclude + ("utente",)

    def save_model(self, request, obj, form, change):
        password = None
        if not change:
            password = get_random_string(length=12)
            User = get_user_model()
            with transaction.atomic():
                obj.utente = User.objects.create_user(
                    username=obj.email,
                    email=obj.email,
                    password=password,
                    is_staff=True,

                )
                super().save_model(request, obj, form, change)
        else:
            super().save_model(request, obj, form, change)

        if password:
            send_mail(
                "Accesso al CRM",
                f"Per entrare usa questa email: {obj.email} e questa password: {password}",
                "crm@localhost",
                [obj.email],
            )


#rendi_cliente aggiunge la colonna nell’elenco. Il bottone apre la finestra <dialog> già nel browser: Annulla la chiude, Conferma invia il form. rendi_cliente_view crea il cliente copiando nome, cognome, email e telefono dal contatto e salva il collegamento. Indirizzo, città, provincia e CAP restano vuoti: li compili aprendo il cliente dopo. readonly_fields mostra il contatto sulla scheda già creata, come testo, senza tendina. has_add_permission toglie Aggiungi cliente.#

class ContattoAdmin(TracciamentoAdmin):
    list_display = ("__str__", "email", "telefono", "rendi_cliente")

    def changelist_view(self, request, extra_context=None):
        self._request = request
        return super().changelist_view(request, extra_context)

    def rendi_cliente(self, obj):
        if Cliente.objects.filter(contatto=obj).exists():
            return "Già cliente"
        url = reverse("admin:contatti_contatto_rendi_cliente", args=[obj.pk])
        return format_html(
            """
            <button type="button" class="button"
                onclick="document.getElementById('rendi-{id}').showModal()">
                Rendi cliente
            </button>
            <dialog id="rendi-{id}">
                <form method="post" action="{url}">
                    <input type="hidden" name="csrfmiddlewaretoken" value="{token}">
                    <p>Creare il cliente per {nome}?</p>
                    <button type="submit" class="button">Conferma</button>
                    <button type="button" class="button"
                        onclick="this.closest('dialog').close()">Annulla</button>
                </form>
            </dialog>
            """,
            id=obj.pk,
            url=url,
            token=get_token(self._request),
            nome=f"{obj.nome} {obj.cognome}",
        )
    rendi_cliente.short_description = "Cliente"

    def get_urls(self):
        urls = super().get_urls()
        mie = [
            path(
                "<path:object_id>/rendi-cliente/",
                self.admin_site.admin_view(self.rendi_cliente_view),
                name="contatti_contatto_rendi_cliente",
            ),
        ]
        return mie + urls

    def rendi_cliente_view(self, request, object_id):
        contatto = self.get_object(request, object_id)
        if contatto is None:
            raise Http404
        if request.method == "POST" and not Cliente.objects.filter(contatto=contatto).exists():
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
                creato_da=request.user,
                modificato_da=request.user,
            )
            self.message_user(request, "Cliente creato.")
        else:
            self.message_user(request, "Questo contatto è già un cliente.", level=messages.WARNING)
        return redirect("admin:contatti_contatto_changelist")

class ClienteAdmin(TracciamentoAdmin):
    readonly_fields = ("contatto",)

    def has_add_permission(self, request):
        return False

#obj is None significa che stai creando il progetto: stato viene tolto dal form. obj.stato_id = 1 lo imposta su In corso prima del salvataggio. Aprendo un progetto già esistente, obj c’è, quindi la tendina resta e lo stato si può cambiare.#

class ProgettoAdmin(TracciamentoAdmin):
    def get_exclude(self, request, obj=None):
        esclusi = super().get_exclude(request, obj)
        if obj is None:
            return esclusi + ("stato",)
        return esclusi

    def save_model(self, request, obj, form, change):
        if not change:
            obj.stato_id = 1
        super().save_model(request, obj, form, change)


#obj is None toglie lo stato dal form di inserimento. obj.stato_id = 1 scrive Bozza prima del salvataggio. 
#Il primo if vale solo per l’offerta nuova e le mette Bozza. Dopo il salvataggio si legge lo stato: se il nome è Accettata e non esiste già un’attività per quell’offerta, ne viene creata una. Titolo e progetto sono quelli dell’offerta. Lo stato dell’attività è Da fare. Il dipendente resta vuoto: si assegna al passo successivo.#

class OffertaAdmin(TracciamentoAdmin):
    def get_exclude(self, request, obj=None):
        esclusi = super().get_exclude(request, obj)
        if obj is None:
            return esclusi + ("stato",)
        return esclusi

    def save_model(self, request, obj, form, change):
        if not change:
            obj.stato_id = 1
        super().save_model(request, obj, form, change)
        if obj.stato.nome == "Accettata" and not Attivita.objects.filter(offerta=obj).exists():
            Attivita.objects.create(
                offerta=obj,
                progetto=obj.progetto,
                titolo=obj.titolo,
                descrizione="",
                stato_id=1,
                creato_da=request.user,
                modificato_da=request.user,
            )


#assegna disegna il bottone e la finestra. Dentro c’è un menu con i dipendenti non eliminati. Conferma invia l’id scelto a assegna_view, che scrive quel dipendente sull’attività e mette lo stato a 2. Annulla chiude la finestra senza salvare.#
class AttivitaAdmin(TracciamentoAdmin):
    list_display = ("titolo", "progetto", "dipendente", "stato", "assegna")

    def changelist_view(self, request, extra_context=None):
        self._request = request
        return super().changelist_view(request, extra_context)

    def assegna(self, obj):
        if obj.dipendente_id:
            return f"{obj.dipendente.nome} {obj.dipendente.cognome}"
        url = reverse("admin:contatti_attivita_assegna", args=[obj.pk])
        opzioni = format_html_join(
            "",
            '<option value="{}">{}</option>',
            (
                (dipendente.pk, f"{dipendente.nome} {dipendente.cognome}")
                for dipendente in Dipendente.objects.filter(eliminato=False)
            ),
        )
        return format_html(
            """
            <button type="button" class="button"
                onclick="document.getElementById('assegna-{id}').showModal()">
                Assegna
            </button>
            <dialog id="assegna-{id}">
                <p>Assegna «{titolo}» a:</p>
                <select name="dipendente-{id}" required>{opzioni}</select>
                <button type="submit" class="button" formaction="{url}">Conferma</button>
                <button type="button" class="button"
                    onclick="this.closest('dialog').close()">Annulla</button>
            </dialog>
            """,
            id=obj.pk,
            url=url,
            titolo=obj.titolo,
            opzioni=opzioni,
        )

    assegna.short_description = "Assegnata"

    def get_urls(self):
        urls = super().get_urls()
        mie = [
            path(
                "<path:object_id>/assegna/",
                self.admin_site.admin_view(self.assegna_view),
                name="contatti_attivita_assegna",
            ),
        ]
        return mie + urls

    def assegna_view(self, request, object_id):
        attivita = self.get_object(request, object_id)
        if attivita is None:
            raise Http404
        dipendente = None
        if request.method == "POST":
            dipendente = Dipendente.objects.filter(
                pk=request.POST.get(f"dipendente-{attivita.pk}"),
                eliminato=False,
            ).first()
        if dipendente is None:
            self.message_user(request, "Scegli un dipendente.", level=messages.WARNING)
        else:
            attivita.dipendente = dipendente
            attivita.stato_id = 2
            attivita.modificato_da = request.user
            attivita.save()
            self.message_user(request, "Attività assegnata.")
        return redirect("admin:contatti_attivita_changelist")

admin.site.register(Attivita, AttivitaAdmin)
admin.site.register(Contatto, ContattoAdmin)
admin.site.register(Cliente, ClienteAdmin)
admin.site.register(Dipendente, DipendenteAdmin)
admin.site.register(Progetto, ProgettoAdmin)
admin.site.register(Offerta, OffertaAdmin)

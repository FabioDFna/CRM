from django.urls import path
from . import views

# Indirizzi dell'app contatti.
# path vuoto: /contatti/ chiama la vista elenco_contatti.
# Il nome serve per ritrovare questo indirizzo dal codice, senza scriverlo a mano.
urlpatterns = [
    path("", views.elenco_contatti, name="elenco_contatti"),
    # <int:contatto_id> prende il numero nell'indirizzo, per esempio 1 in /contatti/1/.
    path("<int:contatto_id>/", views.scheda_contatto, name="scheda_contatto"),
    # Il modulo dell'elenco invia qui sia il contatto nuovo sia la modifica.
    path("salva/", views.salva_contatto, name="salva_contatto"),
    # /contatti/1/elimina/ riceve la conferma e lo segna come eliminato.
    path("<int:contatto_id>/elimina/", views.elimina_contatto, name="elimina_contatto"),
    # /contatti/1/rendi-cliente/ riceve la conferma e crea il cliente.
    path("<int:contatto_id>/rendi-cliente/", views.rendi_cliente, name="rendi_cliente"),
    # /contatti/clienti/3/ è la scheda del cliente 3.
    path("clienti/<int:cliente_id>/", views.scheda_cliente, name="scheda_cliente"),
    # /contatti/clienti/3/progetto/ riceve il titolo e crea il progetto di quel cliente.
    path(
        "clienti/<int:cliente_id>/progetto/",
        views.salva_progetto,
        name="salva_progetto",
    ),
    # /contatti/clienti/3/offerta/ crea l'offerta sul progetto indicato nel modulo.
    path(
        "clienti/<int:cliente_id>/offerta/", views.salva_offerta, name="salva_offerta"
    ),
    # /contatti/clienti/3/offerta/8/stato/ cambia lo stato dell'offerta 8.
    path(
        "clienti/<int:cliente_id>/offerta/<int:offerta_id>/stato/",
        views.aggiorna_stato_offerta,
        name="aggiorna_stato_offerta",
    ),
    # Elenchi ancora vuoti: il menu ha già la voce, la pagina vera arriva dopo.
    path("progetti/", views.sezione, {"titolo": "Progetti"}, name="elenco_progetti"),
    path("offerte/", views.sezione, {"titolo": "Offerte"}, name="elenco_offerte"),
    path("attivita/", views.sezione, {"titolo": "Attività"}, name="elenco_attivita"),
    path(
        "dipendenti/", views.sezione, {"titolo": "Dipendenti"}, name="elenco_dipendenti"
    ),
    # Pagine del sito per ruoli e stati. Non passano dall'admin.
    path(
        "impostazioni/ruoli/",
        views.elenco_impostazione,
        {"chiave": "ruoli"},
        name="impostazioni_ruoli",
    ),
    path(
        "impostazioni/stati-progetto/",
        views.elenco_impostazione,
        {"chiave": "stati-progetto"},
        name="impostazioni_stati_progetto",
    ),
    path(
        "impostazioni/stati-offerta/",
        views.elenco_impostazione,
        {"chiave": "stati-offerta"},
        name="impostazioni_stati_offerta",
    ),
    path(
        "impostazioni/stati-attivita/",
        views.elenco_impostazione,
        {"chiave": "stati-attivita"},
        name="impostazioni_stati_attivita",
    ),
    # /contatti/clienti/ è l'elenco. /contatti/clienti/3/ resta la scheda.
    path("clienti/", views.elenco_clienti, name="elenco_clienti"),
]

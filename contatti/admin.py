# Questa pagina non crea tabelle e non salva i dati.
# Dice all'admin di Django quali modelli mostrare nel menu.
# Per ogni modello registrato Django prepara da solo l'elenco,
# il form di inserimento, la modifica e il pulsante Elimina.
# Nel form compaiono i campi modificabili del modello.
# creato_il e modificato_il restano fuori: li compila Django al salvataggio.
# creato_da, modificato_da, eliminato, eliminato_il e eliminato_da
# compaiono ancora, perché qui sotto non sono nascosti e non vengono
# riempiti con l'utente connesso. Quella parte va aggiunta in questa pagina.

from django.contrib import admin

# Classi scritte in contatti/models.py.
from .models import Contatto, RuoloDipendente, Dipendente, Cliente, StatoProgetto, Progetto, StatoOfferta, Offerta, StatoAttivita, Attivita
# Ogni riga aggiunge quella tabella al menu dell'admin.
admin.site.register(Contatto)
admin.site.register(RuoloDipendente)
admin.site.register(Dipendente)
admin.site.register(Cliente)
admin.site.register(StatoProgetto)
admin.site.register(Progetto)
admin.site.register(StatoOfferta)
admin.site.register(Offerta)
admin.site.register(StatoAttivita)
admin.site.register(Attivita)

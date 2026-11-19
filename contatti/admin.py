from django.contrib import admin

#importazione dei modelli



# Register your models here.
from .models import Contatto, RuoloDipendente, Dipendente, Cliente, StatoProgetto, Progetto, StatoOfferta, Offerta, StatoAttivita, Attivita
from django.utils import timezone
from django.contrib.auth import get_user_model #per ottenere il modello di utente
from django.core.mail import send_mail #per inviare email
from django.db import transaction #per eseguire transazioni
from django.utils.crypto import get_random_string #per generare stringhe casuali

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
        
admin.site.register(Dipendente, DipendenteAdmin)
admin.site.register(Contatto, TracciamentoAdmin)
admin.site.register(Cliente, TracciamentoAdmin)
admin.site.register(Progetto, TracciamentoAdmin)
admin.site.register(Offerta, TracciamentoAdmin)
admin.site.register(Attivita, TracciamentoAdmin)
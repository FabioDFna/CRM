from django.contrib import admin

#importazione dei modelli



# Register your models here.
from .models import Contatto, RuoloDipendente, Dipendente, Cliente, StatoProgetto, Progetto, StatoOfferta, Offerta, StatoAttivita, Attivita
admin.site.register(RuoloDipendente)
admin.site.register(StatoProgetto)
admin.site.register(StatoOfferta)
admin.site.register(StatoAttivita)

from django.utils import timezone

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

admin.site.register(Contatto, TracciamentoAdmin)
admin.site.register(Dipendente, TracciamentoAdmin)
admin.site.register(Cliente, TracciamentoAdmin)
admin.site.register(Progetto, TracciamentoAdmin)
admin.site.register(Offerta, TracciamentoAdmin)
admin.site.register(Attivita, TracciamentoAdmin)
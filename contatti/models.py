from django.db import models
from django.conf import settings


# Create your models here.

#tabella contatti
class Contatto(models.Model):
    nome = models.CharField(max_length=100)
    cognome = models.CharField(max_length=100)
    email =models.EmailField() #quando non specifico la lunghezza, django crea una colonna varchar(254)
    telefono =models.CharField(max_length=100)
    note = models.TextField(blank=True) #campo opzionale
    creato_il = models.DateTimeField(auto_now_add=True)
    creato_da = models.ForeignKey(
        settings.AUTH_USER_MODEL, #riferimento al modello di django auth
        on_delete=models.SET_NULL, #se l'utente viene eliminato, il contatto rimane
        null=True, #campo opzionale
        related_name = "contatti_creati", #nome del campo che si riferisce al modello di django auth
    )
    modificato_il = models.DateTimeField(auto_now=True)
    modificato_da = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True, #campo opzionale
        related_name = "contatti_modificati",
    )
    eliminato = models.BooleanField(default=False)
    eliminato_il = models.DateTimeField(null=True, blank=True)
    eliminato_da = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True, #campo opzionale
        related_name = "contatti_eliminati",
    )
    def __str__(self):
        return f"{self.nome} {self.cognome}"

    class Meta:
        verbose_name = "Contatto"
        verbose_name_plural = "Contatti"

#tabella ruolo del dipendente
class RuoloDipendente(models.Model):
    nome = models.CharField(max_length=100)
    def __str__(self):
        return self.nome
    class Meta:
        verbose_name = "Ruolo dipendente"
        verbose_name_plural = "Ruoli dipendenti"

#tabella dipendenti
class Dipendente(models.Model):
    nome = models.CharField(max_length=100)
    cognome = models.CharField(max_length=100)
    email = models.EmailField(max_length=100)
    ruolo = models.ForeignKey(RuoloDipendente, on_delete=models.PROTECT)
    utente = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL, #se l'utente viene eliminato, il dipendente rimane
        null=True, #campo opzionale
        blank=True, #campo opzionale
        related_name = "dipendenti",
    )
    creato_il = models.DateTimeField(auto_now_add=True)
    creato_da = models.ForeignKey(
        settings.AUTH_USER_MODEL, #riferimento al modello di django auth
        on_delete=models.SET_NULL, #se l'utente viene eliminato, il contatto rimane
        null=True, #campo opzionale
        related_name = "dipendenti_creati", #nome del campo che si riferisce al modello di django auth
    )
    modificato_il = models.DateTimeField(auto_now=True)
    modificato_da = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True, #campo opzionale
        related_name = "dipendenti_modificati",
    )
    eliminato = models.BooleanField(default=False)
    eliminato_il = models.DateTimeField(null=True, blank=True)
    eliminato_da = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True, #campo opzionale
        related_name = "dipendenti_eliminati",
    )
    def __str__(self):
        return f"{self.nome} {self.cognome}"
    class Meta:
        verbose_name = "Dipendente"
        verbose_name_plural = "Dipendenti"

class Cliente(models.Model):
    nome = models.CharField(max_length=100)
    cognome = models.CharField(max_length=100)
    email = models.EmailField(max_length=100)
    telefono = models.CharField(max_length=100)
    indirizzo = models.CharField(max_length=100)
    citta = models.CharField(max_length=100)
    provincia = models.CharField(max_length=100)
    cap = models.CharField(max_length=100)
    contatto = models.OneToOneField(
        Contatto,
        on_delete=models.PROTECT, #se il contatto viene eliminato, il cliente rimane
        related_name = "cliente",
    )
    creato_il = models.DateTimeField(auto_now_add=True)
    creato_da = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True, #campo opzionale
        related_name = "clienti_creati",
    )
    modificato_il = models.DateTimeField(auto_now=True)
    modificato_da = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True, #campo opzionale
        related_name = "clienti_modificati",
    )
    eliminato = models.BooleanField(default=False)
    eliminato_il = models.DateTimeField(null=True, blank=True)
    eliminato_da = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True, #campo opzionale
        related_name = "clienti_eliminati",
    )
    def __str__(self):
        return f"{self.nome} {self.cognome}"

    class Meta:
        verbose_name = "Cliente"
        verbose_name_plural = "Clienti"

class StatoProgetto(models.Model):
    nome = models.CharField(max_length=100)
    def __str__(self):
        return self.nome

    class Meta:
        verbose_name = "Stato progetto"
        verbose_name_plural = "Stati progetto"

class Progetto(models.Model):
    titolo = models.CharField(max_length=100)
    descrizione = models.TextField(blank=True)
    cliente = models.ForeignKey(Cliente, on_delete=models.PROTECT)
    stato = models.ForeignKey(StatoProgetto, on_delete=models.PROTECT)
    creato_il = models.DateTimeField(auto_now_add=True)
    creato_da = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True, #campo opzionale
        related_name = "progetti_creati",
    )
    modificato_il = models.DateTimeField(auto_now=True)
    modificato_da = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True, #campo opzionale
        related_name = "progetti_modificati",
    )
    eliminato = models.BooleanField(default=False)
    eliminato_il = models.DateTimeField(null=True, blank=True)
    eliminato_da = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True, #campo opzionale
        related_name = "progetti_eliminati",
    )
    def __str__(self):
        return self.titolo

    class Meta:
        verbose_name = "Progetto"
        verbose_name_plural = "Progetti"

class StatoOfferta(models.Model):
    nome = models.CharField(max_length=100)
    def __str__(self):
        return self.nome

    class Meta:
        verbose_name = "Stato offerta"
        verbose_name_plural = "Stati offerta"

class Offerta(models.Model):
    progetto = models.ForeignKey(Progetto, on_delete=models.PROTECT)
    titolo = models.CharField(max_length=100)
    importo = models.DecimalField(max_digits=10, decimal_places=2)
    stato = models.ForeignKey(StatoOfferta, on_delete=models.PROTECT)
    creato_il = models.DateTimeField(auto_now_add=True)
    creato_da = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True, #campo opzionale
        related_name = "offerte_creati",
    )
    modificato_il = models.DateTimeField(auto_now=True)
    modificato_da = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True, #campo opzionale
        related_name = "offerte_modificati",
    )
    eliminato = models.BooleanField(default=False)
    eliminato_il = models.DateTimeField(null=True, blank=True)
    eliminato_da = models.ForeignKey(   
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True, #campo opzionale
        related_name = "offerte_eliminati",
    )
    def __str__(self):
        return self.titolo

    class Meta:
        verbose_name = "Offerta"
        verbose_name_plural = "Offerte"

class StatoAttivita(models.Model):
    nome = models.CharField(max_length=100)
    def __str__(self):
        return self.nome

    class Meta:
        verbose_name = "Stato attività"
        verbose_name_plural = "Stati attività"

class Attivita(models.Model):
    offerta = models.ForeignKey(Offerta, on_delete=models.PROTECT)
    progetto = models.ForeignKey(Progetto, on_delete=models.PROTECT)
    dipendente = models.ForeignKey(
        Dipendente,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
    )    
    titolo = models.CharField(max_length=100)
    descrizione = models.TextField(blank=True)
    stato = models.ForeignKey(StatoAttivita, on_delete=models.PROTECT)
    creato_il = models.DateTimeField(auto_now_add=True)
    creato_da = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True, #campo opzionale
        related_name = "attivita_creati",
    )
    modificato_il = models.DateTimeField(auto_now=True)
    modificato_da = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True, #campo opzionale
        related_name = "attivita_modificati",
    )
    eliminato = models.BooleanField(default=False)
    eliminato_il = models.DateTimeField(null=True, blank=True)
    eliminato_da = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True, #campo opzionale
        related_name = "attivita_eliminati",
    )
    def __str__(self):
        return self.titolo

    class Meta:
        verbose_name = "Attività"
        verbose_name_plural = "Attività"



        
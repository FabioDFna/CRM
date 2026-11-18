# Piano del CRM

Domani si riparte dal **Passo 1**. Si fa un passo per volta. Quando un passo funziona, lo si segna con `[x]` e si può passare al successivo. Se ci si blocca, ci si ferma: il passo dopo resta per la sessione successiva.

I comandi si lanciano dalla cartella `CRM`. Python è quello dell'ambiente virtuale:

```powershell
.\.venv\Scripts\python.exe manage.py <comando>
```

Il sito di prova, quando serve, si avvia con:

```powershell
.\.venv\Scripts\python.exe manage.py runserver
```

Poi si apre `http://127.0.0.1:8000/admin/`.

## Già fatto

- [x] Python 3.13 e ambiente `.venv` con Django
- [x] Progetto Django (`manage.py`, cartella `config`)
- [x] App `contatti` (i modelli sono ancora vuoti)
- [x] Database SQLite `db.sqlite3`, con le tabelle di Django
- [x] Git locale, `.gitignore`, primo commit
- [x] Repository privato https://github.com/FabioDFna/CRM

`.venv` e `db.sqlite3` restano sul PC e non vanno su GitHub.

## Come sono collegati i dati

Tutto resta nell'app `contatti`, finché il flusso non è completo.

1. **Contatto**: nome, email, telefono, note.
2. **Cliente**: un contatto diventato cliente. Un contatto senza cliente resta solo un contatto.
3. **Progetto**: appartiene a un cliente.
4. **Offerta**: appartiene a un progetto. Stati: bozza, inviata, accettata, rifiutata.
5. **Attività**: nasce quando un'offerta viene accettata. Si assegna a un dipendente.
6. **Dipendente**: nome, cognome, email, ruolo. L'accesso con password dei dipendenti arriva dopo, non blocca i passi sopra.

In admin, «rendere cliente» significa creare un Cliente collegato a quel Contatto. Il pulsante dedicato arriva al Passo 3.

## Passo 1. Contatti nel database e in admin

Obiettivo: inserire, modificare e cancellare un contatto da `http://127.0.0.1:8000/admin/`.

- Scrivere il modello `Contatto` in `contatti/models.py`.
- Registrarlo in `contatti/admin.py`.
- Creare e applicare le tabelle:

```powershell
.\.venv\Scripts\python.exe manage.py makemigrations
.\.venv\Scripts\python.exe manage.py migrate
```

- Creare l'utente amministratore, solo la prima volta:

```powershell
.\.venv\Scripts\python.exe manage.py createsuperuser
```

- Avviare il sito, entrare in admin e salvare un contatto di prova.

Fatto quando il contatto compare nella lista admin e resta nel database dopo un aggiornamento della pagina.

## Passo 2. Dipendenti

Obiettivo: gestire i dipendenti in admin, con nome, cognome, email e ruolo.

- Modello `Dipendente`, registrazione in admin, `makemigrations`, `migrate`.
- Inserire un dipendente di prova.

Si può fare subito dopo i contatti perché non dipende da loro.

## Passo 3. Rendere un contatto cliente

Obiettivo: da un contatto si ottiene un cliente, senza duplicare nome e telefono.

- Modello `Cliente` collegato a un solo `Contatto`.
- In admin, creare un cliente scegliendo un contatto esistente.
- Poi, se il passo precedente è stabile, aggiungere in admin l'azione «Rendi cliente» sul contatto.

Fatto quando un contatto di prova ha un cliente collegato e un altro contatto resta senza cliente.

## Passo 4. Progetti del cliente

Obiettivo: ogni progetto appartiene a un cliente.

- Modello `Progetto`: cliente, nome, descrizione, stato.
- Admin, migrazioni, un progetto di prova sul cliente del Passo 3.

## Passo 5. Offerte del progetto

Obiettivo: ogni offerta appartiene a un progetto.

- Modello `Offerta`: progetto, titolo, importo, stato (`bozza`, `inviata`, `accettata`, `rifiutata`), data.
- Admin, migrazioni, un'offerta in bozza sul progetto di prova.

## Passo 6. Accettare l'offerta e creare l'attività

Obiettivo: quando l'offerta passa ad `accettata`, nasce un'`Attività` collegata a quell'offerta e al suo progetto.

- Modello `Attività`: offerta, progetto, titolo, descrizione, stato.
- Regola nel codice: il passaggio a `accettata` crea l'attività una sola volta.
- Prova in admin: cambiare lo stato dell'offerta e vedere l'attività comparire.

## Passo 7. Assegnare l'attività a un dipendente

Obiettivo: ogni attività può avere un dipendente responsabile.

- Aggiungere il collegamento al `Dipendente` sull'attività.
- Migrazioni.
- In admin, assegnare l'attività di prova al dipendente del Passo 2.

## Passo 8. Pagine nel browser

Si inizia solo quando i passi 1–7 funzionano in admin. Stesso ordine dei dati, una schermata alla volta:

1. Elenco e scheda dei contatti, con creazione e modifica.
2. Azione «Rendi cliente».
3. Progetti del cliente.
4. Offerte del progetto, con il cambio di stato.
5. Attività e scelta del dipendente.

Ogni schermata si prova nel browser prima di passare alla successiva.

## Passo 9. Accesso dei dipendenti

Dopo le pagine: un dipendente può entrare con la propria utenza e vedere le attività assegnate a lui. Fino a quel momento basta l'utente amministratore.

## Dopo ogni passo riuscito

Controllare cosa verrebbe salvato, poi commit e invio su GitHub:

```powershell
git add .
git status
git commit -m "Descrizione breve del passo"
git push
```

In `git status` non devono comparire `.venv/` né `db.sqlite3`.

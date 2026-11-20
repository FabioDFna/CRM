# CRM

Un piccolo sistema per seguire i clienti di un’azienda. Tiene il percorso da un primo contatto fino al lavoro assegnato a un dipendente.

Un contatto può diventare un cliente. Un cliente ha dei progetti. Un progetto ha delle offerte. Quando un’offerta viene accettata, nasce una sola attività, che si può assegnare a un dipendente. Eliminare un dato non cancella la riga: viene segnata come eliminata e sparisce dagli elenchi.

Sono previsti tre tipi di account:

- **Superadmin**: chi sviluppa il programma. Accesso completo, compresa la parte tecnica di amministrazione.
- **Admin**: il capo dell’azienda. Può aggiungere, modificare ed eliminare clienti, progetti, offerte e attività, senza gli strumenti riservati a chi sviluppa.
- **Dipendente**: vede solo le attività assegnate a lui e può aggiornarle. Non elimina nulla e non crea progetti, clienti o offerte.

L’applicazione è un progetto Django. I dati stanno nel file SQLite locale `db.sqlite3`. L’interfaccia usata oggi è l’admin di Django, all’indirizzo `http://127.0.0.1:8000/admin/`.

Dalla cartella del progetto, con l’ambiente virtuale:

```powershell
.\.venv\Scripts\python.exe manage.py runserver
```

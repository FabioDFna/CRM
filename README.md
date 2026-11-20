# CRM

A small customer relationship system for one company. It keeps the path from a first contact to the work assigned to an employee.

A contact can become a client. A client has projects. A project has offers. When an offer is accepted, one activity is created and can be assigned to an employee. Removing a record does not delete the row: it is marked as removed and hidden from the lists.

Three kinds of account are planned:

- **Superadmin**: the developer. Full access, including the technical admin area.
- **Admin**: the company owner. Can add, change, and remove clients, projects, offers, and activities, without the developer-only tools.
- **Employee**: sees only the activities assigned to them and can update those. Cannot delete records or create projects, clients, or offers.

The application is a Django project. Data is stored in a local SQLite file, `db.sqlite3`. The working interface today is the Django admin at `http://127.0.0.1:8000/admin/`.

From the project folder, with the virtual environment:

```powershell
.\.venv\Scripts\python.exe manage.py runserver
```


Project Management Tool

A Django-based web application that allows users to manage collaborative projects, assign tasks, and communicate through direct messaging. This tool includes user profiles, project/task dashboards, and private chat between users.

---

🌟 Features

- ✅ User Registration, Login & Authentication
- ✅ User Profile with bio, location, and birthdate
- ✅ Create and manage Projects
- ✅ Create and assign Tasks to users
- ✅ Direct Messaging system (Inbox + threaded chat)
- ✅ Responsive, clean UI with Django templates & CSS
- ✅ Permission checks to ensure secure user interactions

---

📁 Project Structure

project_management_tool/
├── core/
│ ├── migrations/
│ ├── templates/
│ │ └── core/
│ │ ├── base.html
│ │ ├── profile.html
│ │ ├── inbox.html
│ │ ├── thread.html
│ │ └── ...
│ ├── static/
│ ├── models.py
│ ├── views.py
│ ├── urls.py
│ └── ...
├── project_management_tool/
│ ├── settings.py
│ ├── urls.py
│ └── ...
├── manage.py
└── README.md

## ⚙️ Setup Instructions

1. Clone the Repository

git clone https://github.com/yourusername/project-management-tool.git
cd project-management-tool

2. Create a Virtual Environment

python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

3. Install Dependencies

pip install -r requirements.txt

4. Apply Migrations

python manage.py makemigrations
python manage.py migrate

5. Create a Superuser (Admin)

python manage.py createsuperuser

6. Run the Server

python manage.py runserver

Visit http://127.0.0.1:8000/ in your browser.
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
🛠️ Tech Stack

- Backend: Django
- Frontend: HTML, CSS, JavaScript
- Database: SQLite (default, can switch to PostgreSQL)
- Version Control: Git & GitHub


⚙️ Setup Instructions

```bash

# Clone the repo
git clone https://github.com/likhithamuddala/CodeAlpha_project_management_tool.git

# Navigate into the project
cd simple-ecommerce-store/ecommerce

# (Optional) Create virtual environment
python -m venv env
source env/bin/activate  # On Windows: env\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Run migrations
python manage.py migrate

# Run the server
python manage.py runserver

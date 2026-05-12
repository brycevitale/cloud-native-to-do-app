# Cloud Native To-Do App

This project began as Homework 4 for my Cloud Computing course and was extended into a more complete cloud deployment project. The original version already separated the frontend and backend into different components, but it still functioned as one shared task list. For the final project, I redesigned it into a multi user to-do application with authentication, per user task ownership, and a cleaner frontend layout.

The final version includes user registration, login, logout, session based user tracking, a redesigned database, a Dockerized frontend, a backend API running on a Google Cloud VM, and frontend deployment through Kubernetes.


## Project Overview
The main goal of this project was to build on my Homework 4 architecture. I kept the split deployment model and extended the application itself.


In my original Homework 4 version:
- the frontend was deployed separately from the backend
- the frontend ran on Kubernetes
- the backend API ran on a Google Cloud VM
- all users shared the same task list


In the final version:
- users can register for their own account
- users can log in and log out
- each task belongs to a specific user
- the frontend only loads tasks for the logged in user
- the overall cloud architecture remains split between Kubernetes and a VM


## What I Added Beyond Homework 4

The main extension was changing the application from a shared to-do list into a multi user cloud application.


### Backend changes
- added a `users` table
- updated the `entries` table to include `user_id`
- added API routes for registration and login
- updated task routes so they only return tasks for a specific user
- added password hashing for safer credential storage


### Frontend changes
- added a login page
- added a register page
- added logout
- stored the logged in username in session
- updated the task dashboard to show only the logged in user’s tasks
- improved the dashboard layout to make the app feel cleaner


## Architecture

This project uses a split architecture:

- **Frontend:** Flask app in `todolist.py`
- **Backend API:** Flask API in `todolist_api.py`
- **Database:** SQLite database in `todolist.db`
- **Containerization:** Docker
- **Cloud backend hosting:** Google Cloud VM
- **Cloud frontend hosting:** Google Kubernetes Engine (GKE)


### How the pieces work together

1. The browser talks to the frontend Flask app.
2. The frontend handles login, registration, page rendering, and session tracking.
3. The frontend sends requests to the backend API.
4. The backend API handles database reads and writes.
5. The database stores users and user specific tasks.


## Project Structure

```text
final_project/
├── Dockerfile
├── README.md
├── cleanup.sh
├── init_db.py
├── startup.sh
├── test.sh
├── todolist.py
├── todolist_api.py
├── todolist.db
└── templates/
    ├── index.html
    ├── login.html
    └── register.html

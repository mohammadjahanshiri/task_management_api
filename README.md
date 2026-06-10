# 🚀 Django Task Management API

A professional Task Management API built with **Django REST Framework**, featuring a fully containerized environment using **Docker** and **PostgreSQL**.

---

## 🌟 Overview
This project provides a backend service for managing tasks efficiently. It is designed with scalability and developer experience in mind, utilizing Docker for easy setup and PostgreSQL for reliable data management.

## ✨ Features
- **Task Management:** Full CRUD (Create, Read, Update, Delete) functionality for tasks.
- **Interactive Documentation:** Integrated Swagger and ReDoc for easy API testing.
- **Containerization:** Environment consistency across different machines using Docker.
- **Database:** Production-ready PostgreSQL integration.
- **Environment Safety:** Secure configuration using environment variables.

## 🛠 Tech Stack
- **Backend:** Python, Django, Django REST Framework (DRF)
- **Database:** PostgreSQL
- **DevOps:** Docker, Docker Compose
- **Documentation:** Swagger UI, ReDoc

---

## 🚀 Getting Started

Follow these steps to get the project running locally on your machine.

### 1. Clone the Repository
```bash
git clone https://github.com/mohammadjahanshiri/task_management_api.git
cd task_management_api

2_Then run the following command in the project's root directory:

docker-compose up -d --build
docker-compose exec web python manage.py migrate

The API is now available at:
http://localhost:8000/

### API Documentation

http://localhost:8000/swagger/
http://localhost:8000/redoc/

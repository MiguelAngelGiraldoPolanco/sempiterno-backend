# FastAPI Secure Backend API

A production-ready backend architecture built with **FastAPI**. This project focuses on implementing robust authentication mechanisms, secure session handling, and a clean, scalable service-oriented structure.

## 🚀 Key Technical Features

* **Authentication & Security**: Fully implemented JWT (JSON Web Token) authentication for secure API access.
* **User Flow**: Logic for user creation, verification, and profile management.
* **Architecture**: Modular structure separating routes, services, and database models to maintain high maintainability.
* **Infrastructure**: Containerized with **Docker** for consistent deployment across environments.
* **External Integration**: Integrated `resend` library for transactional email handling (e.g., user verification/recovery).

## 🏗 Architecture Overview

The system follows a professional pattern to decouple business logic from the HTTP layer:



* **Routes/Endpoints**: Handles request parsing and response delivery.
* **Services**: Contains the core business logic, decoupled from the API layer.
* **Models**: Database definitions ensuring data integrity.
* **Middleware/Security**: Interceptors for JWT validation and role-based access.

## 🛠 Tech Stack

* **Framework**: FastAPI
* **Security**: PyJWT, bcrypt (for password hashing)
* **Email Service**: Resend
* **Database**: PostgreSQL (standard integration)
* **Containerization**: Docker

## ⚡ Quick Start

1. **Clone the repository:**
   ```bash
   git clone <your-repo-url>
   cd <your-repo-folder>
   ```
2. **Install dependencies:**
```bash
Bash
pip install -r requirements.txt
```
3. **Run with Docker:**
```bash
Bash
docker build -t my-api-backend .
docker run -p 8000:8000 my-api-backend
```
**📜 License**
MIT © [Miguel Ángel Giraldo Polanco]

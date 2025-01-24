## Overview
This project is a backend solution for the Car Pooling platform. It is designed to handle user registrations, matchmaking, reservations, notifications, and file uploads. The backend is implemented using **Python** and communicates with a **MariaDB** database. The entire solution is Dockerized for seamless deployment.

---

## Features
1. **Database Management**:
   - Interacts with a MariaDB database to manage users, matches, and reservations.
   - Securely handles user data with encryption.

2. **Notification System**:
   - Notifies users about upcoming reservations and pending matches.
   - Sends notifications via email, SMS, or push notifications based on user preferences.

3. **Matchmaking Module**:
   - Logic for matching users based on time, location, and preferences.
   - Handles match acceptance, rejection, and updates.

4. **Reservation System**:
   - Creates, updates, and cancels reservations.
   - Notifies users of reservation status changes.

5. **File Upload Module**:
   - Allows users to upload profile pictures with file validation (max size: 2MB).
   - Converts images to `.jpg` format with medium-to-high compression.

6. **Dockerized Deployment**:
   - Easy-to-deploy backend using Docker for development and production environments.

---

## Prerequisites
- **Python 3.12** or higher
- **Flask**
- **MariaDB**
- **Docker** and **Docker Compose**
- **Git** for version control

---


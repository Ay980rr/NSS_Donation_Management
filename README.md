# NSS_Donation_Management


A web-based donation management system developed as part of an NSS academic project.  
The application manages user registrations, donations, and administrative monitoring using a secure and structured workflow.

---

## Project Overview

The NSS Donation Management System provides:
- Secure user registration and login
- Role-based access for users and administrators
- Donation management with payment simulation
- Administrative dashboard for monitoring users and donations

The system demonstrates real-world web development practices using a three-tier architecture.

---

## Features

- User registration with password protection
- Common login for admin and normal users
- Secure password hashing
- Donation creation and status tracking
- Razorpay sandbox payment integration
- Admin dashboard with summary statistics
- View registered users and donation history
- Export-ready structured data
- Clean and documented GitHub repository

---

## Tech Stack

- **Frontend:** HTML, CSS, JavaScript  
- **Backend:** Python, Django, Django REST Framework  
- **Database:** SQLite  
- **Payment Gateway:** Razorpay (Sandbox/Test Mode)  
- **Version Control:** Git & GitHub  

---

---

## Database Design

### User Table
- id
- name
- email (unique)
- password (hashed)

### Donation Table
- id
- user_id (foreign key)
- amount
- status (SUCCESS / FAILED / PENDING)
- created_at

---

## Authentication Flow

1. User enters email and password
2. Backend validates credentials
3. Role (admin or user) is identified
4. User is redirected to the appropriate dashboard
5. Unauthorized access is rejected

---

## Payment Integration

- Razorpay sandbox mode is used
- No real money transactions occur
- Payment success or failure updates donation status
- Suitable for academic demonstration purposes

---

## How to Run the Project (Local Setup)

1. Clone the repository
2. Create and activate a virtual environment
3. Install required dependencies
4. Run Django migrations
5. Start the Django development server
6. Open frontend in a browser

---

## Notes

- This project is intended for **educational and NSS demonstration purposes only**
- Payment gateway operates in **test mode**
- Not deployed on a live production server

---

## Author

**Ayush Barnwal**  
NSS / Academic Project



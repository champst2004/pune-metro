# 🚆 Pune Metro System

A **Metro Ticketing System** built using **Flask (Python) and MySQL**.  
Users can issue metro cards, book metro tickets, and track ride history with **discounts for students**.

## 📜 Features
✅ **User Management**: Admin & Normal Users  
✅ **Metro Card System**: Regular (10% discount) & Student (25% discount)  
✅ **Ticket Booking**: Select stations & calculate fare dynamically  
✅ **Transaction Logging**: Tracks payments & fare deductions  
✅ **Ride History**: View past metro rides  

## 🏷️ Fare Calculation
₹10 for the next station  
₹15 for traveling 2 stations ahead  
₹20 for traveling 3 stations ahead  
₹25 for traveling 4 stations ahead  
₹30 for more than 5 stations  

Discounts:  
MITWPU Students: 25% discount  
Regular Card Holders: 10% discount  
Non-Card Holders: No discount  

---

## 📂 Tech Stack
- **Backend:** Flask (Python) 🐍  
- **Frontend:** HTML, CSS, JavaScript 🎨  
- **Database:** MySQL 🗄  

---

## 🔧 Installation & Setup

### 1️⃣ **Clone the Repository**
```bash
git clone https://github.com/champst2004/pune-metro.git
cd pune-metro
```
### 2️⃣ Install Dependencies
Make sure you have Python installed. Then, install the required libraries:  
```bash
pip install -r requirements.txt
```
### 3️⃣ Set Up the Database
Run **`tables.sql`** and **`stations.sql`** to create database and tables

## 🚀 Running the Application

### 1. Start the Flask App
```bash
python app.py
```

### 2. Open in Browser
```
http://127.0.0.1:5000/
```

## 🖥 Pages in the App
| Page                | URL                  | Description |
|---------------------|---------------------|-------------|
| **Home**           | `/`                 | Landing page |
| **Issue Card**     | `/issue_card`       | Issue a new metro card |
| **View Users**     | `/view_users`       | Show all users who have issued a metro card |
| **Book Ticket**    | `/book_ticket`      | Select stations, calculate fare, and book a ride |
| **Ride History**   | `/ride_history`     | View past rides of metro card users |

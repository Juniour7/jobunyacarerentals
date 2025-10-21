# 🚗 Car Rental Application (Django + Django REST Framework)

This is a **Car Rental Application** built with Django and Django REST Framework (DRF).

It allows:
- The **Admin** to log in through a separate dashboard, add vehicles to the inventory, and manage bookings.
- The **Customer** to view available vehicles, check details and daily rates, and make bookings through the website.

---

## 🧾 Features

### 👨‍💼 Admin
- Login via  Admin dashboard
- Add, edit, and delete vehicles
- View and manage customer bookings
- Approve or deny booking requests
- Mark vehicles as unavailable during rental periods

### 👩‍💻 Customer
- Register and log in
- Browse available vehicles
- View detailed vehicle information
- Make and track bookings
- See booking statuses (Pending, Approved, Denied, Completed)

---

## ⚙️ Project Setup

### 1️⃣ User Enpoints
Registration - /api/user/register/ (POST)
Registers a new  Customer

Request Example:
{
  "full_name": "Edwin Boge",
  "email": "boge@gmail.com",
  "phone_number": "0716794363",
  "license_number": "DL294345",
  "password": "bogespassword",
  "password2": "bogespassword",
  "agree_terms": "True"
}

Login - /api/user/login/ (POST)
Request Example:
{
  "email": "boge@gmail.com",
  "password": "bogespassword"
}

Response Example:
{
  "id": 1,
  "email": "boge@gmail.com",
  "full_name": "Edwin Boge",
  "roles": "customer",
  "token": "your-auth-token-here"
}

*Note* Admin users are created in the django admin dashboard and use the same login endpoint


### 🚘 Vehicle Endpoints
List all Vehciles - /api/vehicles/ (GET)
Public endpoint. Return all vehicles currently in the inventory

Example Response:
{
    "count": 3,
    "next": null,
    "previous": null,
    "results": [
        {
            "id": 3,
            "name": "Toyota Corolla",
            "model": "2023",
            "car_type": "Sedan",
            "description": "Reliable 5-seater family car",
            "seats": 5,
            "transmission": "Automatic",
            "fuel_type": "Petrol",
            "daily_rate": "80.00",
            "status": "Available",
            "features": "Air conditioning, Bluetooth, Rear Camera",
            "image": "http://127.0.0.1:8000/media/vehicles/b2e7ebd7fd3e312c861406c2f0e0f616_GdV2mRo.jpg",
            "created_at": "2025-10-21T06:16:41.336923Z"
        },
        {
            "id": 2,
            "name": "BMW X5",
            "model": "2015",
            "car_type": "SUV",
            "description": "Experience the perfect combination of luxury, performance, and versatility with the BMW X5. This premium SUV delivers a commanding presence on the road, advanced technology inside the cabin, and the power you expect from BMW engineering.\r\n\r\nUnder the hood, the BMW X5 packs a turbocharged engine that provides smooth yet thrilling acceleration, making highway drives and city cruising equally enjoyable. Its intelligent all-wheel-drive system (xDrive) ensures confident handling and stability across any terrain or weather condition.\r\n\r\nStep inside and you’re greeted by a spacious, leather-appointed interior, complete with ambient lighting, panoramic sunroof, and advanced infotainment system with touchscreen navigation, Apple CarPlay, and premium sound. Whether you’re traveling for business, a family trip, or a weekend getaway, the BMW X5 provides first-class comfort for every passenger.",
            "seats": 7,
            "transmission": "Automatic",
            "fuel_type": "Diesel",
            "daily_rate": "230.00",
            "status": "Available",
            "features": "Open Roof",
            "image": "http://127.0.0.1:8000/media/vehicles/b2e7ebd7fd3e312c861406c2f0e0f616.jpg",
            "created_at": "2025-10-19T17:26:14Z"
        },
        {
            "id": 1,
            "name": "Porsche 911 gt3 rs",
            "model": "2011",
            "car_type": "Sports Car",
            "description": "Get behind the wheel of pure racing DNA. The Porsche 911 GT3 RS is not just another sports car — it’s a road-legal race machine built to thrill. Powered by a 4.0-liter naturally aspirated flat-six engine producing over 500 horsepower, this GT3 RS delivers breathtaking acceleration, razor-sharp handling, and the unmistakable Porsche soundtrack that climbs to 9,000 rpm.\\r\\n\\r\\nIts lightweight carbon-fibre body, massive active rear wing, and aerodynamic design give it incredible cornering grip and stability — perfect for drivers who crave precision and excitement.\\r\\n\\r\\nInside, you’ll find Alcantara-trimmed sport bucket seats, a racing-inspired cockpit, and Porsche’s latest technology to keep every drive engaging yet comfortable.\\r\\n\\r\\nWhether you’re attending a high-profile event, exploring scenic highways, or simply want to experience the thrill of a true performance icon, the 911 GT3 RS offers an unforgettable driving experience that combines race-track performance with everyday usability.",
            "seats": 3,
            "transmission": "Automatic",
            "fuel_type": "Petrol",
            "daily_rate": "345.00",
            "status": "Available",
            "features": "Cool Engine",
            "image": "http://127.0.0.1:8000/media/vehicles/867c7e51bc55db43a6764b70773078df_ASCpP9H.jpg",
            "created_at": "2025-10-19T17:23:50Z"
        }
    ]
}

Vehicle Detail View - /api/vehicles/<int:pk>/ (GET)
Return details of a single vehicle

Create Vehicle - /api/vehicles/ (POST)
Admin only endpoint

Request Example:
{
  "name": "Toyota Corolla",
  "model": "2023",
  "car_type": "Sedan",
  "description": "Reliable 5-seater family car",
  "seats": 5,
  "transmission": "Automatic",
  "fuel_type": "Petrol",
  "daily_rate": "80.00",
  "status": "Available",
  "features": "Air conditioning, Bluetooth, Rear Camera"
}

Response Example:
{
  "id": 3,
  "name": "Toyota Corolla",
  "model": "2023",
  "car_type": "Sedan",
  "description": "Reliable 5-seater family car",
  "seats": 5,
  "transmission": "Automatic",
  "fuel_type": "Petrol",
  "daily_rate": "80.00",
  "status": "Available",
  "features": "Air conditioning, Bluetooth, Rear Camera",
  "image": "http://127.0.0.1:8000/media/vehicles/example.jpg",
  "created_at": "2025-10-21T06:16:41.336923Z"
}


### 📅 Booking Endpoints
Create Booking - /api/bookings/ (POST)
Authenticated for logged in users.

Request Example:
{
  "vehicle": 1,
  "start_date": "2025-10-25",
  "end_date": "2025-10-27"
}


Response Example:
{
  "id": 1,
  "user": 1,
  "vehicle": 1,
  "vehicle_name": "Porsche 911 GT3 RS",
  "vehicle_image": "/media/vehicles/867c7e51bc55db43a6764b70773078df.jpg",
  "start_date": "2025-10-25",
  "end_date": "2025-10-27",
  "total_price": "1035.00",
  "status": "pending",
  "daily_rate": "345.00",
  "created_at": "2025-10-19T17:27:44.578261Z"
}


View user Bookings - /api/my-bookings/ (GET)
Returns all booking made by the current user

Example Response:
{
  "id": 1,
  "user": 1,
  "vehicle": 1,
  "vehicle_name": "Porsche 911 GT3 RS",
  "vehicle_image": "/media/vehicles/867c7e51bc55db43a6764b70773078df.jpg",
  "start_date": "2025-10-25",
  "end_date": "2025-10-27",
  "total_price": "1035.00",
  "status": "completed",
  "daily_rate": "345.00",
  "created_at": "2025-10-19T17:27:44.578261Z"
}

*The status field reflects admin approval*

View all current Bookings - /api/all-bookings/ (GET)
Returns all the booking slots opened for the admin


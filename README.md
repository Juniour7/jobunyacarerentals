This is a car rental application, It a software that will allow the owner, i.e the admin to login in a separe admin dashboard, add vehicles into the inventory and the users will be able to see them in the website side. The user i.e a cutomer, will be able to selct the vehicle they want, view the daily rate and the finer details of the vehicle and make a booking. The booking will then be displayed in the admin dashboard where the admin can either approve or deny this booking application after contacting the customer. The can then mark the vehicle as unavailable until the period set ofr the hiring period is over. 

### User Enpoints
# Registratioin : api/user/register/ as Customer
{
    "full_name" : "Giftmacvane Momanyi",
    "email" : "giftmomanyi@gmail.com",
    "phone_number" : "0716794363",
    "license_number" : "DL2345",
    "password" : "giftpassword",
    "password2" : "giftpassword",
    "agree_terms" : "True"
}

# Login: api/user/login/
{
    "email" : "giftmomanyi@gmail.com",
    "password" : "giftpassword"
}

- Login return an authorization token 


## Vehicle view enpoints
All vehicle viewing endpoints are open to all user acces bithe logged in and unauthenticated user to all selection.

<!-- All Vehicle list endpoint -->
# Vehicle list api/vehicles/
example output
{
    "id": 1,
    "name": "porsche 911 gt3 rs",
    "model": "2011",
    "car_type": "Sports Car",
    "description": "Get behind the wheel of pure racing DNA. The Porsche 911 GT3 RS is not just another sports car — it’s a road-legal race machine built to thrill. Powered by a 4.0-liter naturally aspirated flat-six engine producing over 500 horsepower, this GT3 RS delivers breathtaking acceleration, razor-sharp handling, and the unmistakable Porsche soundtrack that climbs to 9,000 rpm.\r\n\r\nIts lightweight carbon-fibre body, massive active rear wing, and aerodynamic design give it incredible cornering grip and stability — perfect for drivers who crave precision and excitement.\r\n\r\nInside, you’ll find Alcantara-trimmed sport bucket seats, a racing-inspired cockpit, and Porsche’s latest technology to keep every drive engaging yet comfortable.\r\n\r\nWhether you’re attending a high-profile event, exploring scenic highways, or simply want to experience the thrill of a true performance icon, the 911 GT3 RS offers an unforgettable driving experience that combines race-track performance with everyday usability.",
    "seats": 3,
    "transmission": "Automatic",
    "fuel_type": "Petrol",
    "daily_rate": "345.00",
    "status": "Available",
    "features": "Cool Engine",
    "image": "/media/vehicles/867c7e51bc55db43a6764b70773078df.jpg",
    "created_at": "2025-10-19T16:21:54Z"
}

<!-- Vehicle detail view enpoint -->
# Vehicle detail view endpoint api/vehicles/<int:pk>/
This returns a specific vehcile based upon what the customer selects and from here they can make a booking


## Booking Enpoints


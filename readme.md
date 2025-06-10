#Fitness Class Booking API:

    *A RESTful API developed using Flask and SQLite that enables users to view, book, and manage fitness classes such as Yoga, Zumba, and     HIIT. Designed to demonstrate backend development skills including API design, database operations, and error handling.

#Project Overview:

    *This API simulates a backend system for a fictional fitness studio. It allows:

 1. Listing all available fitness classes.
 2. Adding new classes.
 3. Booking classes by clients.
 4. Filtering bookings using client email.

 #Key Features:

 1. View all upcoming fitness classes.  
 2. Add new fitness classes (with instructor, slots, and datetime).
 3. Book a spot in a class. 
 4. Check all bookings by a specific client email. 
 5. Timezone support for class times. 
 6. SQLite database integration.

 #Technologies Used:
 1. Python 3
 2. Flask– Web framework.  
 3. SQLite – Lightweight database.  
 4. Pytz – Timezone handling.

 #Folder Structure,
 
  fitness_booking_api/
│
├── app.py # Main Flask application
├── fitness.db # SQLite database (auto-created)
├── venv/ # Python virtual environment (optional)
└── README.md # Project documentation
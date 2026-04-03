import sqlite3
from utils import hash_password

class DatabaseManager:
    def __init__(self, db_name="bus_system.db"):
        self.conn = sqlite3.connect(db_name)
        self.cursor = self.conn.cursor()
        self.create_tables()
        self.seed_data()

    def create_tables(self):
        # Users Table
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS users 
            (id INTEGER PRIMARY KEY, username TEXT UNIQUE, password TEXT, role TEXT)''')
        
        # Buses Table
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS buses 
            (id INTEGER PRIMARY KEY, name TEXT, route TEXT, total_seats INTEGER, time TEXT)''')
        
        # Bookings Table
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS bookings 
            (id INTEGER PRIMARY KEY, user_id INTEGER, bus_id INTEGER, seat_num INTEGER, passenger_name TEXT,
            FOREIGN KEY(user_id) REFERENCES users(id),
            FOREIGN KEY(bus_id) REFERENCES buses(id))''')
            
        # Support DB migrations seamlessly
        try:
            self.cursor.execute("ALTER TABLE users ADD COLUMN security_key TEXT DEFAULT 'Alliance'")
        except sqlite3.OperationalError:
            pass
            
        try:
            self.cursor.execute("ALTER TABLE bookings ADD COLUMN passenger_name TEXT DEFAULT ''")
        except sqlite3.OperationalError:
            pass
            
        try:
            self.cursor.execute("ALTER TABLE bookings ADD COLUMN passenger_age INTEGER DEFAULT 0")
        except sqlite3.OperationalError:
            pass
            
        try:
            self.cursor.execute("ALTER TABLE bookings ADD COLUMN passenger_gender TEXT DEFAULT ''")
        except sqlite3.OperationalError:
            pass
            
        try:
            self.cursor.execute("ALTER TABLE bookings ADD COLUMN contact_number TEXT DEFAULT ''")
        except sqlite3.OperationalError:
            pass
            
        self.conn.commit()

    def seed_data(self):
        """Pre-loads 3 buses and 1 Admin if they don't exist."""
        # Add Admin (Username: admin, Password: password123)
        try:
            admin_pass = hash_password("password123")
            self.cursor.execute("INSERT INTO users (username, password, role, security_key) VALUES (?, ?, ?, ?)", 
                                ("admin", admin_pass, "admin", "AdminKey"))
        except sqlite3.IntegrityError:
            pass # Admin already exists

        # Add 3 Buses
        self.cursor.execute("SELECT COUNT(*) FROM buses")
        if self.cursor.fetchone()[0] == 0:
            buses = [
                ("Alliance Express", "Siliguri - Kolkata", 30, "10:00 AM"),
                ("Himalayan Travel", "Siliguri - Gangtok", 20, "02:00 PM"),
                ("Bengal Cruiser", "Siliguri - Darjeeling", 25, "08:00 AM")
            ]
            self.cursor.executemany("INSERT INTO buses (name, route, total_seats, time) VALUES (?, ?, ?, ?)", buses)
        self.conn.commit()

    def cancel_booking(self, booking_id):
        """Removes a booking by ID from the bookings table."""
        self.cursor.execute("DELETE FROM bookings WHERE id=?", (booking_id,))
        self.conn.commit()

# Testing the database setup
if __name__ == "__main__":
    db = DatabaseManager()
    print("Database initialized with Admin and 3 Buses.")
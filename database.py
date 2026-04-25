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

        # Seats Table (for per-bus seat tracking)
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS seats
            (id INTEGER PRIMARY KEY, bus_id INTEGER, seat_number INTEGER, status TEXT DEFAULT 'available',
            FOREIGN KEY(bus_id) REFERENCES buses(id))''')
            
        # ── Users migrations ──
        try:
            self.cursor.execute("ALTER TABLE users ADD COLUMN security_key TEXT DEFAULT 'Alliance'")
        except sqlite3.OperationalError:
            pass
            
        # ── Bookings migrations ──
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
            
        try:
            self.cursor.execute("ALTER TABLE bookings ADD COLUMN status TEXT DEFAULT 'active'")
        except sqlite3.OperationalError:
            pass
            
        try:
            self.cursor.execute("ALTER TABLE bookings ADD COLUMN admin_comment TEXT DEFAULT ''")
        except sqlite3.OperationalError:
            pass

        # ── Buses migrations (new fleet-management columns) ──
        buses_migrations = [
            "ALTER TABLE buses ADD COLUMN bus_number TEXT DEFAULT ''",
            "ALTER TABLE buses ADD COLUMN source TEXT DEFAULT ''",
            "ALTER TABLE buses ADD COLUMN destination TEXT DEFAULT ''",
            "ALTER TABLE buses ADD COLUMN departure_time TEXT DEFAULT ''",
            "ALTER TABLE buses ADD COLUMN date TEXT DEFAULT ''",
            "ALTER TABLE buses ADD COLUMN fare REAL DEFAULT 0",
        ]
        for stmt in buses_migrations:
            try:
                self.cursor.execute(stmt)
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

            # Create seat rows for each seed bus
            self.cursor.execute("SELECT id, total_seats FROM buses")
            for bus_id, total_seats in self.cursor.fetchall():
                seat_rows = [(bus_id, s, 'available') for s in range(1, total_seats + 1)]
                self.cursor.executemany(
                    "INSERT OR IGNORE INTO seats (bus_id, seat_number, status) VALUES (?, ?, ?)",
                    seat_rows
                )

        # Back-fill seats for any existing buses that have no seat rows (one-time migration)
        self.cursor.execute(
            """SELECT id, total_seats FROM buses
               WHERE id NOT IN (SELECT DISTINCT bus_id FROM seats)"""
        )
        for bus_id, total_seats in self.cursor.fetchall():
            seat_rows = [(bus_id, s, 'available') for s in range(1, total_seats + 1)]
            self.cursor.executemany(
                "INSERT OR IGNORE INTO seats (bus_id, seat_number, status) VALUES (?, ?, ?)",
                seat_rows
            )

        self.conn.commit()

    # ── Fleet Management ──────────────────────────────────────

    def add_bus(self, bus_number, source, destination, departure_time, date, total_seats, fare):
        """
        Adds a new bus to the fleet.
        Returns (True, bus_id) on success, or (False, error_message) on failure.
        Automatically creates seat entries in the seats table.
        """
        # Safety check: prevent duplicate bus_number + date
        self.cursor.execute(
            "SELECT id FROM buses WHERE bus_number=? AND date=?",
            (bus_number, date)
        )
        if self.cursor.fetchone():
            return (False, f"A bus with number '{bus_number}' already exists on {date}.")

        # Build backward-compatible values for legacy columns
        name = bus_number
        route = f"{source} - {destination}"
        time_val = departure_time

        self.cursor.execute(
            """INSERT INTO buses 
               (name, route, total_seats, time, bus_number, source, destination, departure_time, date, fare)
               VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)""",
            (name, route, total_seats, time_val, bus_number, source, destination, departure_time, date, fare)
        )
        bus_id = self.cursor.lastrowid

        # Automatic seat initialization
        seat_rows = [(bus_id, seat_num, 'available') for seat_num in range(1, total_seats + 1)]
        self.cursor.executemany(
            "INSERT INTO seats (bus_id, seat_number, status) VALUES (?, ?, ?)",
            seat_rows
        )

        self.conn.commit()
        return (True, bus_id)

    def get_all_buses(self):
        """Returns all buses with their full details."""
        self.cursor.execute(
            """SELECT id, bus_number, name, source, destination, departure_time, date,
                      total_seats, fare, route, time
               FROM buses ORDER BY id DESC"""
        )
        return self.cursor.fetchall()

    # ── Booking Management ────────────────────────────────────

    def cancel_booking(self, booking_id):
        """Removes a booking by ID from the bookings table."""
        self.cursor.execute("DELETE FROM bookings WHERE id=?", (booking_id,))
        self.conn.commit()

# Testing the database setup
if __name__ == "__main__":
    db = DatabaseManager()
    print("Database initialized with Admin and 3 Buses.")
    print("Buses table columns:", [desc[0] for desc in db.cursor.execute("PRAGMA table_info(buses)").fetchall()])
    print("Seats table columns:", [desc[0] for desc in db.cursor.execute("PRAGMA table_info(seats)").fetchall()])
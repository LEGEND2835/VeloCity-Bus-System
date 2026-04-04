import customtkinter as ctk
import tkinter.messagebox as messagebox
from PIL import Image
from utils import hash_password

class LoginFrame(ctk.CTkFrame):
    def __init__(self, master, controller, db):
        super().__init__(master)
        self.controller = controller
        self.db = db

        self.container = ctk.CTkFrame(self)
        self.container.place(relx=0.5, rely=0.5, anchor="center")

        # --- VeloCity Branding Start ---
        self.brand_frame = ctk.CTkFrame(self.container, fg_color="transparent")
        self.brand_frame.pack(pady=(20, 10), padx=50)

        self.logo_top = ctk.CTkFrame(self.brand_frame, fg_color="transparent")
        self.logo_top.pack()

        try:
            self.logo_img = ctk.CTkImage(Image.open("logo.png"), size=(120, 120))
            self.logo_label = ctk.CTkLabel(self.logo_top, image=self.logo_img, text="")
            self.logo_label.pack(side="left", padx=(0, 10))
        except Exception as e:
            self.logo_label = ctk.CTkLabel(self.logo_top, text="[Logo Missing]", text_color="red")
            self.logo_label.pack(side="left", padx=(0, 10))

        self.brand_name = ctk.CTkLabel(self.logo_top, text="VeloCity", font=("Arial", 40, "bold"), text_color="#00d4ff")
        self.brand_name.pack(side="left")

        self.tagline = ctk.CTkLabel(self.brand_frame, text="Redefining Urban Transit", font=("Arial", 16, "italic"), text_color="gray")
        self.tagline.pack(pady=(5,0))

        self.separator = ctk.CTkFrame(self.brand_frame, height=2, fg_color="#00d4ff")
        self.separator.pack(fill="x", pady=(10, 0))
        # --- VeloCity Branding End ---

        self.label = ctk.CTkLabel(self.container, text="Account Access", font=("Arial", 16, "bold"))
        self.label.pack(pady=(10, 5))

        self.username_entry = ctk.CTkEntry(self.container, placeholder_text="Username", width=250)
        self.username_entry.pack(pady=10)

        self.pw_frame = ctk.CTkFrame(self.container, fg_color="transparent")
        self.pw_frame.pack(pady=10)
        self.password_entry = ctk.CTkEntry(self.pw_frame, placeholder_text="Password", show="*", width=208)
        self.password_entry.pack(side="left")
        self.pw_toggle = ctk.CTkButton(self.pw_frame, text="👁", width=30, fg_color="transparent", text_color="white", hover_color="#555555", command=lambda: self.toggle_password(self.password_entry, self.pw_toggle))
        self.pw_toggle.pack(side="left", padx=(2, 10))

        self.login_btn = ctk.CTkButton(self.container, text="Login", fg_color="#0066ff", hover_color="#005ce6", command=self.login, width=250)
        self.login_btn.pack(pady=10)

        self.register_btn = ctk.CTkButton(self.container, text="Go to Register", fg_color="gray", hover_color="darkgray", 
                                          command=lambda: controller.show_frame("RegisterFrame"), width=250)
        self.register_btn.pack(pady=10)

        self.forgot_pw_btn = ctk.CTkButton(self.container, text="Forgot Password?", fg_color="transparent", text_color="#1f538d", hover_color="lightgray", command=self.forgot_password, width=250)
        self.forgot_pw_btn.pack(pady=5)

    def toggle_password(self, entry, button):
        if entry.cget("show") == "*":
            entry.configure(show="")
            button.configure(text="🔒")
        else:
            entry.configure(show="*")
            button.configure(text="👁")

    def login(self):
        username = self.username_entry.get()
        password = self.password_entry.get()

        if not username or not password:
            messagebox.showwarning("Warning", "Please enter both username and password.")
            return

        hashed_password = hash_password(password)

        self.db.cursor.execute("SELECT id, role FROM users WHERE username=? AND password=?", (username, hashed_password))
        user = self.db.cursor.fetchone()

        if user:
            self.username_entry.delete(0, 'end')
            self.password_entry.delete(0, 'end')
            user_id, role = user
            if role == "admin":
                self.controller.show_frame("AdminDashboard", user_id=user_id)
            else:
                self.controller.show_frame("CustomerDashboard", user_id=user_id)
        else:
            self.password_entry.delete(0, 'end')
            messagebox.showerror("Error", "Invalid username or password")

    def forgot_password(self):
        forgot_win = ctk.CTkToplevel(self)
        forgot_win.title("Forgot Password")
        forgot_win.geometry("350x400")
        forgot_win.attributes("-topmost", True)
        
        lbl = ctk.CTkLabel(forgot_win, text="Reset Password", font=("Arial", 20, "bold"))
        lbl.pack(pady=20)
        
        user_entry = ctk.CTkEntry(forgot_win, placeholder_text="Username", width=200)
        user_entry.pack(pady=10)
        
        hint_display_label = ctk.CTkLabel(forgot_win, text="", text_color="#FBC02D")

        def show_hint():
            u = user_entry.get().strip()
            if not u:
                messagebox.showwarning("Warning", "Enter a username first.")
                return
            self.db.cursor.execute("SELECT security_key FROM users WHERE username=?", (u,))
            row = self.db.cursor.fetchone()
            if row and row[0]:
                key = str(row[0])
                hint = key[:2] + "*" * len(key[2:]) if len(key) >= 2 else key + "*"
                hint_display_label.configure(text=f"Hint: {hint}")
            else:
                messagebox.showerror("Error", "Username not found.")
                
        hint_btn = ctk.CTkButton(forgot_win, text="Get Hint", width=200, fg_color="gray", hover_color="darkgray", command=show_hint)
        hint_btn.pack(pady=5)
        
        hint_display_label.pack(pady=2)
        
        sec_entry = ctk.CTkEntry(forgot_win, placeholder_text="Security Answer", width=200)
        sec_entry.pack(pady=5)
        
        new_pw_frame = ctk.CTkFrame(forgot_win, fg_color="transparent")
        new_pw_frame.pack(pady=10)
        new_pw_entry = ctk.CTkEntry(new_pw_frame, placeholder_text="New Password", show="*", width=158)
        new_pw_entry.pack(side="left")
        new_pw_toggle = ctk.CTkButton(new_pw_frame, text="👁", width=30, fg_color="transparent", text_color="white", hover_color="#555555", command=lambda: self.toggle_password(new_pw_entry, new_pw_toggle))
        new_pw_toggle.pack(side="left", padx=(2, 10))
        
        def reset_pw():
            u = user_entry.get().strip()
            s = sec_entry.get().strip()
            np = new_pw_entry.get().strip()
            
            if not u or not s or not np:
                messagebox.showwarning("Warning", "All fields are required.")
                return
                
            self.db.cursor.execute("SELECT security_key FROM users WHERE username=?", (u,))
            row = self.db.cursor.fetchone()
            if not row:
                messagebox.showerror("Error", "Username not found.")
                return
                
            real_key = str(row[0])
            if s.lower() != real_key.lower():
                messagebox.showerror("Error", "Incorrect security answer.")
                return
                
            hashed_pw = hash_password(np)
            try:
                self.db.cursor.execute("UPDATE users SET password=? WHERE username=?", (hashed_pw, u))
                self.db.conn.commit()
                messagebox.showinfo("Success", "Password reset successfully! You can now login.")
                forgot_win.destroy()
            except Exception as e:
                messagebox.showerror("Error", f"Failed to update password: {e}")
                
        reset_btn = ctk.CTkButton(forgot_win, text="Reset Password", fg_color="#0066ff", hover_color="#005ce6", command=reset_pw, width=200)
        reset_btn.pack(pady=20)

class RegisterFrame(ctk.CTkFrame):
    def __init__(self, master, controller, db):
        super().__init__(master)
        self.controller = controller
        self.db = db

        self.container = ctk.CTkFrame(self)
        self.container.place(relx=0.5, rely=0.5, anchor="center")

        self.label = ctk.CTkLabel(self.container, text="Register", font=("Arial", 24, "bold"))
        self.label.pack(pady=20, padx=50)

        self.username_entry = ctk.CTkEntry(self.container, placeholder_text="Username", width=250)
        self.username_entry.pack(pady=10)

        self.pw_frame = ctk.CTkFrame(self.container, fg_color="transparent")
        self.pw_frame.pack(pady=10)
        self.password_entry = ctk.CTkEntry(self.pw_frame, placeholder_text="Password", show="*", width=208)
        self.password_entry.pack(side="left")
        self.pw_toggle = ctk.CTkButton(self.pw_frame, text="👁", width=30, fg_color="transparent", text_color="white", hover_color="#555555", command=lambda: self.toggle_password(self.password_entry, self.pw_toggle))
        self.pw_toggle.pack(side="left", padx=(2, 10))
        
        self.conf_pw_frame = ctk.CTkFrame(self.container, fg_color="transparent")
        self.conf_pw_frame.pack(pady=10)
        self.confirm_password_entry = ctk.CTkEntry(self.conf_pw_frame, placeholder_text="Confirm Password", show="*", width=208)
        self.confirm_password_entry.pack(side="left")
        self.conf_pw_toggle = ctk.CTkButton(self.conf_pw_frame, text="👁", width=30, fg_color="transparent", text_color="white", hover_color="#555555", command=lambda: self.toggle_password(self.confirm_password_entry, self.conf_pw_toggle))
        self.conf_pw_toggle.pack(side="left", padx=(2, 10))

        self.security_key_entry = ctk.CTkEntry(self.container, placeholder_text="Security Key (Recovery)", width=250)
        self.security_key_entry.pack(pady=10)

        self.register_btn = ctk.CTkButton(self.container, text="Register", fg_color="#0066ff", hover_color="#005ce6", command=self.register, width=250)
        self.register_btn.pack(pady=10)

        self.login_btn = ctk.CTkButton(self.container, text="Go to Login", fg_color="gray", hover_color="darkgray",
                                       command=lambda: controller.show_frame("LoginFrame"), width=250)
        self.login_btn.pack(pady=10)

    def toggle_password(self, entry, button):
        if entry.cget("show") == "*":
            entry.configure(show="")
            button.configure(text="🔒")
        else:
            entry.configure(show="*")
            button.configure(text="👁")

    def register(self):
        username = self.username_entry.get().strip()
        password = self.password_entry.get().strip()
        conf_password = self.confirm_password_entry.get().strip()
        sec_key = self.security_key_entry.get().strip()

        if not username or not password or not conf_password or not sec_key:
            messagebox.showwarning("Warning", "Please enter all fields including security key.")
            return
            
        if password != conf_password:
            messagebox.showwarning("Warning", "Passwords do not match!")
            return

        hashed_password = hash_password(password)

        try:
            self.db.cursor.execute("INSERT INTO users (username, password, role, security_key) VALUES (?, ?, ?, ?)", 
                                   (username, hashed_password, "customer", sec_key))
            self.db.conn.commit()
            messagebox.showinfo("Success", "Registration successful. Please login.")
            self.username_entry.delete(0, 'end')
            self.password_entry.delete(0, 'end')
            self.confirm_password_entry.delete(0, 'end')
            self.security_key_entry.delete(0, 'end')
            self.controller.show_frame("LoginFrame")
        except Exception as e:
            messagebox.showerror("Error", "Username already exists or registration failed.")

class CustomerDashboard(ctk.CTkFrame):
    def __init__(self, master, controller, db):
        super().__init__(master)
        self.controller = controller
        self.db = db
        
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=2)
        self.grid_columnconfigure(2, weight=1)
        self.grid_rowconfigure(1, weight=1)

        self.header_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.header_frame.grid(row=0, column=0, columnspan=3, sticky="ew", padx=20, pady=10)
        self.header_frame.grid_columnconfigure(0, weight=1)

        self.logo_top = ctk.CTkFrame(self.header_frame, fg_color="transparent")
        self.logo_top.grid(row=0, column=0, sticky="w")

        self.circle_logo = ctk.CTkFrame(self.logo_top, width=40, height=40, corner_radius=20, fg_color="#001F54")
        self.circle_logo.pack(side="left", padx=(0, 10))
        self.circle_logo.pack_propagate(False)
        self.v_label = ctk.CTkLabel(self.circle_logo, text="V", font=("Arial", 28, "bold"), text_color="white")
        self.v_label.place(relx=0.5, rely=0.5, anchor="center")

        self.brand_name = ctk.CTkLabel(self.logo_top, text="VeloCity", font=("Arial", 24, "bold"), text_color="#00d4ff")
        self.brand_name.pack(side="left")

        self.header = ctk.CTkLabel(self.logo_top, text="| Customer", font=("Arial", 20), text_color="gray")
        self.header.pack(side="left", padx=10)

        self.btns_frame = ctk.CTkFrame(self.header_frame, fg_color="transparent")
        self.btns_frame.grid(row=0, column=1, sticky="e")

        self.admin_btn = ctk.CTkButton(self.btns_frame, text="⚙ Admin Dashboard", fg_color="#FBC02D", text_color="black", hover_color="#F9A825", command=lambda: controller.show_frame("AdminDashboard", user_id=self.controller.current_user_id))
        
        self.logout_btn = ctk.CTkButton(self.btns_frame, text="Logout", width=100, fg_color="#FF4C4C", hover_color="#D32F2F", command=lambda: controller.show_frame("LoginFrame"))
        self.logout_btn.grid(row=0, column=1, padx=(5, 0))

        self.bus_list_frame = ctk.CTkScrollableFrame(self, label_text="Available Buses")
        self.bus_list_frame.grid(row=1, column=0, sticky="nsew", padx=20, pady=10)
        
        self.selected_seats = []
        self.current_bus_context = {}

        self.seat_frame_container = ctk.CTkFrame(self)
        self.seat_frame_container.grid(row=1, column=1, sticky="nsew", padx=20, pady=10)
        
        self.seat_info_label = ctk.CTkLabel(self.seat_frame_container, text="Select a bus to view seats", font=("Arial", 16))
        self.seat_info_label.pack(pady=10)
        
        self.cart_frame = ctk.CTkFrame(self.seat_frame_container, fg_color="transparent")
        self.cart_frame.pack(fill="x", padx=20)
        
        self.price_label = ctk.CTkLabel(self.cart_frame, text="Ticket Price: ₹500", font=("Arial", 14))
        self.price_label.pack(side="left")
        
        self.total_label = ctk.CTkLabel(self.cart_frame, text="Total Amount: ₹0", font=("Arial", 16, "bold"), text_color="#4CAF50")
        self.total_label.pack(side="left", padx=20)
        
        self.checkout_btn = ctk.CTkButton(self.cart_frame, text="Proceed to Details", fg_color="#0066ff", hover_color="#005ce6", command=self.open_checkout)
        self.checkout_btn.pack(side="right")
        self.checkout_btn.configure(state="disabled")
        
        self.seat_frame = ctk.CTkFrame(self.seat_frame_container, fg_color="transparent")
        self.seat_frame.pack(expand=True, fill="both", padx=20, pady=10)
        
        self.my_bookings_list = ctk.CTkScrollableFrame(self, label_text="My Bookings")
        self.my_bookings_list.grid(row=1, column=2, sticky="nsew", padx=20, pady=10)

        self.load_buses()
        self.load_user_bookings()

    def refresh_permissions(self):
        self.db.cursor.execute("SELECT role FROM users WHERE id=?", (self.controller.current_user_id,))
        role = self.db.cursor.fetchone()
        if role and role[0] == 'admin':
            self.admin_btn.grid(row=0, column=0)
        else:
            self.admin_btn.grid_forget()

    def load_user_bookings(self):
        self.refresh_permissions()
        for widget in self.my_bookings_list.winfo_children():
            widget.destroy()
            
        query = """
            SELECT bookings.id, buses.name, bookings.seat_num, buses.id, buses.total_seats, bookings.status, bookings.admin_comment
            FROM bookings
            JOIN buses ON bookings.bus_id = buses.id
            WHERE bookings.user_id = ?
        """
        self.db.cursor.execute(query, (self.controller.current_user_id,))
        user_bookings = self.db.cursor.fetchall()
        
        if not user_bookings:
            lbl = ctk.CTkLabel(self.my_bookings_list, text="No bookings yet.")
            lbl.pack(pady=10)
        else:
            for bkg in user_bookings:
                booking_id, bus_name, seat_num, bus_id, total_seats, status, admin_comment = bkg
                
                frame = ctk.CTkFrame(self.my_bookings_list)
                frame.pack(fill="x", pady=5, padx=5)
                
                lbl = ctk.CTkLabel(frame, text=f"{bus_name} - Seat {seat_num}")
                lbl.pack(side="left", padx=10, pady=5)
                
                if status == 'cancelled':
                    err_lbl = ctk.CTkLabel(frame, text="", text_color="#FF4C4C", font=("Arial", 12, "bold"), width=250, anchor="e")
                    err_lbl.pack(side="right", padx=10, pady=5)
                    full_text = f"⚠️ Ticket Cancelled by Admin: {admin_comment}"
                    self.start_marquee(err_lbl, full_text, display_width=30)
                else:
                    btn_cancel = ctk.CTkButton(frame, text="Cancel", fg_color="#FF4C4C", hover_color="#D32F2F", width=60,
                                        command=lambda b_id=booking_id, bus=bus_id, total=total_seats, b_name=bus_name: self.cancel_my_booking(b_id, bus, total, b_name))
                    btn_cancel.pack(side="right", padx=10, pady=5)
                    
                    btn_dl = ctk.CTkButton(frame, text="Download", fg_color="#4CAF50", hover_color="#388E3C", width=60,
                                        command=lambda b_id=booking_id: self.download_ticket(b_id))
                    btn_dl.pack(side="right", padx=(0, 5), pady=5)

    def start_marquee(self, label, full_text, display_width=30, delay=80):
        # Always pad for continuous effect
        padded_text = full_text + "   •   "
        
        # Ensure string is long enough to slice the display width out of it
        multiplier = (display_width // len(padded_text)) + 2
        
        def update_marquee(offset):
            if not label.winfo_exists():
                return
                
            current_text = (padded_text * multiplier)[offset : offset + display_width]
            label.configure(text=current_text)
            
            next_offset = (offset + 1) % len(padded_text)
            label.after(delay, update_marquee, next_offset)
            
        update_marquee(0)

    def download_ticket(self, booking_id):
        import tkinter.filedialog as filedialog
        import shutil
        import os
        import tkinter.messagebox as messagebox
        
        save_path = filedialog.asksaveasfilename(
            defaultextension=".pdf",
            filetypes=[("PDF files", "*.pdf"), ("JPEG files", "*.jpg"), ("Text files", "*.txt")],
            title="Save Ticket As",
            initialfile=f"Ticket_{booking_id}"
        )
        
        if save_path:
            ext = os.path.splitext(save_path)[1].lower()
            if ext == ".pdf":
                source_file = f"tickets/Ticket_{booking_id}.pdf"
            elif ext in [".jpg", ".jpeg"]:
                source_file = f"tickets/Ticket_{booking_id}.jpg"
            else:
                source_file = f"tickets/Ticket_{booking_id}.txt"
                
            if os.path.exists(source_file):
                try:
                    shutil.copy2(source_file, save_path)
                    messagebox.showinfo("Success", f"Ticket saved successfully!")
                except Exception as e:
                    messagebox.showerror("Error", f"Failed to save: {e}")
            else:
                messagebox.showerror("Error", "Ticket file not found in system.")

    def cancel_my_booking(self, booking_id, bus_id, total_seats, bus_name):
        confirm = messagebox.askyesno("Confirm Cancel", "Cancel this booking?")
        if confirm:
            try:
                self.db.cancel_booking(booking_id)
                from utils import void_ticket
                void_ticket(booking_id)
                messagebox.showinfo("Success", "Booking has been VOIDED in the system records.")
                self.load_user_bookings()
                
                # Refresh seat grid if currently viewing this bus
                if self.seat_info_label.cget("text") == f"Seats for {bus_name}":
                    self.show_seats(bus_id, total_seats, bus_name)
            except Exception as e:
                messagebox.showerror("Error", f"Cancel failed: {e}")

    def load_buses(self):
        self.db.cursor.execute("SELECT id, name, route, total_seats, time FROM buses limit 3")
        buses = self.db.cursor.fetchall()

        for widget in self.bus_list_frame.winfo_children():
            widget.destroy()

        for bus in buses:
            bus_id, name, route, total_seats, time = bus
            btn_text = f"{name}\n{route} - {time}"
            btn = ctk.CTkButton(self.bus_list_frame, text=btn_text, 
                                command=lambda b_id=bus_id, s=total_seats, n=name: self.show_seats(b_id, s, n))
            btn.pack(pady=10, fill="x", padx=10)

    def show_seats(self, bus_id, total_seats, bus_name):
        self.current_bus_context = {"id": bus_id, "name": bus_name, "total": total_seats}
        self.selected_seats = []
        self.update_cart_ui()
        self.seat_info_label.configure(text=f"Seats for {bus_name}")
        
        for widget in self.seat_frame.winfo_children():
            widget.destroy()

        self.db.cursor.execute("SELECT seat_num FROM bookings WHERE bus_id=? AND status='active'", (bus_id,))
        booked_seats = [row[0] for row in self.db.cursor.fetchall()]

        cols = 5  # 5 seats per row (2+3 configuration)
        for i in range(total_seats):
            seat_num = i + 1
            row_idx = i // cols
            grid_col_idx = i % cols
            
            # create an aisle at column 2 visually
            if grid_col_idx >= 2:
                grid_col_idx += 1 # Shifts 2,3,4 to 3,4,5

            is_booked = seat_num in booked_seats
            color = "#FF4C4C" if is_booked else "#4CAF50" # Red if booked, Green if available
            hover_color = "#D32F2F" if is_booked else "#388E3C"
            state = "disabled" if is_booked else "normal"

            btn = ctk.CTkButton(self.seat_frame, text=str(seat_num), width=45, height=45,
                                fg_color=color, hover_color=hover_color, state=state, text_color="white",
                                command=lambda s=seat_num: self.toggle_seat(s))
            btn.grid(row=row_idx, column=grid_col_idx, padx=8, pady=8)
            
        # Give all 6 columns (including empty aisle column 2) equal weight
        for i in range(6): 
            self.seat_frame.grid_columnconfigure(i, weight=1)

    def toggle_seat(self, seat_num):
        if seat_num in self.selected_seats:
            self.selected_seats.remove(seat_num)
        else:
            self.selected_seats.append(seat_num)
        
        self.update_cart_ui()
        for widget in self.seat_frame.winfo_children():
            if isinstance(widget, ctk.CTkButton) and widget.cget("text") == str(seat_num):
                if seat_num in self.selected_seats:
                    widget.configure(fg_color="#FBC02D", hover_color="#F9A825")
                else:
                    widget.configure(fg_color="#4CAF50", hover_color="#388E3C")

    def update_cart_ui(self):
        total = len(self.selected_seats) * 500
        self.total_label.configure(text=f"Total Amount: ₹{total}")
        if len(self.selected_seats) > 0:
            self.checkout_btn.configure(state="normal")
        else:
            self.checkout_btn.configure(state="disabled")

    def open_checkout(self):
        if not self.selected_seats:
            return
            
        checkout_win = ctk.CTkToplevel(self)
        checkout_win.title("Checkout Details")
        checkout_win.geometry("500x600")
        checkout_win.attributes("-topmost", True)
        
        lbl = ctk.CTkLabel(checkout_win, text=f"Booking for {self.current_bus_context['name']}", font=("Arial", 20, "bold"))
        lbl.pack(pady=10)
        
        contact_frame = ctk.CTkFrame(checkout_win, fg_color="transparent")
        contact_frame.pack(pady=(10, 20))
        
        contact_lbl = ctk.CTkLabel(contact_frame, text="Primary Contact:", font=("Arial", 14, "bold"))
        contact_lbl.pack(side="left", padx=10)
        
        contact_var = ctk.StringVar()
        contact_entry = ctk.CTkEntry(contact_frame, placeholder_text="Enter 10-digit number", width=200, textvariable=contact_var)
        contact_entry.pack(side="left", padx=10)
        
        scroll = ctk.CTkScrollableFrame(checkout_win, label_text="Passenger Details")
        scroll.pack(expand=True, fill="both", padx=20, pady=10)
        
        passenger_inputs = {}
        for seat in sorted(self.selected_seats):
            frame = ctk.CTkFrame(scroll)
            frame.pack(fill="x", pady=5)
            ctk.CTkLabel(frame, text=f"Seat {seat}:", font=("Arial", 14, "bold"), width=60).pack(side="left", padx=5)
            
            n_var = ctk.StringVar()
            a_var = ctk.StringVar()
            g_var = ctk.StringVar(value="Gender")
            
            ctk.CTkEntry(frame, placeholder_text="Name", width=120, textvariable=n_var).pack(side="left", padx=5)
            ctk.CTkEntry(frame, placeholder_text="Age", width=50, textvariable=a_var).pack(side="left", padx=5)
            ctk.CTkOptionMenu(frame, values=["Male", "Female", "Other"], width=90, variable=g_var).pack(side="left", padx=5)
            
            passenger_inputs[seat] = {"name": n_var, "age": a_var, "gender": g_var}
            
        def confirm_batch():
            phone = contact_var.get().strip()
            if not phone:
                messagebox.showwarning("Warning", "Contact phone is required.")
                return
                
            payloads = []
            for seat, inputs in passenger_inputs.items():
                n = inputs['name'].get().strip()
                a = inputs['age'].get().strip()
                g = inputs['gender'].get()
                
                if not n or not a or g == "Gender":
                    messagebox.showwarning("Warning", f"Details missing for Seat {seat}")
                    return
                if not a.isdigit():
                    messagebox.showwarning("Warning", f"Age must be a number for Seat {seat}")
                    return
                    
                payloads.append((seat, n, int(a), g))
                
            confirm_btn.configure(state="disabled")
            try:
                self.db.cursor.execute("SELECT username FROM users WHERE id=?", (self.controller.current_user_id,))
                username = self.db.cursor.fetchone()[0]
                
                from utils import generate_ticket
                for payload in payloads:
                    seat, p_name, p_age, p_gender = payload
                    self.db.cursor.execute("INSERT INTO bookings (user_id, bus_id, seat_num, passenger_name, passenger_age, passenger_gender, contact_number) VALUES (?, ?, ?, ?, ?, ?, ?)",
                                        (self.controller.current_user_id, self.current_bus_context['id'], seat, p_name, p_age, p_gender, phone))
                    booking_id = self.db.cursor.lastrowid
                    generate_ticket(username, self.current_bus_context['name'], seat, booking_id, p_name, p_age, p_gender, phone)
                
                self.db.conn.commit()
                self.selected_seats.clear()
                
                bus_id, total, b_name = self.current_bus_context['id'], self.current_bus_context['total'], self.current_bus_context['name']
                self.show_seats(bus_id, total, b_name)
                self.load_user_bookings()
                
                checkout_win.destroy()
                messagebox.showinfo("Success", f"{len(payloads)} seats successfully booked! Tickets generated.")
                
            except Exception as e:
                confirm_btn.configure(state="normal")
                messagebox.showerror("Error", f"Batch booking failed: {e}")
                
        confirm_btn = ctk.CTkButton(checkout_win, text="Confirm Batch Booking", fg_color="#4CAF50", hover_color="#388E3C", command=confirm_batch)
        confirm_btn.pack(pady=20)

class AdminDashboard(ctk.CTkFrame):
    def __init__(self, master, controller, db):
        super().__init__(master)
        self.controller = controller
        self.db = db

        self.grid_columnconfigure(0, weight=3)
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(1, weight=1)

        self.header_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.header_frame.grid(row=0, column=0, columnspan=2, sticky="ew", padx=20, pady=10)
        self.header_frame.grid_columnconfigure(0, weight=1)

        self.logo_top = ctk.CTkFrame(self.header_frame, fg_color="transparent")
        self.logo_top.grid(row=0, column=0, sticky="w")

        self.circle_logo = ctk.CTkFrame(self.logo_top, width=40, height=40, corner_radius=20, fg_color="#001F54")
        self.circle_logo.pack(side="left", padx=(0, 10))
        self.circle_logo.pack_propagate(False)
        self.v_label = ctk.CTkLabel(self.circle_logo, text="V", font=("Arial", 28, "bold"), text_color="white")
        self.v_label.place(relx=0.5, rely=0.5, anchor="center")

        self.brand_name = ctk.CTkLabel(self.logo_top, text="VeloCity", font=("Arial", 24, "bold"), text_color="#00d4ff")
        self.brand_name.pack(side="left")

        self.header = ctk.CTkLabel(self.logo_top, text="| Admin", font=("Arial", 20), text_color="gray")
        self.header.pack(side="left", padx=10)

        self.btns_frame = ctk.CTkFrame(self.header_frame, fg_color="transparent")
        self.btns_frame.grid(row=0, column=1, sticky="e")

        self.switch_btn = ctk.CTkButton(self.btns_frame, text="Switch to Booking View", width=150, fg_color="#4CAF50", hover_color="#388E3C",
                                        command=lambda: controller.show_frame("CustomerDashboard", user_id=self.controller.current_user_id))
        self.switch_btn.pack(side="left", padx=10)

        self.logout_btn = ctk.CTkButton(self.btns_frame, text="Logout", width=100, fg_color="#FF4C4C", hover_color="#D32F2F",
                                        command=lambda: controller.show_frame("LoginFrame"))
        self.logout_btn.pack(side="left")

        self.bookings_frame = ctk.CTkScrollableFrame(self, label_text="All Bookings")
        self.bookings_frame.grid(row=1, column=0, sticky="nsew", padx=20, pady=10)

        self.admins_frame = ctk.CTkFrame(self)
        self.admins_frame.grid(row=1, column=1, sticky="nsew", padx=20, pady=10)
        
        self.admins_label = ctk.CTkLabel(self.admins_frame, text="Registered Admins", font=("Arial", 16, "bold"))
        self.admins_label.pack(pady=10)
        
        self.admins_list = ctk.CTkScrollableFrame(self.admins_frame)
        self.admins_list.pack(expand=True, fill="both", padx=10, pady=10)

        self.promote_entry = ctk.CTkEntry(self.admins_frame, placeholder_text="Username to promote")
        self.promote_entry.pack(pady=(5,0), padx=10, fill="x")
        
        self.promote_btn = ctk.CTkButton(self.admins_frame, text="Promote to Admin", fg_color="#0066ff", hover_color="#005ce6", command=self.promote_admin)
        self.promote_btn.pack(pady=(5,10), padx=10, fill="x")

        self.revenue_frame = ctk.CTkFrame(self)
        self.revenue_frame.grid(row=2, column=0, columnspan=2, sticky="ew", padx=20, pady=10)
        
        self.revenue_label = ctk.CTkLabel(self.revenue_frame, text="Total Revenue: ₹0", font=("Arial", 18, "bold"), text_color="#4CAF50")
        self.revenue_label.pack(side="left", padx=20, pady=10)
        
        self.refresh_btn = ctk.CTkButton(self.revenue_frame, text="Refresh", fg_color="#0066ff", hover_color="#005ce6", command=self.load_data)
        self.refresh_btn.pack(side="right", padx=20, pady=10)

        self.vault_frame = ctk.CTkScrollableFrame(self, label_text="The Admin Vault (User Management)")
        self.vault_frame.grid(row=3, column=0, columnspan=2, sticky="nsew", padx=20, pady=10)
        self.grid_rowconfigure(3, weight=2)

        self.load_data()

    def load_data(self):
        # Load bookings using SQL JOIN
        query = """
            SELECT bookings.id, users.username, buses.name, bookings.seat_num, bookings.status
            FROM bookings
            JOIN users ON bookings.user_id = users.id
            JOIN buses ON bookings.bus_id = buses.id
        """
        self.db.cursor.execute(query)
        all_bookings = self.db.cursor.fetchall()

        for widget in self.bookings_frame.winfo_children():
            widget.destroy()

        if not all_bookings:
            lbl = ctk.CTkLabel(self.bookings_frame, text="No bookings found.")
            lbl.pack(pady=10)
        else:
            for bkg in all_bookings:
                bkg_id, username, bus_name, seat, status = bkg
                
                frame = ctk.CTkFrame(self.bookings_frame, fg_color="transparent")
                frame.pack(fill="x", pady=2)
                
                status_text = "[CANCELLED] " if status == 'cancelled' else ""
                lbl_text = f"Booking ID: {bkg_id} | User: {username} | Bus: {bus_name} | Seat: {seat} {status_text}"
                lbl = ctk.CTkLabel(frame, text=lbl_text, font=("Arial", 14))
                lbl.pack(side="left", padx=10)
                
                if status == 'active':
                    cancel_btn = ctk.CTkButton(frame, text="Cancel Ticket", width=100, fg_color="#FF4C4C", hover_color="#D32F2F",
                                        command=lambda b=bkg_id: self.admin_cancel_ticket(b))
                    cancel_btn.pack(side="right", padx=5)

                btn = ctk.CTkButton(frame, text="View Ticket File", width=120, fg_color="#1f538d",
                                    command=lambda b=bkg_id: self.open_ticket(b))
                btn.pack(side="right", padx=5)

        # Load admins
        self.db.cursor.execute("SELECT username FROM users WHERE role='admin'")
        admins = self.db.cursor.fetchall()

        for widget in self.admins_list.winfo_children():
            widget.destroy()

        for adm in admins:
            lbl = ctk.CTkLabel(self.admins_list, text=adm[0], font=("Arial", 14))
            lbl.pack(pady=5)

        # Load Revenue
        self.db.cursor.execute("SELECT COUNT(*) FROM bookings WHERE status='active'")
        total_bookings = self.db.cursor.fetchone()[0]
        revenue = total_bookings * 500
        self.revenue_label.configure(text=f"Total Revenue: ₹{revenue}")

        # Load Admin Vault
        self.db.cursor.execute("SELECT username, role, password FROM users")
        vault_users = self.db.cursor.fetchall()
        
        for widget in self.vault_frame.winfo_children():
            widget.destroy()
            
        for v_user in vault_users:
            u_name, u_role, u_pass = v_user
            display_pass = str(u_pass)[:10] + "..." if len(str(u_pass)) > 10 else u_pass
            
            frame = ctk.CTkFrame(self.vault_frame, fg_color="transparent")
            frame.pack(fill="x", pady=2)
            
            lbl = ctk.CTkLabel(frame, text=f"Username: {u_name}  |  Role: {u_role}  |  Hash: {display_pass}", font=("Arial", 14))
            lbl.pack(side="left", padx=10)
            
            btn = ctk.CTkButton(frame, text="Reset Password", width=120, fg_color="#FF9800", hover_color="#F57C00",
                                command=lambda u=u_name: self.force_reset_password(u))
            btn.pack(side="right", padx=10)

    def force_reset_password(self, target_username):
        dialog = ctk.CTkInputDialog(text=f"Enter new password for '{target_username}':", title="Force Password Reset")
        new_pw = dialog.get_input()
        
        if new_pw and new_pw.strip():
            try:
                from utils import hash_password
                hashed_pw = hash_password(new_pw.strip())
                self.db.cursor.execute("UPDATE users SET password=? WHERE username=?", (hashed_pw, target_username))
                self.db.conn.commit()
                messagebox.showinfo("Success", f"Password for '{target_username}' forcefully overridden!")
                self.load_data()
            except Exception as e:
                messagebox.showerror("Error", f"Failed to reset: {e}")

    def admin_cancel_ticket(self, booking_id):
        dialog = ctk.CTkInputDialog(text="Reason for Cancellation:", title="Cancel Ticket")
        reason = dialog.get_input()
        
        if reason and reason.strip():
            try:
                self.db.cursor.execute("UPDATE bookings SET status='cancelled', admin_comment=? WHERE id=?", (reason.strip(), booking_id))
                self.db.conn.commit()
                
                from utils import void_ticket
                void_ticket(booking_id)
                
                messagebox.showinfo("Success", f"Ticket {booking_id} cancelled successfully.")
                self.load_data()
            except Exception as e:
                messagebox.showerror("Error", f"Failed to cancel ticket: {e}")

    def open_ticket(self, booking_id):
        import os
        filepath = os.path.abspath(f"tickets/Ticket_{booking_id}.txt")
        if os.path.exists(filepath):
            try:
                # Safely open for Windows
                os.startfile(filepath)
            except Exception as e:
                messagebox.showerror("Error", f"Failed to open file: {e}")
        else:
            messagebox.showerror("Error", f"Ticket file for Booking {booking_id} not found.")

    def promote_admin(self):
        target_username = self.promote_entry.get().strip()
        if not target_username:
            messagebox.showwarning("Warning", "Please enter a username.")
            return
            
        self.db.cursor.execute("SELECT id, role FROM users WHERE username=?", (target_username,))
        user = self.db.cursor.fetchone()
        
        if not user:
            messagebox.showerror("Error", "Username not found.")
            return
            
        if user[1] == 'admin':
            messagebox.showinfo("Info", "User is already an admin.")
            return

        confirm = messagebox.askyesno("Confirm Promotion", f"Promote '{target_username}' to Admin?")
        if confirm:
            try:
                self.db.cursor.execute("UPDATE users SET role='admin' WHERE username=?", (target_username,))
                self.db.conn.commit()
                messagebox.showinfo("Success", f"'{target_username}' is now an Admin!")
                self.promote_entry.delete(0, 'end')
                self.load_data()  # Refresh lists
            except Exception as e:
                messagebox.showerror("Error", f"Failed to promote: {e}")
                
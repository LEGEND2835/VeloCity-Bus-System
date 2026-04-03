import customtkinter as ctk
from database import DatabaseManager
from ui_frames import LoginFrame, RegisterFrame, CustomerDashboard, AdminDashboard

class App(ctk.CTk):
    def __init__(self):
        super().__init__()
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("blue")
        self.title("VeloCity | Smart Bus Management")
        self.geometry("800x600")
        
        self.db = DatabaseManager()
        self.current_user_id = None
        
        self.container = ctk.CTkFrame(self)
        self.container.pack(fill="both", expand=True)
        self.container.grid_rowconfigure(0, weight=1)
        self.container.grid_columnconfigure(0, weight=1)
        
        self.frames = {}
        
        for F in (LoginFrame, RegisterFrame):
            frame = F(master=self.container, controller=self, db=self.db)
            self.frames[F.__name__] = frame
            frame.grid(row=0, column=0, sticky="nsew")
            
        self.show_frame("LoginFrame")
        
        self.protocol("WM_DELETE_WINDOW", self.on_closing)

    def on_closing(self):
        # Gracefully disconnect before exiting
        try:
            self.db.conn.close()
        except:
            pass
        self.destroy()

    def show_frame(self, frame_name, user_id=None):
        if user_id is not None:
            self.current_user_id = user_id
            
        if frame_name == "LoginFrame":
            self.current_user_id = None # clear user on logout
            
        if frame_name == "CustomerDashboard":
            frame = CustomerDashboard(master=self.container, controller=self, db=self.db)
            self.frames["CustomerDashboard"] = frame
            frame.grid(row=0, column=0, sticky="nsew")
            
        if frame_name == "AdminDashboard":
            frame = AdminDashboard(master=self.container, controller=self, db=self.db)
            self.frames["AdminDashboard"] = frame
            frame.grid(row=0, column=0, sticky="nsew")
            
        frame = self.frames[frame_name]
        frame.tkraise()

if __name__ == "__main__":
    app = App()
    app.mainloop()

import hashlib
import os
import sys
import types
from datetime import datetime

# Prevent ReportLab from crashing due to the blocked Pillow DLL
mock_pil = types.ModuleType('PIL')
mock_pil.Image = type('MockImage', (), {})
sys.modules['PIL'] = mock_pil

from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter

def hash_password(password):
    """Encodes the password into a secure hash so it's not stored as plain text."""
    return hashlib.sha256(password.encode()).hexdigest()

def generate_ticket(username, bus_name, seat_num, booking_id, passenger_name="", age=0, gender="", contact=""):
    """Generates a professional text-based ticket, PDF, and JPG, and saves it to a folder."""
    if not os.path.exists("tickets"):
        os.makedirs("tickets")
        
    date_str = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    
    # 1. TXT Generation
    txt_filename = f"tickets/Ticket_{booking_id}.txt"
    ticket_content = f"""
    ========================================
       VeloCity - Official E-Ticket
    ========================================
    Booking ID    : {booking_id}
    Account User  : {username}
    Contact Phone : {contact}
    ----------------------------------------
    Ticket Holder : {passenger_name}
    Demographics  : Age {age} | {gender}
    Bus Name      : {bus_name}
    Seat Number   : {seat_num}
    Booking Status: ACTIVE
    Date/Time     : {date_str}
    ========================================
       Thank you for traveling with us!
    ========================================
    """
    with open(txt_filename, "w") as f:
        f.write(ticket_content)
        
    # 2. PDF Generation
    pdf_filename = f"tickets/Ticket_{booking_id}.pdf"
    c = canvas.Canvas(pdf_filename, pagesize=letter)
    
    # Native VeloCity Logo (Blue Square with White V)
    c.setFillColorRGB(0.0, 0.122, 0.329) # #001F54 equivalent
    c.rect(50, 690, 50, 50, fill=1, stroke=0)
    c.setFillColorRGB(1, 1, 1) # White
    c.setFont("Helvetica-Bold", 36)
    c.drawString(64, 702, "V")
    
    c.setFillColorRGB(0, 0, 0) # Reset to black
    c.setFont("Helvetica-Bold", 24)
    c.drawString(115, 708, "VeloCity Transit - E-Ticket")
    
    c.setFont("Helvetica", 12)
    c.drawString(50, 650, f"Booking ID: {booking_id}")
    c.drawString(50, 630, f"Account User: {username}")
    c.drawString(50, 610, f"Booking Status: ACTIVE")
    
    c.setFont("Helvetica-Bold", 14)
    c.drawString(50, 570, "Passenger Details")
    c.setFont("Helvetica", 12)
    c.drawString(50, 550, f"Ticket Holder: {passenger_name}")
    c.drawString(50, 530, f"Demographics: Age {age} | {gender}")
    c.drawString(50, 510, f"Bus/Route: {bus_name}")
    c.drawString(50, 490, f"Seat Number: {seat_num}")
    c.drawString(50, 470, f"Total Fare: INR 500")
    
    c.drawString(50, 450, f"Primary Contact: {contact}")
    c.drawString(50, 430, f"Date/Time: {date_str}")
    c.save()
    
    return txt_filename

def void_ticket(booking_id):
    """Voids existing ticket files."""
    
    # Void TXT
    txt_filename = f"tickets/Ticket_{booking_id}.txt"
    if os.path.exists(txt_filename):
        void_content = f"""
    ========================================
             CANCELLED / VOID
    ========================================
    Booking ID        : {booking_id}
    Cancellation Time : {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
    ========================================
       This ticket is no longer valid.
    ========================================
    """
        with open(txt_filename, "w") as f:
            f.write(void_content)
            
    # Void PDF
    pdf_filename = f"tickets/Ticket_{booking_id}.pdf"
    if os.path.exists(pdf_filename):
        c = canvas.Canvas(pdf_filename, pagesize=letter)
        c.setFont("Helvetica-Bold", 40)
        c.setFillColorRGB(1, 0, 0)
        c.drawString(100, 400, "*** VOID / CANCELED ***")
        c.setFont("Helvetica", 14)
        c.drawString(100, 350, f"Booking ID {booking_id} has been voided.")
        c.save()
        
    # JPG voiding removed
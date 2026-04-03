import hashlib
import os
from datetime import datetime

from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from PIL import Image, ImageDraw, ImageFont

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
    
    try:
        if os.path.exists("logo.png"):
            c.drawImage("logo.png", 50, 700, width=50, height=50) # Very basic logo rendering
    except:
        pass
        
    c.setFont("Helvetica-Bold", 24)
    c.drawString(110, 715, "VeloCity - Official E-Ticket")
    
    c.setFont("Helvetica", 12)
    c.drawString(50, 650, f"Booking ID: {booking_id}")
    c.drawString(50, 630, f"Account User: {username}")
    c.drawString(50, 610, f"Booking Status: ACTIVE")
    
    c.setFont("Helvetica-Bold", 14)
    c.drawString(50, 570, "Passenger Details")
    c.setFont("Helvetica", 12)
    c.drawString(50, 550, f"Ticket Holder: {passenger_name}")
    c.drawString(50, 530, f"Demographics: Age {age} | {gender}")
    c.drawString(50, 510, f"Bus Name: {bus_name}")
    c.drawString(50, 490, f"Seat Number: {seat_num}")
    
    c.drawString(50, 450, f"Primary Contact: {contact}")
    c.drawString(50, 430, f"Date/Time: {date_str}")
    c.save()
    
    # 3. JPG Generation
    jpg_filename = f"tickets/Ticket_{booking_id}.jpg"
    img = Image.new('RGB', (600, 400), color=(255, 255, 255))
    d = ImageDraw.Draw(img)
    
    try:
        if os.path.exists("logo.png"):
            logo = Image.open("logo.png").convert("RGBA")
            logo = logo.resize((60, 60))
            img.paste(logo, (20, 20), logo)
    except:
        pass
        
    d.text((90, 35), "VeloCity - Official E-Ticket", fill=(0, 0, 0))
    d.text((20, 100), f"Booking ID: {booking_id}", fill=(0, 0, 0))
    d.text((20, 120), f"Status: ACTIVE", fill=(0, 128, 0))
    
    d.text((20, 160), "Passenger Details:", fill=(0, 0, 0))
    d.text((20, 180), f"Name: {passenger_name} | Age: {age} | Gender: {gender}", fill=(0, 0, 0))
    d.text((20, 200), f"Bus: {bus_name} | Seat: {seat_num}", fill=(0, 0, 0))
    
    d.text((20, 300), f"Primary Contact: {contact}", fill=(0, 0, 0))
    d.text((20, 320), f"Date: {date_str}", fill=(0, 0, 0))
    
    img.save(jpg_filename)
    
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
        
    # Void JPG
    jpg_filename = f"tickets/Ticket_{booking_id}.jpg"
    if os.path.exists(jpg_filename):
        img = Image.new('RGB', (600, 400), color=(255, 200, 200))
        d = ImageDraw.Draw(img)
        d.text((150, 180), "*** VOID / CANCELED ***", fill=(255, 0, 0))
        d.text((150, 220), f"Booking ID {booking_id} has been voided.", fill=(255, 0, 0))
        img.save(jpg_filename)
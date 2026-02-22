# Health System - Connection and Contact tracking

from config import DEBUG
import time

class HealthSystem:
    def __init__(self):
        """
        Initialize health system with two bars:
        - wireless_health: depletes if no LoRA sync, resets on sync
        - contact_health: depletes if no physical contact, resets on contact
        """
        self.wireless_health = 100  # 0-100
        self.contact_health = 100   # 0-100
        
        self.last_wireless_update = time.time()
        self.last_contact_update = time.time()
        
        # Time constants (in seconds)
        self.wireless_timeout = 10.0  # Health fully depletes in 10 seconds without sync
        self.contact_timeout = 30.0   # Health fully depletes in 30 seconds without contact
    
    def on_wireless_sync(self):
        """Called when LoRA packet is received"""
        self.wireless_health = 100
        self.last_wireless_update = time.time()
        if DEBUG:
            print("Wireless sync! Health reset to 100")
    
    def on_physical_contact(self):
        """Called when OneWire contact detected"""
        self.contact_health = 100
        self.last_contact_update = time.time()
        if DEBUG:
            print("Physical contact! Contact health reset to 100")
    
    def update(self):
        """Update health bars based on elapsed time since last update"""
        current_time = time.time()
        
        # Update wireless health
        wireless_elapsed = current_time - self.last_wireless_update
        self.wireless_health = max(0, 100 - (wireless_elapsed / self.wireless_timeout * 100))
        
        # Update contact health
        contact_elapsed = current_time - self.last_contact_update
        self.contact_health = max(0, 100 - (contact_elapsed / self.contact_timeout * 100))
    
    def get_wireless_health_percent(self):
        """Return wireless health as 0-100"""
        return int(self.wireless_health)
    
    def get_contact_health_percent(self):
        """Return contact health as 0-100"""
        return int(self.contact_health)
    
    def get_wireless_health_pixels(self, max_height=32):
        """Convert health to pixel height for bar display"""
        return int((self.wireless_health / 100.0) * max_height)
    
    def get_contact_health_pixels(self, max_height=32):
        """Convert health to pixel height for bar display"""
        return int((self.contact_health / 100.0) * max_height)

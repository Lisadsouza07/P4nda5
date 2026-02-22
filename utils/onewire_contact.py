# OneWire Contact Detection - Physical contact sensor

from machine import Pin
from config import DEBUG
import time

class OneWireContact:
    def __init__(self, pin_number):
        """
        Initialize OneWire contact detection
        
        Args:
            pin_number: GPIO pin to use for OneWire protocol
        """
        self.pin = Pin(pin_number, Pin.OPEN_DRAIN)  # OneWire uses open-drain
        self.callback = None
        self.last_contact_time = 0
        self.contact_debounce_ms = 100  # Debounce time in ms
    
    def on_contact(self, callback):
        """
        Register callback for contact detection
        
        Args:
            callback: Function to call when contact detected
        """
        self.callback = callback
    
    def _pull_low(self, duration_us):
        """Pull line low for specified duration (microseconds)"""
        self.pin.value(0)
        time.sleep_us(duration_us)
        self.pin.value(1)  # Release (open-drain)
    
    def _read_response(self, timeout_us=500):
        """
        Read response from OneWire device
        Returns True if device pulled line low within timeout
        """
        start = time.ticks_us()
        while time.ticks_diff(time.ticks_us(), start) < timeout_us:
            if self.pin.value() == 0:
                return True
        return False
    
    def reset_detect(self):
        """
        Perform OneWire reset and detect presence
        Returns True if device detected (short circuit from contact)
        """
        current_time = time.time() * 1000  # Convert to milliseconds
        
        # Debounce: ignore contacts within debounce window
        if (current_time - self.last_contact_time) < self.contact_debounce_ms:
            return False
        
        try:
            # Pull line low for 480µs (OneWire reset pulse)
            self._pull_low(480)
            
            # Wait 65µs for device presence pulse
            time.sleep_us(65)
            
            # Read for presence pulse (device pulls low for 60-240µs)
            presence = self._read_response(240)
            
            if presence:
                self.last_contact_time = current_time
                if self.callback:
                    self.callback()
                if DEBUG:
                    print("OneWire: Contact detected!")
                return True
            
        except Exception as e:
            if DEBUG:
                print(f"OneWire error: {e}")
        
        return False
    
    def check(self):
        """Periodically call to check for contact"""
        self.reset_detect()

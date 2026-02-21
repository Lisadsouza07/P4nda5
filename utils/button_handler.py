# Button Input Handler

from config import BUTTON_PIN, BUTTON_DEBOUNCE_MS
from machine import Pin
import time

class ButtonHandler:
    def __init__(self, callback):
        """
        Initialize button handler
        
        Args:
            callback: Function to call on button press
        """
        self.button = Pin(BUTTON_PIN, Pin.IN, Pin.PULL_UP)
        self.callback = callback
        self.last_press_time = 0
    
    def check(self):
        """Check for button press with debouncing"""
        if not self.button.value():  # Button pressed (active low)
            current_time = time.time() * 1000  # Convert to milliseconds
            if current_time - self.last_press_time > BUTTON_DEBOUNCE_MS:
                self.last_press_time = current_time
                self.callback()

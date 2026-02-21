# LoRA Communication Module

from config import (
    LORA_MOSI_PIN, LORA_MISO_PIN, LORA_CLK_PIN, LORA_CS_PIN,
    LORA_RESET_PIN, LORA_IRQ_PIN, LORA_FREQUENCY
)
from machine import SPI, Pin
import time

class LoRaCommunication:
    def __init__(self):
        """Initialize LoRA module (using upylora library)"""
        try:
            import lora
            
            # SPI configuration
            spi = SPI(
                1,
                baudrate=10000000,
                polarity=0,
                phase=0,
                bits=8,
                firstbit=SPI.MSB,
                sck=Pin(LORA_CLK_PIN),
                mosi=Pin(LORA_MOSI_PIN),
                miso=Pin(LORA_MISO_PIN)
            )
            
            # LoRA initialization
            self.lora = lora.LoRa(
                spi,
                cs=Pin(LORA_CS_PIN),
                reset=Pin(LORA_RESET_PIN),
                irq=Pin(LORA_IRQ_PIN),
                freq=LORA_FREQUENCY,
                tx_power_level=17,
                comm_timeout=5000
            )
            
            self.initialized = True
        except ImportError:
            print("Warning: upylora library not found")
            self.initialized = False
    
    def send(self, data):
        """
        Send data via LoRA
        
        Args:
            data: Bytes to send
        """
        if self.initialized:
            try:
                self.lora.send_data(data, True, 10)  # Blocking send with timeout
                return True
            except Exception as e:
                print(f"LoRA send error: {e}")
                return False
        return False
    
    def receive(self):
        """
        Check for incoming LoRA data
        
        Returns:
            Received bytes or None if no data
        """
        if self.initialized:
            try:
                if self.lora.received_packet():
                    return self.lora.read_payload()
            except Exception as e:
                print(f"LoRA receive error: {e}")
        return None

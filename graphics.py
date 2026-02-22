# Graphics Rendering Engine

from config import DISPLAY_WIDTH, DISPLAY_HEIGHT, ANIMATION_FRAME_MS
from sprites.sprite_manager import SpriteManager
from sprites.sprite_data import SPRITE_DATA
import time

class GraphicsEngine:
    def __init__(self, display):
        """
        Initialize graphics engine
        
        Args:
            display: SSD1306 display object
        """
        self.display = display
        self.sprite_manager = SpriteManager()
        self.last_frame_time = time.time()
        self.should_update_frame = False
    
    def update(self, pet_state, health_system=None):
        """
        Update and render the display
        
        Args:
            pet_state: PetState object
            health_system: HealthSystem object (optional)
        """
        current_time = time.time()
        elapsed_ms = (current_time - self.last_frame_time) * 1000
        
        # Update health system if provided
        if health_system:
            health_system.update()
        
        # Check if it's time to update animation frame
        if elapsed_ms >= ANIMATION_FRAME_MS:
            pet_state.update_animation()
            self.last_frame_time = current_time
        
        # Only redraw if state changed
        if pet_state.is_dirty:
            self.draw_frame(pet_state, health_system)
    
    def draw_frame(self, pet_state, health_system=None):
        """Draw current pet state with health bars"""
        self.display.fill(0)  # Clear display
        
        state_name = pet_state.get_state_name()
        frame_idx = pet_state.animation_frame
        
        # Get sprite for current state and frame
        sprite_bitmap = self.sprite_manager.get_sprite(state_name, frame_idx)
        
        if sprite_bitmap:
            # Draw sprite centered on display
            sprite_width = sprite_bitmap.get('width', 32)
            sprite_height = sprite_bitmap.get('height', 32)
            x = (DISPLAY_WIDTH - sprite_width) // 2
            y = (DISPLAY_HEIGHT - sprite_height) // 2
            
            self._draw_bitmap(sprite_bitmap, x, y)
        
        # Draw health bars on sides if health_system provided
        if health_system:
            self._draw_health_bars(health_system)
        
        # Draw status text at bottom
        self.display.text(state_name.upper(), 0, 56, 1)
        
        self.display.show()
        pet_state.reset_dirty_flag()
    
    def _draw_health_bars(self, health_system):
        """
        Draw two health bars on left and right sides with indicator sprites
        Left: Wireless health (LoRA sync)
        Right: Contact health (physical contact)
        """
        bar_width = 4
        bar_height = 32
        bar_y = (DISPLAY_HEIGHT - bar_height) // 2
        
        # Left side - Wireless health with signal icon
        left_x = 1
        
        # Draw wireless indicator sprite (simple signal bars pattern)
        # 8x8 pixel antenna/signal icon
        self._draw_signal_icon(left_x - 8, bar_y)
        
        # Draw left health bar
        wireless_pixels = health_system.get_wireless_health_pixels(bar_height)
        if wireless_pixels > 0:
            # Draw filled portion
            for px in range(wireless_pixels):
                for py in range(bar_width):
                    self.display.pixel(left_x + py, bar_y + (bar_height - px - 1), 1)
        
        # Right side - Contact health with touch icon
        right_x = DISPLAY_WIDTH - bar_width - 1
        
        # Draw contact indicator sprite (simple hand/touch pattern)
        self._draw_contact_icon(right_x + bar_width + 1, bar_y)
        
        # Draw right health bar
        contact_pixels = health_system.get_contact_health_pixels(bar_height)
        if contact_pixels > 0:
            # Draw filled portion
            for px in range(contact_pixels):
                for py in range(bar_width):
                    self.display.pixel(right_x + py, bar_y + (bar_height - px - 1), 1)
    
    def _draw_signal_icon(self, x, y):
        """Draw wireless/signal indicator icon (8x8) from sprite data"""
        if "signal_icon" in SPRITE_DATA and SPRITE_DATA["signal_icon"]:
            icon_data = SPRITE_DATA["signal_icon"][0]
            pattern = icon_data.get('pattern', [])
            for row in range(8):
                for col in range(8):
                    if pattern and row < len(pattern) and col < len(pattern[row]):
                        if pattern[row][col]:
                            px = x + col
                            py = y + row
                            if 0 <= px < DISPLAY_WIDTH and 0 <= py < DISPLAY_HEIGHT:
                                self.display.pixel(px, py, 1)
    
    def _draw_contact_icon(self, x, y):
        """Draw contact/touch indicator icon (8x8) from sprite data"""
        if "contact_icon" in SPRITE_DATA and SPRITE_DATA["contact_icon"]:
            icon_data = SPRITE_DATA["contact_icon"][0]
            pattern = icon_data.get('pattern', [])
            for row in range(8):
                for col in range(8):
                    if pattern and row < len(pattern) and col < len(pattern[row]):
                        if pattern[row][col]:
                            px = x + col
                            py = y + row
                            if 0 <= px < DISPLAY_WIDTH and 0 <= py < DISPLAY_HEIGHT:
                                self.display.pixel(px, py, 1)
    
    def _draw_bitmap(self, bitmap_data, x, y):
        """
        Draw bitmap to display
        
        Args:
            bitmap_data: Dictionary with 'width', 'height', and 'data' keys
            x, y: Position on display
        """
        width = bitmap_data.get('width', 0)
        height = bitmap_data.get('height', 0)
        data = bitmap_data.get('data', [])
        
        if not data:
            return
        
        # Draw pixel by pixel (bitmap format: list of bytes, 8 pixels per byte)
        for byte_idx, byte_val in enumerate(data):
            row = byte_idx // ((width + 7) // 8)
            col = (byte_idx % ((width + 7) // 8)) * 8
            
            for bit in range(8):
                if col + bit < width and row < height:
                    if byte_val & (1 << bit):
                        px = x + col + bit
                        py = y + row
                        if 0 <= px < DISPLAY_WIDTH and 0 <= py < DISPLAY_HEIGHT:
                            self.display.pixel(px, py, 1)

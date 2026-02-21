# Graphics Rendering Engine

from config import DISPLAY_WIDTH, DISPLAY_HEIGHT, ANIMATION_FRAME_MS
from sprites.sprite_manager import SpriteManager
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
        
    def update(self, pet_state):
        """
        Update and render the display
        
        Args:
            pet_state: PetState object
        """
        current_time = time.time()
        elapsed_ms = (current_time - self.last_frame_time) * 1000
        
        # Check if it's time to update animation frame
        if elapsed_ms >= ANIMATION_FRAME_MS:
            pet_state.update_animation()
            self.last_frame_time = current_time
        
        # Only redraw if state changed
        if pet_state.is_dirty:
            self.draw_frame(pet_state)
    
    def draw_frame(self, pet_state):
        """Draw current pet state"""
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
        
        # Draw status text at bottom
        self.display.text(state_name.upper(), 0, 56, 1)
        
        self.display.show()
        pet_state.reset_dirty_flag()
    
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

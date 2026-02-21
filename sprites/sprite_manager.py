# Sprite Management and Animation

from sprites.sprite_data import SPRITE_DATA

class SpriteManager:
    def __init__(self):
        """Initialize sprite manager"""
        self.sprites = SPRITE_DATA
    
    def get_sprite(self, state_name, frame_idx=0):
        """
        Get sprite bitmap for given state and frame
        
        Args:
            state_name: State name (e.g., "happy", "hungry")
            frame_idx: Animation frame index (0-3)
        
        Returns:
            Dictionary with 'width', 'height', and 'data' keys
        """
        if state_name not in self.sprites:
            return self._get_placeholder_sprite()
        
        state_sprites = self.sprites[state_name]
        if isinstance(state_sprites, list):
            frame_idx = frame_idx % len(state_sprites)
            return state_sprites[frame_idx]
        return state_sprites
    
    def _get_placeholder_sprite(self):
        """Return a simple placeholder sprite"""
        return {
            'width': 32,
            'height': 32,
            'data': [0xFF] * 128  # 32x32 bitmap = 128 bytes
        }
    
    def add_custom_sprite(self, state_name, frames):
        """
        Add or update custom sprite
        
        Args:
            state_name: State name
            frames: List of frame dictionaries or single frame dict
        """
        if isinstance(frames, list):
            self.sprites[state_name] = frames
        else:
            self.sprites[state_name] = [frames]

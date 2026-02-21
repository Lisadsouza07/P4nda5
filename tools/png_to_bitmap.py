# PNG to Bitmap Converter Utility
# Converts pixel art PNG sprites to MicroPython bitmap format
# Usage: python png_to_bitmap.py input.png output_name [width] [height]

import sys
from PIL import Image

def png_to_bitmap(input_path, output_name, width=32, height=32):
    """
    Convert PNG image to bitmap data suitable for MicroPython
    
    Args:
        input_path: Path to input PNG file
        output_name: Name for the sprite (used in Python code)
        width: Sprite width in pixels
        height: Sprite height in pixels
    
    Returns:
        Dictionary with sprite data
    """
    try:
        img = Image.open(input_path).convert('1')  # Convert to 1-bit (black/white)
        
        # Resize if dimensions don't match
        if img.size != (width, height):
            img = img.resize((width, height), Image.Resampling.LANCZOS)
        
        # Convert to bitmap bytes
        pixels = img.load()
        bitmap_data = []
        
        # Process row by row, bit by bit
        for y in range(height):
            for x in range(0, width, 8):
                byte_val = 0
                for bit in range(8):
                    if x + bit < width:
                        # Get pixel (255 = white = 1, 0 = black = 0)
                        pixel = pixels[x + bit, y]
                        if pixel > 127:  # White pixel
                            byte_val |= (1 << bit)
                bitmap_data.append(byte_val)
        
        # Generate Python code
        code = f"""
    "{output_name}": {{
        'width': {width},
        'height': {height},
        'data': [{', '.join(f'0x{b:02X}' for b in bitmap_data)}]
    }},
"""
        
        return bitmap_data, code
    
    except Exception as e:
        print(f"Error processing image: {e}")
        return None, None

def main():
    if len(sys.argv) < 3:
        print("Usage: python png_to_bitmap.py input.png output_name [width] [height]")
        print("Example: python png_to_bitmap.py happy_pet.png happy 32 32")
        sys.exit(1)
    
    input_path = sys.argv[1]
    output_name = sys.argv[2]
    width = int(sys.argv[3]) if len(sys.argv) > 3 else 32
    height = int(sys.argv[4]) if len(sys.argv) > 4 else 32
    
    bitmap_data, code = png_to_bitmap(input_path, output_name, width, height)
    
    if bitmap_data:
        print("Bitmap conversion successful!")
        print("\nAdd this to sprites/sprite_data.py:")
        print(code)
        print(f"\nBitmap data ({len(bitmap_data)} bytes)")
    else:
        print("Conversion failed")
        sys.exit(1)

if __name__ == "__main__":
    main()

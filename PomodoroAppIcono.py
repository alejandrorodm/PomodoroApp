from PIL import Image
import sys

def create_icon():
    try:
        img = Image.open('PomodoroAppIcono.png')
        img = img.convert("RGBA")
        
        # Crop to square from center
        width, height = img.size
        print(f"Original size: {width}x{height}")
        
        min_dim = min(width, height)
        left = (width - min_dim) / 2
        top = (height - min_dim) / 2
        right = (width + min_dim) / 2
        bottom = (height + min_dim) / 2
        
        img_cropped = img.crop((left, top, right, bottom))
        
        # Resize smoothly
        img_resized = img_cropped.resize((256, 256), Image.Resampling.LANCZOS)
        
        # Save as ICO
        img_resized.save('PomodoroAppIcono.ico', format='ICO', sizes=[(256, 256)])
        print("Icon created successfully at 256x256.")
    except Exception as e:
        print(f"Error creating icon: {e}")
        sys.exit(1)

if __name__ == '__main__':
    create_icon()

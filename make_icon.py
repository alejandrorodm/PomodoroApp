from PIL import Image, ImageDraw
import sys

def create_transparent_icon():
    try:
        # Load the image
        img = Image.open('PomodoroAppIcono.png')
        img = img.convert("RGBA")
        
        # 1. Use flood fill from the outer corners to only remove the CONTINUOUS background
        replacement_color = (255, 255, 255, 0)
        width = img.width
        height = img.height
        
        corners = [(0, 0), (width - 1, 0), (0, height - 1), (width - 1, height - 1)]
        for corner in corners:
            pixel = img.getpixel(corner)
            if pixel[0] > 230 and pixel[1] > 230 and pixel[2] > 230:
                ImageDraw.floodfill(img, corner, replacement_color, thresh=40)
        
        # 2. Crop to the bounding box of the icon to remove all empty transparent space
        bbox = img.getbbox()
        if bbox:
            img = img.crop(bbox)
            
        # 3. Create a perfect 256x256 canvas and center the icon, resizing it to fill the box
        final_size = 256
        ratio = min(final_size / img.width, final_size / img.height)
        new_w = int(img.width * ratio)
        new_h = int(img.height * ratio)
        
        img_resized = img.resize((new_w, new_h), Image.Resampling.LANCZOS)
        
        final_img = Image.new("RGBA", (final_size, final_size), (255, 255, 255, 0))
        offset_x = (final_size - new_w) // 2
        offset_y = (final_size - new_h) // 2
        
        final_img.paste(img_resized, (offset_x, offset_y))
        
        # Save as ICO
        final_img.save('PomodoroAppIcono.ico', format='ICO', sizes=[(256, 256)])
        print("Icon processed: Background removed, cropped and resized successfully.")
        
    except Exception as e:
        print(f"Error processing icon: {e}")
        sys.exit(1)

if __name__ == '__main__':
    create_transparent_icon()

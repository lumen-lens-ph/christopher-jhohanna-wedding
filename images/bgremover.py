from PIL import Image
import os
import glob

def remove_white_background_advanced(input_path, output_path, threshold=240, feather_edges=False):
    """
    Advanced white background removal with optional edge feathering
    """
    try:
        img = Image.open(input_path)
        
        if img.mode != 'RGBA':
            img = img.convert('RGBA')
        
        datas = img.getdata()
        new_data = []
        
        for item in datas:
            r, g, b = item[0], item[1], item[2]
            
            # Check if pixel is white/near white
            if r > threshold and g > threshold and b > threshold:
                # Fully transparent for white pixels
                new_data.append((255, 255, 255, 0))
            elif feather_edges and (r > threshold-20 or g > threshold-20 or b > threshold-20):
                # Semi-transparent for edge pixels (feathering)
                alpha = int(255 * (1 - (max(r, g, b) / 255)))
                new_data.append((r, g, b, alpha))
            else:
                # Keep original pixel
                new_data.append(item)
        
        img.putdata(new_data)
        img.save(output_path, 'PNG')
        return True
        
    except Exception as e:
        print(f"Error: {e}")
        return False

def interactive_remover():
    print("=== Advanced PNG Background Remover ===\n")
    
    # Get threshold
    try:
        threshold = int(input("White threshold (200-250, default 240): ") or "240")
        threshold = max(200, min(250, threshold))
    except:
        threshold = 240
        print("Using default threshold: 240")
    
    # Ask about edge feathering
    feather = input("Enable edge feathering for smoother edges? (y/n, default n): ").lower().strip() == 'y'
    
    # Process files
    png_files = glob.glob('*.png')
    
    if not png_files:
        print("No PNG files found in current directory!")
        return
    
    output_dir = "no_bg"
    os.makedirs(output_dir, exist_ok=True)
    
    print(f"\nProcessing {len(png_files)} images...")
    
    success_count = 0
    for png_file in png_files:
        output_path = os.path.join(output_dir, os.path.basename(png_file))
        if remove_white_background_advanced(png_file, output_path, threshold, feather):
            print(f"✓ {os.path.basename(png_file)}")
            success_count += 1
        else:
            print(f"✗ {os.path.basename(png_file)}")
    
    print(f"\n✅ Successfully processed {success_count}/{len(png_files)} images!")
    print(f"📁 Output folder: {output_dir}")

if __name__ == "__main__":
    interactive_remover()
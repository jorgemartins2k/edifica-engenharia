from PIL import Image, ImageDraw

def make_transparent(input_path, output_path, tolerance=50):
    img = Image.open(input_path).convert('RGBA')
    data = img.getdata()
    
    # Usually top-left pixel is the background color
    bg_color = data[0][:3]
    
    new_data = []
    for item in data:
        # Calculate Euclidean distance between the current pixel and the background color
        dist = sum((a - b) ** 2 for a, b in zip(item[:3], bg_color)) ** 0.5
        
        if dist < tolerance:
            # Instead of a hard border, maybe do partial transparency to make edges smooth?
            # For simplicity, if it's within tolerance, we make it fully transparent.
            new_data.append((item[0], item[1], item[2], 0))
        else:
            # Keep original pixel
            new_data.append(item)
            
    img.putdata(new_data)
    
    # Remove the small star in the bottom right corner (approx 70x70 px)
    draw = ImageDraw.Draw(img)
    w, h = img.size
    draw.rectangle([(w-90, h-90), (w, h)], fill=(0, 0, 0, 0))
    
    img.save(output_path, "PNG")
    print(f"Saved transparent logo to {output_path}")

if __name__ == "__main__":
    make_transparent("assets/project-photos/logo/logo.png", "assets/project-photos/logo/logo_clean.png")

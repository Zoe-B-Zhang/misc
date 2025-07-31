from PIL import Image, ImageDraw, ImageFont
import os

# === Resize Image for Web ===
def resize_image(input_path, output_path, max_width=1600, quality=75):
    with Image.open(input_path) as img:
        # Resize if needed
        if img.width > max_width:
            ratio = max_width / float(img.width)
            new_height = int(float(img.height) * ratio)
            img = img.resize((max_width, new_height), Image.Resampling.LANCZOS)
            
        # Convert to RGB (if not already), then save
        img = img.convert('RGB') 
        # Save as JPEG
        img.save(output_path, "JPEG", quality=quality, optimize=True)
        # Optional: Save as WebP instead
        # img.save(output_path, "WEBP", quality=quality, method=6)
        print(f"✅ Resized: {output_path}")


# === Resize all imgs of a given directory to a output directory ===
def resize_images_in_directory(input_dir, output_dir, max_width=1600, quality=75):
    os.makedirs(output_dir, exist_ok=True)
    for filename in os.listdir(input_dir):
        if filename.lower().endswith(('.png', '.jpg', '.jpeg', '.tiff', '.bmp', '.gif')):
            input_path = os.path.join(input_dir, filename)
            output_path = os.path.join(output_dir, os.path.splitext(filename)[0] + ".jpg")
            resize_image(input_path, output_path, max_width, quality)

# === cal fond size based on the picture size ===
def calculate_font_size(image_width, divisor=20, min_size=16, max_size=150):
    """
    Dynamically calculate font size based on image width.
    
    :param image_width: width of the image in pixels
    :param divisor: larger value = smaller font
    :param min_size: enforce a minimum size for small images
    :param max_size: cap font size for very large images
    :return: integer font size
    """
    size = image_width // divisor
    return max(min(size, max_size), min_size)
    
# === Add text watermark to a single image ===
def add_watermark_text(
    input_path,
    output_path,
    text,
    font_path = "arial.ttf",
    opacity=120,
    margin=20,
    fill_color=(255, 0, 0)
):
    try:
        with Image.open(input_path).convert("RGBA") as im:
            dynamic_font_size = calculate_font_size(im.width)
            print(f"Using font size: {dynamic_font_size} for image width: {im.width}")
            try:
                font = ImageFont.truetype(font_path, dynamic_font_size)
            except Exception:
                font = ImageFont.load_default()
                print("Using default font due to error loading custom font.")

            draw = ImageDraw.Draw(im)
            text_size = draw.textbbox((0, 0), text, font=font)
            text_position = (im.width - text_size[2] - 20, im.height - text_size[3] - 20)
            draw.text(text_position, text, font=font, fill=(255, 0, 0, opacity))
            # Save result
            im.convert("RGB").save(output_path, quality=95)
            print(f"✅ Text watermarked: {output_path}")

    except Exception as e:
        print(f"❌ Failed to watermark {input_path}: {e}")


# === Calculate logo scale based on image width ===
def calculate_logo_scale(image_width, desired_ratio=0.15, max_width=400):
    """
    Calculate logo width based on image width.
    Caps the logo to a max width if needed.
    """
    logo_width = int(image_width * desired_ratio)
    return min(logo_width, max_width)

# === Add logo watermark to a single image ===
def add_watermark_logo(input_path, output_path, logo_path, desired_ratio=0.15, margin=20):
    """
    Add a logo watermark in the bottom-right corner, scaled to image size.
    
    :param input_path: path to the original image
    :param output_path: where to save the watermarked image
    :param logo_path: path to logo image (PNG with alpha recommended)
    :param desired_ratio: logo width = image.width * ratio (e.g., 0.15 for 15%)
    :param margin: padding from image border
    """
    try:
        image = Image.open(input_path).convert("RGBA")
        logo = Image.open(logo_path).convert("RGBA")

        # Auto-scale logo width
        target_logo_width = min(int(image.width * desired_ratio), 400)
        target_logo_height = int(logo.height * target_logo_width / logo.width)
        logo_resized = logo.resize((target_logo_width, target_logo_height), Image.Resampling.LANCZOS)

        # Position in bottom right
        x = image.width - logo_resized.width - margin
        y = image.height - logo_resized.height - margin

        # Paste logo with alpha mask
        image.paste(logo_resized, (x, y), logo_resized)
        image.convert("RGB").save(output_path, quality=95)

        print(f"✅ Logo Watermarked: {output_path}")

    except Exception as e:
        print(f"❌ Failed to watermark with logo: {e}")

# === Apply watermark (text or logo) to all images in a directory ===
def add_watermark_to_directory(input_dir, output_dir, watermark_text=None, watermark_logo_path=None, opacity=200, margin=20):
    os.makedirs(output_dir, exist_ok=True)

    for filename in os.listdir(input_dir):
        if not filename.lower().endswith(('.jpg', '.jpeg', '.png')):
            continue

        input_path = os.path.join(input_dir, filename)
        output_path = os.path.join(output_dir, f"watermarked_{filename}")

        if watermark_text:
            add_watermark_text(input_path, output_path, watermark_text,"arial.ttf",opacity, margin)
        elif watermark_logo_path:
            add_watermark_logo(input_path, output_path, watermark_logo_path, margin=margin)
        else:
            print(f"❌ No watermark method specified for {filename}")

# === Resize logo image while maintaining aspect ratio ===
def resize_logo_image(im, max_width, max_height):
    """
    Resize image to fit within (max_width, max_height) while keeping aspect ratio.
    Modifies image in place.
    """
    im.thumbnail((max_width, max_height), Image.Resampling.LANCZOS)
    return im

# === Resize and watermark images in a directory ===
def resize_and_watermark_directory(
    input_dir,
    output_dir,
    max_width=1024,
    max_height=1024,
    watermark_text=None,
    watermark_logo_path=None,
    font_path="arial.ttf",
    base_font_size=36,
    opacity=180,
    margin=20,
    logo_ratio=0.15
):
    for filename in os.listdir(input_dir):
        if filename.lower().endswith(('.png', '.jpg', '.jpeg')):
            input_path = os.path.join(input_dir, filename)
            output_path = os.path.join(output_dir, filename)

            try:
                with Image.open(input_path).convert("RGBA") as im:
                    # Step 1: Resize
                    resized = resize_logo_image(im, max_width, max_height)

                    # Step 2: Apply watermark
                    if watermark_text:
                        font_size = calculate_font_size(resized.width, divisor=20)
                        draw = ImageDraw.Draw(resized)

                        try:
                            font = ImageFont.truetype(font_path, font_size)
                        except:
                            font = ImageFont.load_default()

                        bbox = draw.textbbox((0, 0), watermark_text, font=font)
                        x = resized.width - (bbox[2] - bbox[0]) - margin
                        y = resized.height - (bbox[3] - bbox[1]) - margin
                        draw.text((x, y), watermark_text, font=font, fill=(255, 0, 0, opacity))

                    elif watermark_logo_path:
                        with Image.open(watermark_logo_path).convert("RGBA") as logo:
                            target_logo_width = min(int(resized.width * logo_ratio), 400)
                            target_logo_height = int(logo.height * target_logo_width / logo.width)
                            logo_resized = logo.resize((target_logo_width, target_logo_height), Image.Resampling.LANCZOS)
                            x = resized.width - logo_resized.width - margin
                            y = resized.height - logo_resized.height - margin
                            resized.paste(logo_resized, (x, y), logo_resized)

                    # Step 3: Save final
                    resized.convert("RGB").save(output_path, quality=95)
                    print(f"✅ Resized + watermarked: {output_path}")

            except Exception as e:
                print(f"❌ Failed to process {filename}: {e}")

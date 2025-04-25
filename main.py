import os
import csv
from PIL import Image, ImageDraw, ImageFont
import sys
import re

def find_placeholder_position(template_path, placeholder="PLACEHOLDER_NAME"):
    """
    Scan the certificate template to find the position of a placeholder name.
    
    Parameters:
    - template_path: Path to the certificate template image
    - placeholder: The placeholder text to look for (default: "PLACEHOLDER_NAME")
    
    Returns:
    - (x, y, width, height) of the placeholder if found, None otherwise
    """
    try:
        with Image.open(template_path) as img:
            # Convert image to RGB if it's not already
            if img.mode != 'RGB':
                img = img.convert('RGB')
                
            width, height = img.size
            for y in range(height):
                for x in range(width):
                    # Check if current pixel is part of text (assuming black text)
                    # This is a simplistic approach and might need refinement
                    r, g, b = img.getpixel((x, y))
                    if r < 50 and g < 50 and b < 50:  # Dark pixel, potential text
                        # You would need a more sophisticated algorithm to detect text
                        # This is just a placeholder for the concept
                        print(f"Potential text found at position ({x}, {y})")
                        # For demonstration purposes, just return the first dark pixel
                        return (x, y, 100, 20)  # Dummy width and height
            
            print("No placeholder text found in the image.")
            return None
    except Exception as e:
        print(f"Error analyzing template: {e}")
        return None

def generate_certificates(
    template_path: str,
    participants_csv: str,
    output_dir: str,
    font_path: str,
    font_size: int,
    position: tuple = None,
    pdf_output: bool = True,
    has_header: bool = False,
    placeholder_name: str = "PLACEHOLDER_NAME"
):
    """
    Generate certificates by overlaying participant names on a template.

    Parameters:
    - template_path: Path to the certificate template.
    - participants_csv: CSV file containing participant names.
    - output_dir: Directory to save generated certificates.
    - font_path: Path to a .ttf font file.
    - font_size: Font size for the participant names.
    - position: (x, y) coordinates where the name should appear. If None, 
                the function will try to find the placeholder in the template.
    - pdf_output: If True, save certificates as PDF, else PNG.
    - has_header: If True, CSV file has a header row.
    - placeholder_name: The text to look for in the template to determine name position.
    """
    # Ensure output directory exists
    os.makedirs(output_dir, exist_ok=True)

    # Load font
    font = ImageFont.truetype(font_path, font_size)
    
    # If position is not provided, try to find the placeholder
    if position is None:
        placeholder_info = find_placeholder_position(template_path, placeholder_name)
        if placeholder_info:
            x, y, _, _ = placeholder_info
            position = (x, y)
        else:
            print("Warning: Placeholder not found. Using default position (800, 600).")
            position = (800, 600)

    # Read participants
    with open(participants_csv, newline='', encoding='utf-8') as csvfile:
        if has_header:
            reader = csv.DictReader(csvfile)
            participants = [row['name'] for row in reader]
        else:
            reader = csv.reader(csvfile)
            participants = [row[0] for row in reader]

        for name in participants:
            # Open template
            with Image.open(template_path) as im:
                draw = ImageDraw.Draw(im)
                
                # Calculate text dimensions for centering
                bbox = draw.textbbox((0, 0), name, font=font)
                text_width = bbox[2] - bbox[0]
                text_height = bbox[3] - bbox[1]
                
                # Get the center point from position
                x, y = position
                
                # Center the text at the position
                x_centered = x - text_width // 2
                y_centered = y - text_height // 2

                # Draw text (centered)
                draw.text((x_centered, y_centered), name, font=font, fill=(0, 0, 0))  # black text

                # Save output
                output_name = f"{name.replace(' ', '_')}.{'pdf' if pdf_output else 'png'}"
                output_path = os.path.join(output_dir, output_name)

                if pdf_output:
                    # Convert to RGB and save as PDF
                    rgb_im = im.convert('RGB')
                    rgb_im.save(output_path, "PDF", resolution=100.0)
                else:
                    im.save(output_path)

                print(f"Generated certificate for {name} -> {output_path}")

def prepare_template_with_placeholder(template_path, output_path, font_path, font_size=48, placeholder="PLACEHOLDER_NAME"):
    """
    Create a template with a placeholder name that can be used to determine text position.
    
    Parameters:
    - template_path: Original template path
    - output_path: Path to save the template with placeholder
    - font_path: Path to the font file
    - font_size: Font size for the placeholder
    - placeholder: Text to use as placeholder
    
    Returns:
    - Path to the template with placeholder
    """
    try:
        with Image.open(template_path) as im:
            draw = ImageDraw.Draw(im)
            font = ImageFont.truetype(font_path, font_size)
            
            # Default position (center of the image)
            width, height = im.size
            x = width // 2
            y = height // 2
            
            # Calculate text size for centering
            bbox = draw.textbbox((0, 0), placeholder, font=font)
            text_width = bbox[2] - bbox[0]
            text_height = bbox[3] - bbox[1]
            
            # Center the placeholder text
            x_centered = x - text_width // 2
            y_centered = y - text_height // 2
            
            # Draw the placeholder text
            draw.text((x_centered, y_centered), placeholder, font=font, fill=(0, 0, 0))
            
            # Save the template with placeholder
            im.save(output_path)
            print(f"Template with placeholder created at: {output_path}")
            return output_path
    except Exception as e:
        print(f"Error creating template with placeholder: {e}")
        return None

def get_position_from_user():
    """
    Prompt the user to click on the image to select a position.
    This is a placeholder function. In a real implementation, you would need
    a GUI framework to handle this interaction.
    """
    print("This is a placeholder for interactive position selection.")
    print("In a real implementation, you would see the template image")
    print("and be able to click on it to select the position.")
    
    # For demonstration purposes, just return a fixed position
    return (800, 600)

def main():
    if len(sys.argv) > 1 and sys.argv[1] == "--prepare-template":
        # Create a template with placeholder
        prepare_template_with_placeholder(
            template_path='certificate_template.jpg',
            output_path='certificate_template_with_placeholder.jpg',
            font_path='arial.ttf',
            font_size=48,
            placeholder="PLACEHOLDER_NAME"
        )
    else:
        # Regular certificate generation
        generate_certificates(
            template_path='certificate_template.jpg',
            participants_csv='participants.csv',
            output_dir='certificates',
            font_path='arial.ttf',
            font_size=48,
            position=None,  # Will try to find placeholder or use default
            pdf_output=True,
            has_header=False,
            placeholder_name="PLACEHOLDER_NAME"
        )

if __name__ == '__main__':
    main()

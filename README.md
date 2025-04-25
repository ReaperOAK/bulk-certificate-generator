# Certificate Bulk Producer

A user-friendly application for generating personalized certificates in bulk from a template with customizable name placement, font, and color options.

![Certificate Designer Application](https://i.imgur.com/Wkr1YIv.png) 

## Features

- **Visual Certificate Designer**: Interactive GUI to customize certificate appearance
- **Center-Aligned Names**: Automatically centers names at your chosen position
- **Customizable Text**: Change font, size, and color to match your certificate design
- **Bulk Generation**: Generate hundreds of certificates in seconds from a CSV file
- **PDF Output**: Produces professional PDF certificates ready for printing or digital distribution

## Requirements

- Python 3.6 or higher
- Required Python packages:
  - Pillow (PIL Fork)
  - tkinter (usually included with Python)

## Installation

1. Clone or download this repository
2. Install required dependencies:

```bash
pip install pillow
```

## Getting Started

### Using the GUI Certificate Designer

The Certificate Designer application provides a visual way to design and generate your certificates.

1. Run the designer application:

```bash
python certificate_designer.py
```

2. Use the interface to:
   - Load your certificate template image (JPG or PNG)
   - Click on the certificate to position the name
   - Customize the font, size, and color
   - Select your participants CSV file 
   - Generate certificates

### Using the Command Line Tool

For advanced users or batch processing, you can also use the command-line interface:

```bash
python main.py
```

## Certificate Template

- Use any JPG or PNG image as your certificate template
- Recommended resolution: At least 1500×1060 pixels for high-quality prints
- Leave sufficient space for participant names

## CSV File Format

The participants CSV file should contain a list of names, one per line:

```
John Doe
Jane Smith
Robert Johnson
```

## Customization Options

- **Font**: Select any TrueType (.ttf) font file
- **Font Size**: Adjust the size to fit your certificate design
- **Color**: Choose any color for the text
- **Positioning**: Visually place the name anywhere on the certificate

## Output

- Certificates are saved as PDF files in the specified output directory
- Each certificate is named after the participant (spaces replaced with underscores)
- Example: `John_Doe.pdf`

## Advanced Usage

### Command Line Options

The main.py script accepts the following parameters:

```python
generate_certificates(
    template_path='certificate_template.jpg',  # Path to template image
    participants_csv='participants.csv',       # Path to CSV file
    output_dir='certificates',                 # Output directory
    font_path='arial.ttf',                     # Path to TTF font
    font_size=48,                              # Font size
    position=(800, 600),                       # Position (x,y) for name placement
    pdf_output=True,                           # True for PDF, False for PNG
    has_header=False                           # True if CSV has header row
)
```

## Troubleshooting

- **"Font not found" error**: Ensure the font file exists and is a valid TTF font
- **Certificate text not visible**: Try increasing font size or changing font color
- **Incorrect name placement**: Use the visual designer to adjust positioning

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgments

- Uses the Pillow library for image processing
- Tkinter for the GUI interface

---

Created with ❤️ by [Your Name]
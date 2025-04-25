import os
import sys
import csv
import tkinter as tk
from tkinter import filedialog, messagebox, colorchooser
from PIL import Image, ImageTk, ImageDraw, ImageFont

class CertificateDesigner:
    def __init__(self, root):
        self.root = root
        self.root.title("Certificate Designer")
        self.root.geometry("1200x800")
        
        # Variables
        self.template_path = None
        self.placeholder_text = "PLACEHOLDER_NAME"
        self.placeholder_position = None
        self.font_path = "arial.ttf"
        self.font_size = 48
        self.font_color = (0, 0, 0)  # Default: black
        self.color_hex = "#000000"   # Hex representation for the button
        self.participants_csv = "participants.csv"
        self.output_dir = "certificates"
        
        # Create the UI
        self.create_ui()
        
    def create_ui(self):
        # Main frame
        main_frame = tk.Frame(self.root)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Left panel (controls)
        left_panel = tk.Frame(main_frame, width=300, bg="#f0f0f0", padx=10, pady=10)
        left_panel.pack(side=tk.LEFT, fill=tk.Y)
        left_panel.pack_propagate(False)
        
        # Right panel (certificate preview)
        self.right_panel = tk.Frame(main_frame, bg="#ffffff")
        self.right_panel.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)
        
        # Canvas for certificate preview
        self.canvas = tk.Canvas(self.right_panel, bg="white")
        self.canvas.pack(fill=tk.BOTH, expand=True)
        self.canvas.bind("<Button-1>", self.on_canvas_click)
        
        # Controls in left panel
        tk.Label(left_panel, text="Certificate Designer", font=("Arial", 16, "bold"), bg="#f0f0f0").pack(pady=10)
        
        # Button to load template
        tk.Button(left_panel, text="Load Certificate Template", command=self.load_template).pack(fill=tk.X, pady=5)
        
        # Placeholder text entry
        tk.Label(left_panel, text="Placeholder Text:", bg="#f0f0f0").pack(anchor=tk.W)
        self.placeholder_entry = tk.Entry(left_panel)
        self.placeholder_entry.insert(0, self.placeholder_text)
        self.placeholder_entry.pack(fill=tk.X, pady=5)
        
        # Font size
        tk.Label(left_panel, text="Font Size:", bg="#f0f0f0").pack(anchor=tk.W)
        self.font_size_entry = tk.Entry(left_panel)
        self.font_size_entry.insert(0, str(self.font_size))
        self.font_size_entry.pack(fill=tk.X, pady=5)
        
        # Font selection
        tk.Button(left_panel, text="Select Font", command=self.select_font).pack(fill=tk.X, pady=5)
        
        # Font color selection
        tk.Label(left_panel, text="Font Color:", bg="#f0f0f0").pack(anchor=tk.W)
        self.color_button_frame = tk.Frame(left_panel)
        self.color_button_frame.pack(fill=tk.X, pady=5)
        
        self.color_preview = tk.Frame(self.color_button_frame, bg=self.color_hex, width=30, height=20)
        self.color_preview.pack(side=tk.LEFT, padx=5)
        
        tk.Button(self.color_button_frame, text="Select Color", command=self.select_color).pack(side=tk.LEFT, expand=True, fill=tk.X)
        
        # CSV file
        tk.Label(left_panel, text="Participants CSV:", bg="#f0f0f0").pack(anchor=tk.W)
        self.csv_entry = tk.Entry(left_panel)
        self.csv_entry.insert(0, self.participants_csv)
        self.csv_entry.pack(fill=tk.X, pady=5)
        tk.Button(left_panel, text="Browse CSV", command=self.browse_csv).pack(fill=tk.X, pady=2)
        
        # Output directory
        tk.Label(left_panel, text="Output Directory:", bg="#f0f0f0").pack(anchor=tk.W)
        self.output_entry = tk.Entry(left_panel)
        self.output_entry.insert(0, self.output_dir)
        self.output_entry.pack(fill=tk.X, pady=5)
        tk.Button(left_panel, text="Browse Output Directory", command=self.browse_output_dir).pack(fill=tk.X, pady=2)
        
        # Save template with placeholder
        tk.Button(left_panel, text="Save Template with Placeholder", command=self.save_template_with_placeholder).pack(fill=tk.X, pady=10)
        
        # Generate certificates
        tk.Button(left_panel, text="Generate Certificates", command=self.generate_certificates, bg="#4CAF50", fg="white").pack(fill=tk.X, pady=10)
        
        # Status message
        self.status_var = tk.StringVar()
        self.status_var.set("Ready. Load a certificate template to begin.")
        tk.Label(left_panel, textvariable=self.status_var, bg="#f0f0f0", wraplength=280).pack(anchor=tk.W, pady=10)
        
        # Instructions
        instructions = "Instructions:\n1. Load a certificate template\n2. Click where you want to place the names\n3. Customize font, color, and size\n4. Generate certificates"
        tk.Label(left_panel, text=instructions, bg="#f0f0f0", justify=tk.LEFT, wraplength=280).pack(anchor=tk.W, pady=10)
    
    def select_color(self):
        """Open a color chooser dialog and update the font color"""
        color = colorchooser.askcolor(initialcolor=self.color_hex)
        if color[1]:  # color is ((r,g,b), hex)
            self.color_hex = color[1]
            self.font_color = color[0]  # RGB tuple
            # Update color preview
            self.color_preview.config(bg=self.color_hex)
            # Update display if placeholder is set
            if self.placeholder_position:
                self.update_display_with_placeholder()
            
    def load_template(self):
        filepath = filedialog.askopenfilename(
            filetypes=[("Image files", "*.jpg *.jpeg *.png")]
        )
        if filepath:
            self.template_path = filepath
            self.display_template()
            self.status_var.set(f"Template loaded: {os.path.basename(filepath)}")
            
    def display_template(self):
        if self.template_path:
            # Load and display the image
            try:
                self.pil_image = Image.open(self.template_path)
                # Resize to fit canvas if needed
                self.resize_image_to_fit()
                self.tk_image = ImageTk.PhotoImage(self.display_image)
                self.canvas.config(width=self.display_image.width, height=self.display_image.height)
                self.canvas_image = self.canvas.create_image(0, 0, anchor=tk.NW, image=self.tk_image)
                
                # Clear any previous placeholder
                self.placeholder_position = None
                self.status_var.set("Click on the image to place the name placeholder.")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to load image: {str(e)}")
                
    def resize_image_to_fit(self):
        # Get the canvas size
        canvas_width = self.right_panel.winfo_width() - 20
        canvas_height = self.right_panel.winfo_height() - 20
        
        # If image is too large, resize it proportionally
        img_width, img_height = self.pil_image.size
        if img_width > canvas_width or img_height > canvas_height:
            ratio = min(canvas_width / img_width, canvas_height / img_height)
            new_width = int(img_width * ratio)
            new_height = int(img_height * ratio)
            self.display_image = self.pil_image.resize((new_width, new_height), Image.LANCZOS)
            self.scale_factor = ratio
        else:
            self.display_image = self.pil_image.copy()
            self.scale_factor = 1.0
            
    def on_canvas_click(self, event):
        if not self.template_path:
            messagebox.showinfo("Info", "Please load a template first.")
            return
            
        # Get click position and scale to original image size
        x = int(event.x / self.scale_factor)
        y = int(event.y / self.scale_factor)
        
        # Save position
        self.placeholder_position = (x, y)
        
        # Update display with placeholder
        self.update_display_with_placeholder()
        
        # Update status
        self.status_var.set(f"Placeholder position set at ({x}, {y}). You can adjust by clicking elsewhere.")
    
    def update_display_with_placeholder(self):
        if not self.template_path or not self.placeholder_position:
            return
            
        # Create a copy of the original image
        img_copy = self.pil_image.copy()
        draw = ImageDraw.Draw(img_copy)
        
        # Get placeholder text
        placeholder = self.placeholder_entry.get()
        if not placeholder:
            placeholder = "PLACEHOLDER_NAME"
            
        # Get font size
        try:
            font_size = int(self.font_size_entry.get())
        except ValueError:
            font_size = 48
            
        # Load font
        try:
            font = ImageFont.truetype(self.font_path, font_size)
        except:
            font = ImageFont.load_default()
            
        # Calculate text dimensions for centering
        bbox = draw.textbbox((0, 0), placeholder, font=font)
        text_width = bbox[2] - bbox[0]
        text_height = bbox[3] - bbox[1]
        
        # Center the text at the clicked position
        x, y = self.placeholder_position
        x_centered = x - text_width // 2
        y_centered = y - text_height // 2
        
        # Draw placeholder text with selected color
        draw.text((x_centered, y_centered), placeholder, font=font, fill=self.font_color)
        
        # Resize for display
        if self.scale_factor != 1.0:
            display_img = img_copy.resize(self.display_image.size, Image.LANCZOS)
        else:
            display_img = img_copy
            
        # Update display
        self.tk_image = ImageTk.PhotoImage(display_img)
        self.canvas.itemconfig(self.canvas_image, image=self.tk_image)
        
    def select_font(self):
        filepath = filedialog.askopenfilename(
            filetypes=[("TrueType Font", "*.ttf"), ("All files", "*.*")]
        )
        if filepath:
            self.font_path = filepath
            self.status_var.set(f"Font selected: {os.path.basename(filepath)}")
            # Update display if placeholder is set
            if self.placeholder_position:
                self.update_display_with_placeholder()
                
    def browse_csv(self):
        filepath = filedialog.askopenfilename(
            filetypes=[("CSV files", "*.csv"), ("All files", "*.*")]
        )
        if filepath:
            self.participants_csv = filepath
            self.csv_entry.delete(0, tk.END)
            self.csv_entry.insert(0, filepath)
            
    def browse_output_dir(self):
        dirpath = filedialog.askdirectory()
        if dirpath:
            self.output_dir = dirpath
            self.output_entry.delete(0, tk.END)
            self.output_entry.insert(0, dirpath)
            
    def save_template_with_placeholder(self):
        if not self.template_path:
            messagebox.showerror("Error", "Please load a template first.")
            return
            
        if not self.placeholder_position:
            messagebox.showerror("Error", "Please click on the image to set placeholder position.")
            return
            
        # Get save path
        save_path = filedialog.asksaveasfilename(
            defaultextension=".jpg",
            filetypes=[("JPEG files", "*.jpg"), ("PNG files", "*.png"), ("All files", "*.*")],
            initialfile="certificate_template_with_placeholder.jpg"
        )
        
        if not save_path:
            return
            
        # Create a copy of the original image with placeholder
        img_copy = self.pil_image.copy()
        draw = ImageDraw.Draw(img_copy)
        
        # Get placeholder text
        placeholder = self.placeholder_entry.get()
        if not placeholder:
            placeholder = "PLACEHOLDER_NAME"
            
        # Get font size
        try:
            font_size = int(self.font_size_entry.get())
        except ValueError:
            font_size = 48
            
        # Load font
        try:
            font = ImageFont.truetype(self.font_path, font_size)
        except:
            font = ImageFont.load_default()
            
        # Calculate text dimensions for centering
        bbox = draw.textbbox((0, 0), placeholder, font=font)
        text_width = bbox[2] - bbox[0]
        text_height = bbox[3] - bbox[1]
        
        # Center the text at the clicked position
        x, y = self.placeholder_position
        x_centered = x - text_width // 2
        y_centered = y - text_height // 2
        
        # Draw placeholder text with selected color
        draw.text((x_centered, y_centered), placeholder, font=font, fill=self.font_color)
        
        # Save the image
        img_copy.save(save_path)
        self.status_var.set(f"Template with placeholder saved to: {save_path}")
        
    def generate_certificates(self):
        if not self.template_path:
            messagebox.showerror("Error", "Please load a template first.")
            return
            
        if not self.placeholder_position:
            messagebox.showerror("Error", "Please click on the image to set placeholder position.")
            return
            
        # Get values from UI
        csv_path = self.csv_entry.get()
        output_dir = self.output_entry.get()
        font_path = self.font_path
        
        try:
            font_size = int(self.font_size_entry.get())
        except ValueError:
            font_size = 48
            
        # Ensure output directory exists
        os.makedirs(output_dir, exist_ok=True)
        
        try:
            # Read participants
            with open(csv_path, newline='', encoding='utf-8') as csvfile:
                reader = csv.reader(csvfile)
                participants = [row[0] for row in reader]
                
            # Set progress maximum
            total = len(participants)
            processed = 0
            
            # Load font
            font = ImageFont.truetype(font_path, font_size)
            
            # Get placeholder position
            x, y = self.placeholder_position
                
            for name in participants:
                # Open template
                with Image.open(self.template_path) as im:
                    draw = ImageDraw.Draw(im)
                    
                    # Calculate text dimensions for centering
                    bbox = draw.textbbox((0, 0), name, font=font)
                    text_width = bbox[2] - bbox[0]
                    text_height = bbox[3] - bbox[1]
                    
                    # Center the text at the position
                    x_centered = x - text_width // 2
                    y_centered = y - text_height // 2
                    
                    # Draw text (centered) with selected color
                    draw.text((x_centered, y_centered), name, font=font, fill=self.font_color)
                    
                    # Save output
                    output_name = f"{name.replace(' ', '_')}.pdf"
                    output_path = os.path.join(output_dir, output_name)
                    
                    # Convert to RGB and save as PDF
                    rgb_im = im.convert('RGB')
                    rgb_im.save(output_path, "PDF", resolution=100.0)
                    
                    processed += 1
                    self.status_var.set(f"Generated {processed}/{total} certificates... {name}")
                    self.root.update()
                    
            self.status_var.set(f"Successfully generated {processed} certificates in {output_dir}")
            messagebox.showinfo("Success", f"Successfully generated {processed} certificates.")
            
        except Exception as e:
            messagebox.showerror("Error", f"Error generating certificates: {str(e)}")
            
if __name__ == "__main__":
    root = tk.Tk()
    app = CertificateDesigner(root)
    root.mainloop()
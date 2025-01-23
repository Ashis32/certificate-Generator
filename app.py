from flask import Flask, request, send_file, render_template, redirect, url_for
from PIL import Image, ImageDraw, ImageFont
import io

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')  # Your HTML form

@app.route('/generate', methods=['POST'])
def generate_certificate():
    name = request.form['name']
    
    # Load your certificate template (replace with your template file path)
    template = Image.open(r'certificate.png')  # Use raw string or forward slashes
    draw = ImageDraw.Draw(template)
    
    # Define font and size
    font_size = 380  # Adjust this size as needed
    font_path = 'PlaywriteCU-VariableFont_wght.ttf'  # Path to your stylish font file
    font = ImageFont.truetype(font_path, font_size)  # Use the stylish font file
    
    # Get the dimensions of the certificate and text
    template_width, template_height = template.size
    text_bbox = draw.textbbox((0, 0), name, font=font)  # Use textbbox to get text dimensions
    text_width = text_bbox[2] - text_bbox[0]
    text_height = text_bbox[3] - text_bbox[1]
    
    # Calculate position to center the text
    text_x = (template_width - text_width) / 2
    text_y = (template_height - text_height) / 2
    
    # Add the text to the certificate
    draw.text((text_x, text_y), name, font=font, fill='black')
    
    # Save the generated certificate to an in-memory file
    img_byte_arr = io.BytesIO()
    template.save(img_byte_arr, format='PNG')
    img_byte_arr.seek(0)
    
    # Send the file as a downloadable response
    return send_file(
        img_byte_arr,
        mimetype='image/png',
        as_attachment=True,
        download_name='certificate.png'
    )

if __name__ == '__main__':
    app.run(debug=True, port=5001)  # You can use the port you prefer

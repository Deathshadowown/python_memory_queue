from pyzbar.pyzbar import decode
from PIL import Image

# Function to decode barcode
def decode_barcode(image_path):
    # Open image
    img = Image.open(image_path)
    
    # Decode the barcode
    decoded_objects = decode(img)
    
    # Check if any barcode was found
    if decoded_objects:
        # Iterate through the decoded objects and print the data
        for obj in decoded_objects:
            # Print the barcode data (e.g., ID number)
            print("Decoded barcode data:", obj.data.decode('utf-8'))
    else:
        print("No barcode found in image.")

# Test the function with your image
image_path = 'image_path/green_id/id1.jpg'  # Replace with your image file path
decode_barcode(image_path)

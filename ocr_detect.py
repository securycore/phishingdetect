

try:
    import Image
except ImportError:
    from PIL import Image
import pytesseract

pytesseract.pytesseract.tesseract_cmd = '/usr/local/bin/tesseract'
# Include the above line, if you don't have tesseract executable in your PATH
# Example tesseract_cmd: 'C:\\Program Files (x86)\\Tesseract-OCR\\tesseract'


test = 'sewauk.org.png'
print(pytesseract.image_to_string(Image.open(test),lang='eng'))

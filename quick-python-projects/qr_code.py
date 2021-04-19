import qrcode
from pyzbar.pyzbar import decode
from PIL import Image

data = 'https://www.twitch.tv/mymisterfruit'

# Customize QR code
qr = qrcode.QRCode(
    version=1,
    error_correction=qrcode.ERROR_CORRECT_M,
    box_size=10,
    border=1,
)
qr.add_data(data)
qr.make(fit=True)

# Decoding returns an empty list if back_color is black
img = qr.make_image(fill_color='grey', back_color='#fff')

img.save('C:/Users/Martin/Downloads/qrcode.png')

# Decode QR code
img = Image.open('C:/Users/Martin/Downloads/qrcode.png')

result = decode(img)
print(result)
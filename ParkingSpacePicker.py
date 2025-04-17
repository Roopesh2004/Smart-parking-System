import cv2
import pickle
import qrcode
from PIL import Image
import numpy as np

# Constants
width, height = 107, 48
total_slots = 20  # Set the total number of parking slots

# Load saved positions
try:
    with open('CarParkPos', 'rb') as f:
        posList = pickle.load(f)
except:
    posList = []

# Mouse click callback function
def mouseClick(events, x, y, flags, params):
    if events == cv2.EVENT_LBUTTONDOWN:
        posList.append((x, y))
    if events == cv2.EVENT_RBUTTONDOWN:
        for i, pos in enumerate(posList):
            x1, y1 = pos
            if x1 < x < x1 + width and y1 < y < y1 + height:
                posList.pop(i)
                break  # Stop after deleting one to avoid index issues

    with open('CarParkPos', 'wb') as f:
        pickle.dump(posList, f)

# Generate QR code with status text
def generate_qr_code(text):
    qr = qrcode.QRCode(
        version=1,
        box_size=10,
        border=2
    )
    qr.add_data(text)
    qr.make(fit=True)
    img_qr = qr.make_image(fill_color="black", back_color="white")
    return img_qr

while True:
    # Load parking lot image
    img = cv2.imread("carParkImg.png")

    # Draw rectangles for each marked slot
    for pos in posList:
        cv2.rectangle(img, pos, (pos[0]+width, pos[1]+height), (255, 0, 255), 2)

    # Generate QR code with slot info
    available_slots = total_slots - len(posList)
    status_text = f"Available Parking Slots: {available_slots}/{total_slots}"
    qr_img = generate_qr_code(status_text)

    # Convert QR code image to RGB and then to OpenCV format
    qr_img = qr_img.convert('RGB')
    qr_img_cv = np.array(qr_img)
    qr_img_cv = cv2.cvtColor(qr_img_cv, cv2.COLOR_RGB2BGR)

    # Resize QR code
    qr_img_cv = cv2.resize(qr_img_cv, (200, 200))

    # Display windows
    cv2.imshow("Parking Image", img)
    cv2.imshow("QR Code", qr_img_cv)

    # Set mouse callback
    cv2.setMouseCallback("Parking Image", mouseClick)

    # Exit on 'q' key
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cv2.destroyAllWindows()

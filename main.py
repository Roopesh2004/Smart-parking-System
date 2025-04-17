from flask import Flask, render_template, Response, send_file
import cv2
import pickle
import cvzone
import numpy as np
import qrcode
from PIL import Image
import io

app = Flask(__name__)

# Load parking positions
with open('CarParkPos', 'rb') as f:
    posList = pickle.load(f)

width, height = 107, 48

cap = cv2.VideoCapture('carPark.mp4')
current_qr_image = None  # For saving the current QR


def generate_qr_code(text):
    qr = qrcode.QRCode(version=1, box_size=3, border=1)
    qr.add_data(text)
    qr.make(fit=True)
    img_qr = qr.make_image(fill_color="black", back_color="white").convert('RGB')
    return img_qr


def check_parking_space(imgPro, img):
    space_counter = 0
    for pos in posList:
        x, y = pos
        imgCrop = imgPro[y:y + height, x:x + width]
        count = cv2.countNonZero(imgCrop)

        if count < 900:
            color = (0, 255, 0)
            thickness = 5
            space_counter += 1
        else:
            color = (0, 0, 255)
            thickness = 2

        cv2.rectangle(img, pos, (pos[0] + width, pos[1] + height), color, thickness)
        cvzone.putTextRect(img, str(count), (x, y + height - 3), scale=1, thickness=2, offset=0, colorR=color)

    cvzone.putTextRect(img, f'Free Parking: {space_counter}/{len(posList)}', (100, 50), scale=3,
                       thickness=5, offset=20, colorR=(0, 0, 0))

    return space_counter


def generate_frames():
    global current_qr_image
    while True:
        if cap.get(cv2.CAP_PROP_POS_FRAMES) == cap.get(cv2.CAP_PROP_FRAME_COUNT):
            cap.set(cv2.CAP_PROP_POS_FRAMES, 0)

        success, img = cap.read()
        if not success:
            break

        imgGray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        imgBlur = cv2.GaussianBlur(imgGray, (3, 3), 1)
        imgThreshold = cv2.adaptiveThreshold(imgBlur, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
                                             cv2.THRESH_BINARY_INV, 25, 16)
        imgMedian = cv2.medianBlur(imgThreshold, 5)
        kernel = np.ones((3, 3), np.uint8)
        imgDilate = cv2.dilate(imgMedian, kernel, iterations=1)

        free_spaces = check_parking_space(imgDilate, img)

        qr_text = f"Available Slots: {free_spaces}/{len(posList)}"
        qr_img_pil = generate_qr_code(qr_text)
        current_qr_image = qr_img_pil  # Save current QR for download

        qr_img_cv = np.array(qr_img_pil)
        qr_img_cv = cv2.cvtColor(qr_img_cv, cv2.COLOR_RGB2BGR)
        qr_img_cv = cv2.resize(qr_img_cv, (150, 150))

        img[10:160, 10:160] = qr_img_cv

        _, buffer = cv2.imencode('.jpg', img)
        frame = buffer.tobytes()

        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/video')
def video():
    return Response(generate_frames(),
                    mimetype='multipart/x-mixed-replace; boundary=frame')


@app.route('/generate_qr')
def generate_qr():
    global current_qr_image
    if current_qr_image:
        img_io = io.BytesIO()
        current_qr_image.save(img_io, 'PNG')
        img_io.seek(0)
        return send_file(img_io, mimetype='image/png')
    return "No QR code generated yet.", 404



if __name__ == '__main__':
    app.run(debug=True)

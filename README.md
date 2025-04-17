
# 🚗 Smart Parking Space Monitor with QR Code

This project is a Flask-based web application that detects available parking spaces in a video feed using computer vision and displays the status both visually and via a dynamically generated QR code. Users can view real-time parking availability and generate a QR that reflects current availability.

---

## 📸 Features

- 🔍 Real-time detection of available and occupied parking slots using OpenCV.
- 📦 Preloaded parking coordinates from a pickled file.
- 📹 Live video stream rendered directly in the web interface.
- 📲 QR Code generation with parking status.
- ⚡ Clean and responsive frontend with seamless QR preview.

---

## 🛠️ Technologies Used

- **Python 3**
- **Flask** – for the web application and routing
- **OpenCV** – for video frame analysis
- **cvzone** – for simplified drawing and overlays
- **qrcode** – for generating QR codes
- **PIL (Pillow)** – image formatting
- **HTML/CSS** – frontend UI
- **JavaScript** – handling QR fetch and display

---

## 🚀 Getting Started

### 1. Clone the repository

```bash
git clone https://github.com/your-username/smart-parking-qr.git
cd smart-parking-qr
```

### 2. Install dependencies

Make sure you have Python 3 and pip installed. Then run:

```bash
pip install -r requirements.txt
```

#### `requirements.txt` (example content)
```
flask
opencv-python
cvzone
numpy
qrcode
Pillow
```

### 3. Add Required Files

- A video file named `carPark.mp4` (sample parking lot footage).
- A pickle file `CarParkPos` containing parking space coordinates:
  - Format: list of `(x, y)` tuples.

> You can create your own parking space position file using OpenCV and mouse click events.

### 4. Run the Flask App

```bash
python app.py
```

Visit `http://127.0.0.1:5000` in your browser.

---

## 🌐 Web Interface

- **Live Feed**: Monitors and highlights each parking slot in the video.
- **Generate QR**: Button fetches the most recent QR code representing current availability.
- **QR Preview**: Displays updated QR beside the video for mobile-friendly access.

---

## 📁 Project Structure

```
├── app.py
├── carPark.mp4
├── CarParkPos
├── templates/
│   └── index.html
├── static/
│   └── style.css (optional)
└── README.md
```



## 📌 To Do / Future Improvements

- [ ] Add download button for QR Code
- [ ] Make it mobile responsive
- [ ] Add admin panel for custom slot mapping
- [ ] Push QR status to a cloud dashboard

---

## 🤝 Acknowledgements

- Inspired by practical applications in smart cities and IoT.
- Built with 💻 by Roopesh Sai and open-source libraries.

---


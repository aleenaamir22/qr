import streamlit as st
import cv2
import numpy as np
from PIL import Image

print("All modules are installed correctly!")
def generate_qr():
    """Generates a QR code from text input."""
    st.subheader("Generate QR Code")
    with st.form(key='qr_form'):
        raw_text = st.text_area("Enter text to generate QR Code")
        submit_button = st.form_submit_button("Generate")

        if submit_button and raw_text.strip():
            qr = qrcode.make(raw_text)
            qr.save("qrcode.png")  
            img = Image.open("qrcode.png")
            st.image(img, caption="Generated QR Code")

def decode_qr():
    """Decodes QR code from an uploaded image."""
    st.subheader("Upload & Decode QR Code")
    uploaded_file = st.file_uploader("Upload a QR Code Image", type=["png", "jpg", "jpeg"])

    if uploaded_file:
        image = Image.open(uploaded_file)
        st.image(image, caption="Uploaded QR Code", use_column_width=True)

        img_array = np.array(image)
        qr_detector = cv2.QRCodeDetector()
        data, _, _ = qr_detector.detectAndDecode(img_array)

        if data:
            st.success(f"Decoded QR Code Text: {data}")
        else:
            st.error("No QR Code detected. Try another image.")

def scan_qr():
    """Scans QR code using the webcam (requires OpenCV)."""
    st.subheader("Scan QR Code using Webcam")
    start_scan = st.button("Start Scanning")

    if start_scan:
        cap = cv2.VideoCapture(0)  # Open webcam
        qr_detector = cv2.QRCodeDetector()

        st.write("**Scanning... Press 'Q' to exit.**")
        while cap.isOpened():
            ret, frame = cap.read()
            if not ret:
                break

            data, _, _ = qr_detector.detectAndDecode(frame)
            cv2.imshow("QR Code Scanner", frame)

            if data:
                st.success(f"Scanned QR Code Text: {data}")
                break

            if cv2.waitKey(1) & 0xFF == ord('q'):  
                break

        cap.release()
        cv2.destroyAllWindows()

def main():
    st.title("QR Code Generator, Scanner & Decoder")

    # Sidebar Menu
    menu = ["Generate QR Code", "Decode QR Code", "Scan QR Code", "About"]
    choice = st.sidebar.selectbox("Menu", menu)

    if choice == "Generate QR Code":
        generate_qr()
    elif choice == "Decode QR Code":
        decode_qr()
    elif choice == "Scan QR Code":
        scan_qr()
    else:
        st.subheader("About")
        st.write("**QR Code Generator, Scanner & Decoder by Aleena Amir**")
        st.write(
            "This web app allows users to generate, scan, and decode QR codes easily. "
            "Enter text to create a QR code, upload an image to decode a QR code, "
            "or use your webcam to scan QR codes in real time!"
        )

if __name__ == "__main__":
    main()

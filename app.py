import streamlit as st
import face_recognition
import cv2
import numpy as np
from PIL import Image
import os
import time
import webbrowser

st.set_page_config(page_title="Face Auth", layout="centered")

st.title("😎 Autentikasi Wajah Nena")

# Load known face encodings
known_encodings = []
known_names = []

known_dir = "known_faces"
for file in os.listdir(known_dir):
    if file.endswith(".jpg") or file.endswith(".png"):
        image = face_recognition.load_image_file(os.path.join(known_dir, file))
        encodings = face_recognition.face_encodings(image)
        if encodings:
            known_encodings.append(encodings[0])
            known_names.append(file)

# Capture webcam image
img_file_buffer = st.camera_input("Ambil Foto")

if img_file_buffer is not None:
    # Convert to numpy array
    image = Image.open(img_file_buffer)
    img = np.array(image)

    rgb_img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

    faces = face_recognition.face_locations(rgb_img)
    encodings = face_recognition.face_encodings(rgb_img, faces)

    if encodings:
        match_found = False
        for face_encoding in encodings:
            results = face_recognition.compare_faces(known_encodings, face_encoding, tolerance=0.5)
            if any(results):
                match_found = True
                break

        if match_found:
            st.success("✅ Wajah dikenali! Kamu adalah Nena.")
            with st.spinner("Mengarahkan ke halaman spesial..."):
                time.sleep(2)
                webbrowser.open_new_tab("https://shefiyyahaurll.github.io/Nena-Cake/")
        else:
            st.error("❌ Wajah tidak dikenali.")
    else:
        st.warning("Tidak ada wajah terdeteksi.")

import cv2
import time
import os
import sqlite3
import easyocr
import re

CAMERA_SOURCE = 0
SAVE_IMAGES = True
DB_PATH = "plates.db"

def init_db():
    with sqlite3.connect(DB_PATH) as conn:
        conn.execute('''
            CREATE TABLE IF NOT EXISTS plates (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                plate TEXT,
                timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
                image_path TEXT
            )
        ''')

def insert_plate(plate, image_path):
    with sqlite3.connect(DB_PATH) as conn:
        conn.execute("INSERT INTO plates (plate, image_path) VALUES (?, ?)", (plate, image_path))

def clean_plate_text(text):
    # Corrige les confusions fréquentes
    text = text.upper().replace('O', '0').replace('I', '1').replace('S', '5')
    # Supprime les espaces et caractères spéciaux sauf '-'
    text = re.sub(r'[^A-Z0-9-]', '', text)
    # Corrige les formats type "PL123AK" en "PL-123-AK"
    match = re.match(r'^([A-Z]{2})[-\s]?(\d{3})[-\s]?([A-Z]{2})$', text)
    if match:
        return f"{match.group(1)}-{match.group(2)}-{match.group(3)}"
    return text

def recognize_plate_from_frame(frame, reader):
    # Amélioration du prétraitement
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    gray = cv2.bilateralFilter(gray, 11, 17, 17)
    _, thresh = cv2.threshold(gray, 120, 255, cv2.THRESH_BINARY)
    results = reader.readtext(thresh)
    plates = []
    for _, text, conf in results:
        if 4 <= len(text) <= 10 and conf > 0.6 and any(c.isdigit() for c in text):
            cleaned = clean_plate_text(text)
            if re.match(r'^[A-Z]{2}-\d{3}-[A-Z]{2}$', cleaned):
                plates.append(cleaned)
    return plates[0] if plates else None

def main(show_video=False, filter_duplicates=True, save_duplicates_images=False):
    init_db()
    cap = cv2.VideoCapture(CAMERA_SOURCE)
    if not cap.isOpened():
        print("[ERROR] Unable to connect to camera.")
        return
    os.makedirs("images", exist_ok=True)
    reader = easyocr.Reader(['fr'], gpu=True)
    last_plate = None

    while True:
        ret, frame = cap.read()
        if not ret:
            print("[ERROR] Failed to capture frame.")
            continue

        plate = recognize_plate_from_frame(frame, reader)
        is_duplicate = plate == last_plate
        should_print = plate is not None and (not filter_duplicates or not is_duplicate)
        should_save = plate is not None and (
            (not filter_duplicates) or
            (filter_duplicates and (not is_duplicate or save_duplicates_images))
        )

        if should_print:
            print(f"[DETECTED] Plate: {plate}")
            last_plate = plate

        if should_save and SAVE_IMAGES:
            img_path = os.path.join("images", f"{plate}_{int(time.time())}.jpg")
            cv2.imwrite(img_path, frame)
            insert_plate(plate, img_path)

        if show_video:
            cv2.imshow("Video", frame)
            # Quitter avec la touche 'q'
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

        time.sleep(0.5)  # Delay de 1 seconde entre les captures

    cap.release()
    if show_video:
        cv2.destroyAllWindows()

if __name__ == "__main__":
    # Exemple : retour vidéo activé, filtrage des doublons désactivé, mais enregistrement des doublons activé
    main(show_video=True, filter_duplicates=False, save_duplicates_images=True)
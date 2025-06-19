from flask import Flask, render_template, Response
import psycopg2
import cv2
from pyzbar.pyzbar import decode
from datetime import datetime
import time

app = Flask(__name__)

def get_passages():
    conn = psycopg2.connect(
        dbname="postgres",
        user="postgres",
        password="progtr00",
        host="localhost",
        port="5432"
    )
    cursor = conn.cursor()
    cursor.execute("""
        SELECT nom, prenom, badge_id, date_heure, camera_id
        FROM passages
        ORDER BY date_heure DESC LIMIT 10
    """)
    rows = cursor.fetchall()
    cursor.close()
    conn.close()
    return rows

def stream_camera(rtsp_url, camera_id):
    cap = cv2.VideoCapture(rtsp_url)
    if not cap.isOpened():
        print(f"Erreur : impossible d’ouvrir le flux RTSP {rtsp_url}")
        return

    last_detection_time = 0
    interval = 15
    last_badge_id = None

    while True:
        success, frame = cap.read()
        if not success:
            print(f"Erreur de lecture du flux vidéo caméra {camera_id}")
            break

        frame = cv2.resize(frame, (800, 600))
        barcodes = decode(frame)
        current_time = time.time()

        if barcodes:
            badge_id = barcodes[0].data.decode('utf-8')
            if badge_id != last_badge_id or (current_time - last_detection_time >= interval):
                last_badge_id = badge_id
                last_detection_time = current_time
                print(f"Badge détecté caméra {camera_id} : {badge_id}")
                try:
                    conn = psycopg2.connect(
                        dbname="postgres",
                        user="postgres",
                        password="progtr00",
                        host="localhost",
                        port="5432"
                    )
                    cursor = conn.cursor()
                    cursor.execute("SELECT nom, prenom FROM collaborateurs WHERE badge_id = %s", (badge_id,))
                    result = cursor.fetchone()

                    if result:
                        nom, prenom = result
                        cursor.execute("""
                            INSERT INTO passages (badge_id, nom, prenom, date_heure, camera_id)
                            VALUES (%s, %s, %s, %s, %s)
                        """, (badge_id, nom, prenom, datetime.now(), camera_id))
                        conn.commit()
                        print(f"✅ Passage enregistré caméra {camera_id} : {prenom} {nom}\n")
                    else:
                        print(f"❌ Collaborateur inconnu caméra {camera_id}\n")

                    cursor.close()
                    conn.close()
                except Exception as e:
                    print("Erreur base de données :", e)

        ret, buffer = cv2.imencode('.jpg', frame)
        if not ret:
            continue

        frame_bytes = buffer.tobytes()
        yield (
            b'--frame\r\n'
            b'Content-Type: image/jpeg\r\n\r\n' + frame_bytes + b'\r\n'
        )
        time.sleep(0.001)

    cap.release()

def gen_frames():
    return stream_camera("rtsp://admin:123456@192.168.51.6:554/live.sdp", "cam1")

def gen_frames_cam2():
    return stream_camera("rtsp://admin:123456@192.168.51.5:554/live.sdp", "cam2")

@app.route('/video_feed')
def video_feed():
    return Response(gen_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/video_feed_cam2')
def video_feed_cam2():
    return Response(gen_frames_cam2(), mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/')
def index():
    passages = get_passages()
    return render_template('index.html', passages=passages)

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=False)
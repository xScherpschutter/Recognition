import cv2
import pytesseract
import re
from datetime import datetime
from plateRecognition.models import Plate
def plate_detection():
    try:
        pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

        # Inicializar la cámara (0 es normalmente el índice de la cámara por defecto)
        cap = cv2.VideoCapture(0)

        while True:
            # Leer un frame de la cámara
            ret, frame = cap.read()
            if not ret:
                print("Error al acceder a la cámara.")
                break
            new_text = ''
            text = ''
            plate_found: bool = False
            
            # Procesar la imagen
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            gray = cv2.blur(gray, (5, 5))  # Aumentar el blur para reducir el ruido
            canny = cv2.Canny(gray, 50, 150)  # Ajustar umbrales de Canny para mejor detección de bordes
            canny = cv2.dilate(canny, None, iterations=1)

            cnts, _ = cv2.findContours(canny, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
            cv2.drawContours(frame, cnts, -1, (0, 255, 0), 1)  # Dibujar todos los contornos detectados para depuración

            for c in cnts:
                area = cv2.contourArea(c)
                x, y, w, h = cv2.boundingRect(c)
                epsilon = 0.02 * cv2.arcLength(c, True)  # Ajustar epsilon para una aproximación más precisa
                approx = cv2.approxPolyDP(c, epsilon, True)

                if len(approx) == 4 and area > 3000:  # Ajustar el área mínima
                    aspect_ratio = float(w) / h
                    if 2.0 < aspect_ratio < 5.0:  # Mantener el rango del aspect ratio
                        plate = gray[y:y + h, x:x + w]
                        text = pytesseract.image_to_string(plate, lang = 'eng', config='--psm 8')
                        text = (text.strip()).upper()
                        if text:
                            text = re.sub(r'\W+', '', text)
                            plate_found = Plate.objects.filter(Placa=text).exists()
                            cv2.imshow('Plate', plate)
                            cv2.moveWindow('Plate', 780, 10)
                            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 3)
                            cv2.putText(frame, text, (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2, cv2.LINE_AA)
            
            now = datetime.now()
            datetime_str = now.strftime("%Y-%m-%d %H:%M:%S")         
            new_text = text
            found = "Registrado" if plate_found else "No registrado"
            cv2.imshow('Image', frame)
            cv2.moveWindow('Image', 45, 10)
            
            _, frame_encoded = cv2.imencode('.jpg', frame)
            frame_bytes = frame_encoded.tobytes()
            
            yield(b'--frame\r\n' +
                b'Content-Type: image/jpeg\r\n\r\n' + frame_bytes + b'\r\n\r\n' +
                b'--text\r\n' +
                b'Content-Type: text/plain\r\n\r\n' + new_text.encode()+'|'.encode()+datetime_str.encode()+'|'.encode()+found.encode() + b'\r\n\r\n')
            
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

    finally:
        cap.release()
        cv2.destroyAllWindows()
        
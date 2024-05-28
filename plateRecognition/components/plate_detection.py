import cv2
import pytesseract
from PIL import Image
from io import BytesIO

def plate_detection():
    pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

    cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)
    try:
        while True:
            ret, frame = cap.read()
            if not ret:
                break

            annotated_frame = frame.copy()


            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            gray = cv2.blur(gray, (5, 5)) 
            canny = cv2.Canny(gray, 50, 150) 
            canny = cv2.dilate(canny, None, iterations=1)

            cnts, _ = cv2.findContours(canny, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
            cv2.drawContours(annotated_frame, cnts, -1, (0, 255, 0), 1) 

            detection_count = 0  
            max_detections = 1 
            new_text: str = ''
            text: str = ''
            
            for c in cnts:
                if detection_count >= max_detections:
                    break

                area = cv2.contourArea(c)
                x, y, w, h = cv2.boundingRect(c)
                epsilon = 0.02 * cv2.arcLength(c, True)  # Ajustar epsilon para una aproximación más precisa
                approx = cv2.approxPolyDP(c, epsilon, True)

                if len(approx) == 4 and area > 3000:  # Ajustar el área mínima
                    aspect_ratio = float(w) / h
                    if 2.0 < aspect_ratio < 5.0:  # Mantener el rango del aspect ratio
                        plate = gray[y:y + h, x:x + w]
                        text = pytesseract.image_to_string(plate, config='--psm 8')
                        text = text.strip()
                        if text:
                            print('plate: ', text)
                            cv2.rectangle(annotated_frame, (x, y), (x + w, y + h), (0, 255, 0), 3)
                            cv2.putText(annotated_frame, text, (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2, cv2.LINE_AA)
                            detection_count += 1
                            

            pil_image = Image.fromarray(cv2.cvtColor(annotated_frame, cv2.COLOR_BGR2RGB))
            buffer = BytesIO()
            pil_image.save(buffer, format='JPEG')
            frame_bytes = buffer.getvalue()

            new_text = text if text != '' else ''
            yield (b'--frame\r\n'
                b'Content-Type: image/jpeg\r\n\r\n' + frame_bytes + b'\r\n\r\n'+
                
                b'--text\r\n' +
                b'Content-Type: text/plain\r\n\r\n' + new_text.encode() + b'\r\n\r\n')
    finally:
        cap.release()
        cv2.destroyAllWindows()
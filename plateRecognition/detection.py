import cv2
import pytesseract


def detect_plates(frame):
    print(frame)
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    gray = cv2.blur(gray, (5, 5))  # Aumentar el blur para reducir el ruido
    canny = cv2.Canny(gray, 50, 150)
    canny = cv2.dilate(canny, None, iterations=1)

    cnts, _ = cv2.findContours(
        canny, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
    plates = []

    for c in cnts:
        area = cv2.contourArea(c)
        x, y, w, h = cv2.boundingRect(c)
        epsilon = 0.02 * cv2.arcLength(c, True)
        approx = cv2.approxPolyDP(c, epsilon, True)
        if len(approx) == 4 and area > 3000:
            aspect_ratio = float(w) / h
            if 2.0 < aspect_ratio < 5.0:
                placa = gray[y:y + h, x:x + w]
                text = pytesseract.image_to_string(placa, config='--psm 8')
                text = text.strip()
                if text:
                    plates.append({'bbox': [x, y, w, h], 'text': text})

        return plates

import cv2
import pytesseract

# Configurar la ruta de Tesseract OCR
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

# Inicializar la cámara (0 es normalmente el índice de la cámara por defecto)
cap = cv2.VideoCapture(0)


def PlateDetection(frame):
    print(frame)
    while True:
        # # Leer un frame de la cámara
        # ret, frame = cap.read()
        # if not ret:
        #     print("Error al acceder a la cámara.")
        #     break
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        gray = cv2.blur(gray, (5, 5))  # Aumentar el blur para reducir el ruido
        # Ajustar umbrales de Canny para mejor detección de bordes
        canny = cv2.Canny(gray, 50, 150)
        canny = cv2.dilate(canny, None, iterations=1)

        cnts, _ = cv2.findContours(
            canny, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
        # Dibujar todos los contornos detectados para depuración
        cv2.drawContours(frame, cnts, -1, (0, 255, 0), 1)

        for c in cnts:
            area = cv2.contourArea(c)
            x, y, w, h = cv2.boundingRect(c)
            # Ajustar epsilon para una aproximación más precisa
            epsilon = 0.02 * cv2.arcLength(c, True)
            approx = cv2.approxPolyDP(c, epsilon, True)

            if len(approx) == 4 and area > 3000:  # Ajustar el área mínima
                aspect_ratio = float(w) / h
                if 2.0 < aspect_ratio < 5.0:
                    placa = gray[y:y + h, x:x + w]
                    text = pytesseract.image_to_string(placa, config='--psm 8')
                    text = text.strip()
                    if text:
                        print('PLACA: ', text)

                        cv2.imshow('PLACA', placa)
                        cv2.moveWindow('PLACA', 780, 10)
                        cv2.rectangle(
                            frame, (x, y), (x + w, y + h), (0, 255, 0), 3)
                        cv2.putText(
                            frame, text, (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2, cv2.LINE_AA)
    #     # Mostrar el frame procesado
    #     cv2.imshow('Image', frame)
    #     cv2.moveWindow('Image', 45, 10)
    #     # Salir del bucle si se presiona la tecla 'q'
    #     if cv2.waitKey(1) & 0xFF == ord('q'):
    #         break
    # # Liberar el objeto de captura y cerrar las ventanas
    # cap.release()
    # cv2.destroyAllWindows()

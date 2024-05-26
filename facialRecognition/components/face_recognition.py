import cv2
import os

def recognize_face(image_path, dni: str):
    try:
        dataPath = os.path.join(os.path.dirname(__file__), 'data')
        imagePaths = os.listdir(dataPath)

        face_recognizer = cv2.face.EigenFaceRecognizer_create()
        model_path = os.path.join(os.path.dirname(__file__), 'modelEigenface.xml')
        face_recognizer.read(model_path)

        face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
        frame = cv2.imread(image_path)

        if frame is None:
            print('No hay frame')
            return False, dni
        print(frame)
        
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        auxFrame = gray.copy()
        faces = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))
        print("Rostros: ", faces)
        
        if len(faces) == 0:
            print("Cero rostros")
            return False, dni
        
        if len(faces) != 1:
            print("Más de un rostro")
            return False, dni
            
        for (x, y, w, h) in faces:
            face = auxFrame[y:y + h, x:x + w]
            face = cv2.resize(face, (150, 150), interpolation=cv2.INTER_CUBIC)
            result = face_recognizer.predict(face)

            if result[1] < 5700:
                result_dni = str(imagePaths[result[0]])

                if result_dni == dni:
                    print("DNI encontrada")
                    return True, dni
                
                print("DNI no encontrada")
                return False, dni
            
            else:
                print("Rostro desconocido")
                return False, dni

    except Exception as e:
        print("Excepcion")
        return False, "Error"


# imagen = os.path.join(os.path.dirname(__file__), 'data', '0941498941', 'rostro_0.jpg')
# print(imagen)
# dni = '0941498941'

# result, dni = recognize_face(imagen, dni)
# print(result, dni)
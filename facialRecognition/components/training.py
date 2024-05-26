import cv2
import os
import numpy as np

def training():
    try:
        dataPath = os.path.join(os.path.dirname(__file__), 'data')
        peopleList = os.listdir(dataPath)
        print('Lista de personas: ', peopleList)

        labels = []
        facesData = []
        label = 0

        for nameDir in peopleList:
            personPath = dataPath + '/' + nameDir
            print('Entrenando modelo con datos de: {}'.format(nameDir))

            for fileName in os.listdir(personPath):
                print('Rostros: ', nameDir + '/' + fileName)
                labels.append(label)
                facesData.append(cv2.imread(personPath+'/'+fileName,0))
                image = cv2.imread(personPath+'/'+fileName, 0)
                cv2.waitKey(10)
                
            label = label + 1

        face_recognizer = cv2.face.EigenFaceRecognizer_create()


        print("Entrenando...")
        face_recognizer.train(facesData, np.array(labels))

        model_path = os.path.join(os.path.dirname(__file__), 'modelEigenface.xml')
        face_recognizer.write(model_path)
        print("Modelo almacenado en la ruta: {}".format(model_path))
        
        return True, str(model_path)
    except Exception as e:
        return False, str(e)
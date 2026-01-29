import cv2
import numpy as np
from ultralytics import YOLO
from deepface import DeepFace
import matplotlob.pyplot as plt

def main():
    # 1. Cargar el modelo YOLO (detección de rostros)
    model = YOLO("models\yolov11s-face.pt")

    # 2. Abrir la cámara web
    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        print("No se pudo abrir la cámara web")
        return

    while True:
        ret, frame = cap.read()
        if not ret:
            print("No se pudo leer el frame de la cámara")
            break

        # 3. Realizar la detección con YOLO
        results = model.predict(source=frame, conf=0.3, verbose=False)  # Ajusta la confianza si lo necesitas

        # 4. Procesar las detecciones
        boxes = results[0].boxes if len(results) > 0 else []

        for box in boxes:
            # Extraer coordenadas (x1, y1, x2, y2)
            x1, y1, x2, y2 = box.xyxy[0][:4].tolist()
            x1, y1, x2, y2 = int(x1), int(y1), int(x2), int(y2)

            # Asegurarnos de que las coordenadas estén dentro de la imagen
            h, w = frame.shape[:2]
            x1, y1 = max(0, x1), max(0, y1)
            x2, y2 = min(w-1, x2), min(h-1, y2)

            # 5. Recortar la región del rostro
            face_crop = frame[y1:y2, x1:x2]
            if face_crop.size == 0:
                continue

            # 6. Estimar edad con DeepFace
            try:
                analysis = DeepFace.analyze(face_crop, actions=['age'], enforce_detection=False)

                # Si analysis es una lista, tomamos el primer elemento
                if isinstance(analysis, list):
                    analysis = analysis[0]

                # Obtenemos la edad
                estimated_age = analysis.get("age", 0)

            except Exception as e:
                print("Error en la estimación de edad:", e)
                estimated_age = 0

            # 7. Dibujar bounding box y mostrar la edad
            cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
            # Colocar el texto con la edad (encima del cuadro)
            label = f"Age: {int(estimated_age)}"
            cv2.putText(frame, label, (x1, max(y1 - 10, 0)), cv2.FONT_HERSHEY_SIMPLEX, 
                        0.8, (0, 255, 0), 2, cv2.LINE_AA)

        # 8. Mostrar el frame
        cv2.imshow("Webcam - Face Age Estimation", frame)

        #plt.imshow(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))
        #plt.axis("off")
        #plt.show()

        # Cerrar si presionamos 'q'
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()

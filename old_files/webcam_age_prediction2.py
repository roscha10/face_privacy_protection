import cv2
import torch
from transformers import AutoModelForImageClassification, AutoProcessor
from ultralytics import YOLO
from PIL import Image

# Cargar modelo de clasificación de edad
model_name = "nateraw/vit-age-classifier"
model = AutoModelForImageClassification.from_pretrained(model_name)
processor = AutoProcessor.from_pretrained(model_name)
model.eval()

# Cargar modelo YOLO para detección de rostros
face_detector = YOLO("models/yolov11s-face.pt")  # Ruta correcta del modelo YOLO de detección de caras

# Iniciar captura de video (0 para webcam)
cap = cv2.VideoCapture(0)

while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        print("No se pudo leer el frame")
        break

    # Detección de rostros con YOLO
    results = face_detector.predict(frame, conf=0.3, verbose=False)
    boxes = results[0].boxes if len(results) > 0 else []

    for box in boxes:
        x1, y1, x2, y2 = map(int, box.xyxy[0][:4].tolist())  # Convertir coordenadas

        # Verificar si las coordenadas son válidas
        if x1 < 0 or y1 < 0 or x2 <= x1 or y2 <= y1:
            continue

        # Recortar la región del rostro
        face_crop = frame[y1:y2, x1:x2]
        if face_crop.size == 0:
            continue

        try:
            # Convertir imagen a PIL, redimensionar y preprocesar
            face_pil = Image.fromarray(cv2.cvtColor(face_crop, cv2.COLOR_BGR2RGB))
            face_pil = face_pil.resize((224, 224))  # Redimensionar para el modelo
            inputs = processor(images=face_pil, return_tensors="pt")

            # Hacer predicción
            with torch.no_grad():
                outputs = model(**inputs)
            estimated_age = outputs.logits.argmax().item()

            # Clasificación: Mayor o menor de edad
            status = "Mayor de edad" if estimated_age >= 18 else "Menor de edad"
            color = (0, 255, 0) if estimated_age >= 18 else (0, 0, 255)  # Verde para mayor, rojo para menor

        except Exception as e:
            print(f"Error en la clasificación de edad: {e}")
            status = "No detectado"
            color = (255, 255, 255)

        # Dibujar el bounding box y la clasificación en el frame
        cv2.rectangle(frame, (x1, y1), (x2, y2), color, 2)
        cv2.putText(frame, status, (x1, max(y1 - 10, 0)), cv2.FONT_HERSHEY_SIMPLEX, 
                    0.8, color, 2, cv2.LINE_AA)

    # Mostrar el resultado en la ventana
    cv2.imshow("Detección de mayor o menor de edad", frame)

    # Presiona 'q' para salir
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Liberar recursos
cap.release()
cv2.destroyAllWindows()

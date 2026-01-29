from transformers import AutoModelForImageClassification, AutoProcessor
from PIL import Image
import torch

# Cargar modelo de estimación de edad
model_name = "nateraw/vit-age-classifier"
model = AutoModelForImageClassification.from_pretrained(model_name)
processor = AutoProcessor.from_pretrained(model_name)

# Cargar imagen de prueba
image_path = "test/foto2.jpg"
image = Image.open(image_path)

# Preprocesar imagen
inputs = processor(images=image, return_tensors="pt")

# Hacer predicción
with torch.no_grad():
    outputs = model(**inputs)

predicted_age = outputs.logits.argmax().item()
print(f"Edad estimada: {predicted_age}")

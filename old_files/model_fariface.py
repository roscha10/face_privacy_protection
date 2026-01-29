import torch

# URL del modelo preentrenado de FairFace
model_url = "https://github.com/dchen236/FairFace/raw/master/fairface_models/fairface_alldata_20191111.pt"

# Descarga el modelo
model_path = "fairface_model.pth"
torch.hub.download_url_to_file(model_url, model_path)
print("Modelo FairFace descargado exitosamente.")

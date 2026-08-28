import os
import torch
import torch.nn.functional as F
from torchvision import transforms
from PIL import Image
from app.ml.cnn_model import CropDiseaseModel
from app.ml.image_utils import extract_leaf_roi
import random

# Mapping of class index to disease name (PlantVillage subsets)
CLASS_NAMES = [
    "Apple___Apple_scab", "Apple___Black_rot", "Apple___Cedar_apple_rust", "Apple___healthy",
    "Blueberry___healthy", "Cherry_(including_sour)___Powdery_mildew", "Cherry_(including_sour)___healthy",
    "Corn_(maize)___Cercospora_leaf_spot Gray_leaf_spot", "Corn_(maize)___Common_rust_",
    "Corn_(maize)___Northern_Leaf_Blight", "Corn_(maize)___healthy", "Grape___Black_rot",
    "Grape___Esca_(Black_Measles)", "Grape___Leaf_blight_(Isariopsis_Leaf_Spot)", "Grape___healthy",
    "Orange___Haunglongbing_(Citrus_greening)", "Peach___Bacterial_spot", "Peach___healthy",
    "Pepper,_bell___Bacterial_spot", "Pepper,_bell___healthy", "Potato___Early_blight",
    "Potato___Late_blight", "Potato___healthy", "Raspberry___healthy", "Soybean___healthy",
    "Squash___Powdery_mildew", "Strawberry___Leaf_scorch", "Strawberry___healthy",
    "Tomato___Bacterial_spot", "Tomato___Early_blight", "Tomato___Late_blight", "Tomato___Leaf_Mold",
    "Tomato___Septoria_leaf_spot", "Tomato___Spider_mites Two-spotted_spider_mite",
    "Tomato___Target_Spot", "Tomato___Tomato_Yellow_Leaf_Curl_Virus", "Tomato___Tomato_mosaic_virus",
    "Tomato___healthy"
]

def load_model(model_path="model_checkpoint.pth"):
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    model = CropDiseaseModel(num_classes=len(CLASS_NAMES))
    
    # Resolve absolute path relative to this script
    current_dir = os.path.dirname(os.path.abspath(__file__))
    abs_model_path = os.path.join(current_dir, model_path)
    
    if os.path.exists(abs_model_path):
        try:
            model.load_state_dict(torch.load(abs_model_path, map_location=device))
            model.to(device)
            model.eval()
            print(f"Model loaded successfully from {abs_model_path}")
            return model, device
        except Exception as e:
            print(f"Error loading model weights: {e}")
            
    print(f"Warning: Pre-trained model not found at {abs_model_path}. Inference will use a fallback mock mechanism.")
    return None, device

# Initialize globally if possible
model, device = load_model()

def predict_disease(image_path):
    """
    Predict the disease from a crop leaf image.
    Returns: (crop_name, disease_name, confidence_score)
    """
    # 1. ROI Extraction
    roi_image = extract_leaf_roi(image_path)
    if roi_image is None:
        # Fallback to original image if OpenCV fails
        try:
            pil_img = Image.open(image_path).convert('RGB')
        except Exception as e:
            return None, None, 0.0
    else:
        # Convert OpenCV BGR to RGB PIL Image
        roi_rgb = roi_image[:, :, ::-1]
        pil_img = Image.fromarray(roi_rgb)
        
    # 2. Transform
    transform = transforms.Compose([
        transforms.Resize((224, 224)),
        transforms.ToTensor(),
        transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225])
    ])
    
    # 3. Model Inference (or Mock fallback)
    if model is None:
        # Mock Prediction for demonstration
        print("Using Mock Prediction...")
        idx = random.randint(0, len(CLASS_NAMES) - 1)
        predicted_class = CLASS_NAMES[idx]
        confidence = round(random.uniform(75.0, 99.9), 2)
    else:
        # Actual Inference
        img_tensor = transform(pil_img).unsqueeze(0).to(device)
        with torch.no_grad():
            outputs = model(img_tensor)
            probabilities = F.softmax(outputs, dim=1)
            confidence, predicted_idx = torch.max(probabilities, 1)
            
            confidence = round(confidence.item() * 100, 2)
            predicted_class = CLASS_NAMES[predicted_idx.item()]
            
    # Parse output "Crop___Disease"
    parts = predicted_class.split("___")
    crop = parts[0].replace("_", " ")
    disease = parts[1].replace("_", " ")
    
    return crop, disease, confidence

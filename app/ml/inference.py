import os
import random
import numpy as np
from PIL import Image
from app.ml.image_utils import extract_leaf_roi
import onnxruntime as ort

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

def load_model():
    current_dir = os.path.dirname(os.path.abspath(__file__))
    model_path = os.path.join(current_dir, "mobilenetv2_plant.onnx")
    
    if os.path.exists(model_path):
        try:
            session = ort.InferenceSession(model_path)
            print(f"ONNX Model loaded successfully from {model_path}")
            return session
        except Exception as e:
            print(f"Error loading ONNX model: {e}")
            
    print(f"Warning: ONNX model not found at {model_path}. Inference will use a fallback mock mechanism.")
    return None

# Initialize globally
ort_session = load_model()

def softmax(x):
    e_x = np.exp(x - np.max(x, axis=1, keepdims=True))
    return e_x / np.sum(e_x, axis=1, keepdims=True)

def preprocess_image(pil_img):
    # Resize
    img = pil_img.resize((224, 224), Image.BILINEAR)
    # To numpy array and scale to [0, 1]
    img_arr = np.array(img).astype(np.float32) / 255.0
    # ToTensor equivalent: HWC to CHW
    img_arr = np.transpose(img_arr, (2, 0, 1))
    # Normalize
    mean = np.array([0.485, 0.456, 0.406]).reshape(3, 1, 1)
    std = np.array([0.229, 0.224, 0.225]).reshape(3, 1, 1)
    img_arr = (img_arr - mean) / std
    # Add batch dimension
    return np.expand_dims(img_arr, axis=0).astype(np.float32)

def predict_disease(image_path):
    """
    Predict the disease from a crop leaf image using ONNX.
    Returns: (crop_name, disease_name, confidence_score)
    """
    # 1. ROI Extraction
    roi_image = extract_leaf_roi(image_path)
    if roi_image is None:
        try:
            pil_img = Image.open(image_path).convert('RGB')
        except Exception as e:
            return None, None, 0.0
    else:
        # Convert OpenCV BGR to RGB PIL Image
        roi_rgb = roi_image[:, :, ::-1]
        pil_img = Image.fromarray(roi_rgb)
        
    # 2. Model Inference (or Mock fallback)
    if ort_session is None:
        print("Using Mock Prediction...")
        idx = random.randint(0, len(CLASS_NAMES) - 1)
        predicted_class = CLASS_NAMES[idx]
        confidence = round(random.uniform(75.0, 99.9), 2)
    else:
        # Actual ONNX Inference
        img_tensor = preprocess_image(pil_img)
        input_name = ort_session.get_inputs()[0].name
        output_name = ort_session.get_outputs()[0].name
        
        outputs = ort_session.run([output_name], {input_name: img_tensor})
        probabilities = softmax(outputs[0])
        
        predicted_idx = np.argmax(probabilities, axis=1)[0]
        confidence = round(probabilities[0][predicted_idx] * 100, 2)
        predicted_class = CLASS_NAMES[predicted_idx]
            
    # Parse output "Crop___Disease"
    parts = predicted_class.split("___")
    crop = parts[0].replace("_", " ")
    disease = parts[1].replace("_", " ")
    
    return crop, disease, confidence

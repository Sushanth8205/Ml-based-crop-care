import cv2
import numpy as np

def extract_leaf_roi(image_path):
    """
    Extracts the Region of Interest (leaf) from the background.
    Returns a processed numpy image or the original image if extraction fails.
    """
    try:
        image = cv2.imread(image_path)
        if image is None:
            return None
            
        # Convert to HSV color space
        hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
        
        # Define range for green color (most leaves)
        lower_green = np.array([25, 40, 40])
        upper_green = np.array([100, 255, 255])
        
        # Threshold the HSV image
        mask = cv2.inRange(hsv, lower_green, upper_green)
        
        # Find contours
        contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        
        if not contours:
            return image
            
        # Get largest contour
        largest_contour = max(contours, key=cv2.contourArea)
        
        # Create a bounding box
        x, y, w, h = cv2.boundingRect(largest_contour)
        
        # Crop the image to the bounding box
        roi = image[y:y+h, x:x+w]
        
        return roi
    except Exception as e:
        print(f"Error in ROI extraction: {e}")
        # Fallback to returning original image loaded by cv2 if possible
        return cv2.imread(image_path)

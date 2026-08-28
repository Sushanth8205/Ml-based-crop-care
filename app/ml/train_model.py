import os
import torch
import torch.nn as nn
import torch.optim as optim
from torchvision import datasets, transforms
from torch.utils.data import DataLoader
from app.ml.cnn_model import CropDiseaseModel

def train_model(data_dir="knowledge_base/plantvillage dataset/color", epochs=5, batch_size=32, save_path="app/ml/model_checkpoint.pth"):
    if not os.path.exists(data_dir):
        print(f"Dataset directory {data_dir} not found. Cannot train.")
        return

    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    print(f"Using device: {device}")

    # Data transformations
    transform = transforms.Compose([
        transforms.Resize((224, 224)),
        transforms.RandomHorizontalFlip(),
        transforms.ToTensor(),
        transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225])
    ])

    try:
        # Load dataset
        dataset = datasets.ImageFolder(root=data_dir, transform=transform)
        num_classes = len(dataset.classes)
        print(f"Found {num_classes} classes.")
        
        dataloader = DataLoader(dataset, batch_size=batch_size, shuffle=True, num_workers=2)
        
        # Initialize model
        model = CropDiseaseModel(num_classes=num_classes).to(device)
        criterion = nn.CrossEntropyLoss()
        optimizer = optim.Adam(model.parameters(), lr=0.0001)

        # Training Loop
        for epoch in range(epochs):
            model.train()
            running_loss = 0.0
            
            print(f"Epoch {epoch+1}/{epochs}")
            for inputs, labels in dataloader:
                inputs, labels = inputs.to(device), labels.to(device)
                
                optimizer.zero_grad()
                outputs = model(inputs)
                loss = criterion(outputs, labels)
                loss.backward()
                optimizer.step()
                
                running_loss += loss.item() * inputs.size(0)
                
            epoch_loss = running_loss / len(dataset)
            print(f"Loss: {epoch_loss:.4f}")
            
        # Save model
        torch.save(model.state_dict(), save_path)
        print(f"Model saved to {save_path}")

    except Exception as e:
        print(f"Error during training: {e}")

if __name__ == "__main__":
    train_model()

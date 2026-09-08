# CropCare AI Architecture & Data Flow

This document provides the high-level architecture and data flow diagrams for the CropCare AI system based on the current project structure and plans.

## High-Level Architecture

The architecture relies on a Flask backend, a MongoDB database for storage, a PyTorch ML pipeline for inference, and the Gemini API for the RAG-based AI system.

```mermaid
graph TD
    Client[Web / Mobile Client] -->|HTTP/HTTPS| FlaskApp[Flask Application]
    
    subgraph Backend Server
        FlaskApp --> Auth[Authentication & Roles]
        FlaskApp --> Detection[Disease Detection]
        FlaskApp --> AI[AI RAG System]
        FlaskApp --> AdvisorSystem[Advisor & Appointments]
        FlaskApp --> Report[PDF Generation]
    end
    
    subgraph Machine Learning Pipeline
        Detection --> ImageUtils[OpenCV Preprocessing]
        ImageUtils --> MLModel[PyTorch VGG-16 + Attention]
        MLModel -.->|Prediction & Confidence| Detection
    end
    
    subgraph External Services
        AI --> GeminiAPI[Gemini AI API]
    end
    
    subgraph Database Layer
        Auth --> MongoDB[(MongoDB)]
        Detection --> MongoDB
        AI --> MongoDB
        AdvisorSystem --> MongoDB
    end
    
    MongoDB -.-> Users[Users / Advisors]
    MongoDB -.-> Detections[Detection History]
    MongoDB -.-> Knowledge[Knowledge Base]
    MongoDB -.-> Appointments[Appointments]
```

## Data Flow Diagram

This diagram illustrates how data moves through the system from the moment a user uploads a crop leaf image to generating a report and booking an advisor.

```mermaid
sequenceDiagram
    participant Farmer
    participant App as Flask Backend
    participant ML as ML Pipeline (PyTorch)
    participant DB as MongoDB
    participant AI as Gemini API
    participant Advisor
    
    Farmer->>App: 1. Upload Crop Image
    App->>ML: 2. Send Image for Preprocessing (ROI) & Inference
    ML-->>App: 3. Return Disease Prediction & Confidence Score
    App->>DB: 4. Save Detection Record
    App-->>Farmer: 5. Display Prediction Result
    
    Farmer->>App: 6. Click "Ask AI"
    App->>DB: 7. Fetch Context (Crop, Disease, Location) from Knowledge Base
    DB-->>App: 8. Return Grounded Context
    App->>AI: 9. Send Context + User Prompt
    AI-->>App: 10. Generate Agricultural Advice
    App-->>Farmer: 11. Display AI Response
    
    Farmer->>App: 12. Request PDF Report
    App-->>Farmer: 13. Generate & Download PDF
    
    Farmer->>App: 14. Browse Advisors & Select Slot
    Farmer->>App: 15. Book Appointment & Attach PDF
    App->>DB: 16. Create Appointment Record
    DB-->>Advisor: 17. Update Advisor Dashboard with Appointment & PDF
```

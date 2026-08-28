# Master Architecture and Implementation Plan

## Overview
CropCare AI is an explainable crop disease detection and decision-support system. It integrates CNN-based image classification (VGG-16 with Attention Mechanism), RAG-based AI decision support, and a role-based consultation system (Farmers and Agricultural Advisors).

## 1. Folder Structure
```
app/
├── __init__.py          # Flask app factory and DB initialization
├── routes/              # Modular routing (Blueprints)
│   ├── auth.py          # Authentication & Role management
│   ├── main.py          # Dashboard & Core pages
│   ├── detection.py     # Image upload, CNN inference, Results
│   ├── ai.py            # Gemini AI RAG endpoint
│   ├── advisor.py       # Advisor listing, Appointment booking
│   └── report.py        # PDF generation and handling
├── models/              # MongoDB data access layers
│   ├── user.py          # User schema and methods
│   ├── advisor.py       # Advisor-specific extensions
│   ├── detection.py     # Inference history
│   ├── appointment.py   # Booking and scheduling logic
│   └── knowledge.py     # RAG knowledge base access
├── static/              # Frontend assets
│   ├── css/style.css    # Responsive, mobile-first design
│   ├── js/              # Client-side interactions
│   └── uploads/         # Temporary storage for images/PDFs
├── templates/           # Jinja2 HTML templates
│   ├── base.html        # Main layout
│   ├── dashboard/       # Role-specific dashboards
│   └── ...
└── ml/                  # Machine Learning pipeline
    ├── cnn_model.py     # PyTorch model definition (VGG-16 + Attention)
    ├── inference.py     # Prediction pipeline
    └── image_utils.py   # OpenCV ROI extraction
```

## 2. MongoDB Collections and Relationships
- **users**: `_id`, `name`, `email`, `password_hash`, `role` (user/advisor), `location_details`.
- **advisors**: Links to `users._id`. Stores `experience`, `qualification`, `specializations`, `availability_slots`.
- **detections**: `_id`, `user_id` (ref: users), `crop`, `disease_predicted`, `confidence`, `image_path`, `timestamp`.
- **appointments**: `_id`, `farmer_id` (ref: users), `advisor_id` (ref: users), `date_time`, `status`, `report_pdf_path`.
- **ai_chats**: `_id`, `user_id`, `context` (crop/disease), `chat_history`.
- **knowledge_base**: Curated data for RAG (crop, disease, symptoms, prevention, management).

## 3. Flows

### Authentication & User Role Flow
- **Registration**: User selects role (Farmer or Advisor). Advisors provide additional details.
- **Login**: Verifies hashed password and sets `session['role']`.
- **Authorization**: Flask routes use decorators to restrict access (e.g., only Advisors can see the Advisor Dashboard).

### CNN Integration & Disease Detection Flow
1. User uploads a crop leaf image via the frontend.
2. `detection.py` route saves the image temporarily.
3. `image_utils.py` applies OpenCV preprocessing (ROI extraction).
4. `inference.py` passes the tensor through the PyTorch model (VGG-16 + Attention).
5. The model outputs a prediction label and confidence score.
6. If confidence > threshold, display the result; else, request a clearer image.

### RAG/AI Flow (Ask AI)
1. User clicks "Ask AI" from a positive disease result.
2. The frontend sends `crop`, `disease`, and `location` as hidden context.
3. `ai.py` queries the `knowledge_base` collection to retrieve grounded context.
4. Gemini API receives the grounded context + user prompt to generate safe, agricultural-specific advice.

### PDF Report & Upload Flow
1. User requests a report. `report.py` uses ReportLab to compile detection details, user info, and recommended actions into a PDF.
2. The PDF is saved locally/provided for download.
3. When booking an appointment, the user can upload this PDF.
4. The Advisor can download and view the PDF from their dashboard.

### Advisor & Appointment Flow
1. Farmer browses advisors filtered by specialization/location.
2. Farmer views available slots (pulled from `advisors` collection).
3. Farmer selects a slot and attaches the PDF report.
4. `appointment.py` checks for double-booking and creates the record.
5. Advisor dashboard displays the upcoming appointment and attached PDF.

## 4. Mobile Responsive UI Structure
- **CSS Strategy**: Mobile-first media queries (`@media (min-width: 768px)`).
- **Aesthetics**: Glassmorphism (`backdrop-filter: blur`), vibrant harmonious colors (greens for agriculture), and fluid typography (Inter font).
- **Components**: Flexible grid/flexbox for dashboard cards, off-canvas menu for mobile navigation.

## Implementation Order
1. **Phase 2: ML Pipeline**: Build the PyTorch VGG-16 + Attention architecture, integrate OpenCV for ROI, and create the upload/detection endpoints.
2. **Phase 3: RAG & PDF**: Implement the ReportLab PDF generator and the Gemini API RAG chatbot interface.
3. **Phase 4: Advisor System**: Build the Advisor profiles, search functionality, and the appointment booking system with double-booking prevention.
4. **Phase 5: Polish & UI**: Finalize the mobile-responsive Glassmorphism UI and perform end-to-end testing.

import os
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, ListFlowable, ListItem
from reportlab.lib.styles import getSampleStyleSheet

def create_status_report(filename):
    doc = SimpleDocTemplate(filename, pagesize=letter)
    styles = getSampleStyleSheet()
    story = []

    story.append(Paragraph("Project Status Report: CropCare AI", styles['Title']))
    story.append(Spacer(1, 12))

    story.append(Paragraph("<b>Completed Work:</b>", styles['Heading2']))
    completed = [
        "Phase 1: Robust Authentication System for Farmers and Advisors with Role-Based Dashboards.",
        "Phase 2: PyTorch CNN Inference Pipeline (VGG-16 + Custom Attention Mechanism) for leaf disease detection.",
        "Phase 2: Model weights successfully initialized and PyTorch absolute path resolution implemented (Real CNN Inference active, replacing mock mechanisms).",
        "Phase 3: Automated PDF Diagnosis Report Generation for detected diseases.",
        "Phase 3: RAG AI Assistant integration using Google Gemini API (Updated to gemini-3.6-flash).",
        "Phase 4: Advisor Network with search, filtering, and appointment booking system.",
        "Phase 4: Double-booking prevention and seamless PDF report handoff to advisors.",
        "Phase 5: UI/UX Glassmorphism styling and mobile responsiveness testing."
    ]
    for item in completed:
        story.append(Paragraph(f"- {item}", styles['Normal']))
    story.append(Spacer(1, 12))

    story.append(Paragraph("<b>Pending Work:</b>", styles['Heading2']))
    pending = [
        "Train the CNN model using the complete PlantVillage dataset (currently using initialized demo weights).",
        "Deploy the application to a production server (e.g., Render, Heroku) using a production WSGI server (Gunicorn).",
        "Set up a dedicated MongoDB Atlas cluster for production data.",
        "Expand the AI prompt engineering to support regional language translations."
    ]
    for item in pending:
        story.append(Paragraph(f"- {item}", styles['Normal']))

    doc.build(story)
    print(f"Generated {filename}")

def create_architecture_report(filename):
    doc = SimpleDocTemplate(filename, pagesize=letter)
    styles = getSampleStyleSheet()
    story = []

    story.append(Paragraph("System Architecture & Model Documentation", styles['Title']))
    story.append(Spacer(1, 12))

    story.append(Paragraph("<b>1. How the Whole Project Works</b>", styles['Heading2']))
    story.append(Paragraph("CropCare AI is a comprehensive web application designed to connect farmers directly with AI diagnostics and human agricultural advisors.", styles['Normal']))
    story.append(Spacer(1, 12))
    story.append(Paragraph("<b>The Flow:</b>", styles['Normal']))
    flow = [
        "Farmers upload an image of a diseased crop leaf.",
        "The image is processed by a PyTorch Convolutional Neural Network (CNN) to predict the disease. Real PyTorch inference is executed utilizing the initialized model_checkpoint.pth.",
        "A downloadable PDF diagnosis report is generated.",
        "The farmer can ask the Gemini-powered AI Assistant follow-up questions, which automatically knows the detected disease (RAG context).",
        "If further help is needed, the farmer can search for a registered Agricultural Advisor and book a time slot, attaching their PDF report."
    ]
    for item in flow:
        story.append(Paragraph(f"- {item}", styles['Normal']))
    story.append(Spacer(1, 12))

    story.append(Paragraph("<b>2. AI Model Used (Disease Detection)</b>", styles['Heading2']))
    story.append(Paragraph("The system uses a custom deep learning architecture built on top of <b>VGG-16</b>.", styles['Normal']))
    story.append(Paragraph("- <b>Base Model:</b> Pre-trained VGG-16 network for robust feature extraction.", styles['Normal']))
    story.append(Paragraph("- <b>Attention Mechanism:</b> A custom Spatial Attention Block is added to the CNN. This allows the model to focus specifically on the diseased spots on the leaf and ignore the background.", styles['Normal']))
    story.append(Paragraph("- <b>Preprocessing:</b> OpenCV is used to extract the Leaf Region of Interest (ROI) by masking out non-green backgrounds. This extracted ROI is then fed directly into the model tensor.", styles['Normal']))
    story.append(Spacer(1, 12))

    story.append(Paragraph("<b>3. AI Assistant (Gemini API)</b>", styles['Heading2']))
    story.append(Paragraph("The conversational AI is powered by the latest <b>Google Gemini 3.6 Flash</b> utilizing the google-genai SDK. It uses Retrieval-Augmented Generation (RAG) principles by dynamically injecting the farmer's location, crop type, and predicted disease into the hidden prompt, ensuring highly relevant answers without requiring the farmer to type long explanations.", styles['Normal']))
    story.append(Spacer(1, 12))

    story.append(Paragraph("<b>4. Tech Stack</b>", styles['Heading2']))
    tech = [
        "Backend: Python, Flask",
        "Database: MongoDB (PyMongo)",
        "Machine Learning: PyTorch, TorchVision, OpenCV",
        "Generative AI: Google Gemini GenAI SDK (gemini-3.6-flash)",
        "Frontend: HTML5, CSS3 (Glassmorphism UI), JavaScript",
        "PDF Generation: ReportLab"
    ]
    for item in tech:
        story.append(Paragraph(f"- {item}", styles['Normal']))

    doc.build(story)
    print(f"Generated {filename}")

if __name__ == "__main__":
    create_status_report("Project_Status_Report.pdf")
    create_architecture_report("Project_Architecture_Model.pdf")

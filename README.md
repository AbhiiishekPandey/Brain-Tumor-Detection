# Brain Tumor Detection with Explainable AI (XAI)

A production-ready deep learning application for detecting brain tumors from MRI scans. The system utilizes an **EfficientNetV2-S** model and provides visual explanations using **Grad-CAM++**, followed by a professional diagnostic PDF report.

![Dashboard Preview](static/ui_preview.png) *(Note: Add your UI preview here)*

## 🚀 Features
- **High Accuracy Detection**: Leveraging state-of-the-art EfficientNetV2-S architecture.
- **Explainable AI (XAI)**: Provides Grad-CAM++ heatmaps to show exactly where the model is looking.
- **Professional Reporting**: Automated generation of diagnostic PDF reports for clinical support.
- **Production Hardened**: Secure file handling, robust error logging, and environment-based configuration.
- **Web Interface**: Clean, dark-themed dashboard for intuitive MRI analysis.

## 🛠️ Tech Stack
- **Backend**: Python, Flask
- **Deep Learning**: PyTorch, Timm (EfficientNetV2)
- **XAI**: OpenCV, Matplotlib
- **Reporting**: ReportLab
- **Frontend**: HTML5, CSS3, Vanilla JS

## 📦 Installation

1. **Clone the repository:**
   ```bash
   git clone https://github.com/YourUsername/Brain-Tumor-Detection.git
   cd Brain-Tumor-Detection
   ```

2. **Create a virtual environment:**
   ```bash
   python -m venv .venv
   source .venv/bin/activate  # Windows: .venv\Scripts\activate
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Setup Environment Variables:**
   Copy the example environment file and update it:
   ```bash
   cp .env.example .env
   ```

## 🖥️ Usage

1. **Run the application:**
   ```bash
   python frontend/app.py
   ```
2. Open `http://127.0.0.1:5000` in your browser.
3. Upload an MRI scan (supported: PNG, JPG, WEBP).
4. View the AI prediction and the generated Grad-CAM heatmap.
5. Click **Download Diagnostic Report** to export the findings.

## 📁 Project Structure
- `src/`: Core logic and model utilities.
  - `models/`: Training and inference engine.
  - `explainability/`: Grad-CAM++ implementation.
- `frontend/`: Flask application and UI templates.
- `static/`: Assets, uploads (ignored by git), and generated reports.
- `results/`: Evaluation metrics and training curves.

## ⚖️ Disclaimer
*This application is designed for educational and clinical support purposes only. It is not a replacement for professional medical diagnosis. All findings should be reviewed by a certified radiologist.*

## 📄 License
This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

# 📄 Resume Analyzer AI

**Empowering Job Seekers & Recruiters with Intelligent AI Insights.**

Resume Analyzer AI is a sophisticated web application built with **Flask** and powered by **Google Gemini AI**. It provides deep analysis of resumes by comparing them against job descriptions, offering detailed feedback, skill matching, and an overall relevance score.

Live Demo Link : https://resume-analyzer-ai-8l0s.onrender.com

---

## 🚀 Key Features

-   **Multi-Format Support**: Effortlessly upload resumes in **PDF**, **DOCX**, or **Image (JPG, PNG)** formats.
-   **AI-Powered Scoring**: Get instant feedback on your resume's relevance, sentiment, and alignment with the job description.
-   **Skill Gap Analysis**: Automatically identifies matching skills and highlights areas for improvement.
-   **Google Gemini Integration**: Leverages the latest LLM tech for human-like feedback and actionable suggestions.
-   **Optical Character Recognition (OCR)**: Built-in Tesseract OCR to read and analyze scanned image-based resumes.
-   **Modern Dashboard**: A clean, intuitive interface to visualize your results.

---

## 🛠️ Tech Stack

-   **Frontend**: HTML5, CSS3 (Vanilla), JavaScript
-   **Backend**: Python, Flask
-   **AI/NLP**: 
    -   Google Gemini AI (Generative Insights)
    -   spaCy (Natural Language Processing)
    -   TextBlob (Sentiment Analysis)
    -   Scikit-learn (TF-IDF & Cosine Similarity)
-   **Document Processing**:
    -   Pdfminer.six (PDF Extraction)
    -   Docx2txt (DOCX Extraction)
    -   Tesseract OCR (Image Text Extraction)

---

## 🔧 Installation & Setup

Follow these steps to get the system running locally:

### 1. Prerequisites

Ensure you have the following installed:
-   **Python 3.8+**
-   **Tesseract OCR**: 
    -   Windows: [Download Tesseract](https://github.com/UB-Mannheim/tesseract/wiki)
    -   Linux: `sudo apt install tesseract-ocr`
    -   Mac: `brew install tesseract`

### 2. Clone the Repository

```bash
git clone https://github.com/your-username/resume-analyzer-ai.git
cd resume-analyzer-ai
```

### 3. Create a Virtual Environment

```bash
python -m venv venv
# Windows
venv\Scripts\activate
# Linux/Mac
source venv/bin/activate
```

### 4. Install Dependencies

```bash
pip install -r requirements.txt
python -m spacy download en_core_web_sm
```

### 5. Configure Environment Variables

Create a `.env` file in the root directory and add your **Google Gemini API Key**:

```env
GEMINI_API_KEY=your_api_key_here
```
*You can get an API key from [Google AI Studio](https://aistudio.google.com/).*

---

## 🏃 Running the Application

Start the Flask server:

```bash
python app.py
```

Open your browser and navigate to:
`http://127.0.0.1:5000`

---

## 📖 Usage Guide

1.  **Paste Job Description**: Copy and paste the target job description into the text area.
2.  **Upload Resume**: Select your resume file (PDF, DOCX, or Image).
3.  **Analyze**: Click "Analyze Resume" and wait for the AI to process.
4.  **Review Results**: See your score, skill matches, and detailed Gemini-powered recommendations.

---

## 🤝 Contributing

Contributions are welcome! If you'd like to improve the AI logic, UI, or add new features:
1.  Fork the Project.
2.  Create your Feature Branch (`git checkout -b feature/AmazingFeature`).
3.  Commit your Changes (`git commit -m 'Add some AmazingFeature'`).
4.  Push to the Branch (`git push origin feature/AmazingFeature`).
5.  Open a Pull Request.

---

## 📜 License

Distributed under the **MIT License**. See `LICENSE` for more information.

---

**Developed with ❤️ by [Samuel Heman John](https://github.com/Cherukuri-Samuel)**

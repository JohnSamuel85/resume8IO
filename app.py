import os
import re
import spacy
import pytesseract
from PIL import Image
from textblob import TextBlob
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.feature_extraction.text import TfidfVectorizer
from pdfminer.high_level import extract_text as extract_pdf_text
import docx2txt
import google.generativeai as genai
from flask import Flask, render_template, request, jsonify
from werkzeug.utils import secure_filename
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

app = Flask(__name__)

# Configure upload folder
UPLOAD_FOLDER = 'uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16 MB limit

# Allowed extensions
ALLOWED_EXTENSIONS = {'pdf', 'docx', 'jpg', 'jpeg', 'png'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# --- AI Logic Ported from Script ---

# Load spaCy model (will need python -m spacy download en_core_web_sm eventually)
try:
    nlp = spacy.load('en_core_web_sm')
except Exception as e:
    print(f"Warning: spaCy model not loaded. Run 'python -m spacy download en_core_web_sm'. Error: {e}")
    nlp = None

# Skills Database
SKILLS_DB = ["python", "java", "sql", "machine learning", "excel", "communication", "django", "c++", "html", "css", "data science", "react", "node.js", "javascript"]

# Gemini API Setup
GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY")
if GEMINI_API_KEY:
    genai.configure(api_key=GEMINI_API_KEY)
    model = genai.GenerativeModel("gemini-2.5-flash")
else:
    print("Warning: GEMINI_API_KEY is not set. Please check your .env file.")
    model = None

# Function for Gemini Feedback
def analyze_with_gemini(resume_text, job_description):
    if not model:
        return "Gemini model is not configured."
    
    prompt = f"""
    You are an expert resume reviewer. Analyze the following resume for its relevance to the given job description.
    
    Resume:
    {resume_text}

    Job Description:
    {job_description}

    Provide the following:
    1. Matching skills
    2. Level of confidence inferred from the text
    3. Suggestions for improvement
    4. Final score (between 1 and 10)
    
    Format the output cleanly.
    """
    try:
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        error_msg = str(e)
        print(f"Gemini API Error: {error_msg}")
        if "429" in error_msg or "quota" in error_msg.lower():
            return "Gemini API Quota Exceeded. Please try again later or check your Google AI Studio quota."
        return f"Error analyzing with Gemini: {error_msg}"

# Extract skills
def extract_skills(text):
    return list({skill for skill in SKILLS_DB if re.search(rf'\b{re.escape(skill)}\b', text.lower())})

# Sentiment (Confidence)
def analyze_sentiment(text):
    blob = TextBlob(text)
    return blob.sentiment.polarity

# Cosine similarity with TF-IDF
def compare_with_job_description(resume_text, job_desc_text):
    if not resume_text.strip() or not job_desc_text.strip():
        return 0.0
    vectorizer = TfidfVectorizer()
    try:
        tfidf_matrix = vectorizer.fit_transform([resume_text, job_desc_text])
        return cosine_similarity(tfidf_matrix[0], tfidf_matrix[1])[0][0]
    except Exception as e:
        print(f"TF-IDF Error: {e}")
        return 0.0

# AI Score combining factors
def ai_score(resume_text, job_desc_text):
    skills = extract_skills(resume_text)
    skills_score = len(skills) / len(SKILLS_DB) if len(SKILLS_DB) > 0 else 0
    sentiment_score = analyze_sentiment(resume_text)
    relevance_score = compare_with_job_description(resume_text, job_desc_text)
    final_score = (0.3 * skills_score) + (0.25 * sentiment_score) + (0.45 * relevance_score)
    return final_score, skills, sentiment_score, relevance_score

# Extract text from PDF, DOCX, or Image
def extract_text(file_path):
    ext = os.path.splitext(file_path)[1].lower()
    if ext == '.pdf':
        try:
            return extract_pdf_text(file_path)
        except Exception as e:
            print(f"PDF Extraction Error: {e}")
            return ""
    elif ext == '.docx':
        try:
             return docx2txt.process(file_path)
        except Exception as e:
            print(f"DOCX Extraction Error: {e}")
            return ""
    elif ext in ['.jpg', '.jpeg', '.png']:
        try:
            image = Image.open(file_path)
            # pytesseract.tesseract_cmd might need setup depending on OS
            return pytesseract.image_to_string(image)
        except Exception as e:
            print(f"Error processing image: {e}")
            return ""
    else:
        return ""

# --- Flask Routes ---

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/analyze', methods=['POST'])
def analyze_resume():
    if 'resume' not in request.files:
        return jsonify({"success": False, "error": "No file part"}), 400
    
    file = request.files['resume']
    job_desc_text = request.form.get('job_description', '')
    
    if file.filename == '':
        return jsonify({"success": False, "error": "No selected file"}), 400
        
    if not job_desc_text:
        return jsonify({"success": False, "error": "Job description is required"}), 400
        
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(file_path)
        
        try:
            # Process the file
            resume_text = extract_text(file_path)
            
            if not resume_text.strip():
                return jsonify({"success": False, "error": "Failed to extract text from the file or file is empty."}), 400
            
            score, skills, sentiment, relevance = ai_score(resume_text, job_desc_text)
            gemini_feedback = analyze_with_gemini(resume_text, job_desc_text)
            
            # Format scores for display (1-10 scale approximation)
            display_sentiment = ((sentiment + 1) / 2 * 9 + 1)
            display_relevance = ((relevance + 1) / 2 * 9 + 1)
            # Normalizing final score slightly higher for better aesthetics, or just scaling raw score
            display_score = min(max((score * 10) + 3, 1), 10) 
            
            result = {
                "success": True,
                "resume_name": filename,
                "score": round(display_score, 1),
                "skills": skills,
                "sentiment_score": round(display_sentiment, 1),
                "relevance_score": round(display_relevance, 1),
                "gemini_feedback": gemini_feedback
            }
            
            # Optionally delete the file after processing
            # os.remove(file_path)
            
            return jsonify(result)
            
        except Exception as e:
            return jsonify({"success": False, "error": str(e)}), 500
            
    return jsonify({"success": False, "error": "Invalid file type"}), 400

if __name__ == '__main__':
    app.run(debug=True, port=5000)

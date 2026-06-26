# 🛡️ SentinelAI – AI Cyber Fraud Detection Platform

An advanced, AI-powered Cyber Fraud Detection Platform designed to protect users by identifying phishing messages, malicious URLs, and suspicious imagery. By integrating Deep Learning, Optical Character Recognition (OCR), and state-of-the-art Generative AI, **SentinelAI** not only detects threats but also assesses risk and automatically generates official cybercrime complaints.

---

# 📌 Problem Statement

With the exponential surge in digital transactions and online communication, modern cyber fraud—ranging from deceptive phishing emails and scam SMS to fraudulent advertisements—has become highly sophisticated. Most everyday internet users struggle to recognize subtle social engineering patterns, resulting in massive financial losses and identity theft. **SentinelAI** bridges this gap by acting as an intelligent, accessible defensive layer that breaks down complex cyber threats into plain, actionable insights.

---

# 🚀 Core Features

## 📩 Multi-Channel Scam Detection

- **Text & Email Parsing:** Dynamically classifies phishing text and spam patterns using a fine-tuned BERT model.
- **Explainable Security:** Provides confidence scores, contextual threat explanations, and risk analysis instead of simple Safe/Scam predictions.

---

## 🌐 Intelligent URL Analysis

- Detects phishing, malicious, and fake URLs.
- Evaluates suspicious links before users access them.
- Generates AI-powered security recommendations and safety guidance.

---

## 🖼️ OCR-Driven Image Auditing

- Extracts text from screenshots, advertisements, and scam images using EasyOCR.
- Processes extracted text through the NLP pipeline for scam detection.
- Performs AI-based analysis on image content.

---

## 📄 Automated Cyber Crime Complaint Generator

- Generates formal cybercrime complaints from user-provided incident descriptions.
- Produces complaint drafts that are ready to submit to Cyber Crime Cells.

---

## 📊 Threat Intelligence Dashboard

- Responsive Streamlit-based user interface.
- Interactive visualizations using Plotly.
- Easy navigation between different cyber security modules.

---

# ⚙️ Technical Architecture

## System Workflow

```text
           User Input
   (SMS / Email / URL / Image)
               │
               ▼
        EasyOCR Text Extraction
          (Only for Images)
               │
               ▼
      BERT Scam Detection Model
               │
               ▼
   Prediction & Confidence Score
               │
               ▼
     Google Gemini AI Analysis
        ├───────────────┐
        ▼               ▼
 Threat Explanation   Risk Assessment
        │               │
        └──────┬────────┘
               ▼
 Cyber Crime Complaint Generator
```

---

# 🛠️ Technology Stack

| Domain | Technology | Purpose |
|----------|------------|---------|
| Frontend | Streamlit | Responsive Web Application |
| Programming Language | Python 3.10+ | Core Development |
| NLP Model | Hugging Face Transformers | Scam Classification |
| Deep Learning Model | BERT (mrm8488/bert-tiny-finetuned-sms-spam-detection) | SMS & Email Detection |
| Generative AI | Google Gemini 1.5 Flash | AI Explanations & Complaint Generation |
| OCR | EasyOCR | Text Extraction from Images |
| Image Processing | Pillow (PIL) | Image Handling |
| Data Processing | Pandas | Data Manipulation |
| Machine Learning Utilities | Scikit-Learn | Feature Processing |
| Visualization | Plotly | Interactive Charts |
| Environment Management | Python Dotenv | Secure API Key Management |

---

# 🤖 AI Models Utilized

## Spam Detection Model

**Model:** `mrm8488/bert-tiny-finetuned-sms-spam-detection`

**Purpose**
- SMS Scam Detection
- Email Spam Classification
- Confidence Score Prediction

---

## Google Gemini 1.5 Flash

**Purpose**
- Scam Explanation
- Threat Analysis
- Risk Assessment
- Safety Recommendations
- Cyber Crime Complaint Generation

---

## EasyOCR

**Purpose**
- OCR Text Extraction
- Screenshot Analysis
- Image Scam Detection

---

# 📂 Repository Architecture

```text
SentinelAI-Cyber-Fraud-Detection/
│
└── AI/
    ├── modules/
    │   ├── scam_classifier.py
    │   ├── gemini_explainer.py
    │   ├── ocr_reader.py
    │   └── url_checker.py
    │
    ├── assets/
    ├── appCyberFraud.py
    ├── requirements.txt
    ├── README.md
    └── .gitignore
```

---

# 🚀 Local Installation & Deployment

## 1. Clone the Repository

```bash
git clone https://github.com/Amisha-55/SentinelAI-Cyber-Fraud-Detection.git

cd SentinelAI-Cyber-Fraud-Detection/AI
```

---

## 2. Install Dependencies

It is recommended to create a virtual environment before installing the required packages.

```bash
pip install -r requirements.txt
```

---

## 3. Configure Environment Variables

Create a `.env` file inside the **AI** directory.

```env
GOOGLE_API_KEY=YOUR_GEMINI_API_KEY
```

---

## 4. Run the Application

```bash
streamlit run appCyberFraud.py
```

---

# 📦 Python Dependencies

- Streamlit
- Google Generative AI
- Hugging Face Transformers
- Torch
- EasyOCR
- Pillow
- Plotly
- Pandas
- Scikit-Learn
- Validators
- Python Dotenv

---

# 📈 Output

The platform provides:

- ✅ Scam/Ham Prediction
- ✅ Confidence Score
- ✅ AI-powered Threat Explanation
- ✅ Risk Level Assessment
- ✅ Suspicious Keyword Detection
- ✅ URL Security Analysis
- ✅ OCR Text Extraction
- ✅ Downloadable Cyber Crime Complaint

---

# 🔮 Future Scope

- Multi-language Scam Detection
- Voice Call Fraud Detection
- Browser Extension Integration
- WhatsApp & Telegram Scam Analysis
- QR Code Fraud Detection
- Live Threat Intelligence Database
- User Authentication & Complaint History
- Real-time AI Threat Monitoring

---

# 👩‍💻 Developed By

**Amisha Tripathy**

B.Tech – Artificial Intelligence & Machine Learning

---

# 📚 References

- Google AI Studio – https://ai.google.dev/
- Hugging Face – https://huggingface.co/
- Streamlit – https://streamlit.io/
- PyTorch – https://pytorch.org/
- Scikit-Learn – https://scikit-learn.org/
- Plotly – https://plotly.com/
- Pandas – https://pandas.pydata.org/
- EasyOCR – https://easyocr.readthedocs.io/
- Python – https://www.python.org/

---

# 🙏 Acknowledgements

This project demonstrates the practical application of Artificial Intelligence, Machine Learning, Optical Character Recognition, and Large Language Models in combating cyber fraud. SentinelAI combines modern AI technologies with an intuitive interface to improve cyber awareness and help users identify online threats effectively.

---

# 📜 License

This project is developed for **educational, research, and demonstration purposes**.

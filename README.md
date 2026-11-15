# 🛡️ PhishGuard – AI-Based Phishing Website and Email Detection System

PhishGuard is an AI-based phishing detection system designed to identify malicious URLs and phishing emails using Machine Learning and Natural Language Processing techniques. It also uses SHAP explainability to help users understand the factors influencing email detection results.

## 🌐 Live Demo

**Try PhishGuard here:**  
https://phishguard-ko3g.onrender.com/

## ✨ Key Features

- **URL Phishing Detection:** Identifies suspicious and legitimate URLs using a Random Forest classifier.
- **Email Phishing Detection:** Classifies email content using TF-IDF and Logistic Regression.
- **Explainable AI:** Uses SHAP to highlight important words and phrases influencing email predictions.
- **Risk Analysis:** Displays prediction results and associated risk levels.
- **User-Friendly Interface:** Simple and responsive web interface.
- **Light and Dark Themes:** Provides theme options for a better user experience.

## 🧠 Technologies Used

| Category | Technologies |
|---|---|
| Programming Language | Python |
| Machine Learning | Scikit-learn |
| URL Detection | Random Forest |
| Email Detection | Logistic Regression |
| Text Processing | TF-IDF |
| Explainable AI | SHAP |
| Web Framework | Flask |
| Data Processing | Pandas, NumPy |
| Frontend | HTML, CSS, JavaScript |
| Deployment | Render |
| Version Control | Git and GitHub |

## ⚙️ System Modules

### 1. URL Phishing Detection
The system extracts URL-based features and uses a trained Random Forest model to classify URLs as phishing or legitimate.

### 2. Email Phishing Detection
The email detection module uses TF-IDF vectorization and Logistic Regression to classify email content as phishing or legitimate.

### 3. SHAP Explainability
SHAP is integrated into the email detection module to identify words and phrases that influence the model's prediction.

### 4. Risk Analysis
The application displays prediction results, risk probabilities, and security recommendations to help users understand potential threats.

## 🔄 System Workflow

1. The user enters a URL or email content.
2. The system processes the submitted input.
3. The appropriate trained Machine Learning model performs classification.
4. The system generates a prediction and risk information.
5. For email detection, SHAP provides an explanation of influential words and phrases.
6. The results are displayed through the web interface.

## 🖥️ Installation and Execution

### Prerequisites
- Python 3.x
- Git
- Visual Studio Code (recommended)

### Steps to Run Locally

**1. Clone the repository**

```bash
git clone https://github.com/JesnaSemreen/PhishGuard.git
```

**2. Navigate to the project directory**

```bash
cd PhishGuard
```

**3. Create a virtual environment**

```bash
python -m venv phish_env
```

**4. Activate the virtual environment**

Windows:

```bash
phish_env\Scripts\activate
```

**5. Install the required dependencies**

```bash
pip install -r requirements.txt
```

**6. Run the application**

```bash
python app.py
```

**7. Open the application**

Visit:

```text
http://127.0.0.1:5000/
```

*Note: Ensure that the required trained model files and dependencies are available before running the application.*

## 📊 Machine Learning Models

| Module | Algorithm | Purpose |
|---|---|---|
| URL Detection | Random Forest | Detects phishing URLs |
| Email Detection | Logistic Regression | Classifies phishing emails |
| Email Explainability | SHAP | Explains influential words and phrases |

## 👥 Team Members

1. **JESNA SEMREEN** 
2. **FATHIMA FIDHA CM**
3. **LEKHA SHREE V**
4. **JISHNU DEV AS**

## 🎯 Project Objective

The main objective of PhishGuard is to develop an accessible AI-based solution that helps users identify potential phishing websites and emails, understand associated risks, and improve awareness of online security threats.

## 🚀 Future Enhancements

- Real-time phishing URL intelligence integration.
- Browser extension for instant URL checking.
- Improved detection of newly emerging phishing techniques.
- Enhanced email analysis and explainability.
- Support for additional languages.

## ⚠️ Disclaimer

PhishGuard is an educational project developed for phishing detection and awareness. Its predictions are based on trained machine learning models and should not be considered a guarantee that a website or email is safe.

## 📌 Repository

GitHub: https://github.com/JesnaSemreen/PhishGuard

---

**Developed as an academic mini-project by the PhishGuard team.**

# 📌 Table of Contents

- [🎯 Introduction](#-introduction)
- [🎥 Demo](#-demo)
- [💡 Inspiration](#-inspiration)
- [⚙️ What It Does](#-what-it-does)
- [🛠️ How We Built It](#-how-we-built-it)
- [🚧 Challenges We Faced](#-challenges-we-faced)
- [🏃 How to Run](#-how-to-run)
- [🏗️ Tech Stack](#-tech-stack)

---

## 🎯 Introduction

This is the **Proof of Concept (POC)** for the first Use Case for **AI-driven anomaly detection system** using **Streamlit**. We are maajorly considering GL Balance and IHUB Balance as well as detecting anomalies for account based on the pattern identified between the current data as well as historical data.

It is designed to process financial data, identify discrepancies, and provide intelligent insights using **machine learning models** and **LLMs**.

Users can upload their **historical financial records** and **current transaction data** to detect anomalies, understand the reasons behind them, and determine the next steps.

## 🎥 Demo

🔗 **Live Demo** (if applicable)  
📹 **Video Demo** (if applicable)  
🖼️ **Screenshots**:

- Screenshot 1 (Upload page)
- Screenshot 2 (Anomaly detection results)

## 💡 Inspiration

Financial anomalies can lead to **fraud, misreporting, and errors** in financial statements. **Manual reviews are time-consuming and prone to human error.** This POC aims to automate and enhance financial auditing processes using AI-powered anomaly detection.

## ⚙️ What It Does

- **Uploads** historical and test data.
- **Analyzes** financial records using multiple mathematical models.
- **Detects** anomalies and explains reasons using **LLM (Groq API)**.
- **Provides next steps** for handling anomalies.
- **Displays** results interactively on a **Streamlit dashboard**.
- **Allows users to download** anomaly detection reports in **CSV format**.

## 🛠️ How We Built It

- **Streamlit** - Interactive frontend for uploading and viewing results.
- **Python (Pandas, NumPy, SciPy)** - Data processing and statistical modeling.
- **LangChain + Groq API** - AI-powered anomaly reasoning.
- **dotenv** - Secure API key handling.
- **Git & GitHub** - Version control and collaboration.

## 🚧 Challenges We Faced

- **Optimizing anomaly detection models** for financial data.
- **Identiying the right LLM** efficiently in Streamlit.
- **Ensuring API communication** with the LLM for dynamic responses.
- **File uploads and format conversions** within the Streamlit app.

## 🏃 How to Run

### 1️⃣ Clone the repository

```bash
git clone https://github.com/your-repo/anomaly-detection-streamlit.git
cd anomaly-detection-streamlit
```

### 2️⃣ Install dependencies

```bash
pip install -r requirements.txt
```

### 3️⃣ Create a .env file in the root directory

```bash
GROQ_API_KEY=your_api_key_here
```

### 4️⃣ Run the project

```bash
streamlit run app.py
```

## 🏗️ Tech Stack

🔹 Frontend: Streamlit<br>
🔹 Model: LLama 3.3<br>
🔹 Other: LangChain, Groq API, SciPy, Pandas

## Testing instructions

### Run tests using pytest

```bash
pytest
```

# 🔥 AI Calorie Burnt Predictor

An AI-powered fitness analytics application that predicts the number of calories burnt during exercise using an **XGBoost Regression Model**.

The application provides a modern web interface built with **Gradio**, generates a professional PDF fitness report, and is deployed on **Hugging Face Spaces**.

---

## 🚀 Live Demo

👉 https://huggingface.co/spaces/WalterCodes/Calorie-burnt-predictor

---

# ✨ Features

- 🤖 Machine Learning based calorie prediction using XGBoost
- 🎨 Modern Fitness Dashboard UI built with Gradio
- 📊 Dynamic Fitness Analysis
- 📄 Professional AI-generated PDF Report
- 🆔 Auto-generated Report ID
- 📅 Indian Standard Time (IST) timestamp
- ⚖ Automatic BMI Calculation
- 🏋 Workout Intensity Classification
- ❤️ Heart Rate Analysis
- 🌡 Body Temperature Analysis
- ⭐ Overall Fitness Score
- 💡 Personalized Fitness Recommendations
- 📱 Responsive interface
- ☁ Hosted on Hugging Face Spaces

---

# 🖥 Application Preview

*(Add a screenshot of your application here)*

Example:

![Application Screenshot](images/app-preview.png)

---

# 📄 PDF Report Preview

*(Add a screenshot of the generated PDF here)*

Example:

![PDF Preview](images/report-preview.png)

---

# 🧠 Machine Learning Model

| Attribute | Details |
|-----------|---------|
| Model | XGBoost Regressor |
| Problem Type | Regression |
| Framework | Scikit-Learn + XGBoost |
| Target Variable | Calories Burnt |

---

# 📥 Input Parameters

| Parameter | Unit |
|-----------|------|
| Gender | Male / Female |
| Age | Years |
| Height | cm |
| Weight | kg |
| Exercise Duration | Minutes |
| Heart Rate | BPM |
| Body Temperature | °C |

---

# 📤 Output

The application predicts

- Estimated Calories Burnt
- Workout Intensity
- BMI
- BMI Category
- Heart Rate Status
- Temperature Status
- Duration Status
- Overall Fitness Score
- Personalized Recommendations

---

# 📄 PDF Report Includes

The downloadable report contains:

- Report ID
- Generation Date & Time (IST)
- Personal Information
- Workout Details
- Estimated Calories Burnt
- BMI Analysis
- Workout Intensity
- Fitness Analysis
- Fitness Score
- Personalized Recommendations
- Disclaimer

---

# 🛠 Tech Stack

| Technology | Purpose |
|------------|---------|
| Python | Core Programming Language |
| NumPy | Numerical Computation |
| Scikit-Learn | Data Processing |
| XGBoost | Machine Learning Model |
| Gradio | Interactive User Interface |
| FPDF | PDF Report Generation |
| Hugging Face Spaces | Deployment |

---

# 📦 Installation

```bash
git clone https://github.com/YOUR_USERNAME/calorie-burnt-predictor.git

cd calorie-burnt-predictor

pip install -r requirements.txt

python app.py
```

---

# 📂 Project Structure

```
.
├── app.py
├── calorie_model.pkl
├── requirements.txt
├── README.md
└── images
    ├── app-preview.png
    └── report-preview.png
```

---

# 👨‍💻 Developed By

**Satvik Mishra**

---

# 📜 License

This project is intended for educational and portfolio purposes.

---

# ⚠ Disclaimer

This application provides calorie estimates using a Machine Learning model and should not be considered medical advice.

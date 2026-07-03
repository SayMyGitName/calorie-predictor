import gradio as gr
import numpy as np
import pickle
from fpdf import FPDF
import datetime
import re

# Load model
model = pickle.load(open("calorie_model.pkl", "rb"))

# Helper: sanitize filename
def _safe_filename(s: str) -> str:
    s = s or "patient"
    s = re.sub(r"[^A-Za-z0-9_\-]", "_", s)
    return s[:100]

# Generate professional advice based on vitals
def generate_advice(age, bmi, heart_rate, body_temp, duration, prediction):
    advice_lines = []

    # General interpretation
    advice_lines.append(f"Estimated calories burned: {prediction:.2f} kcal over {duration} minute(s).")
    advice_lines.append("\nClinical considerations:")

    # BMI interpretation
    if bmi is not None:
        if bmi < 18.5:
            advice_lines.append(f"- BMI {bmi:.1f}: underweight. Consider nutritional evaluation and a tailored exercise program to gain healthy weight.")
        elif bmi < 25:
            advice_lines.append(f"- BMI {bmi:.1f}: normal range. Maintain a balanced diet and regular physical activity.")
        elif bmi < 30:
            advice_lines.append(f"- BMI {bmi:.1f}: overweight. Recommend gradual increase in aerobic activity, dietary counseling, and follow-up.")
        else:
            advice_lines.append(f"- BMI {bmi:.1f}: obesity. Advise comprehensive assessment and supervised weight-management program.")

    # Heart rate flags
    if heart_rate is not None:
        try:
            hr = float(heart_rate)
        except Exception:
            hr = None
        if hr is not None:
            if hr < 50:
                advice_lines.append(f"- Heart rate {hr} bpm: relatively low for exercise — ensure symptoms (dizziness, syncope) are absent and consider cardiology review if concerning.")
            elif hr > 180:
                advice_lines.append(f"- Heart rate {hr} bpm: very high for exercise — stop activity and seek immediate medical review.")
            elif hr > 100:
                advice_lines.append(f"- Heart rate {hr} bpm: elevated; monitor for symptoms and consider a clinical review if persistent.")
            else:
                advice_lines.append(f"- Heart rate {hr} bpm: within acceptable range for many exercise intensities, adjust based on fitness level.")

    # Body temperature
    if body_temp is not None:
        try:
            bt = float(body_temp)
        except Exception:
            bt = None
        if bt is not None:
            if bt >= 38.0:
                advice_lines.append(f"- Body temperature {bt} °C: fever-range temperature — defer strenuous exercise and seek medical advice.")
            elif bt < 35.0:
                advice_lines.append(f"- Body temperature {bt} °C: low temperature — ensure appropriate environment and consider medical assessment for hypothermia if symptomatic.")

    # Age-related notes
    try:
        age_val = float(age) if age is not None else None
    except Exception:
        age_val = None
    if age_val is not None and age_val >= 65:
        advice_lines.append("- Age-related considerations: tailor intensity, consider supervised or lower-impact exercise, and evaluate cardiovascular risk before high-intensity workouts.")

    # Practical recommendations
    advice_lines.append("\nRecommendations:")
    advice_lines.append("- Maintain adequate hydration before, during, and after exercise.")
    advice_lines.append("- Warm up and cool down for at least 5–10 minutes.")
    advice_lines.append("- If you experience chest pain, severe breathlessness, dizziness, or fainting, stop exercise and seek medical attention immediately.")
    advice_lines.append("- For personalized guidance, follow up with a licensed physician or an exercise physiologist.")

    return "\n".join(advice_lines)

# Prediction function
def predict_calories(patient_name, hospital_name, doctor_name, gender, age, height, weight, duration, heart_rate, body_temp, additional_notes):
    gender_encoded = 0 if (gender and str(gender).lower() == "male") else 1
    input_data = np.array([[gender_encoded, float(age or 0), float(height or 0), float(weight or 0), float(duration or 0), float(heart_rate or 0), float(body_temp or 0)]])
    prediction = float(model.predict(input_data)[0])

    # Derived metrics
    bmi = None
    try:
        h_m = float(height) / 100.0
        if h_m > 0:
            bmi = float(weight) / (h_m * h_m)
    except Exception:
        bmi = None

    # Generate advice text
    advice_text = generate_advice(age, bmi, heart_rate, body_temp, duration, prediction)

    # Generate PDF report
    pdf = FPDF()
    pdf.set_auto_page_break(auto=True, margin=15)
    pdf.add_page()

    # Header: Hospital name and title
    pdf.set_font("Arial", 'B', 16)
    if hospital_name:
        pdf.cell(0, 8, txt=str(hospital_name), ln=True, align='C')
    pdf.set_font("Arial", 'B', 12)
    pdf.cell(0, 8, txt="Clinical Exercise Report", ln=True, align='C')
    pdf.ln(4)

    # Meta
    pdf.set_font("Arial", size=10)
    pdf.cell(0, 6, txt=f"Report generated: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}", ln=True, align='R')
    pdf.ln(4)

    # Patient & clinician details
    pdf.set_font("Arial", 'B', 11)
    pdf.cell(0, 6, txt="Patient Details:", ln=True)
    pdf.set_font("Arial", size=10)
    pdf.cell(0, 6, txt=f"Name: {patient_name or '—'}", ln=True)
    pdf.cell(0, 6, txt=f"Age: {age or '—'}    Gender: {gender or '—'}", ln=True)
    pdf.cell(0, 6, txt=f"Height: {height or '—'} cm    Weight: {weight or '—'} kg    BMI: {bmi:.1f if bmi else '—'}", ln=True)
    pdf.ln(4)

    pdf.set_font("Arial", 'B', 11)
    pdf.cell(0, 6, txt="Clinician / Facility:", ln=True)
    pdf.set_font("Arial", size=10)
    pdf.cell(0, 6, txt=f"Doctor: {doctor_name or '—'}", ln=True)
    pdf.cell(0, 6, txt=f"Facility: {hospital_name or '—'}", ln=True)
    pdf.ln(6)

    # Recorded vitals
    pdf.set_font("Arial", 'B', 11)
    pdf.cell(0, 6, txt="Recorded Vitals and Exercise Data:", ln=True)
    pdf.set_font("Arial", size=10)
    pdf.cell(0, 6, txt=f"Duration: {duration or '—'} min    Heart Rate: {heart_rate or '—'} bpm    Body Temp: {body_temp or '—'} °C", ln=True)
    pdf.ln(6)

    # Brief summary
    pdf.set_font("Arial", 'B', 11)
    pdf.cell(0, 6, txt="Summary:", ln=True)
    pdf.set_font("Arial", size=10)
    summary_text = (
        f"This report estimates the energy expenditure (calories burned) during the recorded exercise session. "
        f"The estimate is model-based and depends on the provided vitals and session duration. "
    )
    pdf.multi_cell(0, 6, txt=summary_text)
    pdf.ln(2)

    # Prediction highlight
    pdf.set_font("Arial", 'B', 12)
    pdf.set_text_color(0, 70, 0)
    pdf.cell(0, 8, txt=f"Estimated Calories Burned: {prediction:.2f} kcal", ln=True)
    pdf.set_text_color(0, 0, 0)
    pdf.ln(4)

    # Additional notes
    if additional_notes:
        pdf.set_font("Arial", 'B', 11)
        pdf.cell(0, 6, txt="Notes / Patient Comments:", ln=True)
        pdf.set_font("Arial", size=10)
        pdf.multi_cell(0, 6, txt=str(additional_notes))
        pdf.ln(4)

    # Advice
    pdf.set_font("Arial", 'B', 11)
    pdf.cell(0, 6, txt="Clinical Advice:", ln=True)
    pdf.set_font("Arial", size=10)
    pdf.multi_cell(0, 6, txt=advice_text)
    pdf.ln(4)

    # Footer / signature area
    pdf.ln(10)
    pdf.set_font("Arial", size=10)
    pdf.cell(0, 6, txt=f"Reviewed by: {doctor_name or '—'}", ln=True)
    pdf.cell(0, 6, txt="Signature: ________________________", ln=True)

    # Save PDF
    safe_name = _safe_filename(patient_name)
    timestamp = datetime.datetime.now().strftime('%Y%m%d%H%M%S')
    filename = f"calorie_report_{safe_name}_{timestamp}.pdf"
    pdf.output(filename)

    # Return user-facing summary and file
    return f"🔥 Estimated calories burned: {prediction:.2f} kcal (detailed report generated)", filename


custom_css = """
body {
    background: linear-gradient(135deg, #a1c4fd, #c2e9fb);
    font-family: 'Segoe UI', sans-serif;
    color: #003366;
    text-align: center;
    margin: 0;
    padding: 0;
}

h1, h2 {
    color: #0d47a1;
}

.gr-button {
    background-color: #00bcd4 !important;
    color: white !important;
    font-weight: bold;
    border-radius: 10px;
    width: 200px;
    margin: auto;
}

.gr-input, .gr-box {
    border-radius: 10px;
}

.gr-row {
    justify-content: center;
}
"""

# Build interface
with gr.Blocks(css=custom_css) as demo:
    gr.Markdown("## 🔥 <center>Mishraji ka Calorie Burnt Predictor</center>")
    gr.Markdown("<center>Estimate your burnt calories based on your workout and vitals. A detailed clinical-style report can be generated for records.</center>")

    with gr.Row():
        patient_name = gr.Textbox(label="Patient Full Name", placeholder="e.g., John Doe")
        hospital_name = gr.Textbox(label="Hospital / Facility Name", placeholder="e.g., Central General Hospital")
        doctor_name = gr.Textbox(label="Doctor / Clinician Name", placeholder="e.g., Dr. A. Kumar")

    with gr.Row():
        gender = gr.Radio(["Male", "Female"], label="Gender")
        age = gr.Number(label="Age (years)")
        height = gr.Number(label="Height (cm)")
        weight = gr.Number(label="Weight (kg)")

    with gr.Row():
        duration = gr.Number(label="Exercise Duration (min)")
        heart_rate = gr.Number(label="Heart Rate (bpm)")
        body_temp = gr.Number(label="Body Temp (°C)")

    additional_notes = gr.Textbox(label="Additional notes / patient comments", lines=3)

    submit_btn = gr.Button("🔥 Predict and Generate Report")
    output = gr.Textbox(label="Result Summary", lines=2)
    download = gr.File(label="Download Report")

    submit_btn.click(fn=predict_calories,
                     inputs=[patient_name, hospital_name, doctor_name, gender, age, height, weight, duration, heart_rate, body_temp, additional_notes],
                     outputs=[output, download])

# Guarded launch so app can be imported without starting Gradio
if __name__ == "__main__":
    demo.launch(share=True)

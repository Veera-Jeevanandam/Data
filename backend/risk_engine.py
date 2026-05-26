from models import UserBiomarkers

def calculate_risk(data: UserBiomarkers) -> tuple[str, str, list, int]:
    """
    Calculates health risk based on biomarkers.
    Returns: (Risk Level, Risk Summary, Detailed Analysis List, Risk Score)
    """
    risk_score = 0
    reasons = []
    analysis = []

    # Helper to add analysis
    def add_analysis(name, value, unit, status, min_val, max_val):
        analysis.append({
            "name": name,
            "value": value,
            "unit": unit,
            "status": status,
            "min": min_val,
            "max": max_val
        })

    # BMI Risk
    bmi_status = "Normal"
    if data.bmi >= 30:
        risk_score += 2
        reasons.append("Obesity (BMI >= 30)")
        bmi_status = "High"
    elif data.bmi >= 25:
        risk_score += 1
        reasons.append("Overweight (BMI >= 25)")
        bmi_status = "Moderate"
    elif data.bmi < 18.5:
        risk_score += 2
        reasons.append("Underweight (BMI < 18.5)")
        bmi_status = "High"
    add_analysis("BMI", data.bmi, "", bmi_status, 15, 40)

    # Blood Pressure Risk
    bp_status = "Normal"
    if data.blood_pressure_systolic >= 140 or data.blood_pressure_diastolic >= 90:
        risk_score += 2
        reasons.append("High Blood Pressure (Hypertension)")
        bp_status = "High"
    elif data.blood_pressure_systolic >= 120 or data.blood_pressure_diastolic >= 80:
        risk_score += 1
        reasons.append("Elevated Blood Pressure")
        bp_status = "Moderate"
    elif data.blood_pressure_systolic <= 90 or data.blood_pressure_diastolic <= 60:
        risk_score += 2
        reasons.append("Low Blood Pressure (Hypotension)")
        bp_status = "High"
    add_analysis("Systolic BP", data.blood_pressure_systolic, "mmHg", bp_status, 90, 180)

    # Diabetes Risk (HbA1c)
    hba1c_status = "Normal"
    if data.hba1c >= 6.5:
        risk_score += 3
        reasons.append("Diabetes Indicators (High HbA1c)")
        hba1c_status = "High"
    elif data.hba1c >= 5.7:
        risk_score += 1
        reasons.append("Prediabetes Indicators")
        hba1c_status = "Moderate"
    elif data.hba1c < 4.0:
        risk_score += 2
        reasons.append("Abnormally Low HbA1c (Hypoglycemia risk)")
        hba1c_status = "High"
    add_analysis("HbA1c", data.hba1c, "%", hba1c_status, 4.0, 10.0)

    # Fasting Glucose 
    glucose_status = "Normal"
    if data.glucose_fasting >= 126:
        risk_score += 3
        reasons.append("High Fasting Glucose (Diabetes Indicator)")
        glucose_status = "High"
    elif data.glucose_fasting >= 100:
        risk_score += 1
        reasons.append("Elevated Fasting Glucose (Prediabetes)")
        glucose_status = "Moderate"
    elif data.glucose_fasting < 70:
        risk_score += 2
        reasons.append("Low Fasting Glucose (Hypoglycemia)")
        glucose_status = "High"
    add_analysis("Fasting Glucose", data.glucose_fasting, "mg/dL", glucose_status, 50, 200)


    # Cholesterol Risk
    chol_status = "Normal"
    if data.cholesterol_total >= 240:
        risk_score += 2
        reasons.append("High Total Cholesterol")
        chol_status = "High"
    elif data.cholesterol_total >= 200:
        risk_score += 1
        reasons.append("Borderline High Total Cholesterol")
        chol_status = "Moderate"
    add_analysis("Total Cholesterol", data.cholesterol_total, "mg/dL", chol_status, 100, 300)

    # LDL Risk
    ldl_status = "Normal"
    if data.cholesterol_ldl >= 160:
        risk_score += 2
        reasons.append("High LDL Cholesterol")
        ldl_status = "High"
    elif data.cholesterol_ldl >= 130:
        risk_score += 1
        reasons.append("Borderline High LDL Cholesterol")
        ldl_status = "Moderate"
    add_analysis("LDL Cholesterol", data.cholesterol_ldl, "mg/dL", ldl_status, 50, 200)

    # Triglycerides Risk
    tri_status = "Normal"
    if data.triglycerides >= 200:
        risk_score += 2
        reasons.append("High Triglycerides")
        tri_status = "High"
    elif data.triglycerides >= 150:
        risk_score += 1
        reasons.append("Borderline High Triglycerides")
        tri_status = "Moderate"
    add_analysis("Triglycerides", data.triglycerides, "mg/dL", tri_status, 50, 300)

    # Determine Level
    if risk_score >= 4:
        level = "High"
    elif risk_score >= 2:
        level = "Moderate"
    else:
        level = "Low"

    summary = f"Identified risk factors: {', '.join(reasons)}." if reasons else "No significant risk factors identified based on provided data."
    
    return level, summary, analysis, risk_score

import React, { useState } from 'react';

const BiomarkerForm = ({ onSubmit, isLoading }) => {
  const [formData, setFormData] = useState({
    age: '',
    gender: 'Male',
    weight: '',
    bmi: '',
    blood_pressure_systolic: '',
    blood_pressure_diastolic: '',
    cholesterol_total: '',
    cholesterol_hdl: '',
    cholesterol_ldl: '',
    triglycerides: '',
    hba1c: '',
    glucose_fasting: '',
    activity_level: 'Moderate',
    sleep_hours: ''
  });

  const handleChange = (e) => {
    setFormData({ ...formData, [e.target.name]: e.target.value });
  };

  const handleSubmit = (e) => {
    e.preventDefault();
    // Convert types
    const processedData = {
      ...formData,
      age: parseInt(formData.age),
      weight: parseFloat(formData.weight),
      bmi: parseFloat(formData.bmi),
      blood_pressure_systolic: parseInt(formData.blood_pressure_systolic),
      blood_pressure_diastolic: parseInt(formData.blood_pressure_diastolic),
      cholesterol_total: parseInt(formData.cholesterol_total),
      cholesterol_hdl: parseInt(formData.cholesterol_hdl),
      cholesterol_ldl: parseInt(formData.cholesterol_ldl),
      triglycerides: parseInt(formData.triglycerides),
      hba1c: parseFloat(formData.hba1c),
      glucose_fasting: parseInt(formData.glucose_fasting),
      sleep_hours: parseFloat(formData.sleep_hours)
    };
    onSubmit(processedData);
  };

  return (
    <form onSubmit={handleSubmit}>
      <div className="form-grid">
        <div className="form-group">
          <label>Age</label>
          <input type="number" name="age" value={formData.age} onChange={handleChange} required placeholder="e.g. 30" />
        </div>
        <div className="form-group">
          <label>Gender</label>
          <select name="gender" value={formData.gender} onChange={handleChange}>
            <option>Male</option>
            <option>Female</option>
            <option>Other</option>
          </select>
        </div>
        <div className="form-group">
          <label>Weight (kg)</label>
          <input type="number" step="0.1" name="weight" value={formData.weight} onChange={handleChange} required placeholder="e.g. 75.5" />
        </div>
        <div className="form-group">
          <label>BMI</label>
          <input type="number" step="0.1" name="bmi" value={formData.bmi} onChange={handleChange} required placeholder="e.g. 24.5" />
        </div>
        <div className="form-group">
          <label>Activity Level</label>
          <select name="activity_level" value={formData.activity_level} onChange={handleChange}>
            <option>Sedentary</option>
            <option>Light</option>
            <option>Moderate</option>
            <option>Active</option>
          </select>
        </div>
        <div className="form-group">
          <label>Systolic BP (mmHg)</label>
          <input type="number" name="blood_pressure_systolic" value={formData.blood_pressure_systolic} onChange={handleChange} required placeholder="e.g. 120" />
        </div>
        <div className="form-group">
          <label>Diastolic BP (mmHg)</label>
          <input type="number" name="blood_pressure_diastolic" value={formData.blood_pressure_diastolic} onChange={handleChange} required placeholder="e.g. 80" />
        </div>
        <div className="form-group">
          <label>Total Cholesterol (mg/dL)</label>
          <input type="number" name="cholesterol_total" value={formData.cholesterol_total} onChange={handleChange} required placeholder="e.g. 200" />
        </div>
        <div className="form-group">
          <label>HDL Cholesterol (mg/dL)</label>
          <input type="number" name="cholesterol_hdl" value={formData.cholesterol_hdl} onChange={handleChange} required placeholder="e.g. 50" />
        </div>
        <div className="form-group">
          <label>LDL Cholesterol (mg/dL)</label>
          <input type="number" name="cholesterol_ldl" value={formData.cholesterol_ldl} onChange={handleChange} required placeholder="e.g. 100" />
        </div>
        <div className="form-group">
          <label>Triglycerides (mg/dL)</label>
          <input type="number" name="triglycerides" value={formData.triglycerides} onChange={handleChange} required placeholder="e.g. 150" />
        </div>
        <div className="form-group">
          <label>HbA1c (%)</label>
          <input type="number" step="0.1" name="hba1c" value={formData.hba1c} onChange={handleChange} required placeholder="e.g. 5.7" />
        </div>
        <div className="form-group">
          <label>Fasting Glucose (mg/dL)</label>
          <input type="number" name="glucose_fasting" value={formData.glucose_fasting} onChange={handleChange} required placeholder="e.g. 90" />
        </div>
        <div className="form-group">
          <label>Sleep Hours</label>
          <input type="number" step="0.5" name="sleep_hours" value={formData.sleep_hours} onChange={handleChange} required placeholder="e.g. 7.5" />
        </div>
      </div>
      <button type="submit" disabled={isLoading} className="btn-primary">
        {isLoading ? 'Analyzing Health Profile...' : 'Generate Recommendations'}
      </button>
    </form>
  );
};

export default BiomarkerForm;

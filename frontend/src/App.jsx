import React, { useState } from 'react';
import BiomarkerForm from './components/BiomarkerForm';
import ResultDisplay from './components/ResultDisplay';

function App() {
  const [results, setResults] = useState(null);
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState(null);

  const handleFormSubmit = async (data) => {
    setIsLoading(true);
    setError(null);
    try {
      const response = await fetch('http://localhost:8000/recommend', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(data),
      });

      if (!response.ok) {
        throw new Error('Failed to fetch recommendations');
      }

      const resultData = await response.json();
      resultData.id = Date.now();
      setResults(resultData);
    } catch (err) {
      setError(err.message);
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="container">
      <header style={{ marginBottom: '3rem', textAlign: 'center' }}>
        <h1>AI Health Assistant</h1>
        <p className="subtitle">Personalized fitness and diet recommendations based on your biomarkers</p>
      </header>

      <div className="card">
        <BiomarkerForm onSubmit={handleFormSubmit} isLoading={isLoading} />

        {error && (
          <div style={{
            backgroundColor: 'var(--error-bg)',
            color: 'var(--error-text)',
            padding: '1rem',
            borderRadius: 'var(--radius-md)',
            marginTop: '1.5rem',
            textAlign: 'center',
            fontWeight: '500'
          }}>
            {error}
          </div>
        )}
      </div>

      <ResultDisplay results={results} />

      <footer style={{ marginTop: '4rem', textAlign: 'center', color: 'var(--text-muted)', fontSize: '0.9rem' }}>
        <p>© {new Date().getFullYear()} AI Health Assistant. Not medical advice.</p>
      </footer>
    </div>
  );
}

export default App;

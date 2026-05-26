import React from 'react';
import ReactMarkdown from 'react-markdown';
import BiomarkerAnalysis from './BiomarkerAnalysis';
import FeedbackForm from './FeedbackForm';

const ResultDisplay = ({ results }) => {
    if (!results) return null;

    return (
        <div className="result-section">
            <div className="risk-card">
                <h2 style={{ marginBottom: '1.5rem' }}>Health Risk Assessment</h2>
                <span className={`risk-badge risk-${results.risk_level}`}>
                    Risk Level: {results.risk_level}
                </span>
                <p style={{ marginTop: '1.5rem', fontSize: '1.1rem', maxWidth: '600px', margin: '1.5rem auto 0' }}>
                    {results.risk_summary}
                </p>

                {/* Risk Score Bar */}
                <div style={{ marginTop: '2rem', maxWidth: '400px', margin: '2rem auto 0' }}>
                    <div style={{ display: 'flex', justifyContent: 'space-between', marginBottom: '0.5rem', fontSize: '0.9rem', fontWeight: '600' }}>
                        <span>Risk Score</span>
                        <span>{results.risk_score} / 10</span>
                    </div>
                    <div style={{ height: '16px', background: '#e2e8f0', borderRadius: '8px', overflow: 'hidden' }}>
                        <div
                            style={{
                                width: `${Math.min((results.risk_score / 10) * 100, 100)}%`,
                                height: '100%',
                                background: results.risk_level === 'High' ? '#ef4444' : results.risk_level === 'Moderate' ? '#f59e0b' : '#10b981',
                                transition: 'width 1s ease-out'
                            }}
                        ></div>
                    </div>
                </div>
            </div>

            <BiomarkerAnalysis analysis={results.biomarker_analysis} />

            <div className="recommendation-grid">
                <div className="rec-card">
                    <h3>Exercise Plan</h3>
                    <div className="markdown-content">
                        <ReactMarkdown>{results.fitness_recommendations}</ReactMarkdown>
                    </div>
                </div>

                <div className="rec-card">
                    <h3>Dietary Plan</h3>
                    <div className="markdown-content">
                        <ReactMarkdown>{results.diet_recommendations}</ReactMarkdown>
                    </div>
                </div>

                <div className="rec-card">
                    <h3>Activity & Lifestyle</h3>
                    <div className="markdown-content">
                        <ReactMarkdown>{results.lifestyle_recommendations}</ReactMarkdown>
                    </div>
                </div>
            </div>

            <div className="disclaimer">
                <strong>Disclaimer:</strong> {results.disclaimer}
            </div>

            <hr style={{ border: 'none', borderTop: '1px solid #e2e8f0', margin: '3rem 0' }} />
            <FeedbackForm key={results.id} />
        </div>
    );
};

export default ResultDisplay;

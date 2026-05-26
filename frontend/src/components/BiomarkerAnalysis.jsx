import React from 'react';

const BiomarkerAnalysis = ({ analysis }) => {
    if (!analysis || analysis.length === 0) return null;

    return (
        <div className="card" style={{ marginTop: '2rem' }}>
            <h2 style={{ marginBottom: '1.5rem', textAlign: 'center' }}>Biomarker Analysis</h2>
            <div className="biomarker-grid">
                {analysis.map((item, index) => (
                    <div key={index} className="biomarker-item">
                        <div className="biomarker-header">
                            <span className="biomarker-name">{item.name}</span>
                            <span className={`biomarker-value status-${item.status}`}>
                                {item.value} {item.unit}
                            </span>
                        </div>

                        <div className="gauge-container">
                            {/* Background Bar */}
                            <div className="gauge-bar">
                                <div className="gauge-zone zone-green"></div>
                                <div className="gauge-zone zone-yellow"></div>
                                <div className="gauge-zone zone-red"></div>
                            </div>

                            {/* Marker */}
                            <div
                                className="gauge-marker"
                                style={{
                                    left: `${Math.min(Math.max(((item.value - item.min) / (item.max - item.min)) * 100, 0), 100)}%`
                                }}
                            ></div>
                        </div>

                        <div className="gauge-labels">
                            <span>{item.min}</span>
                            <span className="status-label">{item.status}</span>
                            <span>{item.max}</span>
                        </div>
                    </div>
                ))}
            </div>
        </div>
    );
};

export default BiomarkerAnalysis;

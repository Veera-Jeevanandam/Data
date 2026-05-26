import React, { useState } from 'react';

const FeedbackForm = () => {
    const [rating, setRating] = useState(0);
    const [hover, setHover] = useState(0);
    const [comments, setComments] = useState('');
    const [isHelpful, setIsHelpful] = useState(null);
    const [submitted, setSubmitted] = useState(false);
    const [error, setError] = useState('');
    const [submitting, setSubmitting] = useState(false);

    const handleSubmit = async (e) => {
        e.preventDefault();
        if (rating === 0 || isHelpful === null) {
            setError('Please provide a rating and let us know if it was helpful.');
            return;
        }

        setError('');
        setSubmitting(true);

        const payload = {
            rating,
            is_helpful: isHelpful,
            comments,
            timestamp: new Date().toISOString()
        };

        try {
            const response = await fetch('http://127.0.0.1:8000/feedback', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify(payload),
            });

            if (response.ok) {
                setSubmitted(true);
            } else {
                setError('Failed to submit feedback. Please try again later.');
            }
        } catch (err) {
            setError('Network error. Please try again later.');
        } finally {
            setSubmitting(false);
        }
    };

    if (submitted) {
        return (
            <div className="feedback-form success-state">
                <div className="success-icon">✓</div>
                <h3>Thanks for your feedback!</h3>
                <p>We appreciate your input to help improve our AI recommendations.</p>
                <button className="btn reset-btn" onClick={() => {
                    setSubmitted(false);
                    setRating(0);
                    setComments('');
                    setIsHelpful(null);
                }}>Submit another</button>
            </div>
        );
    }

    return (
        <div className="feedback-form">
            <h3>How was your experience?</h3>
            <p>Your feedback helps us train a better AI for you.</p>

            <form onSubmit={handleSubmit}>
                <div className="form-group">
                    <label>Rate your recommendations</label>
                    <div className="star-rating">
                        {[...Array(5)].map((star, index) => {
                            index += 1;
                            return (
                                <button
                                    type="button"
                                    key={index}
                                    className={index <= (hover || rating) ? "on" : "off"}
                                    onClick={() => setRating(index)}
                                    onMouseEnter={() => setHover(index)}
                                    onMouseLeave={() => setHover(rating)}
                                >
                                    <span className="star">&#9733;</span>
                                </button>
                            );
                        })}
                    </div>
                </div>

                <div className="form-group">
                    <label>Was this helpful?</label>
                    <div className="helpful-buttons">
                        <button 
                            type="button" 
                            className={`btn-toggle ${isHelpful === true ? 'active' : ''}`}
                            onClick={() => setIsHelpful(true)}>
                            Yes, helpful
                        </button>
                        <button 
                            type="button" 
                            className={`btn-toggle ${isHelpful === false ? 'active' : ''}`}
                            onClick={() => setIsHelpful(false)}>
                            No, not quite
                        </button>
                    </div>
                </div>

                <div className="form-group">
                    <label>Any additional comments?</label>
                    <textarea 
                        rows="4"
                        placeholder="Tell us what you liked or what could be improved..."
                        value={comments}
                        onChange={(e) => setComments(e.target.value)}
                    ></textarea>
                </div>

                {error && <div className="error-message">{error}</div>}

                <button 
                    type="submit" 
                    className="btn submit-btn"
                    disabled={submitting}>
                    {submitting ? 'Submitting...' : 'Submit Feedback'}
                </button>
            </form>
        </div>
    );
};

export default FeedbackForm;

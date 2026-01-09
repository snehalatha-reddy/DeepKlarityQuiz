import React, { useState } from 'react';
import { generateQuiz } from '../api';
import { Loader2 } from 'lucide-react';
import QuizResult from './QuizResult';

const QuizView = () => {
    const [url, setUrl] = useState('');
    const [loading, setLoading] = useState(false);
    const [data, setData] = useState(null);
    const [error, setError] = useState(null);

    const handleGenerate = async () => {
        if (!url) return;
        setLoading(true);
        setError(null);
        setData(null);

        try {
            const result = await generateQuiz(url);
            setData(result);
        } catch (err) {
            setError(err.response?.data?.detail || "Failed to generate quiz. Make sure the backend is running and the URL is valid.");
        } finally {
            setLoading(false);
        }
    };

    return (
        <div style={{ maxWidth: '800px', margin: '0 auto' }}>
            {/* Input Section */}
            <div className="card flex-row" style={{ padding: '16px' }}>
                <input
                    type="text"
                    placeholder="Paste Wikipedia URL (e.g., https://en.wikipedia.org/wiki/Alan_Turing)"
                    className="input-field"
                    value={url}
                    onChange={(e) => setUrl(e.target.value)}
                    onKeyDown={(e) => e.key === 'Enter' && handleGenerate()}
                />
                <button
                    onClick={handleGenerate}
                    disabled={loading}
                    className="btn btn-primary"
                    style={{ whiteSpace: 'nowrap' }}
                >
                    {loading ? <Loader2 className="animate-spin" size={20} /> : "Generate Quiz"}
                </button>
            </div>

            {error && (
                <div style={{ background: '#fef2f2', border: '1px solid #fee2e2', color: '#b91c1c', padding: '16px', borderRadius: '12px', marginBottom: '24px', display: 'flex', alignItems: 'center', gap: '12px' }}>
                    <div style={{ width: 6, height: 6, background: '#ef4444', borderRadius: '50%' }}></div>
                    {error}
                </div>
            )}

            {/* Content Section */}
            {data && <QuizResult data={data} />}
        </div>
    );
};

export default QuizView;

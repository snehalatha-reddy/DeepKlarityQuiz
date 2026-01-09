import React, { useState } from 'react';
import { ExternalLink, CheckCircle, XCircle } from 'lucide-react';
import { motion } from 'framer-motion';

const QuizResult = ({ data }) => {
    const [selectedAnswers, setSelectedAnswers] = useState({}); // { questionIndex: optionIndex }
    const [showResults, setShowResults] = useState({}); // { questionIndex: boolean }

    const handleOptionSelect = (qIndex, opt) => {
        if (showResults[qIndex]) return;
        setSelectedAnswers(prev => ({ ...prev, [qIndex]: opt }));
        setShowResults(prev => ({ ...prev, [qIndex]: true }));
    };

    if (!data) return null;

    return (
        <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            className="grid-col"
        >
            {/* Header Card */}
            <div className="card">
                <div className="flex-between" style={{ marginBottom: '20px', alignItems: 'flex-start' }}>
                    <h1 style={{ fontSize: '2rem', fontWeight: '800', letterSpacing: '-0.03em', lineHeight: 1.2 }}>{data.title}</h1>
                    <a href={data.url} target="_blank" rel="noopener noreferrer" className="btn" style={{ color: 'var(--primary-color)', background: '#eff6ff', padding: '8px 16px', fontSize: '0.9rem' }}>
                        View Article <ExternalLink size={16} />
                    </a>
                </div>
                <p style={{ color: 'var(--text-secondary)', lineHeight: '1.7', marginBottom: '24px', fontSize: '1.1rem' }}>{data.summary}</p>

                {/* Entities */}
                <div style={{ display: 'flex', flexWrap: 'wrap', gap: '8px' }}>
                    {Object.entries(data.key_entities || {}).map(([type, items]) => (
                        items.map((item, i) => (
                            <span key={type + i} className="badge" style={{ background: '#f1f5f9', color: '#475569', border: '1px solid #e2e8f0', textTransform: 'capitalize' }}>
                                {item} <span style={{ opacity: 0.5, marginLeft: 4 }}>({type})</span>
                            </span>
                        ))
                    ))}
                </div>
            </div>

            {/* Quiz Cards */}
            <div>
                <h2 style={{ fontSize: '1.5rem', fontWeight: '700', marginBottom: '24px', color: 'var(--text-primary)' }}>Quiz Questions</h2>
                <div className="grid-col">
                    {data.quiz.map((q, idx) => {
                        const isAnswered = showResults[idx];

                        return (
                            <motion.div
                                key={idx}
                                initial={{ opacity: 0 }}
                                animate={{ opacity: 1 }}
                                transition={{ delay: idx * 0.1 }}
                                className="card"
                                style={{ marginBottom: 0, padding: '32px' }}
                            >
                                <div className="flex-between" style={{ marginBottom: '24px' }}>
                                    <h3 style={{ fontSize: '1.15rem', fontWeight: '600', paddingRight: '16px', lineHeight: 1.5 }}>
                                        <span style={{ color: 'var(--text-secondary)', marginRight: '8px' }}>{idx + 1}.</span>
                                        {q.question}
                                    </h3>
                                    <span className="badge" style={{
                                        background: q.difficulty === 'easy' ? '#f0fdf4' : q.difficulty === 'medium' ? '#fefce8' : '#fef2f2',
                                        color: q.difficulty === 'easy' ? '#166534' : q.difficulty === 'medium' ? '#854d0e' : '#991b1b',
                                        border: '1px solid transparent'
                                    }}>
                                        {q.difficulty}
                                    </span>
                                </div>

                                <div className="grid-col" style={{ gap: '12px' }}>
                                    {q.options.map((opt, optIdx) => {
                                        let className = "quiz-option";

                                        if (isAnswered) {
                                            if (opt === q.answer) className += " correct";
                                            else if (selectedAnswers[idx] === opt) className += " incorrect";
                                            else className += " disabled";
                                        }

                                        return (
                                            <button
                                                key={optIdx}
                                                onClick={() => handleOptionSelect(idx, opt)}
                                                disabled={isAnswered}
                                                className={className}
                                            >
                                                <span style={{ display: 'flex', gap: '12px', alignItems: 'center' }}>
                                                    <span style={{
                                                        fontWeight: '600',
                                                        color: isAnswered ? 'inherit' : 'var(--text-secondary)',
                                                        width: '24px',
                                                        height: '24px',
                                                        borderRadius: '50%',
                                                        background: isAnswered ? 'transparent' : '#f1f5f9',
                                                        display: 'flex',
                                                        alignItems: 'center',
                                                        justifyContent: 'center',
                                                        fontSize: '0.8rem'
                                                    }}>
                                                        {String.fromCharCode(65 + optIdx)}
                                                    </span>
                                                    {opt}
                                                </span>
                                                {isAnswered && opt === q.answer && <CheckCircle size={20} color="#16a34a" />}
                                                {isAnswered && selectedAnswers[idx] === opt && opt !== q.answer && <XCircle size={20} color="#dc2626" />}
                                            </button>
                                        );
                                    })}
                                </div>

                                {isAnswered && (
                                    <motion.div
                                        initial={{ opacity: 0, height: 0 }}
                                        animate={{ opacity: 1, height: 'auto' }}
                                        className="explanation-box"
                                    >
                                        <div style={{ display: 'flex', gap: '8px', alignItems: 'center', marginBottom: '8px', color: 'var(--primary-color)', fontWeight: '600', fontSize: '0.9rem' }}>
                                            <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2"><circle cx="12" cy="12" r="10"></circle><line x1="12" y1="16" x2="12" y2="12"></line><line x1="12" y1="8" x2="12.01" y2="8"></line></svg>
                                            Explanation
                                        </div>
                                        <p style={{ color: 'var(--text-secondary)', lineHeight: 1.6 }}>{q.explanation}</p>
                                    </motion.div>
                                )}
                            </motion.div>
                        );
                    })}
                </div>
            </div>

            {/* Related Topics */}
            {data.related_topics && data.related_topics.length > 0 && (
                <div className="card">
                    <h3 style={{ fontSize: '1.1rem', fontWeight: '600', marginBottom: '16px', color: 'var(--text-secondary)', textTransform: 'uppercase', letterSpacing: '0.05em' }}>Explore More Topics</h3>
                    <div style={{ display: 'flex', flexWrap: 'wrap', gap: '10px' }}>
                        {data.related_topics.map((topic, i) => (
                            <span key={i} style={{
                                padding: '8px 16px',
                                background: 'white',
                                color: 'var(--primary-color)',
                                border: '1px solid var(--border-color)',
                                borderRadius: '8px',
                                cursor: 'pointer',
                                fontSize: '0.9rem',
                                fontWeight: '500',
                                boxShadow: '0 1px 2px rgba(0,0,0,0.05)',
                                transition: 'all 0.2s'
                            }}
                                onMouseOver={(e) => { e.currentTarget.style.borderColor = 'var(--primary-color)'; e.currentTarget.style.transform = 'translateY(-1px)'; }}
                                onMouseOut={(e) => { e.currentTarget.style.borderColor = 'var(--border-color)'; e.currentTarget.style.transform = 'translateY(0)'; }}
                            >
                                {topic}
                            </span>
                        ))}
                    </div>
                </div>
            )}
        </motion.div>
    );
};

export default QuizResult;

import React, { useEffect, useState } from 'react';
import { getHistory, getQuizDetails } from '../api';
import { Eye, Clock, Loader2, X } from 'lucide-react';
import { motion, AnimatePresence } from 'framer-motion';
import QuizResult from './QuizResult';

const HistoryView = () => {
    const [history, setHistory] = useState([]);
    const [loading, setLoading] = useState(true);
    const [selectedQuiz, setSelectedQuiz] = useState(null);
    const [loadingDetails, setLoadingDetails] = useState(false);

    useEffect(() => {
        loadHistory();
    }, []);

    const loadHistory = async () => {
        try {
            const data = await getHistory();
            setHistory(data);
        } catch (e) {
            console.error(e);
        } finally {
            setLoading(false);
        }
    };

    const handleViewDetails = async (id) => {
        setLoadingDetails(true);
        try {
            const data = await getQuizDetails(id);
            setSelectedQuiz(data);
        } catch (e) {
            console.error(e);
        } finally {
            setLoadingDetails(false);
        }
    };

    return (
        <div style={{ maxWidth: '1000px', margin: '0 auto' }}>
            <h2 style={{ fontSize: '1.8rem', fontWeight: 'bold', marginBottom: '24px' }}>Past Quizzes</h2>

            {loading ? (
                <div style={{ display: 'flex', justifyContent: 'center', padding: '40px' }}><Loader2 className="animate-spin" size={40} color="#3b82f6" /></div>
            ) : (
                <div className="table-container">
                    <table>
                        <thead>
                            <tr>
                                <th>Title</th>
                                <th>URL</th>
                                <th>Date Generated</th>
                                <th style={{ textAlign: 'right' }}>Actions</th>
                            </tr>
                        </thead>
                        <tbody>
                            {history.length === 0 ? (
                                <tr>
                                    <td colSpan={4} style={{ textAlign: 'center', padding: '32px', color: 'var(--text-secondary)' }}>No history found. Generate a quiz first!</td>
                                </tr>
                            ) : (
                                history.map((item) => (
                                    <tr key={item.id}>
                                        <td style={{ fontWeight: '500' }}>{item.title}</td>
                                        <td style={{ maxWidth: '300px', whiteSpace: 'nowrap', overflow: 'hidden', textOverflow: 'ellipsis' }}>
                                            <a href={item.url} target="_blank" rel="noopener noreferrer" style={{ color: '#60a5fa', textDecoration: 'none' }}>{item.url}</a>
                                        </td>
                                        <td style={{ fontSize: '0.9rem', color: 'var(--text-secondary)' }}>
                                            <div style={{ display: 'flex', alignItems: 'center', gap: '8px' }}>
                                                <Clock size={14} />
                                                {item.created_at ? new Date(item.created_at).toLocaleDateString() : 'N/A'}
                                            </div>
                                        </td>
                                        <td style={{ textAlign: 'right' }}>
                                            <button
                                                onClick={() => handleViewDetails(item.id)}
                                                className="btn"
                                                style={{ padding: '8px 16px', background: '#334155', color: '#e2e8f0', fontSize: '0.9rem' }}
                                            >
                                                <Eye size={16} /> Details
                                            </button>
                                        </td>
                                    </tr>
                                ))
                            )}
                        </tbody>
                    </table>
                </div>
            )}

            {/* Modal */}
            <AnimatePresence>
                {selectedQuiz && (
                    <div className="modal-overlay" onClick={() => setSelectedQuiz(null)}>
                        <motion.div
                            initial={{ opacity: 0, scale: 0.95 }}
                            animate={{ opacity: 1, scale: 1 }}
                            exit={{ opacity: 0, scale: 0.95 }}
                            className="modal-content"
                            onClick={(e) => e.stopPropagation()}
                        >
                            <button
                                onClick={() => setSelectedQuiz(null)}
                                className="close-btn"
                            >
                                <X size={20} />
                            </button>
                            <div style={{ padding: '32px' }}>
                                <QuizResult data={selectedQuiz} />
                            </div>
                        </motion.div>
                    </div>
                )}
            </AnimatePresence>

            {/* Loading Modal Overlay */}
            {loadingDetails && (
                <div className="modal-overlay" style={{ background: 'rgba(0,0,0,0.5)' }}>
                    <Loader2 className="animate-spin" size={48} color="white" />
                </div>
            )}
        </div>
    );
};

export default HistoryView;

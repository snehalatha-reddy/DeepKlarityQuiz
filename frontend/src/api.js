import axios from 'axios';

const API_URL = import.meta.env.VITE_API_URL || 'http://127.0.0.1:8000';

export const generateQuiz = async (url) => {
    console.log("DEBUG: Using API URL:", API_URL);
    console.log("DEBUG: Posting to:", `${API_URL}/generate_quiz`);
    const response = await axios.post(`${API_URL}/generate_quiz`, { url });
    return response.data;
};

export const getHistory = async () => {
    const response = await axios.get(`${API_URL}/history`);
    return response.data;
};

export const getQuizDetails = async (id) => {
    const response = await axios.get(`${API_URL}/quiz/${id}`);
    return response.data;
};

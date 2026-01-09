import React, { useState } from 'react';
import QuizView from './components/QuizView';
import HistoryView from './components/HistoryView';
import { Sparkles, History } from 'lucide-react';
import './App.css';

import logo from './assets/logo.jpg';

function App() {
  const [activeTab, setActiveTab] = useState('generate');

  return (
    <div className="min-h-screen">
      {/* Navbar */}
      <header style={{ background: 'white', borderBottom: '1px solid var(--border-color)', position: 'sticky', top: 0, zIndex: 40, boxShadow: 'var(--shadow-sm)' }}>
        <div className="container flex-between" style={{ height: '70px' }}>
          <div className="flex-row">
            <img src={logo} alt="DeepKlarity Logo" style={{ width: 40, height: 40, borderRadius: '50%', objectFit: 'cover', border: '2px solid white', boxShadow: '0 2px 4px rgba(0,0,0,0.1)' }} />
            <h1 style={{ fontSize: '1.4rem', fontWeight: '700', color: 'var(--text-primary)', letterSpacing: '-0.02em', marginLeft: '12px' }}>DeepKlarity Quiz</h1>
          </div>

          <nav className="flex-row" style={{ background: '#f1f5f9', padding: '4px', borderRadius: '8px' }}>
            <button
              onClick={() => setActiveTab('generate')}
              className={`nav-link ${activeTab === 'generate' ? 'active' : ''}`}
            >
              <Sparkles size={16} /> Generate
            </button>
            <button
              onClick={() => setActiveTab('history')}
              className={`nav-link ${activeTab === 'history' ? 'active' : ''}`}
            >
              <History size={16} /> History
            </button>
          </nav>
        </div>
      </header>

      {/* Main Content */}
      <main className="container" style={{ marginTop: '20px' }}>
        {activeTab === 'generate' ? <QuizView /> : <HistoryView />}
      </main>

      <footer style={{ textAlign: 'center', padding: '32px', color: 'var(--text-secondary)', fontSize: '13px' }}>
        <p>© 2026 DeepKlarity Quiz • Powered by Groq & Llama 3</p>
      </footer>
    </div>
  );
}

export default App;

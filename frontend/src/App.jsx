import React, { useState, useEffect, useRef } from 'react';
import axios from 'axios';
import { motion, AnimatePresence } from 'framer-motion';
import { 
  Send, User, Bot, Sparkles, MessageSquare, Clock, Trash2, 
  ShieldCheck, Zap, History, Plus, Copy, Check, Info, CreditCard, Truck, RefreshCcw 
} from 'lucide-react';

const API_BASE = import.meta.env.PROD ? "" : (import.meta.env.VITE_API_URL || "http://localhost:8000");

const QUICK_ACTIONS = [
  { text: "Where is my order?", icon: <Truck size={14} /> },
  { text: "Refund policy?", icon: <RefreshCcw size={14} /> },
  { text: "Shipping times?", icon: <Clock size={14} /> },
  { text: "Payment methods", icon: <CreditCard size={14} /> }
];

function App() {
  const [messages, setMessages] = useState([]);
  const [history, setHistory] = useState([]);
  const [input, setInput] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const [copiedId, setCopiedId] = useState(null);
  const messagesEndRef = useRef(null);

  useEffect(() => {
    fetchHistory();
  }, []);

  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
  }, [messages, isLoading]);

  const fetchHistory = async () => {
    try {
      const response = await axios.get(`${API_BASE}/logs`);
      setHistory(response.data.slice(0, 8));
    } catch (error) {
      console.error("Failed to fetch history", error);
    }
  };

  const copyToClipboard = (text, id) => {
    navigator.clipboard.writeText(text);
    setCopiedId(id);
    setTimeout(() => setCopiedId(null), 2000);
  };

  const sendMessage = async (text) => {
    if (!text.trim() || isLoading) return;

    const userMessage = { 
      id: Date.now(), 
      text: text, 
      sender: 'user', 
      timestamp: new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' }) 
    };
    setMessages(prev => [...prev, userMessage]);
    setInput('');
    setIsLoading(true);

    try {
      const response = await axios.post(`${API_BASE}/ask`, { query: text });
      const botMessage = { 
        id: response.data.id, 
        text: response.data.response, 
        sender: 'bot', 
        intent: response.data.intent,
        timestamp: new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' }) 
      };
      setMessages(prev => [...prev, botMessage]);
      fetchHistory();
    } catch (error) {
      setMessages(prev => [...prev, { 
        id: Date.now(), 
        text: "Neural link interrupted. Please restart the backend server.", 
        sender: 'bot', 
        isError: true,
        timestamp: new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' }) 
      }]);
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="dashboard">
      <aside className="sidebar">
        <div style={{ display: 'flex', alignItems: 'center', gap: '12px', marginBottom: '32px' }}>
          <div style={{ background: 'var(--gold-gradient)', padding: '10px', borderRadius: '14px', boxShadow: '0 4px 12px rgba(184, 134, 11, 0.2)' }}>
            <Zap size={20} color="white" />
          </div>
          <span className="golden-text" style={{ fontWeight: 800, fontSize: '1.4rem', letterSpacing: '-0.5px' }}>SupportOS</span>
        </div>

        <button onClick={() => setMessages([])} className="send-btn" style={{ 
          width: '100%', 
          height: '50px',
          background: 'rgba(197, 160, 89, 0.1)', 
          border: '1px solid var(--primary)', 
          color: 'var(--accent)',
          marginBottom: '32px',
          fontWeight: 600,
          display: 'flex',
          gap: '10px'
        }}>
          <Plus size={18} /> New Chat
        </button>

        <div className="sidebar-title">
          <History size={14} /> Recent Conversations
        </div>
        <div style={{ flex: 1, overflowY: 'auto' }}>
          {history.map((item) => (
            <div key={item.id} className="history-item">
              <MessageSquare size={14} style={{ marginRight: '10px', opacity: 0.5 }} />
              {item.user_query}
            </div>
          ))}
        </div>

        <div style={{ padding: '20px', background: 'white', border: '1px solid var(--glass-border)', borderRadius: '24px', boxShadow: '0 5px 15px rgba(197, 160, 89, 0.05)' }}>
          <div style={{ display: 'flex', alignItems: 'center', gap: '10px' }}>
            <div className="status-indicator"></div>
            <span style={{ fontSize: '0.8rem', fontWeight: 600 }}>System Live</span>
          </div>
          <p style={{ fontSize: '0.7rem', color: 'var(--text-muted)', marginTop: '4px' }}>Latency: 142ms</p>
        </div>
      </aside>

      <main className="main-chat">
        <header className="chat-header">
          <div>
            <h1>AI Powered Customer Support Services</h1>
            <div style={{ display: 'flex', alignItems: 'center', gap: '8px', marginTop: '4px' }}>
              <ShieldCheck size={12} color="#10b981" />
              <span style={{ fontSize: '0.75rem', color: 'var(--text-muted)' }}>Llama-3.1 Secure Protocol</span>
            </div>
          </div>
          <button onClick={fetchHistory} style={{ background: 'transparent', border: 'none', color: 'var(--text-muted)', cursor: 'pointer' }}>
            <RefreshCcw size={18} />
          </button>
        </header>

        <div className="messages-list">
          <AnimatePresence>
            {messages.length === 0 ? (
              <motion.div 
                initial={{ opacity: 0, scale: 0.9 }} 
                animate={{ opacity: 1, scale: 1 }}
                style={{ 
                  flex: 1, 
                  display: 'flex', 
                  flexDirection: 'column', 
                  alignItems: 'center', 
                  justifyContent: 'center',
                  textAlign: 'center',
                  padding: '40px'
                }}
              >
                <div style={{ background: 'rgba(197, 160, 89, 0.1)', padding: '24px', borderRadius: '30px', marginBottom: '24px' }}>
                  <Sparkles size={48} color="var(--accent)" />
                </div>
                <h2 style={{ fontSize: '2rem', marginBottom: '12px' }}>How can I help you?</h2>
                <p style={{ color: 'var(--text-muted)', maxWidth: '400px' }}>
                  Ask me anything about your orders, shipping, or refunds. I'm here to provide instant support.
                </p>
              </motion.div>
            ) : (
              messages.map((msg) => (
                <motion.div
                  key={msg.id}
                  initial={{ opacity: 0, y: 20 }}
                  animate={{ opacity: 1, y: 0 }}
                  className={`message ${msg.sender}`}
                >
                  <div style={{ 
                    width: '40px', 
                    height: '40px', 
                    borderRadius: '12px', 
                    background: msg.sender === 'bot' ? 'rgba(197, 160, 89, 0.1)' : 'white',
                    display: 'flex', 
                    alignItems: 'center', 
                    justifyContent: 'center',
                    border: '1px solid var(--glass-border)'
                  }}>
                    {msg.sender === 'bot' ? <Bot size={20} color="var(--accent)" /> : <User size={20} color="var(--accent)" />}
                  </div>
                  <div style={{ flex: 1, position: 'relative' }}>
                    <div className="message-bubble">
                      {msg.text}
                      {msg.sender === 'bot' && !msg.isError && (
                        <div style={{ display: 'flex', gap: '8px', marginTop: '16px' }}>
                          <button 
                            onClick={() => copyToClipboard(msg.text, msg.id)}
                            style={{ background: 'rgba(255,255,255,0.05)', border: 'none', color: 'var(--text-muted)', padding: '6px', borderRadius: '8px', cursor: 'pointer', display: 'flex', alignItems: 'center', gap: '4px', fontSize: '0.7rem' }}
                          >
                            {copiedId === msg.id ? <Check size={12} color="#10b981" /> : <Copy size={12} />}
                            {copiedId === msg.id ? 'Copied' : 'Copy'}
                          </button>
                          {!msg.escalated && (
                            <button 
                              onClick={() => handleEscalate(msg.id)}
                              style={{ background: 'rgba(239, 68, 68, 0.1)', border: 'none', color: '#f87171', padding: '6px 12px', borderRadius: '8px', cursor: 'pointer', fontSize: '0.7rem' }}
                            >
                              Escalate
                            </button>
                          )}
                        </div>
                      )}
                      {msg.escalated && (
                        <div style={{ marginTop: '12px', fontSize: '0.75rem', color: '#fbbf24', display: 'flex', alignItems: 'center', gap: '6px' }}>
                          <Info size={12} /> Support ticket created #9821
                        </div>
                      )}
                    </div>
                    <span className="message-meta">{msg.timestamp}</span>
                  </div>
                </motion.div>
              ))
            )}
          </AnimatePresence>
          {isLoading && (
            <div className="message bot">
              <div style={{ width: '40px', height: '40px' }}></div>
              <div className="message-bubble" style={{ background: 'transparent', border: '1px dashed var(--glass-border)' }}>
                <motion.div animate={{ opacity: [0.3, 1, 0.3] }} transition={{ repeat: Infinity, duration: 1.5 }} style={{ fontSize: '0.9rem', color: 'var(--text-muted)' }}>
                  Processing intelligence...
                </motion.div>
              </div>
            </div>
          )}
          <div ref={messagesEndRef} />
        </div>

        <div className="chat-input-container">
          <div className="quick-actions">
            {QUICK_ACTIONS.map((action, idx) => (
              <button key={idx} className="quick-pill" onClick={() => sendMessage(action.text)}>
                {action.icon} {action.text}
              </button>
            ))}
          </div>
          <form className="input-wrapper" onSubmit={(e) => { e.preventDefault(); sendMessage(input); }}>
            <input
              type="text"
              value={input}
              onChange={(e) => setInput(e.target.value)}
              placeholder="Ask anything..."
              disabled={isLoading}
            />
            <button type="submit" className="send-btn" disabled={!input.trim() || isLoading}>
              <Send size={20} />
            </button>
          </form>
        </div>
      </main>
    </div>
  );
}

export default App;

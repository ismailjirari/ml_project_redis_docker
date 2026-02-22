import React, { useState, useEffect } from 'react';
import './App.css';

function App() {
  const [phrase, setPhrase] = useState('');
  const [modelNumber, setModelNumber] = useState(1);
  const [availableModels, setAvailableModels] = useState({});
  const [phrases, setPhrases] = useState([]);
  const [loading, setLoading] = useState(false);
  const [submitting, setSubmitting] = useState(false);
  const [error, setError] = useState(null);
  const [successMessage, setSuccessMessage] = useState('');
  const [apiStatus, setApiStatus] = useState('checking');

  // Fetch available models and phrases on component mount
  useEffect(() => {
    checkApiHealth();
    fetchModels();
    fetchPhrases();
  }, []);

  // Check if API is reachable
  const checkApiHealth = async () => {
    try {
      const response = await fetch('http://localhost:8000/');
      if (response.ok) {
        setApiStatus('connected');
      } else {
        setApiStatus('error');
      }
    } catch (error) {
      console.error('API health check failed:', error);
      setApiStatus('disconnected');
    }
  };

  // Fetch available models
  const fetchModels = async () => {
    try {
      setLoading(true);
      const response = await fetch('http://localhost:8000/models/');
      if (!response.ok) throw new Error('Failed to fetch models');
      const data = await response.json();
      setAvailableModels(data);
    } catch (error) {
      console.error('Error fetching models:', error);
      setError('Failed to load models. Make sure the backend server is running.');
    } finally {
      setLoading(false);
    }
  };

  // Fetch all phrases
  const fetchPhrases = async () => {
    try {
      const response = await fetch('http://localhost:8000/gettage/');
      if (!response.ok) throw new Error('Failed to fetch phrases');
      const data = await response.json();
      setPhrases(data.phrases || []);
    } catch (error) {
      console.error('Error fetching phrases:', error);
      setError('Failed to load phrases.');
    }
  };

  // Handle form submission
  const handleSubmit = async (e) => {
    e.preventDefault();
    
    if (!phrase.trim()) {
      setError('Please enter a phrase');
      return;
    }

    setSubmitting(true);
    setError(null);
    setSuccessMessage('');

    try {
      const response = await fetch('http://localhost:8000/postageee/', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          phrase: phrase,
          modelnumber: parseInt(modelNumber)
        }),
      });

      if (!response.ok) {
        const errorData = await response.json();
        throw new Error(errorData.detail || 'Failed to create phrase');
      }

      const data = await response.json();
      setSuccessMessage(`✅ Phrase created successfully! (ID: ${data.phrase.id})`);
      setPhrase('');
      fetchPhrases(); // Refresh the list
    } catch (error) {
      console.error('Error submitting phrase:', error);
      setError(error.message);
    } finally {
      setSubmitting(false);
    }
  };

  // Format embedding for display
  const formatEmbedding = (embedding) => {
    if (!embedding) return 'No embedding';
    if (Array.isArray(embedding)) {
      // If it's a 2D array (multiple phrases)
      if (Array.isArray(embedding[0])) {
        return `[${embedding.length} embeddings, dim: ${embedding[0].length}]`;
      }
      // If it's a 1D array (single phrase)
      return `[${embedding.length} dimensions]`;
    }
    return 'Invalid embedding';
  };

  // Get embedding preview (first few values)
  const getEmbeddingPreview = (embedding) => {
    if (!embedding || !Array.isArray(embedding)) return '';
    const flatEmbedding = Array.isArray(embedding[0]) ? embedding[0] : embedding;
    const preview = flatEmbedding.slice(0, 5).map(v => v.toFixed(4)).join(', ');
    return `[${preview}${flatEmbedding.length > 5 ? ', ...' : ''}]`;
  };

  return (
    <div className="app">
      <header className="header">
        <h1>🧠 Sentence Embedding API</h1>
        <div className="api-status">
          API Status: 
          <span className={`status-badge status-${apiStatus}`}>
            {apiStatus === 'connected' && '🟢 Connected'}
            {apiStatus === 'disconnected' && '🔴 Disconnected'}
            {apiStatus === 'checking' && '🟡 Checking...'}
            {apiStatus === 'error' && '🟠 Error'}
          </span>
        </div>
      </header>

      <main className="main">
        {/* API Info Section */}
        <section className="info-section">
          <h2>📡 API Endpoints</h2>
          <div className="endpoints">
            <div className="endpoint">
              <code>POST /postageee/</code>
              <span>Create new sentence embedding</span>
            </div>
            <div className="endpoint">
              <code>GET /gettage/</code>
              <span>Retrieve all phrases</span>
            </div>
            <div className="endpoint">
              <code>GET /models/</code>
              <span>List available models</span>
            </div>
          </div>
        </section>

        {/* Form Section */}
        <section className="form-section">
          <h2>📝 Create New Embedding</h2>
          
          {apiStatus !== 'connected' && (
            <div className="warning-message">
              ⚠️ Backend server is not connected. Please make sure it's running on http://localhost:8000
            </div>
          )}

          <form onSubmit={handleSubmit} className="embedding-form">
            <div className="form-group">
              <label htmlFor="phrase">Phrase:</label>
              <textarea
                id="phrase"
                value={phrase}
                onChange={(e) => setPhrase(e.target.value)}
                placeholder="Enter a sentence or phrase..."
                rows="3"
                disabled={submitting || apiStatus !== 'connected'}
              />
            </div>

            <div className="form-group">
              <label htmlFor="model">Model:</label>
              <select
                id="model"
                value={modelNumber}
                onChange={(e) => setModelNumber(e.target.value)}
                disabled={submitting || loading || apiStatus !== 'connected'}
              >
                {Object.entries(availableModels).map(([key, value]) => (
                  <option key={key} value={key}>
                    {key}: {value}
                  </option>
                ))}
              </select>
            </div>

            {error && <div className="error-message">{error}</div>}
            {successMessage && <div className="success-message">{successMessage}</div>}

            <button 
              type="submit" 
              disabled={submitting || apiStatus !== 'connected' || !phrase.trim()}
              className="submit-button"
            >
              {submitting ? '⏳ Creating...' : '🚀 Generate Embedding'}
            </button>
          </form>
        </section>

        {/* Results Section */}
        <section className="results-section">
          <div className="results-header">
            <h2>📋 Generated Embeddings ({phrases.length})</h2>
            <button 
              onClick={fetchPhrases} 
              className="refresh-button"
              disabled={apiStatus !== 'connected'}
            >
              🔄 Refresh
            </button>
          </div>

          {phrases.length === 0 ? (
            <div className="empty-state">
              <p>No embeddings generated yet. Create your first one above!</p>
            </div>
          ) : (
            <div className="phrases-grid">
              {phrases.map((item) => (
                <div key={item.id} className="phrase-card">
                  <div className="phrase-header">
                    <span className="phrase-id">#{item.id}</span>
                    <span className="phrase-model">{item.model_used}</span>
                  </div>
                  
                  <div className="phrase-content">
                    <p className="phrase-text">{item.phrase}</p>
                    
                    <div className="embedding-info">
                      <div className="embedding-dim">
                        📊 {item.embedding_dim} dimensions
                      </div>
                      <div className="embedding-preview">
                        <span className="preview-label">Preview:</span>
                        <code>{getEmbeddingPreview(item.embedding)}</code>
                      </div>
                    </div>
                  </div>

                  <details className="embedding-details">
                    <summary>View full embedding</summary>
                    <pre className="embedding-full">
                      {JSON.stringify(item.embedding, null, 2)}
                    </pre>
                  </details>
                </div>
              ))}
            </div>
          )}
        </section>
      </main>

      <footer className="footer">
        <p>Sentence Embedding API Frontend | Powered by FastAPI + React</p>
      </footer>
    </div>
  );
}

export default App;

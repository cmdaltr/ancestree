import { useState } from 'react'
import { searchAPI } from '../services/api'
import { FaTimes, FaSearch, FaSpinner } from 'react-icons/fa'
import '../styles/Modal.css'

export default function SearchModal({ onClose }) {
  const [searchQuery, setSearchQuery] = useState({
    first_name: '',
    last_name: '',
    birth_year: '',
    birth_place: '',
    death_year: '',
    death_place: '',
    use_ai: false,
    sources: ['ancestry', 'familysearch', 'findmypast', 'myheritage']
  })
  const [results, setResults] = useState(null)
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState('')

  const handleSearch = async (e) => {
    e.preventDefault()
    setError('')
    setLoading(true)
    setResults(null)

    try {
      // Convert empty strings to null
      const queryToSend = {
        ...searchQuery,
        birth_year: searchQuery.birth_year ? parseInt(searchQuery.birth_year) : null,
        death_year: searchQuery.death_year ? parseInt(searchQuery.death_year) : null
      }

      const response = await searchAPI.genealogy(queryToSend)
      setResults(response.data)
    } catch (err) {
      setError(err.response?.data?.detail || 'Search failed')
    } finally {
      setLoading(false)
    }
  }

  const toggleSource = (source) => {
    setSearchQuery(prev => ({
      ...prev,
      sources: prev.sources.includes(source)
        ? prev.sources.filter(s => s !== source)
        : [...prev.sources, source]
    }))
  }

  return (
    <div className="modal-overlay modal-large" onClick={onClose}>
      <div className="modal-content" onClick={(e) => e.stopPropagation()}>
        <div className="modal-header">
          <h2>Search Genealogy Records</h2>
          <button className="btn-icon" onClick={onClose}>
            <FaTimes />
          </button>
        </div>

        {error && <div className="error-message">{error}</div>}

        <form onSubmit={handleSearch} className="modal-form search-form">
          <div className="form-row">
            <div className="form-group">
              <label>First Name</label>
              <input
                type="text"
                value={searchQuery.first_name}
                onChange={(e) => setSearchQuery({ ...searchQuery, first_name: e.target.value })}
                placeholder="e.g., John"
              />
            </div>

            <div className="form-group">
              <label>Last Name</label>
              <input
                type="text"
                value={searchQuery.last_name}
                onChange={(e) => setSearchQuery({ ...searchQuery, last_name: e.target.value })}
                placeholder="e.g., Smith"
              />
            </div>
          </div>

          <div className="form-row">
            <div className="form-group">
              <label>Birth Year</label>
              <input
                type="number"
                value={searchQuery.birth_year}
                onChange={(e) => setSearchQuery({ ...searchQuery, birth_year: e.target.value })}
                placeholder="e.g., 1850"
              />
            </div>

            <div className="form-group">
              <label>Birth Place</label>
              <input
                type="text"
                value={searchQuery.birth_place}
                onChange={(e) => setSearchQuery({ ...searchQuery, birth_place: e.target.value })}
                placeholder="e.g., London, England"
              />
            </div>
          </div>

          <div className="form-row">
            <div className="form-group">
              <label>Death Year</label>
              <input
                type="number"
                value={searchQuery.death_year}
                onChange={(e) => setSearchQuery({ ...searchQuery, death_year: e.target.value })}
                placeholder="e.g., 1920"
              />
            </div>

            <div className="form-group">
              <label>Death Place</label>
              <input
                type="text"
                value={searchQuery.death_place}
                onChange={(e) => setSearchQuery({ ...searchQuery, death_place: e.target.value })}
                placeholder="e.g., New York, USA"
              />
            </div>
          </div>

          <div className="form-group">
            <label className="checkbox-label">
              <input
                type="checkbox"
                checked={searchQuery.use_ai}
                onChange={(e) => setSearchQuery({ ...searchQuery, use_ai: e.target.checked })}
              />
              Use AI-powered search (enhances query and analyzes results)
            </label>
          </div>

          <div className="form-group">
            <label>Search Sources</label>
            <div className="source-checkboxes">
              {['ancestry', 'familysearch', 'findmypast', 'myheritage'].map(source => (
                <label key={source} className="checkbox-label">
                  <input
                    type="checkbox"
                    checked={searchQuery.sources.includes(source)}
                    onChange={() => toggleSource(source)}
                  />
                  {source.charAt(0).toUpperCase() + source.slice(1)}
                </label>
              ))}
            </div>
          </div>

          <button type="submit" className="btn btn-primary btn-search" disabled={loading}>
            {loading ? (
              <>
                <FaSpinner className="spinner" /> Searching...
              </>
            ) : (
              <>
                <FaSearch /> Search
              </>
            )}
          </button>
        </form>

        {results && (
          <div className="search-results">
            <h3>Search Results ({results.total_results} found)</h3>

            {results.ai_analysis && (
              <div className="ai-analysis">
                <h4>AI Analysis</h4>
                <p>{results.ai_analysis.ai_analysis}</p>
              </div>
            )}

            {Object.entries(results.results).map(([source, records]) => (
              <div key={source} className="source-results">
                <h4>{source.charAt(0).toUpperCase() + source.slice(1)} ({records.length})</h4>
                {records.length === 0 ? (
                  <p className="no-results">No results from this source</p>
                ) : (
                  <div className="results-list">
                    {records.map((record, idx) => (
                      <div key={idx} className="result-item">
                        <div className="result-name">{record.name}</div>
                        {record.birth_date && (
                          <div className="result-detail">
                            Born: {record.birth_date}
                            {record.birth_place && ` in ${record.birth_place}`}
                          </div>
                        )}
                        {record.death_date && (
                          <div className="result-detail">
                            Died: {record.death_date}
                            {record.death_place && ` in ${record.death_place}`}
                          </div>
                        )}
                        {record.note && (
                          <div className="result-note">{record.note}</div>
                        )}
                        {record.url && (
                          <a
                            href={record.url}
                            target="_blank"
                            rel="noopener noreferrer"
                            className="result-link"
                          >
                            View on {source}
                          </a>
                        )}
                      </div>
                    ))}
                  </div>
                )}
              </div>
            ))}

            <div className="info-message">
              <strong>Note:</strong> This is a demonstration app. Full integration with genealogy
              sites requires API keys and authentication. The search results shown are placeholders.
              To enable real searches, add your API credentials to the backend .env file.
            </div>
          </div>
        )}
      </div>
    </div>
  )
}

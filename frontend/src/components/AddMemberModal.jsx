import { useState } from 'react'
import { useFamilyStore } from '../stores/familyStore'
import { familyAPI } from '../services/api'
import { FaTimes } from 'react-icons/fa'
import '../styles/Modal.css'

export default function AddMemberModal({ onClose, onSuccess }) {
  const { members } = useFamilyStore()
  const [formData, setFormData] = useState({
    first_name: '',
    middle_name: '',
    last_name: '',
    maiden_name: '',
    gender: 'unknown',
    birth_date: '',
    birth_place: '',
    death_date: '',
    death_place: '',
    occupation: '',
    biography: '',
    father_id: '',
    mother_id: ''
  })
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState('')

  const handleSubmit = async (e) => {
    e.preventDefault()
    setError('')
    setLoading(true)

    try {
      // Convert empty strings to null for optional fields
      const dataToSend = Object.fromEntries(
        Object.entries(formData).map(([key, value]) => [key, value === '' ? null : value])
      )

      await familyAPI.create(dataToSend)
      onSuccess()
    } catch (err) {
      setError(err.response?.data?.detail || 'Failed to add family member')
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="modal-overlay" onClick={onClose}>
      <div className="modal-content" onClick={(e) => e.stopPropagation()}>
        <div className="modal-header">
          <h2>Add Family Member</h2>
          <button className="btn-icon" onClick={onClose}>
            <FaTimes />
          </button>
        </div>

        {error && <div className="error-message">{error}</div>}

        <form onSubmit={handleSubmit} className="modal-form">
          <div className="form-row">
            <div className="form-group">
              <label>First Name *</label>
              <input
                type="text"
                value={formData.first_name}
                onChange={(e) => setFormData({ ...formData, first_name: e.target.value })}
                required
                autoFocus
              />
            </div>

            <div className="form-group">
              <label>Middle Name</label>
              <input
                type="text"
                value={formData.middle_name}
                onChange={(e) => setFormData({ ...formData, middle_name: e.target.value })}
              />
            </div>
          </div>

          <div className="form-row">
            <div className="form-group">
              <label>Last Name *</label>
              <input
                type="text"
                value={formData.last_name}
                onChange={(e) => setFormData({ ...formData, last_name: e.target.value })}
                required
              />
            </div>

            <div className="form-group">
              <label>Maiden Name</label>
              <input
                type="text"
                value={formData.maiden_name}
                onChange={(e) => setFormData({ ...formData, maiden_name: e.target.value })}
              />
            </div>
          </div>

          <div className="form-group">
            <label>Gender</label>
            <select
              value={formData.gender}
              onChange={(e) => setFormData({ ...formData, gender: e.target.value })}
            >
              <option value="male">Male</option>
              <option value="female">Female</option>
              <option value="other">Other</option>
              <option value="unknown">Unknown</option>
            </select>
          </div>

          <div className="form-row">
            <div className="form-group">
              <label>Birth Date</label>
              <input
                type="date"
                value={formData.birth_date}
                onChange={(e) => setFormData({ ...formData, birth_date: e.target.value })}
              />
            </div>

            <div className="form-group">
              <label>Birth Place</label>
              <input
                type="text"
                value={formData.birth_place}
                onChange={(e) => setFormData({ ...formData, birth_place: e.target.value })}
              />
            </div>
          </div>

          <div className="form-row">
            <div className="form-group">
              <label>Death Date</label>
              <input
                type="date"
                value={formData.death_date}
                onChange={(e) => setFormData({ ...formData, death_date: e.target.value })}
              />
            </div>

            <div className="form-group">
              <label>Death Place</label>
              <input
                type="text"
                value={formData.death_place}
                onChange={(e) => setFormData({ ...formData, death_place: e.target.value })}
              />
            </div>
          </div>

          <div className="form-group">
            <label>Occupation</label>
            <input
              type="text"
              value={formData.occupation}
              onChange={(e) => setFormData({ ...formData, occupation: e.target.value })}
            />
          </div>

          <div className="form-row">
            <div className="form-group">
              <label>Father</label>
              <select
                value={formData.father_id}
                onChange={(e) => setFormData({ ...formData, father_id: e.target.value })}
              >
                <option value="">Select Father</option>
                {members.filter(m => m.gender === 'male').map(member => (
                  <option key={member.id} value={member.id}>
                    {member.first_name} {member.last_name}
                  </option>
                ))}
              </select>
            </div>

            <div className="form-group">
              <label>Mother</label>
              <select
                value={formData.mother_id}
                onChange={(e) => setFormData({ ...formData, mother_id: e.target.value })}
              >
                <option value="">Select Mother</option>
                {members.filter(m => m.gender === 'female').map(member => (
                  <option key={member.id} value={member.id}>
                    {member.first_name} {member.last_name}
                  </option>
                ))}
              </select>
            </div>
          </div>

          <div className="form-group">
            <label>Biography</label>
            <textarea
              value={formData.biography}
              onChange={(e) => setFormData({ ...formData, biography: e.target.value })}
              rows={4}
            />
          </div>

          <div className="modal-actions">
            <button type="button" className="btn" onClick={onClose} disabled={loading}>
              Cancel
            </button>
            <button type="submit" className="btn btn-primary" disabled={loading}>
              {loading ? 'Adding...' : 'Add Member'}
            </button>
          </div>
        </form>
      </div>
    </div>
  )
}

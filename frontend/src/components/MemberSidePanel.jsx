import { useState, useEffect, useRef } from 'react'
import { FaTimes, FaEdit, FaTrash, FaUpload } from 'react-icons/fa'
import { useFamilyStore } from '../stores/familyStore'
import { familyAPI, documentsAPI } from '../services/api'
import { format } from 'date-fns'
import '../styles/SidePanel.css'

export default function MemberSidePanel() {
  const { selectedMember, selectMember, sidePanelWidth, setSidePanelWidth, updateMember, deleteMember } = useFamilyStore()
  const [isEditing, setIsEditing] = useState(false)
  const [editData, setEditData] = useState({})
  const [documents, setDocuments] = useState([])
  const [isResizing, setIsResizing] = useState(false)
  const panelRef = useRef()

  useEffect(() => {
    if (selectedMember) {
      setEditData(selectedMember)
      loadDocuments()
    }
  }, [selectedMember])

  useEffect(() => {
    if (isResizing) {
      const handleMouseMove = (e) => {
        const newWidth = ((window.innerWidth - e.clientX) / window.innerWidth) * 100
        setSidePanelWidth(Math.max(15, Math.min(50, newWidth)))
      }

      const handleMouseUp = () => {
        setIsResizing(false)
      }

      document.addEventListener('mousemove', handleMouseMove)
      document.addEventListener('mouseup', handleMouseUp)

      return () => {
        document.removeEventListener('mousemove', handleMouseMove)
        document.removeEventListener('mouseup', handleMouseUp)
      }
    }
  }, [isResizing])

  const loadDocuments = async () => {
    try {
      const response = await documentsAPI.getAll(selectedMember.id)
      setDocuments(response.data)
    } catch (error) {
      console.error('Failed to load documents:', error)
    }
  }

  const handleSave = async () => {
    try {
      const response = await familyAPI.update(selectedMember.id, editData)
      updateMember(selectedMember.id, response.data)
      setIsEditing(false)
    } catch (error) {
      console.error('Failed to update member:', error)
      alert('Failed to update member')
    }
  }

  const handleDelete = async () => {
    if (!confirm('Are you sure you want to delete this family member?')) return

    try {
      await familyAPI.delete(selectedMember.id)
      deleteMember(selectedMember.id)
      selectMember(null)
    } catch (error) {
      console.error('Failed to delete member:', error)
      alert('Failed to delete member')
    }
  }

  const handleFileUpload = async (e) => {
    const file = e.target.files[0]
    if (!file) return

    const formData = new FormData()
    formData.append('file', file)
    formData.append('title', file.name)
    formData.append('family_member_id', selectedMember.id)
    formData.append('document_type', file.type.startsWith('image/') ? 'photo' : 'document')

    try {
      await documentsAPI.upload(formData)
      loadDocuments()
    } catch (error) {
      console.error('Failed to upload file:', error)
      alert('Failed to upload file')
    }
  }

  const formatDate = (dateString) => {
    if (!dateString) return 'Unknown'
    try {
      return format(new Date(dateString), 'MMM d, yyyy')
    } catch {
      return dateString
    }
  }

  if (!selectedMember) return null

  return (
    <div
      ref={panelRef}
      className="side-panel"
      style={{ width: `${sidePanelWidth}%` }}
    >
      <div
        className="resize-handle"
        onMouseDown={() => setIsResizing(true)}
      />

      <div className="side-panel-header">
        <h2>
          {selectedMember.first_name} {selectedMember.last_name}
        </h2>
        <div className="header-actions">
          {!isEditing && (
            <>
              <button className="btn-icon" onClick={() => setIsEditing(true)} title="Edit">
                <FaEdit />
              </button>
              <button className="btn-icon danger" onClick={handleDelete} title="Delete">
                <FaTrash />
              </button>
            </>
          )}
          <button className="btn-icon" onClick={() => selectMember(null)} title="Close">
            <FaTimes />
          </button>
        </div>
      </div>

      <div className="side-panel-content">
        {isEditing ? (
          <div className="edit-form">
            <div className="form-group">
              <label>First Name</label>
              <input
                type="text"
                value={editData.first_name || ''}
                onChange={(e) => setEditData({ ...editData, first_name: e.target.value })}
              />
            </div>

            <div className="form-group">
              <label>Middle Name</label>
              <input
                type="text"
                value={editData.middle_name || ''}
                onChange={(e) => setEditData({ ...editData, middle_name: e.target.value })}
              />
            </div>

            <div className="form-group">
              <label>Last Name</label>
              <input
                type="text"
                value={editData.last_name || ''}
                onChange={(e) => setEditData({ ...editData, last_name: e.target.value })}
              />
            </div>

            <div className="form-group">
              <label>Gender</label>
              <select
                value={editData.gender || 'unknown'}
                onChange={(e) => setEditData({ ...editData, gender: e.target.value })}
              >
                <option value="male">Male</option>
                <option value="female">Female</option>
                <option value="other">Other</option>
                <option value="unknown">Unknown</option>
              </select>
            </div>

            <div className="form-group">
              <label>Birth Date</label>
              <input
                type="date"
                value={editData.birth_date || ''}
                onChange={(e) => setEditData({ ...editData, birth_date: e.target.value })}
              />
            </div>

            <div className="form-group">
              <label>Birth Place</label>
              <input
                type="text"
                value={editData.birth_place || ''}
                onChange={(e) => setEditData({ ...editData, birth_place: e.target.value })}
              />
            </div>

            <div className="form-group">
              <label>Death Date</label>
              <input
                type="date"
                value={editData.death_date || ''}
                onChange={(e) => setEditData({ ...editData, death_date: e.target.value })}
              />
            </div>

            <div className="form-group">
              <label>Death Place</label>
              <input
                type="text"
                value={editData.death_place || ''}
                onChange={(e) => setEditData({ ...editData, death_place: e.target.value })}
              />
            </div>

            <div className="form-group">
              <label>Occupation</label>
              <input
                type="text"
                value={editData.occupation || ''}
                onChange={(e) => setEditData({ ...editData, occupation: e.target.value })}
              />
            </div>

            <div className="form-group">
              <label>Biography</label>
              <textarea
                value={editData.biography || ''}
                onChange={(e) => setEditData({ ...editData, biography: e.target.value })}
                rows={4}
              />
            </div>

            <div className="form-actions">
              <button className="btn btn-primary" onClick={handleSave}>Save</button>
              <button className="btn" onClick={() => setIsEditing(false)}>Cancel</button>
            </div>
          </div>
        ) : (
          <div className="member-details">
            <div className="detail-section">
              <h3>Basic Information</h3>
              <div className="detail-item">
                <span className="label">Full Name:</span>
                <span className="value">
                  {selectedMember.first_name} {selectedMember.middle_name} {selectedMember.last_name}
                </span>
              </div>
              {selectedMember.maiden_name && (
                <div className="detail-item">
                  <span className="label">Maiden Name:</span>
                  <span className="value">{selectedMember.maiden_name}</span>
                </div>
              )}
              <div className="detail-item">
                <span className="label">Gender:</span>
                <span className="value">{selectedMember.gender}</span>
              </div>
            </div>

            <div className="detail-section">
              <h3>Life Events</h3>
              <div className="detail-item">
                <span className="label">Birth:</span>
                <span className="value">
                  {formatDate(selectedMember.birth_date)}
                  {selectedMember.birth_place && ` in ${selectedMember.birth_place}`}
                </span>
              </div>
              {selectedMember.death_date && (
                <div className="detail-item">
                  <span className="label">Death:</span>
                  <span className="value">
                    {formatDate(selectedMember.death_date)}
                    {selectedMember.death_place && ` in ${selectedMember.death_place}`}
                  </span>
                </div>
              )}
              {selectedMember.occupation && (
                <div className="detail-item">
                  <span className="label">Occupation:</span>
                  <span className="value">{selectedMember.occupation}</span>
                </div>
              )}
            </div>

            {selectedMember.biography && (
              <div className="detail-section">
                <h3>Biography</h3>
                <p>{selectedMember.biography}</p>
              </div>
            )}

            <div className="detail-section">
              <h3>Documents & Photos</h3>
              <div className="documents-list">
                {documents.map((doc) => (
                  <div key={doc.id} className="document-item">
                    {doc.file_type?.startsWith('image/') ? (
                      <img src={`/${doc.file_path}`} alt={doc.title} />
                    ) : (
                      <div className="document-icon">📄</div>
                    )}
                    <span>{doc.title}</span>
                  </div>
                ))}
              </div>
              <label className="btn btn-upload">
                <FaUpload /> Upload File
                <input
                  type="file"
                  onChange={handleFileUpload}
                  style={{ display: 'none' }}
                  accept="image/*,.pdf,.doc,.docx"
                />
              </label>
            </div>
          </div>
        )}
      </div>
    </div>
  )
}

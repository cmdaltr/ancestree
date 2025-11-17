import { useState, useEffect } from 'react'
import { Outlet } from 'react-router-dom'
import { useAuthStore } from '../stores/authStore'
import { useFamilyStore } from '../stores/familyStore'
import { familyAPI } from '../services/api'
import Navbar from './Navbar'
import MemberSidePanel from './MemberSidePanel'
import SearchModal from './SearchModal'
import AddMemberModal from './AddMemberModal'
import '../styles/Dashboard.css'

export default function Dashboard() {
  const { user, logout } = useAuthStore()
  const { members, setMembers, selectedMember, sidePanelWidth } = useFamilyStore()
  const [showSearchModal, setShowSearchModal] = useState(false)
  const [showAddMemberModal, setShowAddMemberModal] = useState(false)
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    loadFamilyMembers()
  }, [])

  const loadFamilyMembers = async () => {
    try {
      const response = await familyAPI.getAll()
      setMembers(response.data)
    } catch (error) {
      console.error('Failed to load family members:', error)
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="dashboard">
      <Navbar
        user={user}
        onLogout={logout}
        onSearch={() => setShowSearchModal(true)}
        onAddMember={() => setShowAddMemberModal(true)}
      />

      <div className="dashboard-content">
        <div
          className="main-view"
          style={{ width: selectedMember ? `${100 - sidePanelWidth}%` : '100%' }}
        >
          {loading ? (
            <div className="loading">Loading family tree...</div>
          ) : (
            <Outlet />
          )}
        </div>

        {selectedMember && <MemberSidePanel />}
      </div>

      {showSearchModal && (
        <SearchModal onClose={() => setShowSearchModal(false)} />
      )}

      {showAddMemberModal && (
        <AddMemberModal
          onClose={() => setShowAddMemberModal(false)}
          onSuccess={() => {
            setShowAddMemberModal(false)
            loadFamilyMembers()
          }}
        />
      )}
    </div>
  )
}

import { FaSearch, FaPlus, FaSignOutAlt, FaUser } from 'react-icons/fa'
import '../styles/Navbar.css'

export default function Navbar({ user, onLogout, onSearch, onAddMember }) {
  return (
    <nav className="navbar">
      <div className="navbar-brand">
        <img src="/ancestree.png" alt="Ancestree" className="navbar-logo" />
        <h1>Ancestree</h1>
      </div>

      <div className="navbar-actions">
        <button className="btn btn-icon" onClick={onSearch} title="Search Genealogy Records">
          <FaSearch />
          <span>Search</span>
        </button>

        <button className="btn btn-primary btn-icon" onClick={onAddMember} title="Add Family Member">
          <FaPlus />
          <span>Add Member</span>
        </button>

        <div className="user-menu">
          <FaUser />
          <span>{user?.username}</span>
        </div>

        <button className="btn btn-icon" onClick={onLogout} title="Logout">
          <FaSignOutAlt />
        </button>
      </div>
    </nav>
  )
}

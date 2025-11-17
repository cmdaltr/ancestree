import { create } from 'zustand'

export const useFamilyStore = create((set) => ({
  members: [],
  selectedMember: null,
  sidePanelWidth: 20, // percentage

  setMembers: (members) => set({ members }),

  addMember: (member) => set((state) => ({
    members: [...state.members, member]
  })),

  updateMember: (id, updatedMember) => set((state) => ({
    members: state.members.map(m => m.id === id ? { ...m, ...updatedMember } : m),
    selectedMember: state.selectedMember?.id === id ? { ...state.selectedMember, ...updatedMember } : state.selectedMember
  })),

  deleteMember: (id) => set((state) => ({
    members: state.members.filter(m => m.id !== id),
    selectedMember: state.selectedMember?.id === id ? null : state.selectedMember
  })),

  selectMember: (member) => set({ selectedMember: member }),

  setSidePanelWidth: (width) => set({ sidePanelWidth: width }),
}))

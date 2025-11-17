import { useEffect, useRef, useState } from 'react'
import { useFamilyStore } from '../stores/familyStore'
import * as d3 from 'd3'
import '../styles/FamilyTree.css'

export default function FamilyTreeView() {
  const { members, selectMember, selectedMember } = useFamilyStore()
  const svgRef = useRef()
  const containerRef = useRef()
  const [dimensions, setDimensions] = useState({ width: 800, height: 600 })

  useEffect(() => {
    const updateDimensions = () => {
      if (containerRef.current) {
        setDimensions({
          width: containerRef.current.offsetWidth,
          height: containerRef.current.offsetHeight
        })
      }
    }

    updateDimensions()
    window.addEventListener('resize', updateDimensions)
    return () => window.removeEventListener('resize', updateDimensions)
  }, [])

  useEffect(() => {
    if (!members.length || !svgRef.current) return

    renderTree()
  }, [members, dimensions, selectedMember])

  const buildHierarchy = () => {
    // Create a map of all members
    const memberMap = new Map(members.map(m => [m.id, { ...m, children: [] }]))

    // Find root members (those without parents) and build tree structure
    const roots = []

    members.forEach(member => {
      const node = memberMap.get(member.id)

      if (!member.father_id && !member.mother_id) {
        roots.push(node)
      } else {
        // Add this member as a child of their parents
        if (member.father_id && memberMap.has(member.father_id)) {
          memberMap.get(member.father_id).children.push(node)
        } else if (member.mother_id && memberMap.has(member.mother_id)) {
          memberMap.get(member.mother_id).children.push(node)
        }
      }
    })

    // If no roots found, use all members
    if (roots.length === 0 && members.length > 0) {
      return { name: 'Root', children: Array.from(memberMap.values()) }
    }

    // Return structure for D3
    return roots.length === 1 ? roots[0] : { name: 'Root', children: roots }
  }

  const renderTree = () => {
    const svg = d3.select(svgRef.current)
    svg.selectAll('*').remove()

    const { width, height } = dimensions
    const margin = { top: 40, right: 120, bottom: 40, left: 120 }

    const treeLayout = d3.tree()
      .size([height - margin.top - margin.bottom, width - margin.left - margin.right])

    const root = d3.hierarchy(buildHierarchy())

    treeLayout(root)

    const g = svg
      .attr('width', width)
      .attr('height', height)
      .append('g')
      .attr('transform', `translate(${margin.left},${margin.top})`)

    // Add zoom functionality
    const zoom = d3.zoom()
      .scaleExtent([0.5, 3])
      .on('zoom', (event) => {
        g.attr('transform', event.transform)
      })

    svg.call(zoom)

    // Draw links
    g.selectAll('.link')
      .data(root.links())
      .enter()
      .append('path')
      .attr('class', 'link')
      .attr('d', d3.linkHorizontal()
        .x(d => d.y)
        .y(d => d.x))
      .style('fill', 'none')
      .style('stroke', '#ccc')
      .style('stroke-width', 2)

    // Draw nodes
    const nodes = g.selectAll('.node')
      .data(root.descendants())
      .enter()
      .append('g')
      .attr('class', d => `node ${selectedMember?.id === d.data.id ? 'selected' : ''}`)
      .attr('transform', d => `translate(${d.y},${d.x})`)
      .style('cursor', 'pointer')
      .on('click', (event, d) => {
        if (d.data.id) {
          selectMember(d.data)
        }
      })

    // Add circles for nodes
    nodes.append('circle')
      .attr('r', 8)
      .style('fill', d => {
        if (selectedMember?.id === d.data.id) return '#4CAF50'
        if (d.data.gender === 'male') return '#64B5F6'
        if (d.data.gender === 'female') return '#F48FB1'
        return '#90A4AE'
      })
      .style('stroke', '#333')
      .style('stroke-width', 2)

    // Add labels
    nodes.append('text')
      .attr('dy', '.31em')
      .attr('x', d => d.children ? -12 : 12)
      .style('text-anchor', d => d.children ? 'end' : 'start')
      .style('font-size', '12px')
      .style('fill', '#333')
      .text(d => {
        if (!d.data.first_name) return d.data.name || ''
        return `${d.data.first_name} ${d.data.last_name || ''}`
      })

    // Add birth/death years
    nodes.append('text')
      .attr('dy', '1.5em')
      .attr('x', d => d.children ? -12 : 12)
      .style('text-anchor', d => d.children ? 'end' : 'start')
      .style('font-size', '10px')
      .style('fill', '#666')
      .text(d => {
        if (!d.data.birth_date && !d.data.death_date) return ''
        const birth = d.data.birth_date ? new Date(d.data.birth_date).getFullYear() : '?'
        const death = d.data.death_date ? new Date(d.data.death_date).getFullYear() : ''
        return death ? `${birth}-${death}` : `b. ${birth}`
      })
  }

  if (members.length === 0) {
    return (
      <div className="empty-state">
        <h2>No family members yet</h2>
        <p>Click "Add Member" to start building your family tree</p>
      </div>
    )
  }

  return (
    <div className="family-tree-container" ref={containerRef}>
      <svg ref={svgRef} className="family-tree-svg"></svg>
    </div>
  )
}

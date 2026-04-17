import type { FamilyTreeNode } from '../types/api'

export default function FamilyTree({ nodes }: { nodes: FamilyTreeNode[] }) {
  if (!nodes.length) {
    return <p className="muted">No historical variations were found for this claim yet.</p>
  }

  return (
    <div className="timeline">
      {nodes.map((node) => (
        <div key={node.id} className="timeline-node">
          <div className="timeline-year">{node.year ?? '—'}</div>
          <div>
            <h4>{node.title}</h4>
            <p>{node.variation_note}</p>
          </div>
          <span className="chip">{node.label}</span>
        </div>
      ))}
    </div>
  )
}

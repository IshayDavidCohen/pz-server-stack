import './Card.css'

interface CardProps {
  title?: string
  children: React.ReactNode
}

function Card({ title, children }: CardProps) {
  return (
    <div className="card">
      {title && <h1 className="card-title">{title}</h1>}
      <div className="card-content">
        {children}
      </div>
    </div>
  )
}

export default Card


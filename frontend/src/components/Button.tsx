import './Button.css'

interface ButtonProps {
  variant?: 'primary' | 'secondary'
  disabled?: boolean
  loading?: boolean
  onClick?: () => void
  children: React.ReactNode
  type?: 'button' | 'submit'
}

function Button({ 
  variant = 'primary', 
  disabled = false, 
  loading = false,
  onClick,
  children,
  type = 'button'
}: ButtonProps) {
  return (
    <button
      type={type}
      className={`btn btn-${variant}`}
      disabled={disabled || loading}
      onClick={onClick}
    >
      {loading ? 'Loading...' : children}
    </button>
  )
}

export default Button


import './Input.css'

interface InputProps {
  label: string
  name: string
  type?: string
  value: string
  onChange: (e: React.ChangeEvent<HTMLInputElement | HTMLTextAreaElement>) => void
  error?: string
  required?: boolean
  placeholder?: string
  multiline?: boolean
  rows?: number
}

function Input({
  label,
  name,
  type = 'text',
  value,
  onChange,
  error,
  required = false,
  placeholder,
  multiline = false,
  rows = 4
}: InputProps) {
  const id = `input-${name}`
  const errorId = error ? `${id}-error` : undefined

  return (
    <div className="input-group">
      <label htmlFor={id} className="input-label">
        {label}
        {required && <span className="required-indicator" aria-label="required">*</span>}
      </label>
      {multiline ? (
        <textarea
          id={id}
          name={name}
          value={value}
          onChange={onChange}
          placeholder={placeholder}
          required={required}
          rows={rows}
          className={`input-field ${error ? 'input-error' : ''}`}
          aria-describedby={errorId}
          aria-invalid={!!error}
        />
      ) : (
        <input
          id={id}
          name={name}
          type={type}
          value={value}
          onChange={onChange}
          placeholder={placeholder}
          required={required}
          className={`input-field ${error ? 'input-error' : ''}`}
          aria-describedby={errorId}
          aria-invalid={!!error}
        />
      )}
      {error && (
        <div id={errorId} className="input-error-message" role="alert">
          {error}
        </div>
      )}
    </div>
  )
}

export default Input


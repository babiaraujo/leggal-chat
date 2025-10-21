interface LogoProps {
  className?: string
}

export function Logo({ className = "h-8" }: LogoProps) {
  return (
    <div className={`flex items-center ${className}`}>
      <span className="text-3xl font-bold text-green-600">Leggal</span>
    </div>
  )
}


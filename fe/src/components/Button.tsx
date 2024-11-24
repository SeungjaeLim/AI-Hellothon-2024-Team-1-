interface ButtonProps {
  children: React.ReactNode;
  icon?: React.ReactNode;
  variant?: "default" | "primary" | "secondary";
  size?: "sm" | "md" | "lg" | "xl";
}

function Button({
  children,
  icon,
  variant = "default",
  size = "sm",
}: ButtonProps) {
  const variantClasses =
    variant === "primary"
      ? "bg-blue-main p-3 rounded-lg"
      : "bg-black-1 p-3 rounded";

  return (
    <button
      className={`flex items-center gap-2.5 text-center ${variantClasses}`}
    >
      <span className={`font-semibold text-${size}`}>{children}</span>
      {icon && (
        <span className="flex h-6 w-6 items-center justify-center">{icon}</span>
      )}
    </button>
  );
}

export default Button;

interface ReportButtonProps {
  text: string;
  icon?: React.ReactNode;
  onClick?: () => void;
  disabled?: boolean;
  size?: string;
}

function ReportButton({
  text,
  icon,
  onClick,
  disabled = false,
  size,
}: ReportButtonProps) {
  return (
    <button
      onClick={onClick}
      disabled={disabled}
      className={`flex items-center justify-center gap-3 rounded border p-3 ${
        disabled ? "border-black-6 bg-black-4" : "border-black-13 bg-black-1"
      } ${size}`}
    >
      <span
        className={`text-base font-semibold ${
          disabled ? "text-black-6" : "text-black-13"
        }`}
      >
        {text}
      </span>
      <span>{icon}</span>
    </button>
  );
}

export default ReportButton;

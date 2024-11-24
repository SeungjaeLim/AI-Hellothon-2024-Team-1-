interface BorderButtonProps
  extends React.ButtonHTMLAttributes<HTMLButtonElement> {
  text: string;
  className?: string;
  icon?: React.ReactNode;
}

function BorderButton({ text, className, icon, ...props }: BorderButtonProps) {
  return (
    <button
      className={`flex h-14 grow items-center justify-center gap-2 rounded border border-black-13 bg-black-1 px-3 py-4 ${className}`}
      {...props}
    >
      <span className="text-black text-center text-base font-semibold">
        {text}
      </span>
      <span>{icon}</span>
    </button>
  );
}

export default BorderButton;

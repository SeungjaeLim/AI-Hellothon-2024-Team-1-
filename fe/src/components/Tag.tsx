interface TagProps {
  label: string;
}

function Tag({ label }: TagProps) {
  return (
    <div className="flex items-center justify-center gap-2.5 rounded bg-black-5 px-2 py-1">
      <span className="text-center text-sm font-semibold">{label}</span>
    </div>
  );
}

export default Tag;

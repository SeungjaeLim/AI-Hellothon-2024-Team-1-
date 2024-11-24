interface MemoryCardProps {
  date?: string;
  title: string;
  image: string;
  description: string;
}

function MemoryCard({ date, title, image, description }: MemoryCardProps) {
  return (
    <div className="flex w-full flex-col items-center gap-6 bg-black-1 py-6">
      <div className="flex w-full flex-col gap-2">
        {date && (
          <div className="w-fit rounded-lg bg-blue-main p-2.5 text-center text-sm font-semibold">
            {date} 만든 추억
          </div>
        )}
        <div className="text-xl font-semibold">{title}</div>
      </div>
      <img className="h-80 w-full object-cover" src={image} alt="Memory" />
      <p className="text-lg font-medium leading-8">{description}</p>
    </div>
  );
}

export default MemoryCard;

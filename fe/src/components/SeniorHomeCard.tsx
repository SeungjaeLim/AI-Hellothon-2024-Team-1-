import Button from "./Button";
import IconMaximize from "../assets/iconMaximize.svg?react";
import { Link } from "@tanstack/react-router";
import Tag from "./Tag";

interface SeniorHomeCardProps {
  title: string;
  tags: string[];
  image: string;
  cardId: string;
}

function SeniorHomeCard({ title, tags, image, cardId }: SeniorHomeCardProps) {
  return (
    <div className="flex flex-col gap-1 space-y-4 rounded-xl bg-black-1 px-6 py-5">
      <div className="flex flex-col gap-8">
        <div className="text-xl font-semibold">{title}</div>
        <div className="flex items-end justify-between">
          <div className="flex space-x-2">
            {tags.map((tag, index) => (
              <Tag key={index} label={tag} />
            ))}
          </div>
          <Link to={`/senior/memories?id=${cardId}`}>
            <Button icon={<IconMaximize />} variant="primary" size="sm">
              기록보기
            </Button>
          </Link>
        </div>
      </div>
      <img
        src={image}
        alt={title}
        className="h-48 w-full rounded-lg object-cover"
      />
    </div>
  );
}

export default SeniorHomeCard;

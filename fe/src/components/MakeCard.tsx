import { Checkbox } from "antd";

interface MakeCardProps {
  questionNumber: number;
  question: string;
  questionId: number;
  isSelected: boolean;
  onSelect: (id: number) => void;
}

const MakeCard = ({
  questionNumber,
  question,
  questionId,
  isSelected,
  onSelect,
}: MakeCardProps) => {
  return (
    <div className="inline-flex items-start justify-end gap-4 rounded-xl bg-black-3 p-5">
      <Checkbox
        checked={isSelected}
        onChange={() => onSelect(questionId)}
        style={{
          transform: "scale(1.5)",
          marginRight: "12px",
        }}
      />
      <div className="inline-flex flex-1 flex-col items-start justify-start gap-4">
        <div className="text-black self-stretch text-base font-semibold">
          질문{questionNumber}. <br />
          {question}
        </div>
      </div>
    </div>
  );
};

export default MakeCard;

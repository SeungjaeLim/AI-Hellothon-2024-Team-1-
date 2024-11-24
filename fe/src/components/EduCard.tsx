interface EduCardProps {
  questionNumber: number;
  question: string;
  answer: string;
}

const EduCard = ({ questionNumber, question, answer }: EduCardProps) => {
  return (
    <div className="inline-flex flex-col items-start justify-start gap-5">
      <div className="flex flex-col items-start justify-center gap-6 self-stretch rounded-xl bg-black-3 px-6 py-5">
        <div className="flex flex-col items-start justify-center gap-2 self-stretch">
          <div className="self-stretch text-lg font-medium">
            질문 {questionNumber}.
            <br />
            {question}
          </div>
        </div>
        <div className="flex flex-col items-start justify-center gap-2 self-stretch">
          <div>
            <span className="text-base font-bold text-blue-highlight">샘</span>
            <span className="text-base font-bold">에서 기록한 내용</span>
          </div>
          <div className="self-stretch text-base font-normal leading-relaxed">
            {answer}
          </div>
        </div>
      </div>
    </div>
  );
};

export default EduCard;

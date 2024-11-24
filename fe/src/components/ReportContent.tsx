interface ReportContentProps {
  questionNumber: number;
  question: string;
  similarity: number;
  ssamAnswer: string;
  samAnswer: string;
}

const ReportContent = ({
  questionNumber,
  question,
  similarity,
  ssamAnswer,
  samAnswer,
}: ReportContentProps) => {
  return (
    <div className="inline-flex flex-col items-start justify-start gap-5">
      <div className="flex flex-col items-start justify-center gap-6 self-stretch rounded-xl bg-black-3 px-6 py-5">
        <div className="flex flex-col items-start justify-center gap-2 self-stretch">
          <div className="text-black self-stretch text-lg font-medium">
            질문 {questionNumber} {question}
          </div>
          <div className="inline-flex items-center justify-center gap-2.5 rounded bg-[#ffe2e2] px-2 py-1">
            <div className="text-center">
              <span className="text-black text-base font-medium">유사도 </span>
              <span className="text-base font-semibold text-red-system">
                {similarity}%
              </span>
            </div>
          </div>
        </div>

        <div className="flex flex-col items-start justify-center gap-2 self-stretch">
          <div>
            <span className="text-base font-bold text-blue-highlight">샘</span>
            <span className="text-base font-bold">에서 기록한 내용</span>
          </div>
          <div className="self-stretch text-base font-normal leading-relaxed">
            {samAnswer}
          </div>
        </div>

        <div className="flex flex-col items-start justify-center gap-2 self-stretch">
          <div>
            <span className="text-base font-bold text-[#cc196e]">쌤</span>
            <span className="text-base font-bold">에서 답변한 내용</span>
          </div>
          <div className="self-stretch text-base font-normal leading-relaxed">
            {ssamAnswer}
          </div>
        </div>
      </div>
    </div>
  );
};

export default ReportContent;

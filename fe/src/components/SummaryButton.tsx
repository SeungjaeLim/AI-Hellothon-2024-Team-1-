import IconArrowCircleRight from "../assets/iconArrowCircleRight.svg?react";

interface SummaryButtonProps {
  onClick: () => void;
}

function SummaryButton({ onClick }: SummaryButtonProps) {
  return (
    <button
      onClick={onClick}
      className="inline-flex h-32 w-full flex-col items-center justify-center gap-1 rounded-xl bg-blue-main"
    >
      <div className="inline-flex items-center justify-start gap-2">
        <span className="text-black text-center text-base font-bold">
          오늘 활동 끝내기
        </span>
        <IconArrowCircleRight />
      </div>
      <div className="text-black text-center text-base font-normal">
        <p>이번 활동도 고생 많으셨습니다.</p>
      </div>
    </button>
  );
}

export default SummaryButton;

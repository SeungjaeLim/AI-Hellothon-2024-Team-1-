import IconArrowCircleRight from "../assets/iconArrowCircleRight.svg?react";
import Loading from "./Loading";

interface MemoFinishButtonProps {
  onClick: () => void;
  isLoading: boolean;
}

function MemoFinishButton({ onClick, isLoading }: MemoFinishButtonProps) {
  return (
    <div
      onClick={onClick}
      className="inline-flex h-32 w-full cursor-pointer flex-col items-center justify-center gap-1 rounded-xl bg-blue-main"
    >
      {isLoading ? (
        <Loading />
      ) : (
        <>
          <div className="inline-flex items-center justify-start gap-2">
            <div className="text-black text-center text-base font-bold">
              오늘 기록한 내용으로 추억만들기
            </div>
            <IconArrowCircleRight />
          </div>
          <div className="text-black text-center text-base font-normal">
            인공지능이 기록을 정리해 <br />
            추억을 만들어드려요
          </div>
        </>
      )}
    </div>
  );
}

export default MemoFinishButton;

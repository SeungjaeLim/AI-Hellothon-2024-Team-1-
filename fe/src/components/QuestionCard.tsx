import BorderButton from "./BorderButton";
import IconMic from "../assets/iconMic.svg?react";
import IconPower from "../assets/iconPower.svg?react";
import IconRefresh from "../assets/iconRefresh.svg?react";
import IconVolume from "../assets/iconVolume.svg?react";
import Loading from "./Loading";

interface QuestionCardProps {
  questionNumber: number;
  question: string;
  isRecording: boolean;
  isLoading: boolean;
  onRefreshQuestion: () => void;
  onReadQuestion: () => void;
  onStartRecording: () => void;
  onEndRecording: () => void;
}

function QuestionCard({
  questionNumber,
  question,
  isRecording,
  isLoading,
  onRefreshQuestion,
  onReadQuestion,
  onStartRecording,
  onEndRecording,
}: QuestionCardProps) {
  return (
    <div className="flex flex-col gap-4 rounded-xl bg-yellow-main px-6 py-5">
      <p className="text-center text-lg font-bold">질문 {questionNumber}</p>
      <p className="text-center text-xl">
        {isLoading ? <Loading /> : question}
      </p>
      <div className="flex flex-col items-center justify-center gap-3 px-8">
        <div className="flex w-full gap-4">
          <BorderButton
            text={"다른 질문 만들어줘"}
            onClick={onRefreshQuestion}
            icon={<IconRefresh />}
          />
          <BorderButton
            text={"질문 읽어줘"}
            onClick={onReadQuestion}
            icon={<IconVolume />}
          />
        </div>
        {!isRecording && (
          <BorderButton
            className="w-full"
            text={"기록 시작하기"}
            onClick={onStartRecording}
            icon={<IconMic />}
          />
        )}
        {isRecording && (
          <BorderButton
            className="w-full"
            text={"기록 종료하기"}
            onClick={onEndRecording}
            icon={<IconPower />}
          />
        )}
      </div>
    </div>
  );
}

export default QuestionCard;

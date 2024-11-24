import IconArrowLeft from "../assets/iconArrowLeft.svg?react";
import { Modal } from "antd";
import { useNavigate } from "@tanstack/react-router";

interface BeforeHeaderProps {
  isModalActive?: boolean;
  to: string;
  text?: string;
}

function BeforeHeader({
  isModalActive = false,
  to,
  text = "메인화면으로 돌아가기",
}: BeforeHeaderProps) {
  const navigate = useNavigate();

  const handleBackClick = (e: React.MouseEvent) => {
    e.preventDefault();
    if (isModalActive) {
      Modal.confirm({
        title: "정말 나가시겠습니까?",
        content: "지금 나가면 기록이 저장되지 않고 종료됩니다.",
        okText: "나가기",
        cancelText: "계속 기록하기",
        onOk: () => navigate({ to }),
      });
    } else {
      navigate({ to });
    }
  };

  return (
    <header className="inline-flex flex-col items-start justify-start gap-4">
      <button
        onClick={handleBackClick}
        className="inline-flex items-center justify-center gap-1 px-2 py-1"
      >
        <IconArrowLeft />
        <span className="p-2 text-center text-base font-medium leading-loose">
          {text}
        </span>
      </button>
    </header>
  );
}

export default BeforeHeader;

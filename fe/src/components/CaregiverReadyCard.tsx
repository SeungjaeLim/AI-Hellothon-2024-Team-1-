import IconFilePlus from "../assets/iconFilePlus.svg?react";
import IconFileSearch from "../assets/iconFileSearch.svg?react";
import MemoryCard from "./MemoryCard";
import { Modal } from "antd";
import ReportButton from "./ReportButton";
import { useNavigate } from "@tanstack/react-router";
import { useState } from "react";

interface CaregiverReadyCardProps {
  recordId: string;
  title: string;
  tags: string[];
  isRecommended?: boolean;
  content: string;
  image: string;
  userId: string;
}

const CaregiverReadyCard = ({
  recordId,
  title,
  tags,
  isRecommended,
  content,
  image,
  userId,
}: CaregiverReadyCardProps) => {
  const navigate = useNavigate();
  const [isModalOpen, setIsModalOpen] = useState(false);

  const showModal = () => {
    setIsModalOpen(true);
  };

  const handleOk = () => {
    setIsModalOpen(false);
  };

  const handleCancel = () => {
    setIsModalOpen(false);
  };

  return (
    <>
      <div className="flex w-full flex-col items-start justify-center gap-6 rounded-xl bg-black-3 px-6 py-5">
        <div className="flex w-full flex-col items-start justify-center gap-3">
          {isRecommended && (
            <div className="inline-flex items-center justify-start gap-2.5 rounded bg-[#fdd7ab] px-2 py-1">
              <div className="text-center text-sm font-medium">
                교안에 적합한 기록이에요!
              </div>
            </div>
          )}
          <div className="self-stretch text-xl font-semibold">{title}</div>
          <div className="flex flex-wrap gap-2">
            {tags.map((tag, index) => (
              <div
                key={index}
                className="flex items-center justify-center gap-2.5 rounded bg-black-5 px-2 py-1"
              >
                <div className="text-center text-sm font-semibold">{tag}</div>
              </div>
            ))}
          </div>
        </div>
        <div className="inline-flex w-full items-start justify-start gap-3">
          <ReportButton
            size="grow"
            text="기록 보기"
            icon={<IconFileSearch />}
            onClick={showModal}
          />
          <ReportButton
            size="grow"
            text="교안 만들기"
            icon={<IconFilePlus />}
            onClick={() =>
              navigate({
                to: "/caregiver/create",
                search: { id: recordId, userId },
              })
            }
          />
        </div>
      </div>
      <Modal
        open={isModalOpen}
        onOk={handleOk}
        onCancel={handleCancel}
        cancelButtonProps={{ style: { display: "none" } }}
      >
        <div className="flex flex-col items-center">
          <div className="w-full">
            <MemoryCard title={title} image={image} description={content} />
          </div>
        </div>
      </Modal>
    </>
  );
};

export default CaregiverReadyCard;

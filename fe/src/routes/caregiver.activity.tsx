import { Link, createFileRoute } from "@tanstack/react-router";

import BeforeHeader from "../components/BeforeHeader";
import BorderButton from "../components/BorderButton";
import { CAREGIVER_TABS } from "../constants/tabs";
import EduCard from "../components/EduCard";
import IconChevron from "../assets/iconChevron.svg?react";
import { Question } from "../types";
import Tabs from "../components/Tabs";
import { useCaregiverMemoStore } from "../stores/caregiverMemoStore";
import { useQuery } from "@tanstack/react-query";
import { useUser } from "../hooks/useUser";

export const Route = createFileRoute("/caregiver/activity")({
  component: CaregiverActivity,
});

const fetchQuestions = async (id: string): Promise<Question[]> => {
  const response = await fetch(
    `https://fjtskwttcrchrywg.tunnel-pt.elice.io/guides/${id}/questions`,
  );
  if (!response.ok) {
    throw new Error("Network response was not ok");
  }
  return response.json();
};

function CaregiverActivity() {
  const { id, userId }: { id: string; userId: string } = Route.useSearch();
  const { data: userData } = useUser(userId);
  const { setQuestions } = useCaregiverMemoStore();

  const {
    data: questions = [],
    isLoading,
    error,
  } = useQuery({
    queryKey: ["questions", id],
    queryFn: () => fetchQuestions(id),
  });

  const handleStartActivity = () => {
    setQuestions(questions);
  };

  if (isLoading) return <div>로딩중...</div>;
  if (error) return <div>에러가 발생했습니다</div>;

  return (
    <div>
      <BeforeHeader to={"/caregiver/home"} />
      <Tabs
        title={userData?.name}
        subtitle="님"
        activeTab="3"
        items={CAREGIVER_TABS.map((tab) => ({
          ...tab,
        }))}
      />
      <div className="mt-6 flex flex-col gap-5">
        <Link
          to={`/caregiver/record`}
          search={{ id, userId }}
          onClick={handleStartActivity}
        >
          <BorderButton
            text="인지활동 시작하기"
            icon={<IconChevron />}
            className="w-full"
          />
        </Link>
        {questions.map((question, index) => (
          <EduCard
            key={question.id}
            questionNumber={index + 1}
            question={question.text}
            answer={question.first_answer?.response || "아직 답변이 없습니다."}
          />
        ))}
      </div>
    </div>
  );
}

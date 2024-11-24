import { Form, Input, Modal } from "antd";
import { createFileRoute, useNavigate } from "@tanstack/react-router";

import BeforeHeader from "../components/BeforeHeader";
import BorderButton from "../components/BorderButton";
import { CAREGIVER_TABS } from "../constants/tabs";
import IconCheckSquare from "../assets/iconCheckSquare.svg?react";
import IconEdit from "../assets/iconEdit.svg?react";
import Loading from "../components/Loading";
import MakeCard from "../components/MakeCard";
import { Question } from "../types";
import Tabs from "../components/Tabs";
import { useQuery } from "@tanstack/react-query";
import { useState } from "react";
import { useUser } from "../hooks/useUser";

export const Route = createFileRoute("/caregiver/create")({
  component: CaregiverCreate,
});

function CaregiverCreate() {
  const { id, userId }: { id: string; userId: string } = Route.useSearch();
  const navigate = useNavigate();
  const [isModalOpen, setIsModalOpen] = useState(false);
  const [form] = Form.useForm();
  const [selectedQuestions, setSelectedQuestions] = useState<number[]>([]);
  const { data: userData } = useUser(userId);

  const {
    data: questions,
    isLoading,
    refetch,
  } = useQuery({
    queryKey: ["questions", id],
    queryFn: async () => {
      const response = await fetch(
        `https://fjtskwttcrchrywg.tunnel-pt.elice.io/questions/record/${id}/questions`,
      );
      if (!response.ok) {
        throw new Error("Failed to fetch questions");
      }
      return response.json() as Promise<Question[]>;
    },
  });

  const handleAddQuestion = async (values: { question: string }) => {
    try {
      const response = await fetch(
        `https://fjtskwttcrchrywg.tunnel-pt.elice.io/questions/?record_id=${id}`,
        {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
          },
          body: JSON.stringify({
            text: values.question,
          }),
        },
      );

      if (!response.ok) {
        throw new Error("Failed to add question");
      }

      setIsModalOpen(false);
      form.resetFields();
      refetch();
    } catch (error) {
      console.error("Error adding question:", error);
    }
  };

  const handleQuestionSelect = (questionId: number) => {
    setSelectedQuestions((prev) =>
      prev.includes(questionId)
        ? prev.filter((id) => id !== questionId)
        : [...prev, questionId],
    );
  };

  const handleConfirm = async () => {
    if (selectedQuestions.length === 0) {
      Modal.warning({ title: "질문을 선택해주세요." });
      return;
    }

    try {
      const response = await fetch(
        "https://fjtskwttcrchrywg.tunnel-pt.elice.io/guides/create_with_questions",
        {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
          },
          body: JSON.stringify({
            elder_id: 1,
            title: "새로운 교안",
            question_ids: selectedQuestions,
          }),
        },
      );

      if (!response.ok) {
        throw new Error("Failed to create guide");
      }

      const data = await response.json();
      navigate({
        to: "/caregiver/activity",
        search: { id: data.id.toString(), userId },
      });
    } catch (error) {
      console.error("Error creating guide:", error);
      Modal.error({ title: "교안 생성에 실패했습니다." });
    }
  };

  if (isLoading) {
    return <Loading />;
  }

  return (
    <div>
      <BeforeHeader to={"/caregiver/home"} />
      <Tabs
        title={userData?.name}
        subtitle="님"
        activeTab="2"
        items={CAREGIVER_TABS.map((tab) => ({
          ...tab,
        }))}
      />
      <div className="mt-6 flex flex-col gap-5">
        {questions?.map((question, index) => (
          <MakeCard
            key={question.id}
            questionNumber={index + 1}
            question={question.text}
            questionId={question.id}
            isSelected={selectedQuestions.includes(question.id)}
            onSelect={handleQuestionSelect}
          />
        ))}

        <BorderButton
          text="직접 질문 추가하기"
          icon={<IconEdit />}
          onClick={() => setIsModalOpen(true)}
        />
        <BorderButton
          text="이 교안으로 확정하기"
          icon={<IconCheckSquare />}
          onClick={() => handleConfirm()}
        />
      </div>

      <Modal
        title="질문 추가하기"
        open={isModalOpen}
        onCancel={() => setIsModalOpen(false)}
        footer={null}
      >
        <Form form={form} onFinish={handleAddQuestion} layout="vertical">
          <Form.Item
            name="question"
            rules={[{ required: true, message: "질문을 입력해주세요" }]}
          >
            <Input placeholder="질문을 입력해주세요" size="large" />
          </Form.Item>
          <Form.Item>
            <BorderButton text="추가하기" className="w-full" />
          </Form.Item>
        </Form>
      </Modal>
    </div>
  );
}

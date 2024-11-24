import { fetchFollowUpQuestion, fetchRandomQuestion } from "../apis";

import { Question } from "../types";
import { useQuery } from "@tanstack/react-query";

interface UseQuestionProps {
  elderId: string;
  questionNumber: number;
  answeredQuestionIds: number[];
  onQuestionFetched: (question: Question) => void;
}

export const useQuestion = ({
  elderId,
  questionNumber,
  answeredQuestionIds,
  onQuestionFetched,
}: UseQuestionProps) => {
  return useQuery({
    queryKey: ["question", questionNumber, answeredQuestionIds],
    queryFn: async () => {
      const question =
        questionNumber === 1
          ? await fetchRandomQuestion()
          : await fetchFollowUpQuestion(elderId, answeredQuestionIds);
      onQuestionFetched(question);
      return question;
    },
  });
};

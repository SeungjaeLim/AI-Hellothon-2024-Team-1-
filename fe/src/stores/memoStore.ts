import { AnswerResponse, Question } from "../types";

import { create } from "zustand";
import { devtools } from "zustand/middleware";

interface Answer extends AnswerResponse {
  question: Question;
}

interface MemoState {
  questions: Question[];
  currentQuestion: Question | null;
  answers: Answer[];
  setCurrentQuestion: (question: Question) => void;
  addAnswer: (answer: AnswerResponse) => void;
  resetAnswers: () => void;
  addQuestion: (question: Question) => void;
  answeredQuestionIds: number[];
  addAnsweredQuestionId: (questionId: number) => void;
  clearAnsweredQuestionIds: () => void;
  currentQuestionNumber: number;
  incrementQuestionNumber: () => void;
  resetQuestionNumber: () => void;
}

export const useMemoStore = create<MemoState>()(
  devtools((set, get) => ({
    questions: [],
    currentQuestion: null,
    answers: [],
    setCurrentQuestion: (question) => {
      const currentQuestion = get().currentQuestion;
      if (currentQuestion?.id === question.id) return;
      set({ currentQuestion: question });
    },
    addAnswer: (answer) =>
      set((state) => ({
        answers: [
          ...state.answers,
          {
            ...answer,
            question: state.currentQuestion!,
          },
        ],
      })),
    resetAnswers: () => set({ answers: [] }),
    addQuestion: (question) =>
      set((state) => ({ questions: [...state.questions, question] })),
    answeredQuestionIds: [],
    addAnsweredQuestionId: (questionId) =>
      set((state) => ({
        answeredQuestionIds: [...state.answeredQuestionIds, questionId],
      })),
    clearAnsweredQuestionIds: () => set({ answeredQuestionIds: [] }),
    currentQuestionNumber: 1,
    incrementQuestionNumber: () =>
      set((state) => ({
        currentQuestionNumber: state.currentQuestionNumber + 1,
      })),
    resetQuestionNumber: () => set({ currentQuestionNumber: 1 }),
  })),
);

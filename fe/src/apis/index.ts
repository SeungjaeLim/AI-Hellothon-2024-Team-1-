import {
  AnswerResponse,
  Question,
  RecordResponse,
  UserResponse,
} from "../types";

const BASE_URL = "https://fjtskwttcrchrywg.tunnel-pt.elice.io";

export const fetchUser = async (userId: string): Promise<UserResponse> => {
  try {
    const response = await fetch(`${BASE_URL}/elders/${userId}`);
    if (!response.ok) {
      throw new Error(
        `서버 오류가 발생했습니다. (상태 코드: ${response.status})`,
      );
    }
    return response.json();
  } catch (error) {
    throw new Error(
      `사용자 정보를 가져오는데 실패했습니다: ${
        error instanceof Error
          ? error.message
          : "알 수 없는 오류가 발생했습니다"
      }`,
    );
  }
};

export const fetchUserRecords = async (
  userId: string,
): Promise<RecordResponse[]> => {
  try {
    const response = await fetch(`${BASE_URL}/records/user/${userId}`);
    if (!response.ok) {
      throw new Error(
        `서버 오류가 발생했습니다. (상태 코드: ${response.status})`,
      );
    }
    return response.json();
  } catch (error) {
    throw new Error(
      `사용자의 기록을 가져오는데 실패했습니다: ${
        error instanceof Error
          ? error.message
          : "알 수 없는 오류가 발생했습니다"
      }`,
    );
  }
};

export const fetchRecord = async (
  recordId: string,
): Promise<RecordResponse> => {
  try {
    const response = await fetch(`${BASE_URL}/records/${recordId}`);
    if (!response.ok) {
      throw new Error(
        `서버 오류가 발생했습니다. (상태 코드: ${response.status})`,
      );
    }
    return response.json();
  } catch (error) {
    throw new Error(
      `기록 정보를 가져오는데 실패했습니다: ${
        error instanceof Error
          ? error.message
          : "알 수 없는 오류가 발생했습니다"
      }`,
    );
  }
};

export const fetchRandomQuestion = async (): Promise<Question> => {
  const response = await fetch(`${BASE_URL}/questions/random`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
  });
  if (!response.ok) {
    throw new Error("Failed to fetch question");
  }
  return response.json();
};

export const sendAnswerToServer = async (
  audioBlob: Blob,
  elderId: string,
  questionId: string,
): Promise<AnswerResponse> => {
  const formData = new FormData();
  formData.append("audio", audioBlob, "recording.wav");
  formData.append("elder_id", elderId);
  formData.append("question_id", questionId);

  const response = await fetch(`${BASE_URL}/answers/`, {
    method: "POST",
    body: formData,
  });

  if (!response.ok) {
    throw new Error("오디오 전송 실패");
  }

  return response.json();
};

export const createRecord = async (elderId: string, questionIds: number[]) => {
  const response = await fetch(`${BASE_URL}/records/`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({
      elder_id: elderId,
      question_ids: questionIds,
    }),
  });

  if (!response.ok) {
    throw new Error("기록 생성 실패");
  }

  return response.json();
};

export const fetchFollowUpQuestion = async (
  elderId: string,
  questionIds: number[],
): Promise<Question> => {
  const response = await fetch(`${BASE_URL}/questions/generate_follow_up`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({
      elder_id: elderId,
      question_ids: questionIds,
    }),
  });

  if (!response.ok) {
    throw new Error("Failed to fetch follow-up question");
  }

  const data = await response.json();
  return {
    id: data.question_id,
    text: data.generated_question,
  };
};

export async function fetchQuestionTTS(questionId: string): Promise<Blob> {
  const response = await fetch(
    `https://fjtskwttcrchrywg.tunnel-pt.elice.io/questions/tts/${questionId}`,
  );
  if (!response.ok) {
    throw new Error("Failed to fetch TTS");
  }
  return await response.blob();
}

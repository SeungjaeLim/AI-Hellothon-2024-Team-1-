export interface UserResponse {
  name: string;
  birth_date: string;
  gender: "M" | "F";
  care_level: string;
  contact_info: string;
  id: number;
  created_at: string;
}

export interface RecordResponse {
  id: number;
  title: string;
  content: string;
  elder_id: number;
  created_at: string;
  image: string | null;
  keywords: string[];
}

export interface Question {
  text: string;
  id: number;
  created_at?: string;
  first_answer?: AnswerResponse;
}

export interface AnswerResponse {
  response: string;
  response_date: string;
  id: number;
  elder_id: number;
  question_id: number;
  created_at: string;
}

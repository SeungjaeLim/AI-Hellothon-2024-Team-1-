import { createFileRoute, useNavigate } from "@tanstack/react-router";
import { fetchQuestionTTS, sendAnswerToServer } from "../apis";
import { useEffect, useRef, useState } from "react";

import BeforeHeader from "../components/BeforeHeader";
import CareQuestionCard from "../components/CareQuestionCard";
import Loading from "../components/Loading";
import RecordedContent from "../components/RecordedContent";
import RecordingStatus from "../components/RecordingStatus";
import SummaryButton from "../components/SummaryButton";
import { useCaregiverMemoStore } from "../stores/caregiverMemoStore";

export const Route = createFileRoute("/caregiver/record")({
  component: CaregiverRecord,
});

function CaregiverRecord() {
  const navigate = useNavigate();
  const {
    questions,
    currentQuestion,
    setCurrentQuestion,
    addAnswer,
    addAnsweredQuestionId,
    answeredQuestionIds,
    currentQuestionNumber,
    incrementQuestionNumber,
  } = useCaregiverMemoStore();

  const { id, userId }: { id: string; userId: string } = Route.useSearch();
  const [recording, setRecording] = useState(false);
  const [recordedContent, setRecordedContent] = useState("");
  const [showRecordedContent, setShowRecordedContent] = useState(false);
  const [isLastQuestion, setIsLastQuestion] = useState(false);
  const mediaRecorderRef = useRef<MediaRecorder | null>(null);
  const audioChunksRef = useRef<Blob[]>([]);
  const recognitionRef = useRef<SpeechRecognition | null>(null);
  const audioRef = useRef<HTMLAudioElement | null>(null);
  const [currentTranscript, setCurrentTranscript] = useState("");
  const [previousTranscripts, setPreviousTranscripts] = useState("");

  useEffect(() => {
    if (currentQuestionNumber <= questions.length) {
      setCurrentQuestion(questions[currentQuestionNumber - 1]);
    }
  }, [currentQuestionNumber]);

  useEffect(() => {
    if ("webkitSpeechRecognition" in window) {
      const recognition = new webkitSpeechRecognition();
      recognition.continuous = true;
      recognition.interimResults = true;
      recognition.lang = "ko-KR";

      recognition.onresult = function (event: SpeechRecognitionEvent) {
        for (let i = event.resultIndex; i < event.results.length; i++) {
          const transcript = event.results[i][0].transcript;
          if (event.results[i].isFinal) {
            setPreviousTranscripts((prev) => prev + transcript + " ");
            setCurrentTranscript("");
          } else {
            setCurrentTranscript(transcript);
          }
        }
      };

      recognitionRef.current = recognition;
    }
  }, [recording]);

  useEffect(() => {
    if (currentQuestionNumber >= questions.length) {
      setIsLastQuestion(true);
    }
  }, [currentQuestionNumber, questions.length]);

  const startRecording = async () => {
    try {
      const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
      const mediaRecorder = new MediaRecorder(stream);
      mediaRecorderRef.current = mediaRecorder;
      audioChunksRef.current = [];

      mediaRecorder.ondataavailable = (event) => {
        if (event.data.size > 0) {
          audioChunksRef.current.push(event.data);
        }
      };

      mediaRecorder.start();
      recognitionRef.current?.start();
      setCurrentTranscript("");
      setPreviousTranscripts("");
      setRecording(true);
      setShowRecordedContent(false);
    } catch (err) {
      console.error("음성 녹음 시작 실패:", err);
    }
  };

  const stopRecording = async () => {
    if (!mediaRecorderRef.current) return;

    return new Promise<void>((resolve) => {
      recognitionRef.current?.stop();
      mediaRecorderRef.current!.onstop = async () => {
        const audioBlob = new Blob(audioChunksRef.current, {
          type: "audio/wav",
        });
        await sendAudioToServer(audioBlob);
        resolve();
      };

      mediaRecorderRef.current!.stop();
      mediaRecorderRef
        .current!.stream.getTracks()
        .forEach((track) => track.stop());
      setRecording(false);
      setShowRecordedContent(true);
    });
  };

  const sendAudioToServer = async (audioBlob: Blob) => {
    try {
      const result = await sendAnswerToServer(
        audioBlob,
        userId,
        currentQuestion?.id?.toString() || "1",
      );
      setRecordedContent(result.response);
      addAnswer(result);
      addAnsweredQuestionId(currentQuestion?.id || 0);
    } catch (err) {
      console.error("오디오 전송 중 에러:", err);
    }
  };

  const handleReadQuestion = async () => {
    if (!currentQuestion?.id) return;

    try {
      const audioBlob = await fetchQuestionTTS(currentQuestion.id.toString());
      const audioUrl = URL.createObjectURL(audioBlob);

      if (audioRef.current) {
        audioRef.current.src = audioUrl;
        await audioRef.current.play();

        audioRef.current.onended = () => {
          URL.revokeObjectURL(audioUrl);
        };
      } else {
        const audio = new Audio(audioUrl);
        audioRef.current = audio;
        await audio.play();

        audio.onended = () => {
          URL.revokeObjectURL(audioUrl);
        };
      }
    } catch (error) {
      console.error("질문 읽기 실패:", error);
      alert("질문을 읽을 수 없습니다.");
    }
  };

  const handleNextQuestion = () => {
    incrementQuestionNumber();
    setShowRecordedContent(false);
    setRecordedContent("");
  };

  const handleFinishActivity = async () => {
    try {
      await fetch(
        `https://fjtskwttcrchrywg.tunnel-pt.elice.io/guides/finish/${id}`,
        {
          method: "PATCH",
          headers: {
            "Content-Type": "application/json",
          },
          body: JSON.stringify({ answeredQuestionIds }),
        },
      );
      navigate({ to: "/caregiver/home" });
    } catch (error) {
      console.error("기록 생성 중 에러:", error);
      alert("기록 생성에 실패했습니다.");
    }
  };

  return (
    <div>
      <BeforeHeader
        to={`/caregiver/activity?id=${id}&userId=${userId}`}
        isModalActive
      />
      <div className="mt-6 flex flex-col gap-10">
        {!showRecordedContent && (
          <CareQuestionCard
            question={currentQuestion?.text || ""}
            questionNumber={currentQuestionNumber}
            isRecording={recording}
            isLoading={false}
            onReadQuestion={handleReadQuestion}
            onStartRecording={startRecording}
            onEndRecording={stopRecording}
          />
        )}
        {recording && (
          <RecordingStatus
            highlightedText={previousTranscripts}
            normalText={currentTranscript}
          />
        )}
        {showRecordedContent && (
          <RecordedContent
            content={recordedContent || <Loading />}
            question={currentQuestion?.text || ""}
            questionNumber={currentQuestionNumber}
            isLastQuestion={isLastQuestion}
            isSam={false}
            onRecordAgain={() => setShowRecordedContent(false)}
            onNextQuestion={handleNextQuestion}
          />
        )}
        {isLastQuestion && showRecordedContent && (
          <SummaryButton onClick={handleFinishActivity} />
        )}
      </div>
    </div>
  );
}

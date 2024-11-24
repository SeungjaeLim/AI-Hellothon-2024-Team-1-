import { createFileRoute, useNavigate } from "@tanstack/react-router";
import { createRecord, fetchQuestionTTS, sendAnswerToServer } from "../apis";
import { useEffect, useRef, useState } from "react";

import BeforeHeader from "../components/BeforeHeader";
import Loading from "../components/Loading";
import { MEMORY_TABS } from "../constants/tabs";
import MemoFinishButton from "../components/MemoFinishButton";
import QuestionCard from "../components/QuestionCard";
import RecordedContent from "../components/RecordedContent";
import RecordingStatus from "../components/RecordingStatus";
import Tabs from "../components/Tabs";
import { useMemoStore } from "../stores/memoStore";
import { useQuestion } from "../hooks/useQuestion";

export const Route = createFileRoute("/senior/record")({
  component: SeniorRecord,
});

function SeniorRecord() {
  const navigate = useNavigate();
  const {
    currentQuestion,
    setCurrentQuestion,
    answers,
    addAnswer,
    addAnsweredQuestionId,
    answeredQuestionIds,
    clearAnsweredQuestionIds,
    currentQuestionNumber,
    incrementQuestionNumber,
    resetQuestionNumber,
  } = useMemoStore();

  const { id }: { id: string } = Route.useSearch();
  const [recording, setRecording] = useState(false);
  const [recordedContent, setRecordedContent] = useState("");
  const [showRecordedContent, setShowRecordedContent] = useState(false);
  const [isResultLoading, setResultLoading] = useState(false);
  const recognitionRef = useRef<SpeechRecognition | null>(null);
  const mediaRecorderRef = useRef<MediaRecorder | null>(null);
  const audioChunksRef = useRef<Blob[]>([]);
  const audioRef = useRef<HTMLAudioElement | null>(null);
  const [currentTranscript, setCurrentTranscript] = useState("");
  const [previousTranscripts, setPreviousTranscripts] = useState("");

  const { isLoading, refetch } = useQuestion({
    elderId: id,
    questionNumber: currentQuestionNumber,
    answeredQuestionIds,
    onQuestionFetched: setCurrentQuestion,
  });

  useEffect(() => {
    setResultLoading(false);

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

      recognition.onerror = function (event: SpeechRecognitionErrorEvent) {
        console.error("음성 인식 에러:", event.error);
      };

      recognition.onend = () => {
        if (recording) {
          console.log("음성 인식 재시작");
          recognition.start();
        }
      };

      recognitionRef.current = recognition;
    }
  }, [recording]);

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
        id,
        currentQuestion?.id?.toString() || "1",
      );
      setRecordedContent(result.response);
      addAnswer(result);
      addAnsweredQuestionId(currentQuestion?.id || 0);
    } catch (err) {
      console.error("오디오 전송 중 에러:", err);
    }
  };

  const handleStartRecording = () => {
    startRecording();
  };

  const handleStopRecording = () => {
    stopRecording();
  };

  const handleRecordAgain = () => {
    setRecording(true);
    setShowRecordedContent(false);
  };

  const handleRefreshQuestion = () => refetch();
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

  const handleNextQuestion = async () => {
    try {
      setShowRecordedContent(false);
      setRecordedContent("");
      incrementQuestionNumber();
      const result = await refetch();
      if (!result.isSuccess) {
        throw new Error("Failed to fetch next question");
      }
    } catch (error) {
      console.error("다음 질문 불러오기 실패:", error);
    }
  };
  const handleFinishMemo = async () => {
    try {
      setResultLoading(true);
      const responseJson = await createRecord(id, answeredQuestionIds);
      resetQuestionNumber();
      clearAnsweredQuestionIds();
      navigate({ to: `/senior/memories?id=${responseJson.id}` });
    } catch (error) {
      console.error("기록 생성 중 에러:", error);
      alert("기록 생성에 실패했습니다.");
    }
  };

  return (
    <div>
      <BeforeHeader to={"/senior/home"} isModalActive={true} />
      <Tabs
        activeTab="1"
        items={MEMORY_TABS.map((tab) => ({
          ...tab,
        }))}
      />
      <div className="mt-6 flex flex-col gap-10">
        {!showRecordedContent && (
          <QuestionCard
            questionNumber={currentQuestionNumber}
            question={`${currentQuestion?.text ?? ""}`}
            isRecording={recording}
            isLoading={isLoading}
            onRefreshQuestion={handleRefreshQuestion}
            onReadQuestion={handleReadQuestion}
            onStartRecording={handleStartRecording}
            onEndRecording={handleStopRecording}
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
            questionNumber={currentQuestionNumber}
            question={
              answers[currentQuestionNumber - 1]?.question.text ||
              currentQuestion?.text ||
              ""
            }
            isSam={true}
            onRecordAgain={handleRecordAgain}
            onNextQuestion={handleNextQuestion}
          />
        )}
        {showRecordedContent && (
          <MemoFinishButton
            onClick={handleFinishMemo}
            isLoading={isResultLoading}
          />
        )}
      </div>
    </div>
  );
}

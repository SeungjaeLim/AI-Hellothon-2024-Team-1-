import BeforeHeader from "../components/BeforeHeader";
import Loading from "../components/Loading";
import ReportContent from "../components/ReportContent";
import Tabs from "../components/Tabs";
import { createFileRoute } from "@tanstack/react-router";
import { useQuery } from "@tanstack/react-query";
import { useUser } from "../hooks/useUser";

interface Analysis {
  id: number;
  question_id: number;
  question: string;
  first_answer_id: number;
  first_answer: string;
  last_answer_id: number;
  last_answer: string;
  similarity: number;
  report_id: number;
  created_at: string;
}

interface Report {
  id: number;
  elder_id: number;
  year: number;
  week_number: number;
  created_at: string;
  analyses: Analysis[];
}

export const Route = createFileRoute("/caregiver/report")({
  component: CaregiverReport,
});

const fetchReports = async (elderId: string): Promise<Report[]> => {
  const response = await fetch(
    `https://fjtskwttcrchrywg.tunnel-pt.elice.io/reports/?elder_id=${elderId}&year=2024&week_number=47`,
    {
      method: "POST",
    },
  );
  return response.json();
};

function CaregiverReport() {
  const { trial, id }: { trial: string; id: string } = Route.useSearch();
  const { data: userData } = useUser(id);
  const { data: reports = [], isLoading } = useQuery({
    queryKey: ["reports", id],
    queryFn: () => fetchReports(id),
  });

  if (isLoading) {
    return <Loading />;
  }

  const currentReport = reports.find(
    (_, index) => index === parseInt(trial) - 1,
  );

  return (
    <div>
      <BeforeHeader to={"/caregiver/home"} />
      <Tabs
        title={userData?.name}
        subtitle="님 주간보고서 (24.11.18 ~ 24.11.24)"
        activeTab={trial}
        items={reports.slice(0, 3).map((_, index) => ({
          id: (index + 1).toString(),
          title: `${index + 1}회차`,
          subtitle: `${new Date(reports[index].created_at).getMonth() + 1}.${new Date(reports[index].created_at).getDate()}`,
          path: `?trial=${index + 1}&id=${id}`,
        }))}
      />
      <div className="mt-6 flex flex-col gap-5">
        {currentReport?.analyses.map((analysis, index) => (
          <ReportContent
            key={analysis.id}
            questionNumber={index + 1}
            question={analysis.question}
            similarity={analysis.similarity}
            ssamAnswer={analysis.first_answer}
            samAnswer={analysis.last_answer}
          />
        ))}
      </div>
    </div>
  );
}

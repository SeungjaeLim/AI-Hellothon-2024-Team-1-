import CaregiverHomeCard from "../components/CaregiverHomeCard";
import Header from "../components/Header";
import ThisWeek from "../components/ThisWeek";
import { createLazyFileRoute } from "@tanstack/react-router";
import { useQuery } from "@tanstack/react-query";

interface ElderResponse {
  id: number;
  name: string;
  birth_date: string;
  gender: string;
  care_level: string;
  contact_info: string;
  created_at: string;
}

interface TaskResponse {
  id: number;
  elder_id: number;
  status: number;
  created_at: string;
  year: number;
  week_number: number;
  iteration: number;
}

const getAllElders = async () => {
  const response = await fetch(
    "https://fjtskwttcrchrywg.tunnel-pt.elice.io/elders/",
  );

  const data: ElderResponse[] = await response.json();
  return data.map((elder) => ({
    id: elder.id,
    name: elder.name,
    age: new Date().getFullYear() - new Date(elder.birth_date).getFullYear(),
    gender: elder.gender === "M" ? "남" : "여",
    currentSession: 1,
    totalSessions: 3,
    progress: {
      recordPrep: false,
      materialPrep: false,
      education: false,
    },
  }));
};

const getThisWeekTasks = async (): Promise<TaskResponse[]> => {
  const response = await fetch(
    "https://fjtskwttcrchrywg.tunnel-pt.elice.io/tasks/this_week",
  );
  return await response.json();
};

export const Route = createLazyFileRoute("/caregiver/home")({
  component: CaregiverHome,
});

function CaregiverHome() {
  const { data: elders = [] } = useQuery({
    queryKey: ["elders"],
    queryFn: getAllElders,
  });

  const { data: tasks = [] } = useQuery({
    queryKey: ["thisWeekTasks"],
    queryFn: getThisWeekTasks,
  });

  const eldersWithProgress = elders.map((elder) => {
    const elderTask = tasks.find((task) => task.elder_id === elder.id);
    if (!elderTask) return elder;

    return {
      ...elder,
      progress: {
        recordPrep: elderTask.status >= 1,
        materialPrep: elderTask.status >= 2,
        education: elderTask.status >= 3,
      },
      currentSession: elderTask.iteration,
    };
  });

  return (
    <div>
      <Header userName="영숙" userAvatar="/assets/avatar.png" />
      <main className="flex flex-col items-end gap-6">
        <ThisWeek startDate="24.11.18" endDate="24.11.24" />
        {eldersWithProgress.map((user) => (
          <CaregiverHomeCard
            key={user.id}
            userId={user.id}
            name={user.name}
            age={user.age}
            gender={user.gender}
            currentSession={user.currentSession}
            totalSessions={user.totalSessions}
            progress={user.progress}
          />
        ))}
      </main>
    </div>
  );
}

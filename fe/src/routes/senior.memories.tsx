import BeforeHeader from "../components/BeforeHeader";
import Loading from "../components/Loading";
import { MEMORY_TABS } from "../constants/tabs";
import MemoryCard from "../components/MemoryCard";
import Tabs from "../components/Tabs";
import { createFileRoute } from "@tanstack/react-router";
import { formatDate } from "../utils";
import { useRecord } from "../hooks/useRecord";

export const Route = createFileRoute("/senior/memories")({
  component: SeniorMemories,
});

function SeniorMemories() {
  const { id }: { id: string } = Route.useSearch();
  const { data, isLoading } = useRecord(id);

  if (isLoading) {
    <Loading />;
  }

  return (
    <div>
      <BeforeHeader to={"/senior/home"} />
      <Tabs
        activeTab="2"
        items={MEMORY_TABS.map((tab) => ({
          ...tab,
        }))}
      />
      <div className="mt-4 flex flex-col items-center">
        <div className="w-full">
          {data ? (
            <MemoryCard
              date={formatDate(data.created_at)}
              title={data.title}
              image={`https://fjtskwttcrchrywg.tunnel-pt.elice.io${data.image}`}
              description={data.content}
            />
          ) : (
            <div className="text-center">아직 추억이 없네요.</div>
          )}
        </div>
      </div>
    </div>
  );
}

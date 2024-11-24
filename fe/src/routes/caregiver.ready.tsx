import { useEffect, useState } from "react";

import BeforeHeader from "../components/BeforeHeader";
import { CAREGIVER_TABS } from "../constants/tabs";
import CaregiverReadyCard from "../components/CaregiverReadyCard";
import { RecordResponse } from "../types";
import Tabs from "../components/Tabs";
import { createFileRoute } from "@tanstack/react-router";
import { useUser } from "../hooks/useUser";

export const Route = createFileRoute("/caregiver/ready")({
  component: CaregiverReady,
});

function CaregiverReady() {
  const { id }: { id: string } = Route.useSearch();
  const [records, setRecords] = useState<RecordResponse[]>([]);
  const { data: userData } = useUser(id);

  useEffect(() => {
    fetchRecords();
  }, []);

  const fetchRecords = async () => {
    try {
      const response = await fetch(
        `https://fjtskwttcrchrywg.tunnel-pt.elice.io/records/user/${id}`,
      );
      const data = await response.json();
      setRecords(data);
    } catch (error) {
      console.error("Error fetching records:", error);
    }
  };

  return (
    <div>
      <BeforeHeader to={"/caregiver/home"} />
      <Tabs
        title={userData?.name}
        subtitle="님"
        activeTab="1"
        items={CAREGIVER_TABS.map((tab) => ({
          ...tab,
        }))}
      />
      <div className="mt-6 flex flex-col gap-5">
        {records.map((record) => (
          <CaregiverReadyCard
            key={record.id}
            recordId={String(record.id)}
            title={record.title}
            userId={String(record.elder_id)}
            tags={record.keywords.slice(0, 3)}
            content={record.content}
            image={`https://fjtskwttcrchrywg.tunnel-pt.elice.io${record.image}`}
          />
        ))}
      </div>
    </div>
  );
}

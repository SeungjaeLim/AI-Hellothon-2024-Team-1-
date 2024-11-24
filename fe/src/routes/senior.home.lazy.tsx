import { Link, createLazyFileRoute } from "@tanstack/react-router";

import Button from "../components/Button";
import Header from "../components/Header";
import IconPlus from "../assets/iconPlus.svg?react";
import IndexCard from "../components/SeniorHomeCard";
import Loading from "../components/Loading";
import { useUser } from "../hooks/useUser";
import { useUserRecords } from "../hooks/useUserRecords";

export const Route = createLazyFileRoute("/senior/home")({
  component: SeniorHome,
});

const DEFAULT_USER_ID = "1";

function SeniorHome() {
  const { data: userData, isLoading: userLoading } = useUser(DEFAULT_USER_ID);
  const { data: recordsData, isLoading: recordsLoading } =
    useUserRecords(DEFAULT_USER_ID);

  if (userLoading || recordsLoading) {
    return <Loading />;
  }

  return (
    <div>
      <Header isSam userName={userData?.name} userAvatar="/assets/avatar.png" />
      <main className="flex flex-col items-end gap-6">
        <Link to={`/senior/record?id=${userData?.id}`}>
          <Button icon={<IconPlus />} size="xl">
            새로운 기록하기
          </Button>
        </Link>
        <div className="flex w-full flex-col gap-6">
          {recordsData?.map((record) => (
            <IndexCard
              key={record.id}
              title={record.title}
              tags={record.keywords.slice(0, 3)}
              image={`https://fjtskwttcrchrywg.tunnel-pt.elice.io${record.image}`}
              cardId={record.id.toString()}
            />
          ))}
        </div>
      </main>
    </div>
  );
}

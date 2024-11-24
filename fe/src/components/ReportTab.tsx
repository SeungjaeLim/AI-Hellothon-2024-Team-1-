interface Session {
  number: number;
  date: string;
}

interface ReportTabProps {
  name: string;
  sessions: Session[];
  currentSession: number;
}

const ReportTab = ({ name, sessions, currentSession }: ReportTabProps) => {
  return (
    <div className="mt-4 flex items-center justify-center gap-3">
      <div>
        <span className="text-2xl font-semibold leading-loose">{name}</span>
        <span className="text-lg font-semibold leading-loose">
          님<br />
          주간보고서
        </span>
      </div>
      <div className="flex grow items-center justify-start">
        {sessions.map((session) => (
          <div
            key={session.number}
            className={`mx-2 flex grow items-center justify-center py-2 ${currentSession === session.number ? "border-b-2 border-black-13" : "border-b-2 border-black-1"}`}
          >
            <div className="text-center">
              <span
                className={`text-xl font-semibold leading-relaxed ${currentSession === session.number ? "" : "text-black-7"}`}
              >
                {session.number}회차
                <br />
              </span>
              <span
                className={`text-base font-medium leading-relaxed ${currentSession === session.number ? "" : "text-black-7"}`}
              >
                {session.date}
              </span>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
};

export default ReportTab;

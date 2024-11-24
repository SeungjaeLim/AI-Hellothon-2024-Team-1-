interface RecordingStatusProps {
  highlightedText: string;
  normalText: string;
}

const RecordingStatus = ({
  highlightedText,
  normalText,
}: RecordingStatusProps) => {
  return (
    <div className="inline-flex flex-col items-center justify-start gap-8 rounded-xl bg-black-3 p-5 pb-16">
      <div className="flex h-44 flex-col items-center justify-center gap-4 self-stretch">
        <div className="flex flex-col items-center justify-start gap-2">
          <div
            className="animate-loading aspect-[2/1] w-[30px] bg-[radial-gradient(closest-side_circle,theme(colors.blue.highlight)_90%,#0000)] bg-[length:33.33%_50%] bg-left-top bg-no-repeat"
            style={{
              backgroundImage: `
                radial-gradient(closest-side circle,#2175FD 90%,#0000),
                radial-gradient(closest-side circle,#2175FD 90%,#0000),
                radial-gradient(closest-side circle,#2175FD 90%,#0000)
              `,
              backgroundPosition: "0% 50%, 50% 50%, 100% 50%",
            }}
          />
          <div className="text-black text-lg font-bold">기록중입니다</div>
        </div>
        <div className="self-stretch text-center">
          <p className="text-xl font-bold leading-[35px] text-black-5">
            {highlightedText}
          </p>
          <p className="text-xl font-bold leading-[35px] text-black-8">
            {normalText}
          </p>
        </div>
      </div>
    </div>
  );
};

export default RecordingStatus;

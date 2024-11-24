import IconCalender from "../assets/iconCalender.svg?react";

interface DateProps {
  startDate: string;
  endDate: string;
}

const ThisWeek = ({ startDate, endDate }: DateProps) => {
  return (
    <div className="inline-flex h-auto items-center justify-start gap-2">
      <div className="flex gap-3 text-center text-xl font-medium text-black-13">
        <span>
          {startDate} ~ {endDate}
        </span>
        <span>
          <IconCalender />
        </span>
      </div>
      <div className="relative aspect-square h-full" />
    </div>
  );
};

export default ThisWeek;

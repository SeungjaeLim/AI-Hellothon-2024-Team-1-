import { RecordResponse } from "../types";
import { fetchUserRecords } from "../apis";
import { useQuery } from "@tanstack/react-query";

export function useUserRecords(userId: string) {
  return useQuery<RecordResponse[]>({
    queryKey: ["records", userId],
    queryFn: () => fetchUserRecords(userId),
  });
}

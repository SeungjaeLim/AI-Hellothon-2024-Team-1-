import { fetchRecord } from "../apis";
import { useQuery } from "@tanstack/react-query";

export function useRecord(recordId: string) {
  return useQuery({
    queryKey: ["record", recordId],
    queryFn: () => fetchRecord(recordId),
  });
}

import { UserResponse } from "../types";
import { fetchUser } from "../apis";
import { useQuery } from "@tanstack/react-query";

export function useUser(userId: string) {
  return useQuery<UserResponse>({
    queryKey: ["user", userId],
    queryFn: () => fetchUser(userId),
  });
}

import {
  Outlet,
  ScrollRestoration,
  createRootRoute,
  useMatchRoute,
} from "@tanstack/react-router";
import { QueryClient, QueryClientProvider } from "@tanstack/react-query";

import { ReactQueryDevtools } from "@tanstack/react-query-devtools";
import { TanStackRouterDevtools } from "@tanstack/router-devtools";

const queryClient = new QueryClient();

const ErrorComponent = () => {
  return (
    <div className="flex h-screen flex-col items-center justify-center">
      <h1 className="text-white text-2xl font-bold">오류가 발생했습니다.</h1>
      <p className="text-gray-400 mt-2">잠시 후 다시 시도해주세요</p>
    </div>
  );
};

const RootComponent = () => {
  const isSeniorHome = useMatchRoute()({ to: "/senior/home" });
  const isCaregiverHome = useMatchRoute()({ to: "/caregiver/home" });
  const isHome = isSeniorHome || isCaregiverHome;

  return (
    <QueryClientProvider client={queryClient}>
      <div className="bg-black-7">
        <div
          className={`m-auto min-h-screen max-w-[500px] ${isHome ? "bg-black-3" : "bg-black-1"} px-5 py-12`}
        >
          <ScrollRestoration />
          <Outlet />
        </div>
      </div>
      <TanStackRouterDevtools />
      <ReactQueryDevtools initialIsOpen={false} />
    </QueryClientProvider>
  );
};

export const Route = createRootRoute({
  component: RootComponent,
  errorComponent: ErrorComponent,
});

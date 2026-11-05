"use client";
import {
  MutationCache,
  QueryClient,
  QueryClientProvider,
} from "@tanstack/react-query";
import { type PropsWithChildren, useState } from "react";

export const QueryContextProvider = ({ children }: PropsWithChildren) => {
  const [client] = useState(() => {
    return new QueryClient({
      defaultOptions: {
        queries: {
          staleTime: 60 * 1000, // 1 min
          refetchOnWindowFocus: false,
        },
      },
      mutationCache: new MutationCache({
        onError: (error) => {
          // Global error handling for mutations (e.g., POST/PUT requests)
          console.log(error);
        },
      }),
    });
  });

  return <QueryClientProvider client={client}>{children}</QueryClientProvider>;
};

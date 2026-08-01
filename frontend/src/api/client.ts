const apiBaseUrl =
  import.meta.env.VITE_API_BASE_URL ?? "http://localhost:8000/api/v1";

export type HealthResponse = {
  status: "ok";
};

export async function getHealth(): Promise<HealthResponse> {
  const response = await fetch(`${apiBaseUrl}/health`, {
    credentials: "include",
  });

  if (!response.ok) {
    throw new Error("The Fish Habit Game API is unavailable.");
  }

  return (await response.json()) as HealthResponse;
}

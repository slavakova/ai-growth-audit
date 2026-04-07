"use client";

import { useEffect, useState } from "react";

import { RunNav } from "@/components/run-nav";
import { Card, ErrorState, LoadingState } from "@/components/ui";
import { apiClient } from "@/lib/api/client";
import type { Run } from "@/lib/api/types";

export default function RunSummaryPage({ params }: { params: { id: string } }) {
  const [run, setRun] = useState<Run | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    apiClient
      .getRun(params.id)
      .then(setRun)
      .catch((e: Error) => setError(e.message))
      .finally(() => setLoading(false));
  }, [params.id]);

  return (
    <div className="space-y-4">
      <h1 className="text-2xl font-bold">Run summary #{params.id}</h1>
      <RunNav runId={params.id} />
      {loading && <LoadingState />}
      {error && <ErrorState message={error} />}
      {run && (
        <Card title="Status">
          <p>Status: {run.status}</p>
          <p>Stage: {run.current_stage ?? "-"}</p>
          <p>Goal: {run.goal}</p>
          {run.error_message && <p className="text-red-600">Error: {run.error_message}</p>}
        </Card>
      )}
    </div>
  );
}

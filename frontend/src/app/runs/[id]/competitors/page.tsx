"use client";

import { useEffect, useState } from "react";

import { RunNav } from "@/components/run-nav";
import { ErrorState, LoadingState } from "@/components/ui";
import { apiClient } from "@/lib/api/client";
import type { Competitor } from "@/lib/api/types";

export default function CompetitorsPage({ params }: { params: { id: string } }) {
  const [items, setItems] = useState<Competitor[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    apiClient.getCompetitors(params.id).then(setItems).catch((e: Error) => setError(e.message)).finally(() => setLoading(false));
  }, [params.id]);

  return (
    <div className="space-y-4">
      <h1 className="text-2xl font-bold">Competitors</h1>
      <RunNav runId={params.id} />
      {loading && <LoadingState />}
      {error && <ErrorState message={error} />}
      <ul className="space-y-2">
        {items.map((item) => (
          <li key={item.id} className="rounded border bg-white p-3">
            <div className="font-medium">{item.domain}</div>
            <div className="text-sm text-slate-600">{item.reason ?? "No reason"}</div>
          </li>
        ))}
      </ul>
    </div>
  );
}

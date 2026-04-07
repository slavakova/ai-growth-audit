"use client";

import { useEffect, useState } from "react";

import { RunNav } from "@/components/run-nav";
import { ErrorState, LoadingState } from "@/components/ui";
import { apiClient } from "@/lib/api/client";
import type { ComparisonMetric } from "@/lib/api/types";

export default function ComparisonPage({ params }: { params: { id: string } }) {
  const [items, setItems] = useState<ComparisonMetric[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    apiClient.getComparison(params.id).then(setItems).catch((e: Error) => setError(e.message)).finally(() => setLoading(false));
  }, [params.id]);

  return (
    <div className="space-y-4">
      <h1 className="text-2xl font-bold">Comparison</h1>
      <RunNav runId={params.id} />
      {loading && <LoadingState />}
      {error && <ErrorState message={error} />}
      <div className="overflow-auto rounded border bg-white">
        <table className="min-w-full text-sm">
          <thead className="bg-slate-100">
            <tr><th className="p-2 text-left">Metric</th><th className="p-2">You</th><th className="p-2">Avg</th><th className="p-2">Delta</th></tr>
          </thead>
          <tbody>
            {items.map((m) => (
              <tr key={m.id} className="border-t"><td className="p-2">{m.metric_name}</td><td className="p-2 text-center">{m.your_value}</td><td className="p-2 text-center">{m.competitor_avg}</td><td className="p-2 text-center">{m.delta}</td></tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
}

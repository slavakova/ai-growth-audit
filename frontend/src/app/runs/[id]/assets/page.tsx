"use client";

import { useEffect, useState } from "react";

import { RunNav } from "@/components/run-nav";
import { ErrorState, LoadingState } from "@/components/ui";
import { apiClient } from "@/lib/api/client";
import type { AssetType, GeneratedAsset } from "@/lib/api/types";

const assetTypes: AssetType[] = ["landing_page", "blog_post", "ad_copy"];

export default function AssetsPage({ params }: { params: { id: string } }) {
  const [assetType, setAssetType] = useState<AssetType>("landing_page");
  const [items, setItems] = useState<GeneratedAsset[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    setLoading(true);
    apiClient.getAssets(params.id, assetType).then(setItems).catch((e: Error) => setError(e.message)).finally(() => setLoading(false));
  }, [params.id, assetType]);

  return (
    <div className="space-y-4">
      <h1 className="text-2xl font-bold">Generated assets</h1>
      <RunNav runId={params.id} />
      <div className="flex gap-2">
        {assetTypes.map((type) => (
          <button key={type} onClick={() => setAssetType(type)} className={`rounded border px-3 py-1 text-sm ${assetType === type ? "bg-slate-900 text-white" : "bg-white"}`}>
            {type}
          </button>
        ))}
      </div>
      {loading && <LoadingState />}
      {error && <ErrorState message={error} />}
      <ul className="space-y-2">
        {items.map((item) => (
          <li key={item.id} className="rounded border bg-white p-3">
            <div className="font-medium">{item.title}</div>
            <pre className="whitespace-pre-wrap text-sm text-slate-700">{item.content}</pre>
          </li>
        ))}
      </ul>
    </div>
  );
}

"use client";

import { useState } from "react";
import { useRouter } from "next/navigation";

import { ErrorState } from "@/components/ui";
import { apiClient } from "@/lib/api/client";

export default function NewProjectPage() {
  const router = useRouter();
  const [form, setForm] = useState({ name: "", website_url: "", region: "", priority_service: "" });
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const onSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setLoading(true);
    setError(null);
    try {
      await apiClient.createProject(form);
      router.push("/projects");
    } catch (err) {
      setError((err as Error).message);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="max-w-xl space-y-4">
      <h1 className="text-2xl font-bold">Create project</h1>
      {error && <ErrorState message={error} />}
      <form onSubmit={onSubmit} className="space-y-3 rounded border bg-white p-4">
        {(["name", "website_url", "region", "priority_service"] as const).map((field) => (
          <label key={field} className="block">
            <span className="mb-1 block text-sm font-medium">{field}</span>
            <input
              required
              className="w-full rounded border px-3 py-2"
              value={form[field]}
              onChange={(e) => setForm((prev) => ({ ...prev, [field]: e.target.value }))}
            />
          </label>
        ))}
        <button disabled={loading} className="rounded bg-blue-600 px-4 py-2 text-white disabled:opacity-50">
          {loading ? "Saving..." : "Create"}
        </button>
      </form>
    </div>
  );
}

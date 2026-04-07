"use client";

import Link from "next/link";
import { useEffect, useState } from "react";

import { ErrorState, LoadingState } from "@/components/ui";
import { apiClient } from "@/lib/api/client";
import type { Project } from "@/lib/api/types";

export default function ProjectsPage() {
  const [projects, setProjects] = useState<Project[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    apiClient
      .listProjects()
      .then(setProjects)
      .catch((e: Error) => setError(e.message))
      .finally(() => setLoading(false));
  }, []);

  return (
    <div className="space-y-4">
      <h1 className="text-2xl font-bold">Projects</h1>
      {loading && <LoadingState />}
      {error && <ErrorState message={error} />}
      {!loading && !error && (
        <div className="space-y-2">
          {projects.map((project) => (
            <div key={project.id} className="rounded border bg-white p-4">
              <div className="font-semibold">{project.name}</div>
              <div className="text-sm text-slate-600">{project.website_url}</div>
              <div className="text-sm text-slate-600">{project.region} · {project.priority_service}</div>
              <Link href={`/runs/101`} className="mt-2 inline-block text-sm text-blue-600">Open latest run</Link>
            </div>
          ))}
        </div>
      )}
    </div>
  );
}

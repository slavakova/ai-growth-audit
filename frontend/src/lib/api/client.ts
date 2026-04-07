import { mockAssetsByType, mockComparison, mockCompetitors, mockProjects, mockRecommendations, mockRuns } from "./mock";
import type {
  AssetType,
  ComparisonMetric,
  Competitor,
  GeneratedAsset,
  Project,
  ProjectCreate,
  Recommendation,
  Run,
} from "./types";

const API_BASE = process.env.NEXT_PUBLIC_API_BASE_URL ?? "http://localhost:8000";
const USE_MOCK = (process.env.NEXT_PUBLIC_USE_MOCK ?? "true") === "true";

async function request<T>(path: string, init?: RequestInit): Promise<T> {
  const res = await fetch(`${API_BASE}${path}`, {
    ...init,
    headers: { "Content-Type": "application/json", ...(init?.headers ?? {}) },
    cache: "no-store",
  });
  if (!res.ok) throw new Error(`API error ${res.status}`);
  return (await res.json()) as T;
}

export const apiClient = {
  async listProjects(): Promise<Project[]> {
    return USE_MOCK ? mockProjects : request<Project[]>("/api/projects");
  },
  async createProject(payload: ProjectCreate): Promise<Project> {
    if (USE_MOCK) {
      return { id: Date.now(), created_at: new Date().toISOString(), ...payload };
    }
    return request<Project>("/api/projects", { method: "POST", body: JSON.stringify(payload) });
  },
  async getRun(runId: string): Promise<Run> {
    return USE_MOCK ? { ...mockRuns[0], id: Number(runId) } : request<Run>(`/api/runs/${runId}`);
  },
  async getCompetitors(runId: string): Promise<Competitor[]> {
    return USE_MOCK ? mockCompetitors : request<Competitor[]>(`/api/runs/${runId}/competitors`);
  },
  async getComparison(runId: string): Promise<ComparisonMetric[]> {
    return USE_MOCK ? mockComparison : request<ComparisonMetric[]>(`/api/runs/${runId}/comparison`);
  },
  async getRecommendations(runId: string): Promise<Recommendation[]> {
    return USE_MOCK ? mockRecommendations : request<Recommendation[]>(`/api/runs/${runId}/recommendations`);
  },
  async getAssets(runId: string, assetType: AssetType): Promise<GeneratedAsset[]> {
    return USE_MOCK ? mockAssetsByType[assetType] : request<GeneratedAsset[]>(`/api/runs/${runId}/assets/${assetType}`);
  },
};

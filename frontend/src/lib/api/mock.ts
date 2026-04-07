import type { AssetType, ComparisonMetric, Competitor, GeneratedAsset, Project, Recommendation, Run } from "./types";

const now = new Date().toISOString();

export const mockProjects: Project[] = [
  {
    id: 1,
    name: "Demo Dental Clinic",
    website_url: "https://demo-dental.example",
    region: "US-NY",
    priority_service: "Dental implants",
    created_at: now,
  },
];

export const mockRuns: Run[] = [
  {
    id: 101,
    project_id: 1,
    goal: "seo_growth",
    status: "completed",
    current_stage: "done",
    error_message: null,
    selected_page_url: null,
    created_at: now,
  },
];

export const mockCompetitors: Competitor[] = [
  { id: 1, domain: "best-dentist.example", reason: "High SERP overlap" },
  { id: 2, domain: "smile-lab.example", reason: "Strong local pages" },
];

export const mockComparison: ComparisonMetric[] = [
  { id: 1, metric_name: "Content Depth", your_value: "Low", competitor_avg: "High", delta: "-2" },
  { id: 2, metric_name: "FAQ Coverage", your_value: "No", competitor_avg: "Yes", delta: "-1" },
];

export const mockRecommendations: Recommendation[] = [
  { id: 1, title: "Add city landing pages", detail: "Create service pages for top local intents.", priority: "high" },
  { id: 2, title: "Improve trust blocks", detail: "Add reviews and certifications above fold.", priority: "medium" },
];

export const mockAssetsByType: Record<AssetType, GeneratedAsset[]> = {
  landing_page: [{ id: 1, asset_type: "landing_page", title: "Implants LP Draft", content: "[MOCK] Landing page draft" }],
  blog_post: [{ id: 2, asset_type: "blog_post", title: "How to choose implants", content: "[MOCK] Blog post draft" }],
  ad_copy: [{ id: 3, asset_type: "ad_copy", title: "Google Ads set", content: "[MOCK] Ad copy set" }],
};

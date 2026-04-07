export type AnalysisGoal = "seo_growth" | "lead_generation" | "conversion_rate";
export type RunStatus = "pending" | "running" | "completed" | "failed";
export type AssetType = "landing_page" | "blog_post" | "ad_copy";

export interface Project {
  id: number;
  name: string;
  website_url: string;
  region: string;
  priority_service: string;
  created_at: string;
}

export interface ProjectCreate {
  name: string;
  website_url: string;
  region: string;
  priority_service: string;
}

export interface Run {
  id: number;
  project_id: number;
  goal: AnalysisGoal;
  status: RunStatus;
  current_stage: string | null;
  error_message: string | null;
  selected_page_url: string | null;
  created_at: string;
}

export interface Competitor {
  id: number;
  domain: string;
  reason: string | null;
}

export interface ComparisonMetric {
  id: number;
  metric_name: string;
  your_value: string | null;
  competitor_avg: string | null;
  delta: string | null;
}

export interface Recommendation {
  id: number;
  title: string;
  detail: string;
  priority: string;
}

export interface GeneratedAsset {
  id: number;
  asset_type: AssetType;
  title: string;
  content: string;
}

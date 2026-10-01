export type Source = "Email" | "Web Form" | "Support Portal";

export type Category =
  | "Bug Report"
  | "Feature Request"
  | "Billing Issue"
  | "Technical Question"
  | "Incident/Outage";

export type Priority = "Low" | "Medium" | "High";

export type Queue = "Engineering" | "Billing" | "Product" | "IT/Security" | "Escalation";

export interface TriageRequest {
  source: Source;
  message: string;
}

export interface TriageRecord {
  id: string;
  source: Source;
  raw_message: string;
  category: Category;
  priority: Priority;
  confidence: number;
  core_issue: string;
  identifiers: string[];
  urgency_signal: string;
  summary: string;
  routing_queue: Queue;
  escalation_flag: boolean;
  escalation_reason: string | null;
  created_at: string;
}

export const SOURCES: Source[] = ["Email", "Web Form", "Support Portal"];

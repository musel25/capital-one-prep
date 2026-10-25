export type Kind =
  "technical" | "case" | "behavioral" | "python" | "reflection";
export type Phase = { title: string; minutes: number; legacyTitle?: string };
export type Block = {
  id: string;
  title: string;
  kind: Kind;
  minutes: number;
  summary: string;
  content: string;
  deliverables: string[];
  rubric: string[];
  hints?: string[];
  solution?: string;
  prompts?: string[];
  labs?: string[];
  setupPrompt?: string;
  phases?: Phase[];
  sources?: string[];
  problems?: { number: number; title: string; url: string; difficulty: string; focus: string }[];
  stages?: { title: string; content: string }[];
  promptGroups?: { question: string; followUps: string[] }[];
};
export type Day = {
  date: string;
  title: string;
  focus: string;
  blocks: Block[];
};
export type Source = {
  id: string;
  title: string;
  url: string;
  level: "official" | "testimony" | "practice" | "repository";
  note: string;
};
export type Plan = {
  title: string;
  startDate: string;
  endDate: string;
  timezone: string;
  dailyMinutes: number;
  archivedBlockIds?: string[];
  archivedBlocks?: Block[];
  days: Day[];
  sources: Source[];
};
export type Status = "pending" | "in-progress" | "done" | "assisted" | "retry";
export type Timer = {
  elapsed: number;
  startedAt: number | null;
  duration: number;
  phase: string;
};
export type Progress = {
  status: Status;
  notes: string;
  prediction: string;
  checked: string[];
  minutes: number;
  reviewed: boolean;
  timer: Timer | null;
};
export type State = {
  version: 1;
  updatedAt: string;
  tasks: Record<string, Progress>;
};

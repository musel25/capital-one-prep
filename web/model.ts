import type { Progress, State, Timer } from "./types";
export const STORAGE_KEY = "capital-one-prep:v1";
export function dayIn(date = new Date()): string {
  return new Intl.DateTimeFormat("en-CA", {
    timeZone: "America/Tijuana",
    year: "numeric",
    month: "2-digit",
    day: "2-digit",
  }).format(date);
}
export function dayIndex(dates: string[], day: string): number {
  const next = dates.findIndex((d) => d >= day);
  return next < 0 ? dates.length - 1 : next;
}
export const emptyProgress = (): Progress => ({
  status: "pending",
  notes: "",
  prediction: "",
  checked: [],
  minutes: 0,
  reviewed: false,
  timer: null,
});
export const freshState = (): State => ({
  version: 1,
  updatedAt: new Date().toISOString(),
  tasks: {},
});
export function replaceProgress(
  state: State,
  id: string,
  patch: Partial<Progress>,
): State {
  return {
    ...state,
    updatedAt: new Date().toISOString(),
    tasks: {
      ...state.tasks,
      [id]: { ...(state.tasks[id] ?? emptyProgress()), ...patch },
    },
  };
}
export function elapsedSeconds(timer: Timer, now = Date.now()): number {
  return (
    timer.elapsed +
    (timer.startedAt === null ? 0 : Math.max(0, (now - timer.startedAt) / 1000))
  );
}
export const finished = (p?: Progress) =>
  !!p && ["done", "assisted", "retry"].includes(p.status);
export const canReview = (p?: Progress) =>
  finished(p) && !!p?.prediction.trim();
const object = (x: unknown): x is Record<string, unknown> =>
  typeof x === "object" && x !== null && !Array.isArray(x);
const text = (x: unknown, max = 30000) =>
  typeof x === "string" && x.length <= max;
const number = (x: unknown, max: number) =>
  typeof x === "number" && Number.isFinite(x) && x >= 0 && x <= max;
export function validateState(input: unknown, ids: string[]): State {
  const fail = () => {
    throw Error(
      "El archivo no es un respaldo válido de este plan. Tu progreso actual se conserva.",
    );
  };
  if (
    !object(input) ||
    input.version !== 1 ||
    !text(input.updatedAt, 50) ||
    !Number.isFinite(Date.parse(input.updatedAt as string)) ||
    !object(input.tasks)
  )
    return fail();
  const validIds = new Set(ids);
  const tasks: Record<string, Progress> = {};
  for (const [id, value] of Object.entries(input.tasks)) {
    if (
      !validIds.has(id) ||
      !object(value) ||
      !["pending", "in-progress", "done", "assisted", "retry"].includes(
        value.status as string,
      ) ||
      !text(value.notes) ||
      !text(value.prediction) ||
      !Array.isArray(value.checked) ||
      value.checked.length > 200 ||
      !value.checked.every((x) => text(x, 80)) ||
      !number(value.minutes, 10000) ||
      typeof value.reviewed !== "boolean"
    )
      return fail();
    const t = value.timer;
    if (
      t !== null &&
      (!object(t) ||
        !number(t.elapsed, 1e8) ||
        !number(t.duration, 86400) ||
        !text(t.phase, 200) ||
        (t.startedAt !== null && !number(t.startedAt, 1e15)))
    )
      return fail();
    tasks[id] = {
      status: value.status as Progress["status"],
      notes: value.notes as string,
      prediction: value.prediction as string,
      checked: value.checked as string[],
      minutes: value.minutes as number,
      reviewed: value.reviewed,
      timer: t as Timer | null,
    };
  }
  return { version: 1, updatedAt: input.updatedAt as string, tasks };
}
export function formatDuration(minutes: number) {
  return minutes >= 60
    ? `${Math.floor(minutes / 60)} h${minutes % 60 ? ` ${minutes % 60} min` : ""}`
    : `${minutes} min`;
}
export function dateLabel(date: string, short = false) {
  return new Date(date + "T12:00:00Z").toLocaleDateString("es-MX", {
    timeZone: "UTC",
    weekday: short ? "short" : "long",
    day: "numeric",
    month: "short",
  });
}

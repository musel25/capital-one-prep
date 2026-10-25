import { useEffect, useRef, useState } from "react";
import {
  ArrowUpRight,
  BookOpen,
  CalendarDays,
  Check,
  ChevronRight,
  Clock3,
  Code2,
  Download,
  ExternalLink,
  FileText,
  Flag,
  ListChecks,
  MessageCircle,
  Play,
  ShieldCheck,
  Upload,
  X,
} from "lucide-react";
import planData from "../curriculum/plan.json";
import type { Block, Plan, Progress, State } from "./types";
import {
  dateLabel,
  dayIn,
  dayIndex,
  elapsedSeconds,
  formatDuration,
  freshState,
  phaseTitle,
  replaceProgress,
  STORAGE_KEY,
  validateState,
} from "./model";
import { kindLabels, TaskDialog } from "./TaskDialog";
type View = "agenda" | "resources" | "behavioral" | "archive";
const plan = planData as Plan;
const all = plan.days.flatMap((d) => d.blocks);
// Accept old closing notes in stored state and backups without scheduling them.
const ids = [
  ...all.map((b) => b.id),
  ...(plan.archivedBlocks ?? []).map((b) => b.id),
  ...(plan.archivedBlockIds ?? []),
];
const done = (p?: Progress) => p?.status === "done" || p?.status === "assisted";
function read() {
  try {
    const raw = localStorage.getItem(STORAGE_KEY);
    return {
      state: raw ? validateState(JSON.parse(raw), ids) : freshState(),
      raw,
      error: "",
    };
  } catch {
    return {
      state: freshState(),
      raw: null,
      error:
        "Could not read saved progress. Download a recovery copy before starting over.",
    };
  }
}
function download(text: string, name: string) {
  const url = URL.createObjectURL(
    new Blob([text], { type: "application/json" }),
  );
  const a = document.createElement("a");
  a.href = url;
  a.download = name;
  a.click();
  setTimeout(() => URL.revokeObjectURL(url), 1000);
}
export default function App() {
  const [initial] = useState(read);
  const [state, setState] = useState<State>(initial.state);
  const stateRef = useRef(state);
  const rawRef = useRef(initial.raw);
  const [error, setError] = useState(initial.error);
  const [blocked, setBlocked] = useState(!!initial.error);
  const [today, setToday] = useState(dayIn());
  const initialDate = new URLSearchParams(location.search).get("day");
  const [selected, setSelected] = useState(() =>
    initialDate && plan.days.some((d) => d.date === initialDate)
      ? plan.days.findIndex((d) => d.date === initialDate)
      : dayIndex(
          plan.days.map((d) => d.date),
          today,
        ),
  );
  const [view, setView] = useState<View>(() => {
    const requested = new URLSearchParams(location.search).get("view");
    return requested === "resources" ||
      requested === "behavioral" ||
      requested === "archive"
      ? requested
      : "agenda";
  });
  const [task, setTask] = useState<Block | null>(null);
  const [notice, setNotice] = useState("");
  const fileRef = useRef<HTMLInputElement>(null);
  useEffect(() => {
    const timer = setInterval(() => setToday(dayIn()), 30000);
    const listener = (e: StorageEvent) => {
      if (e.key === STORAGE_KEY && e.newValue !== rawRef.current) {
        setBlocked(true);
        setError(
          "Progress changed in another tab. Export this version if needed, then reload to continue.",
        );
      }
    };
    window.addEventListener("storage", listener);
    return () => {
      clearInterval(timer);
      window.removeEventListener("storage", listener);
    };
  }, []);
  function persist(next: State) {
    if (blocked) return false;
    try {
      if (localStorage.getItem(STORAGE_KEY) !== rawRef.current) {
        setBlocked(true);
        throw Error(
          "Another tab changed your progress. Export this version, then reload to continue.",
        );
      }
      const raw = JSON.stringify(next);
      localStorage.setItem(STORAGE_KEY, raw);
      rawRef.current = raw;
      stateRef.current = next;
      setState(next);
      setError("");
      return true;
    } catch (e) {
      setError(
        e instanceof Error
          ? e.message
          : "Could not save. Export your progress.",
      );
      return false;
    }
  }
  function save(id: string, patch: Partial<Progress>) {
    let next = stateRef.current;
    if (patch.timer?.startedAt)
      for (const [key, p] of Object.entries(next.tasks))
        if (key !== id && p.timer?.startedAt)
          next = replaceProgress(next, key, {
            timer: {
              ...p.timer,
              elapsed: elapsedSeconds(p.timer),
              startedAt: null,
            },
          });
    return persist(replaceProgress(next, id, patch));
  }
  function selectDay(index: number) {
    setSelected(index);
    setView("agenda");
    const url = new URL(location.href);
    url.searchParams.delete("view");
    url.searchParams.set("day", plan.days[index].date);
    history.replaceState(null, "", url);
  }
  function showView(next: View) {
    setView(next);
    const url = new URL(location.href);
    if (next === "agenda") url.searchParams.delete("view");
    else url.searchParams.set("view", next);
    history.replaceState(null, "", url);
  }
  async function importFile(file?: File) {
    if (!file) return;
    try {
      if (file.size > 5_000_000)
        throw Error("File too large. Choose a Capital One Prep backup.");
      const next = validateState(JSON.parse(await file.text()), ids);
      if (
        !confirm(
          "Replace this browser's progress with the file? A local copy of your previous progress will be kept.",
        )
      )
        return;
      const old = localStorage.getItem(STORAGE_KEY);
      if (old) localStorage.setItem(`${STORAGE_KEY}:backup:${Date.now()}`, old);
      const raw = JSON.stringify(next);
      localStorage.setItem(STORAGE_KEY, raw);
      rawRef.current = raw;
      stateRef.current = next;
      setState(next);
      setBlocked(false);
      setError("");
      setTask(null);
      setNotice(
        "Backup imported. A local copy of your previous progress was kept.",
      );
    } catch (e) {
      setError(
        e instanceof Error
          ? e.message
          : "Could not import. Your progress is unchanged.",
      );
    }
    if (fileRef.current) fileRef.current.value = "";
  }
  function recover() {
    try {
      download(
        localStorage.getItem(STORAGE_KEY) ?? "{}",
        "capital-one-recovery.json",
      );
    } catch {
      setError(
        "Browser storage is blocked. Allow storage for this site to continue.",
      );
    }
  }
  function resetCorrupt() {
    if (!confirm("Start over? Download a recovery copy first.")) return;
    try {
      const old = localStorage.getItem(STORAGE_KEY);
      if (old)
        localStorage.setItem(`${STORAGE_KEY}:recovery:${Date.now()}`, old);
      localStorage.removeItem(STORAGE_KEY);
      location.reload();
    } catch {
      setError("Cannot access browser storage.");
    }
  }
  const day = plan.days[selected];
  const dayMinutes = day.blocks.reduce((n, b) => n + b.minutes, 0);
  const count = day.blocks.filter((b) => done(state.tasks[b.id])).length;
  const completedMinutes = day.blocks
    .filter((b) => done(state.tasks[b.id]))
    .reduce((n, b) => n + b.minutes, 0);
  const next = day.blocks.find((b) => !done(state.tasks[b.id]));
  const totalDone = all.filter((b) => done(state.tasks[b.id])).length;
  const previous = plan.days
    .filter((d) => d.date < day.date)
    .flatMap((d) => d.blocks)
    .filter((b) => !done(state.tasks[b.id]));
  const running = Object.entries(state.tasks).find(
    ([id, p]) => p.timer?.startedAt && all.some((b) => b.id === id),
  );
  const kindIcon = (b: Block) =>
    b.kind === "technical" ? (
      <Code2 />
    ) : b.kind === "case" ? (
      <FileText />
    ) : b.kind === "behavioral" ? (
      <MessageCircle />
    ) : b.kind === "python" ? (
      <Code2 />
    ) : (
      <Flag />
    );
  return (
    <div className="app-shell">
      <aside className="sidebar">
        <a className="brand" href="/grind/capital-one/">
          <span className="brand-icon">
            <ListChecks size={24} />
          </span>
          <span>
            Capital One<span className="brand-sub">Preparation sprint</span>
          </span>
        </a>
        <div className="sprint-meta">
          <CalendarDays size={16} />
          <span>
            Oct 23 – Nov 1, 2026
            <br />
            <strong>
              10 days · {formatDuration(plan.dailyMinutes)} per day
            </strong>
          </span>
        </div>
        <nav aria-label="Practice days" className="day-nav">
          {plan.days.map((d, i) => {
            const n = d.blocks.filter((b) => done(state.tasks[b.id])).length;
            return (
              <button
                className={`day-link ${selected === i && view === "agenda" ? "selected" : ""}`}
                key={d.date}
                onClick={() => selectDay(i)}
                aria-current={
                  selected === i && view === "agenda" ? "date" : undefined
                }
              >
                <span
                  className={`day-dot ${n === d.blocks.length ? "complete" : ""}`}
                >
                  {n === d.blocks.length ? <Check size={15} /> : i + 1}
                </span>
                <span>
                  <strong>{dateLabel(d.date, true)}</strong>
                  <small>
                    {i === 7 || i === 9 ? "Full mock interview" : d.title}
                  </small>
                </span>
                {d.date === today && (
                  <span className="today-dot" title="Today" />
                )}
              </button>
            );
          })}
        </nav>
        <nav className="secondary-nav" aria-label="Resources">
          <button
            className={view === "archive" ? "active" : ""}
            onClick={() => showView("archive")}
          >
            <BookOpen size={17} /> Previous exercises
          </button>
          <button
            className={view === "behavioral" ? "active" : ""}
            onClick={() => showView("behavioral")}
          >
            <MessageCircle size={17} /> Behavioral practice
          </button>
          <button
            className={view === "resources" ? "active" : ""}
            onClick={() => showView("resources")}
          >
            <BookOpen size={17} /> Sources
          </button>
        </nav>
        <div className="sidebar-footer">
          <span>
            <ShieldCheck size={15} /> Saved in this browser
          </span>
          <div className="backup-actions">
            <button
              onClick={() =>
                download(
                  JSON.stringify(stateRef.current, null, 2),
                  `capital-one-progress-${today}.json`,
                )
              }
            >
              <Download size={14} /> Export
            </button>
            <button onClick={() => fileRef.current?.click()}>
              <Upload size={14} /> Import
            </button>
          </div>
          <input
            ref={fileRef}
            type="file"
            accept="application/json,.json"
            className="sr-only"
            aria-label="Import progress"
            onChange={(e) => void importFile(e.target.files?.[0])}
          />
          <a
            href="https://github.com/musel25/capital-one-prep"
            target="_blank"
            rel="noreferrer"
          >
            Repository <ArrowUpRight size={13} />
          </a>
        </div>
      </aside>
      <main className="main">
        <header className="topbar">
          <div>
            <span className="status-dot" /> Practice plan{" "}
            <span className="topbar-sub">TDP Mexico 2027</span>
          </div>
          <a href="https://timer.musel.dev/grind/">
            Grind Recall <ArrowUpRight size={14} />
          </a>
        </header>
        {error && (
          <div className="alert" role="alert">
            <div>{error}</div>
            {blocked && (
              <div className="button-row">
                <button className="button small secondary" onClick={recover}>
                  Download recovery copy
                </button>
                <button
                  className="button small secondary"
                  onClick={() => location.reload()}
                >
                  Reload
                </button>
                {initial.error && (
                  <button
                    className="button small secondary"
                    onClick={resetCorrupt}
                  >
                    Start over
                  </button>
                )}
              </div>
            )}
          </div>
        )}
        {notice && (
          <div className="notice" role="status">
            {notice}
            <button
              className="icon-button"
              onClick={() => setNotice("")}
              aria-label="Dismiss notice"
            >
              <X size={16} />
            </button>
          </div>
        )}
        {view === "agenda" ? (
          <>
            <div className="day-heading">
              <div>
                <p className="date-heading">
                  {dateLabel(day.date)}
                  <span>Day {selected + 1} of 10</span>
                </p>
                <h1>{day.title}</h1>
              </div>
              <button
                className="button secondary small"
                onClick={() =>
                  selectDay(
                    dayIndex(
                      plan.days.map((d) => d.date),
                      today,
                    ),
                  )
                }
              >
                <CalendarDays size={16} />{" "}
                {today < plan.startDate
                  ? "First day"
                  : today > plan.endDate
                    ? "Last day"
                    : "Today"}
              </button>
            </div>
            {today < plan.startDate && (
              <div className="before-start">
                <CalendarDays size={17} />
                <span>
                  Practice starts on October 23. You can set up your environment
                  now.
                </span>
              </div>
            )}
            {today > plan.endDate && (
              <div className="before-start">
                <Flag size={17} />
                <span>
                  The schedule has ended. Your attempts and exercises are still
                  available.
                </span>
              </div>
            )}
            <div className="day-layout">
              <section className="agenda">
                <div className="agenda-top">
                  <h2>Schedule</h2>
                  <span>
                    <Clock3 size={15} /> {formatDuration(dayMinutes)} · breaks
                    excluded
                  </span>
                </div>
                <div className="agenda-list">
                  {day.blocks.map((b, i) => {
                    const p = state.tasks[b.id];
                    return (
                      <button
                        className={`task-row ${done(p) ? "task-done" : ""}`}
                        key={b.id}
                        onClick={() => setTask(b)}
                      >
                        <span className={`task-icon ${b.kind}`}>
                          {done(p) ? <Check /> : kindIcon(b)}
                        </span>
                        <span className="task-info">
                          <span className="task-meta">
                            <span>{kindLabels[b.kind]}</span>
                            <span>{formatDuration(b.minutes)}</span>
                          </span>
                          <strong>{b.title}</strong>
                          <span className="task-description">{b.summary}</span>
                          <span
                            className={`task-status ${p?.status ?? "pending"}`}
                          >
                            {p?.status === "done"
                              ? "Completed"
                              : p?.status === "assisted"
                                ? "Completed with hints"
                                : p?.status === "retry"
                                  ? "Try again"
                                  : p?.status === "in-progress"
                                    ? "In progress"
                                    : `Block ${i + 1}`}
                          </span>
                        </span>
                        <ChevronRight size={19} />
                      </button>
                    );
                  })}
                </div>
              </section>
              <aside className="day-aside">
                <section className="next-panel">
                  <span className="panel-label">
                    {next ? "Up next" : "Day completed"}
                  </span>
                  <h2>{next ? next.title : "Today's tasks are complete"}</h2>
                  <p>
                    {next
                      ? next.kind === "technical"
                        ? "Open the exercise to begin."
                        : next.summary
                      : "Export your progress to keep a backup."}
                  </p>
                  {next && (
                    <button
                      className="button primary"
                      onClick={() => setTask(next)}
                    >
                      <Play size={16} />{" "}
                      {state.tasks[next.id]?.status === "in-progress"
                        ? "Continue"
                        : "Start task"}
                    </button>
                  )}
                </section>
                <section className="progress-panel">
                  <h3>Today's progress</h3>
                  <div className="progress-caption">
                    <strong>
                      {count} of {day.blocks.length} tasks
                    </strong>
                    <span>
                      {formatDuration(completedMinutes)} /{" "}
                      {formatDuration(dayMinutes)}
                    </span>
                  </div>
                  <progress max={day.blocks.length} value={count} />
                  <p>
                    {day.blocks.filter(
                      (b) => state.tasks[b.id]?.status === "retry",
                    ).length > 0
                      ? "Attempts marked for retry remain pending."
                      : "Based on tasks you mark as completed."}
                  </p>
                  <div className="overall">
                    <span>Overall</span>
                    <strong>
                      {totalDone} / {all.length} tasks
                    </strong>
                  </div>
                </section>
              </aside>
            </div>
            {running && (
              <button
                className="running-bar"
                onClick={() =>
                  setTask(all.find((b) => b.id === running[0]) ?? null)
                }
              >
                <Clock3 size={16} /> Timer running:{" "}
                {phaseTitle(
                  all.find((b) => b.id === running[0])?.phases,
                  running[1].timer?.phase,
                )}
                <ChevronRight size={16} />
              </button>
            )}
            {!!previous.length && (
              <details className="previous">
                <summary>
                  {previous.length} earlier tasks pending{" "}
                  <ChevronRight size={16} />
                </summary>
                <p>Resume these anytime.</p>
                <div>
                  {previous.map((b) => (
                    <button key={b.id} onClick={() => setTask(b)}>
                      {b.title}
                      <ChevronRight size={15} />
                    </button>
                  ))}
                </div>
              </details>
            )}
            <div className="day-bottom">
              <button
                className="text-button"
                disabled={selected === 0}
                onClick={() => selectDay(selected - 1)}
              >
                Previous day
              </button>
              <button
                className="text-button"
                disabled={selected === plan.days.length - 1}
                onClick={() => selectDay(selected + 1)}
              >
                Next day
              </button>
            </div>
          </>
        ) : view === "archive" ? (
          <section className="resource-page">
            <h1>Previous exercises</h1>
            <p className="day-focus">
              Original exercises and their saved notes remain available here.
              They do not count toward the updated schedule. Local coding
              attempts keep their original instructions and checks.
            </p>
            {(plan.archivedBlocks ?? []).map((b) => (
              <button
                className="story-row"
                key={b.id}
                onClick={() => setTask(b)}
              >
                <span>
                  <small>
                    {b.id} · {formatDuration(b.minutes)}
                  </small>
                  <strong>{b.title}</strong>
                  <span>
                    {state.tasks[b.id]?.notes
                      ? "Notes saved"
                      : "Original exercise"}
                  </span>
                </span>
                <ChevronRight size={18} />
              </button>
            ))}
          </section>
        ) : view === "resources" ? (
          <section className="resource-page">
            <h1>Sources</h1>
            <p className="day-focus">
              Documentation, candidate accounts, and practice material. Check
              your invitation for your interview format and tools.
            </p>
            {plan.sources.map((s) => (
              <article className="source-row" key={s.id}>
                <span className={`source-level ${s.level}`}>
                  {
                    {
                      official: "Official documentation",
                      testimony: "Candidate account",
                      practice: "Original practice",
                      repository: "Repository",
                    }[s.level]
                  }
                </span>
                <h2>
                  <a href={s.url} target="_blank" rel="noreferrer">
                    {s.title}
                    <ExternalLink size={16} />
                  </a>
                </h2>
                <p>{s.note}</p>
              </article>
            ))}
          </section>
        ) : (
          <section className="resource-page">
            <h1>Behavioral practice</h1>
            <p className="day-focus">
              Choose a day and answer its questions using examples from your own
              projects.
            </p>
            {plan.days.flatMap((d) =>
              d.blocks
                .filter((b) => b.kind === "behavioral")
                .map((b) => (
                  <button
                    key={b.id}
                    className="story-row"
                    onClick={() => setTask(b)}
                  >
                    <span>
                      <small>{dateLabel(d.date, true)}</small>
                      <strong>{b.title}</strong>
                      <span>
                        {state.tasks[b.id]?.notes
                          ? "Notes saved"
                          : "Open questions"}
                      </span>
                    </span>
                    <ChevronRight size={18} />
                  </button>
                )),
            )}
          </section>
        )}
      </main>
      {task && (
        <TaskDialog
          key={task.id}
          block={task}
          progress={state.tasks[task.id]}
          sources={plan.sources}
          close={() => setTask(null)}
          save={(patch) => save(task.id, patch)}
        />
      )}
    </div>
  );
}

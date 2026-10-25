import { useEffect, useRef, useState } from "react";
import {
  X,
  Play,
  Pause,
  RotateCcw,
  Check,
  Copy,
  Clock3,
  ChevronDown,
  Lightbulb,
  Terminal,
  ExternalLink,
} from "lucide-react";
import ReactMarkdown from "react-markdown";
import remarkGfm from "remark-gfm";
import {
  canReview,
  elapsedSeconds,
  emptyProgress,
  formatDuration,
  phaseTitle,
} from "./model";
import type { Block, Progress, Source } from "./types";

export function Markdown({ children }: { children: string }) {
  return (
    <div className="prose">
      <ReactMarkdown
        remarkPlugins={[remarkGfm]}
        components={{
          a: ({ children, ...props }) => (
            <a {...props} target="_blank" rel="noreferrer">
              {children}
            </a>
          ),
          table: ({ children }) => (
            <div className="table-scroll">
              <table>{children}</table>
            </div>
          ),
        }}
      >
        {children}
      </ReactMarkdown>
    </div>
  );
}
export function CopyButton({
  text,
  initialLabel = "Copy",
}: {
  text: string;
  initialLabel?: string;
}) {
  const [label, setLabel] = useState(initialLabel);
  return (
    <button
      className="copy-button"
      onClick={async () => {
        try {
          await navigator.clipboard.writeText(text);
          setLabel("Copied");
        } catch {
          setLabel("Select the text to copy");
        }
      }}
    >
      <Copy size={14} />
      {label}
    </button>
  );
}
export const kindLabels = {
  technical: "AI-assisted coding",
  case: "Technical case",
  behavioral: "Behavioral",
  python: "Python / LeetCode",
  reflection: "Closing reflection",
};
export function TaskDialog({
  block,
  progress,
  sources,
  close,
  save,
}: {
  block: Block;
  progress?: Progress;
  sources: Source[];
  close: () => void;
  save: (patch: Partial<Progress>) => boolean;
}) {
  const ref = useRef<HTMLDialogElement>(null);
  const p = progress ?? emptyProgress();
  const [now, setNow] = useState(Date.now());
  const [tab, setTab] = useState<"brief" | "work">("brief");
  const [prediction, setPrediction] = useState(p.prediction);
  const [notes, setNotes] = useState(p.notes);
  const [copyFeedback, setFeedback] = useState("");
  const [visibleStages, setVisibleStages] = useState(1);
  const [drawn, setDrawn] = useState<number[]>([]);
  const [showFollowUps, setShowFollowUps] = useState(false);
  const groups = block.promptGroups ?? [];
  const currentQuestion = drawn.length ? groups[drawn[drawn.length - 1]] : undefined;
  function drawQuestion() {
    const available = groups.map((_, i) => i).filter((i) => !drawn.includes(i));
    if (!available.length) return;
    setDrawn([...drawn, available[Math.floor(Math.random() * available.length)]]);
    setShowFollowUps(false);
  }
  useEffect(() => {
    ref.current?.showModal();
    const i = setInterval(() => setNow(Date.now()), 500);
    return () => clearInterval(i);
  }, []);
  const phases = block.phases?.length
    ? block.phases
    : [{ title: block.title, minutes: block.minutes }];
  const [phase, setPhase] = useState(
    phaseTitle(phases, p.timer?.phase) || phases[0].title,
  );
  const selectedPhase = phases.find((x) => x.title === phase) ?? phases[0];
  const elapsed = p.timer ? elapsedSeconds(p.timer, now) : 0;
  const remaining = Math.max(
    0,
    (p.timer?.duration ?? selectedPhase.minutes * 60) - elapsed,
  );
  const countdown = `${Math.floor(remaining / 60)
    .toString()
    .padStart(2, "0")}:${Math.floor(remaining % 60)
    .toString()
    .padStart(2, "0")}`;
  const phaseMatches =
    !p.timer || phaseTitle(phases, p.timer.phase) === selectedPhase.title;
  function start() {
    save({
      status: p.status === "pending" ? "in-progress" : p.status,
      timer: {
        elapsed: phaseMatches ? elapsed : 0,
        startedAt: Date.now(),
        duration: selectedPhase.minutes * 60,
        phase: selectedPhase.title,
      },
    });
  }
  function stop() {
    if (p.timer) save({ timer: { ...p.timer, elapsed, startedAt: null } });
  }
  function finish(status: Progress["status"]) {
    const patch: Partial<Progress> = { status, notes };
    if (p.timer) patch.timer = { ...p.timer, elapsed, startedAt: null };
    if (save(patch)) setFeedback("Result saved in this browser.");
  }
  const predictionChanged = prediction !== p.prediction;
  const notesChanged = notes !== p.notes;
  useEffect(() => {
    if (!predictionChanged && !notesChanged) return;
    const protectDraft = (event: BeforeUnloadEvent) => {
      event.preventDefault();
      event.returnValue = "";
    };
    window.addEventListener("beforeunload", protectDraft);
    return () => window.removeEventListener("beforeunload", protectDraft);
  }, [predictionChanged, notesChanged]);
  function requestClose() {
    if ((predictionChanged || notesChanged) && !save({ prediction, notes })) {
      setFeedback(
        "Could not save your draft. Copy it before leaving this page.",
      );
      return;
    }
    close();
  }
  return (
    <dialog
      ref={ref}
      className="task-dialog"
      onCancel={(e) => {
        e.preventDefault();
        requestClose();
      }}
      onClick={(e) => {
        if (e.target === e.currentTarget) requestClose();
      }}
    >
      <div className="dialog-content">
        <header className="dialog-header">
          <div>
            <span className={`kind ${block.kind}`}>
              {kindLabels[block.kind]}
            </span>
            <h2>{block.title}</h2>
            <p>
              {formatDuration(block.minutes)} of practice
              {block.kind === "case" && " · Without running code"}
            </p>
          </div>
          <button
            className="icon-button"
            onClick={requestClose}
            aria-label="Close exercise"
          >
            <X />
          </button>
        </header>
        <div className="timer-strip">
          <div className="timer-clock">
            <Clock3 size={18} />
            <strong role="timer">{countdown}</strong>
            <span>
              {remaining === 0 && p.timer ? "Time's up" : "Phase time"}
            </span>
          </div>
          <label className="phase-select">
            <span className="sr-only">Timer phase</span>
            <select
              value={selectedPhase.title}
              onChange={(e) => {
                stop();
                setPhase(e.target.value);
                const next = phases.find((x) => x.title === e.target.value)!;
                save({
                  timer: {
                    elapsed: 0,
                    startedAt: null,
                    duration: next.minutes * 60,
                    phase: next.title,
                  },
                });
              }}
            >
              {phases.map((x, i) => (
                <option key={`${i}-${x.title}`} value={x.title}>
                  {x.title} · {x.minutes} min
                </option>
              ))}
            </select>
          </label>
          <button
            className="button small primary"
            onClick={p.timer?.startedAt ? stop : start}
          >
            {p.timer?.startedAt ? <Pause size={16} /> : <Play size={16} />}{" "}
            {p.timer?.startedAt ? "Pause" : "Start"}
          </button>
          <button
            className="icon-button"
            title="Reset timer only"
            aria-label="Reset timer only"
            onClick={() =>
              save({
                timer: {
                  elapsed: 0,
                  startedAt: null,
                  duration: selectedPhase.minutes * 60,
                  phase: selectedPhase.title,
                },
              })
            }
          >
            <RotateCcw size={17} />
          </button>
        </div>
        <div className="task-tabs">
          <button
            className={tab === "brief" ? "active" : ""}
            onClick={() => setTab("brief")}
          >
            Exercise
          </button>
          <button
            className={tab === "work" ? "active" : ""}
            onClick={() => setTab("work")}
          >
            My attempt
          </button>
        </div>
        <div className="dialog-body">
          {tab === "brief" ? (
            <>
              <p className="task-summary">{block.summary}</p>
              {!!block.problems?.length && (
                <section className="problem-cards" aria-label="LeetCode assignments">
                  {block.problems.map((problem) => (
                    <a className="problem-card" href={problem.url} key={problem.number} target="_blank" rel="noreferrer">
                      <span className="problem-meta">{problem.difficulty} · Python</span>
                      <strong>{problem.number}. {problem.title} <ExternalLink size={16} /></strong>
                      <span>{problem.focus}</span>
                      <span className="problem-action">Open on LeetCode ↗</span>
                    </a>
                  ))}
                </section>
              )}
              {!!block.labs?.length && (
                <section className="local-work">
                  <h3>
                    <Terminal size={18} /> Open in your editor
                  </h3>
                  <p>
                    Run from <code>/home/musel/Github/capital-one-prep</code>.
                    Open the returned folder and read its README.
                  </p>
                  {block.labs.map((id) => (
                    <div key={id} className="command-row">
                      <code>uv run python scripts/practice.py start {id}</code>
                      <CopyButton
                        text={`cd /home/musel/Github/capital-one-prep && uv run python scripts/practice.py start ${id}`}
                      />
                    </div>
                  ))}
                  <p className="muted">
                    Read the opening brief, write your questions, then consult
                    CLARIFICATIONS.md for the requirements. To resume an
                    attempt, open its existing folder; its original task still applies.
                  </p>
                </section>
              )}
              <Markdown>{block.content}</Markdown>
              {!!block.stages?.length && (
                <section className="section" aria-label="Case stages">
                  <p className="muted">Stage {Math.min(visibleStages, block.stages.length)} of {block.stages.length}. Explain your answer before moving on. These reveals are session-only; save your place in Notes.</p>
                  {block.stages.slice(0, visibleStages).map((stage, i) => (
                    <section className="case-stage" key={i}>
                      <h3>{i + 1}. {stage.title}</h3>
                      <Markdown>{stage.content}</Markdown>
                    </section>
                  ))}
                  {visibleStages < block.stages.length && <button className="button secondary" onClick={() => setVisibleStages(visibleStages + 1)}>Reveal next stage</button>}
                </section>
              )}
              {!!groups.length && (
                <section className="section rehearsal" aria-label="Behavioral rehearsal">
                  <h3>Interview rehearsal</h3>
                  <p>Choose your story after hearing the question. Answer aloud for 90–120 seconds, then open the follow-ups. Questions do not repeat within this round.</p>
                  {currentQuestion && <>
                    <p className="drawn-question" data-testid="drawn-question" aria-live="polite">{currentQuestion.question}</p>
                    {!showFollowUps ? <button className="text-button" onClick={() => setShowFollowUps(true)}>Show follow-ups</button> : <ul>{currentQuestion.followUps.map((q) => <li key={q}>{q}</li>)}</ul>}
                  </>}
                  <div className="button-row">
                    <button className="button secondary" disabled={drawn.length === groups.length} onClick={drawQuestion}>Draw a question</button>
                    {drawn.length === groups.length && <button className="text-button" onClick={() => { setDrawn([]); setShowFollowUps(false); }}>Start another round</button>}
                    <span className="muted">{drawn.length} / {groups.length} asked</span>
                  </div>
                  <p className="muted">Save the question and your answer in My attempt. The shuffled order resets when this exercise is closed.</p>
                </section>
              )}
              {block.setupPrompt && (
                <section className="local-work">
                  <h3>Local setup</h3>
                  <p>
                    Paste this into your local agent to create the starter,
                    tests, and run command.
                  </p>
                  <CopyButton
                    text={block.setupPrompt}
                    initialLabel="Copy prompt"
                  />
                  <details>
                    <summary>View full prompt</summary>
                    <pre className="setup-prompt">{block.setupPrompt}</pre>
                  </details>
                </section>
              )}
              {!!block.prompts?.length && (
                <section className="section">
                  <h3>
                    {block.kind === "behavioral"
                      ? "Today's questions"
                      : "Questions"}
                  </h3>
                  <ol className="prompt-list">
                    {block.prompts.map((q, i) => (
                      <li key={i}>{q}</li>
                    ))}
                  </ol>
                </section>
              )}
              {block.kind !== "behavioral" && (
                <details className="section completion-details">
                  <summary>Deliverables</summary>
                  <ul>
                    {block.deliverables.map((d, i) => (
                      <li key={i}>{d}</li>
                    ))}
                  </ul>
                </details>
              )}
              {!!block.hints?.length && (
                <section className="section">
                  <h3>
                    <Lightbulb size={18} /> Hints
                  </h3>
                  <p className="muted">Open if you get stuck.</p>
                  {block.hints.map((hint, i) => (
                    <details key={i} className="hint">
                      <summary>
                        Hint {i + 1}
                        <ChevronDown size={15} />
                      </summary>
                      <Markdown>{hint}</Markdown>
                    </details>
                  ))}
                </section>
              )}
              <button className="button primary" onClick={() => setTab("work")}>
                Record attempt <Check size={17} />
              </button>
            </>
          ) : (
            <>
              {block.kind === "case" && (
                <section className="section">
                  <h3>Prediction</h3>
                  <p>
                    Record the current output, desired output, and your
                    correction before revealing the solution.
                  </p>
                  <textarea
                    rows={7}
                    maxLength={30000}
                    value={prediction}
                    onChange={(e) => setPrediction(e.target.value)}
                    placeholder="Input → expected result → rule. My counterexamples and proposed change…"
                    aria-label="My prediction"
                  />
                  <button
                    className="button secondary small"
                    disabled={!prediction.trim() || !predictionChanged}
                    onClick={() => {
                      if (save({ prediction }))
                        setFeedback("Prediction saved.");
                    }}
                  >
                    {predictionChanged
                      ? "Save prediction"
                      : p.prediction
                        ? "Prediction saved"
                        : "Save prediction"}
                  </button>
                </section>
              )}
              <details className="section completion-details">
                <summary>Review checklist</summary>
                <p className="muted">Check what you verified.</p>
                <div className="checklist">
                  {block.rubric.map((r, i) => {
                    const key = `rubric-${i}`;
                    return (
                      <label key={key}>
                        <input
                          type="checkbox"
                          checked={p.checked.includes(key)}
                          onChange={(e) =>
                            save({
                              checked: e.target.checked
                                ? [...p.checked, key]
                                : p.checked.filter((k) => k !== key),
                            })
                          }
                        />
                        <span>{r}</span>
                      </label>
                    );
                  })}
                </div>
              </details>
              <section className="section">
                <label className="field-label" htmlFor="task-notes">
                  Notes
                </label>
                <textarea
                  id="task-notes"
                  aria-label="Notes, evidence, and open questions"
                  value={notes}
                  onChange={(e) => {
                    setNotes(e.target.value);
                    save({ notes: e.target.value });
                  }}
                  rows={6}
                  maxLength={30000}
                  placeholder="Your answer, results, or questions…"
                />
                {notesChanged && (
                  <p className="alert" role="alert">
                    Could not save. Your text is still here; copy it before
                    reloading or leaving. Close the exercise to retry saving.
                  </p>
                )}
                <p className="muted">
                  Saved in this browser. Use Export to back it up.
                </p>
              </section>
              {!!block.labs?.length && (
                <div className="callout">
                  <strong>Check your code locally</strong>
                  <p>
                    From the repository root, replace the path with your attempt
                    folder:
                  </p>
                  <code>
                    uv run python scripts/practice.py check
                    attempts/YOUR-ATTEMPT
                  </code>
                  <p>Save the result here; this page does not run your code.</p>
                </div>
              )}
              <section className="section">
                <div className="result-heading">
                  <h3>Finish attempt</h3>
                  <label>
                    Minutes spent{" "}
                    <input
                      type="number"
                      min="0"
                      max="10000"
                      value={p.minutes}
                      onChange={(e) =>
                        save({
                          minutes: Math.max(
                            0,
                            Math.min(10000, Number(e.target.value) || 0),
                          ),
                        })
                      }
                    />
                  </label>
                </div>
                <p className="muted">
                  Choose “with hints” if you used extra help or viewed the
                  solution.
                </p>
                <div className="result-buttons">
                  <button
                    className={`button ${p.status === "done" ? "primary" : "secondary"}`}
                    onClick={() => finish("done")}
                  >
                    <Check size={16} /> Completed
                  </button>
                  <button
                    className={`button ${p.status === "assisted" ? "primary" : "secondary"}`}
                    onClick={() => finish("assisted")}
                  >
                    Completed with hints
                  </button>
                  <button
                    className={`button ${p.status === "retry" ? "primary" : "secondary"}`}
                    onClick={() => finish("retry")}
                  >
                    Try again
                  </button>
                </div>
                <button
                  className="text-button"
                  onClick={() => save({ status: "pending" })}
                >
                  Mark as pending
                </button>
              </section>
              {block.solution && (
                <section className="section solution">
                  <h3>Solution review</h3>
                  {!p.reviewed ? (
                    <>
                      <p>
                        {block.kind === "case"
                          ? "Save your prediction and finish the attempt to reveal the explanation."
                          : "Finish the attempt before viewing the explanation."}
                      </p>
                      <button
                        className="button secondary"
                        disabled={
                          block.kind === "case"
                            ? !canReview(p) || predictionChanged
                            : !["done", "assisted", "retry"].includes(p.status)
                        }
                        onClick={() => save({ reviewed: true })}
                      >
                        Reveal explanation
                      </button>
                    </>
                  ) : (
                    <>
                      <Markdown>{block.solution}</Markdown>
                    </>
                  )}
                </section>
              )}
            </>
          )}
          {copyFeedback && (
            <p className="feedback" role="status">
              {copyFeedback}
            </p>
          )}
          {!!block.sources?.length && (
            <footer className="task-sources">
              <details>
                <summary>Sources</summary>
                {block.sources.map((id) => {
                  const s = sources.find((x) => x.id === id);
                  return s ? (
                    <a key={id} href={s.url} target="_blank" rel="noreferrer">
                      {s.title}
                      <ExternalLink size={13} />
                    </a>
                  ) : null;
                })}
              </details>
            </footer>
          )}
        </div>
      </div>
    </dialog>
  );
}

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
  initialLabel = "Copiar",
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
          setLabel("Copiado");
        } catch {
          setLabel("Selecciona el texto para copiar");
        }
      }}
    >
      <Copy size={14} />
      {label}
    </button>
  );
}
export const kindLabels = {
  technical: "Con agente de IA",
  case: "Caso técnico",
  behavioral: "Behavioral",
  python: "Python",
  reflection: "Cierre y reflexión",
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
  useEffect(() => {
    ref.current?.showModal();
    const i = setInterval(() => setNow(Date.now()), 500);
    return () => clearInterval(i);
  }, []);
  const phases = block.phases?.length
    ? block.phases
    : [{ title: block.title, minutes: block.minutes }];
  const [phase, setPhase] = useState(p.timer?.phase ?? phases[0].title);
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
  const phaseMatches = !p.timer || p.timer.phase === selectedPhase.title;
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
    if (save(patch)) setFeedback("Resultado guardado en este navegador.");
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
        "No se pudo guardar tu borrador. Cópialo antes de salir de la página.",
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
              {formatDuration(block.minutes)} de práctica ·{" "}
              {block.kind === "case"
                ? "Primero razona sin ejecutar código"
                : "Sigue el enunciado y registra la evidencia"}
            </p>
          </div>
          <button
            className="icon-button"
            onClick={requestClose}
            aria-label="Cerrar ejercicio"
          >
            <X />
          </button>
        </header>
        <div className="timer-strip">
          <div className="timer-clock">
            <Clock3 size={18} />
            <strong role="timer">{countdown}</strong>
            <span>
              {remaining === 0 && p.timer
                ? "Tiempo cumplido"
                : "Tiempo de la fase"}
            </span>
          </div>
          <label className="phase-select">
            <span className="sr-only">Fase del temporizador</span>
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
            {p.timer?.startedAt ? "Pausar" : "Iniciar"}
          </button>
          <button
            className="icon-button"
            title="Reiniciar solo el temporizador"
            aria-label="Reiniciar solo el temporizador"
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
            Enunciado y recursos
          </button>
          <button
            className={tab === "work" ? "active" : ""}
            onClick={() => setTab("work")}
          >
            Mi intento y revisión
          </button>
        </div>
        <div className="dialog-body">
          {tab === "brief" ? (
            <>
              <p className="task-summary">{block.summary}</p>
              {!!block.labs?.length && (
                <section className="local-work">
                  <h3>
                    <Terminal size={18} /> Abre el ejercicio en tu editor
                  </h3>
                  <p>
                    Desde <code>/home/musel/Github/capital-one-prep</code>, crea
                    una copia nueva para cada tarea. El comando muestra la
                    carpeta que debes abrir; su README explica cómo ejecutar la
                    aplicación.
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
                    Conserva el primer intento. Para la segunda tarea usa su
                    comando de inicio; no reutilices la copia anterior.
                  </p>
                </section>
              )}
              <Markdown>{block.content}</Markdown>
              {block.setupPrompt && (
                <section className="local-work">
                  <h3>Preparar el ejercicio local</h3>
                  <p>
                    Copia este prompt y pégalo en tu agente local, con este
                    repositorio abierto. Crea el archivo y las pruebas; tú
                    implementas la función. La página no ejecuta Python.
                  </p>
                  <CopyButton
                    text={block.setupPrompt}
                    initialLabel="Copiar prompt"
                  />
                  <details>
                    <summary>Ver o seleccionar el prompt completo</summary>
                    <pre className="setup-prompt">{block.setupPrompt}</pre>
                  </details>
                </section>
              )}
              {!!block.prompts?.length && (
                <section className="section">
                  <h3>Preguntas para practicar en voz alta</h3>
                  <ul className="prompt-list">
                    {block.prompts.map((q, i) => (
                      <li key={i}>{q}</li>
                    ))}
                  </ul>
                </section>
              )}
              <section className="section">
                <h3>Qué debes entregar</h3>
                <ul>
                  {block.deliverables.map((d, i) => (
                    <li key={i}>{d}</li>
                  ))}
                </ul>
              </section>
              {!!block.hints?.length && (
                <section className="section">
                  <h3>
                    <Lightbulb size={18} /> Pistas opcionales
                  </h3>
                  <p className="muted">
                    Intenta primero. Usar pistas queda reflejado al elegir el
                    resultado.
                  </p>
                  {block.hints.map((hint, i) => (
                    <details key={i} className="hint">
                      <summary>
                        Pista {i + 1}
                        <ChevronDown size={15} />
                      </summary>
                      <Markdown>{hint}</Markdown>
                    </details>
                  ))}
                </section>
              )}
              <button className="button primary" onClick={() => setTab("work")}>
                Registrar mi intento <Check size={17} />
              </button>
            </>
          ) : (
            <>
              {block.kind === "case" && (
                <section className="section">
                  <h3>Mi predicción, antes de ejecutar</h3>
                  <p>
                    Escribe las salidas esperadas, la regla que justifica cada
                    una y los cambios que propondrías. Guarda tu respuesta antes
                    de revisar la solución.
                  </p>
                  <textarea
                    rows={7}
                    maxLength={30000}
                    value={prediction}
                    onChange={(e) => setPrediction(e.target.value)}
                    placeholder="Input → expected result → rule. My counterexamples and proposed change…"
                    aria-label="Mi predicción"
                  />
                  <button
                    className="button secondary small"
                    disabled={!prediction.trim() || !predictionChanged}
                    onClick={() => {
                      if (save({ prediction }))
                        setFeedback("Predicción guardada.");
                    }}
                  >
                    {predictionChanged
                      ? "Guardar predicción"
                      : p.prediction
                        ? "Predicción guardada"
                        : "Guardar predicción"}
                  </button>
                </section>
              )}
              <section className="section">
                <h3>Comprueba tu trabajo</h3>
                <p className="muted">
                  Marca únicamente lo que puedes demostrar. Esta lista es una
                  autoevaluación.
                </p>
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
              </section>
              <section className="section">
                <label className="field-label" htmlFor="task-notes">
                  Notas, evidencia y preguntas pendientes
                </label>
                <textarea
                  id="task-notes"
                  value={notes}
                  onChange={(e) => {
                    setNotes(e.target.value);
                    save({ notes: e.target.value });
                  }}
                  rows={6}
                  maxLength={30000}
                  placeholder="Ruta de mi intento, tests ejecutados, resultado, decisiones, lo que todavía no comprobé…"
                />
                {notesChanged && (
                  <p className="alert" role="alert">
                    No se pudo guardar. Tu texto sigue aquí; cópialo antes de
                    recargar o salir. Cierra el ejercicio para reintentar el
                    guardado.
                  </p>
                )}
                <p className="muted">
                  Guardado en este navegador. Exporta el progreso para tener una
                  copia o compartirlo conmigo desde private/.
                </p>
              </section>
              {!!block.labs?.length && (
                <div className="callout">
                  <strong>Comprueba tu código localmente</strong>
                  <p>
                    Desde la raíz del repositorio, sustituye la ruta por la de
                    tu intento:
                  </p>
                  <code>
                    uv run python scripts/practice.py check attempts/TU-CARPETA
                  </code>
                  <p>
                    El verificador comprueba comportamiento; la página no
                    observa ni certifica la ejecución. Para revisarlo conmigo:
                    «Revisa mi intento en attempts/…».
                  </p>
                </div>
              )}
              <section className="section">
                <div className="result-heading">
                  <h3>Terminar este intento</h3>
                  <label>
                    Minutos reales{" "}
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
                  Usar el agente permitido forma parte del ejercicio. «Con
                  pistas» significa que necesitaste ayuda adicional o viste la
                  solución.
                </p>
                <div className="result-buttons">
                  <button
                    className={`button ${p.status === "done" ? "primary" : "secondary"}`}
                    onClick={() => finish("done")}
                  >
                    <Check size={16} /> Completado
                  </button>
                  <button
                    className={`button ${p.status === "assisted" ? "primary" : "secondary"}`}
                    onClick={() => finish("assisted")}
                  >
                    Completado con pistas
                  </button>
                  <button
                    className={`button ${p.status === "retry" ? "primary" : "secondary"}`}
                    onClick={() => finish("retry")}
                  >
                    Necesito otro intento
                  </button>
                </div>
                <button
                  className="text-button"
                  onClick={() => save({ status: "pending" })}
                >
                  Volver a pendiente
                </button>
              </section>
              {block.solution && (
                <section className="section solution">
                  <h3>Revisión del intento</h3>
                  {!p.reviewed ? (
                    <>
                      <p>
                        {block.kind === "case"
                          ? "Termina el intento y guarda tu predicción para abrir la explicación. En un simulacro, espera a finalizar la ronda."
                          : "Termina el intento antes de consultar la explicación."}
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
                        He terminado: abrir explicación
                      </button>
                    </>
                  ) : (
                    <>
                      <p className="muted">
                        Explicación consultada. Para medir tu progreso, el
                        siguiente intento debe usar una variante nueva.
                      </p>
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
              <h3>Fuentes y contexto</h3>
              {block.sources.map((id) => {
                const s = sources.find((x) => x.id === id);
                return s ? (
                  <a key={id} href={s.url} target="_blank" rel="noreferrer">
                    {s.title}
                    <ExternalLink size={13} />
                  </a>
                ) : null;
              })}
            </footer>
          )}
        </div>
      </div>
    </dialog>
  );
}

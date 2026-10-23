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
  HelpCircle,
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
  replaceProgress,
  STORAGE_KEY,
  validateState,
} from "./model";
import { kindLabels, TaskDialog } from "./TaskDialog";
import { Tutorial } from "./Tutorial";
type View = "agenda" | "resources" | "behavioral" | "guide";
const plan = planData as Plan;
const all = plan.days.flatMap((d) => d.blocks);
const ids = all.map((b) => b.id);
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
        "No se pudo leer el progreso guardado. Descarga una copia de recuperación antes de empezar de nuevo.",
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
    return requested === "guide" ||
      requested === "resources" ||
      requested === "behavioral"
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
          "El progreso cambió en otra pestaña. Exporta esta versión si la necesitas y recarga para continuar.",
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
          "Otra pestaña cambió el progreso. Exporta esta versión y recarga antes de continuar.",
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
          : "No se pudo guardar. Exporta tu progreso.",
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
        throw Error(
          "El archivo es demasiado grande. Elige un respaldo de Capital One Prep.",
        );
      const next = validateState(JSON.parse(await file.text()), ids);
      if (
        !confirm(
          "¿Reemplazar el progreso de este navegador por el archivo? Se conservará una copia local del progreso anterior.",
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
        "Respaldo importado. El progreso anterior conserva una copia local.",
      );
    } catch (e) {
      setError(
        e instanceof Error
          ? e.message
          : "No se pudo importar. Tu progreso se conserva.",
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
        "El navegador no permite acceder al almacenamiento. Prueba permitir almacenamiento para este sitio.",
      );
    }
  }
  function resetCorrupt() {
    if (
      !confirm("¿Empezar de nuevo? Primero descarga la copia de recuperación.")
    )
      return;
    try {
      const old = localStorage.getItem(STORAGE_KEY);
      if (old)
        localStorage.setItem(`${STORAGE_KEY}:recovery:${Date.now()}`, old);
      localStorage.removeItem(STORAGE_KEY);
      location.reload();
    } catch {
      setError("No se puede acceder al almacenamiento del navegador.");
    }
  }
  const day = plan.days[selected];
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
    ([, p]) => p.timer?.startedAt,
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
            23 oct – 1 nov, 2026
            <br />
            <strong>10 días · 4 horas al día</strong>
          </span>
        </div>
        <nav aria-label="Días de preparación" className="day-nav">
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
                    {i === 7 || i === 9 ? "Simulacro completo" : d.title}
                  </small>
                </span>
                {d.date === today && <span className="today-dot" title="Hoy" />}
              </button>
            );
          })}
        </nav>
        <nav className="secondary-nav" aria-label="Recursos">
          <button
            className={view === "behavioral" ? "active" : ""}
            onClick={() => showView("behavioral")}
          >
            <MessageCircle size={17} /> Mi práctica behavioral
          </button>
          <button
            className={view === "resources" ? "active" : ""}
            onClick={() => showView("resources")}
          >
            <BookOpen size={17} /> Fuentes y contexto
          </button>
          <button
            className={view === "guide" ? "active" : ""}
            onClick={() => showView("guide")}
          >
            <HelpCircle size={17} /> Empieza aquí · Tutorial
          </button>
        </nav>
        <div className="sidebar-footer">
          <span>
            <ShieldCheck size={15} /> Progreso privado en este navegador
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
              <Download size={14} /> Exportar
            </button>
            <button onClick={() => fileRef.current?.click()}>
              <Upload size={14} /> Importar
            </button>
          </div>
          <input
            ref={fileRef}
            type="file"
            accept="application/json,.json"
            className="sr-only"
            aria-label="Importar progreso"
            onChange={(e) => void importFile(e.target.files?.[0])}
          />
          <a
            href="https://github.com/musel25/capital-one-prep"
            target="_blank"
            rel="noreferrer"
          >
            Repositorio <ArrowUpRight size={13} />
          </a>
        </div>
      </aside>
      <main className="main">
        <header className="topbar">
          <div>
            <span className="status-dot" /> Tu espacio de preparación{" "}
            <span className="topbar-sub">TDP México 2027</span>
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
                  Descargar recuperación
                </button>
                <button
                  className="button small secondary"
                  onClick={() => location.reload()}
                >
                  Recargar
                </button>
                {initial.error && (
                  <button
                    className="button small secondary"
                    onClick={resetCorrupt}
                  >
                    Empezar de nuevo
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
              aria-label="Cerrar aviso"
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
                  <span>Día {selected + 1} de 10</span>
                </p>
                <h1>{day.title}</h1>
                <p className="day-focus">{day.focus}</p>
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
                  ? "Ir al primer día"
                  : today > plan.endDate
                    ? "Ir al último día"
                    : "Volver a hoy"}
              </button>
            </div>
            {today < plan.startDate && (
              <div className="before-start">
                <CalendarDays size={17} />
                <span>
                  Tu sprint empieza el 23 de octubre. Puedes explorar los
                  materiales y preparar el entorno desde ahora.
                </span>
              </div>
            )}
            {today > plan.endDate && (
              <div className="before-start">
                <Flag size={17} />
                <span>
                  El calendario terminó. Tus intentos y materiales siguen
                  disponibles para continuar o repasar.
                </span>
              </div>
            )}
            <div className="tutorial-banner">
              <div>
                <strong>Tu recorrido: página → editor → revisión</strong>
                <p>
                  Guía rápida, ejemplo del primer ejercicio y cómo guardar tu
                  trabajo.
                </p>
              </div>
              <button
                className="button secondary small"
                onClick={() => showView("guide")}
              >
                <HelpCircle size={16} /> Ver tutorial
              </button>
            </div>
            <div className="day-layout">
              <section className="agenda">
                <div className="agenda-top">
                  <h2>Tu agenda</h2>
                  <span>
                    <Clock3 size={15} /> 4 h de trabajo · pausas aparte
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
                              ? "Completado"
                              : p?.status === "assisted"
                                ? "Completado con pistas"
                                : p?.status === "retry"
                                  ? "Pendiente de otro intento"
                                  : p?.status === "in-progress"
                                    ? "En curso"
                                    : `Bloque ${i + 1}`}
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
                    {next ? "Tu siguiente paso" : "Día completado"}
                  </span>
                  <h2>{next ? next.title : "Buen trabajo por hoy."}</h2>
                  <p>
                    {next
                      ? next.kind === "technical"
                        ? "Abre el enunciado y crea tu copia local. Investiga, verifica y explica cada decisión."
                        : next.summary
                      : "Guarda una copia de tu progreso y descansa. Los resultados describen tu práctica, no garantizan el resultado de la entrevista."}
                  </p>
                  {next && (
                    <button
                      className="button primary"
                      onClick={() => setTask(next)}
                    >
                      <Play size={16} />{" "}
                      {state.tasks[next.id]?.status === "in-progress"
                        ? "Continuar"
                        : "Empezar bloque"}
                    </button>
                  )}
                </section>
                <section className="progress-panel">
                  <h3>Avance de este día</h3>
                  <div className="progress-caption">
                    <strong>
                      {count} de {day.blocks.length} bloques
                    </strong>
                    <span>{formatDuration(completedMinutes)} / 4 h</span>
                  </div>
                  <progress max={day.blocks.length} value={count} />
                  <p>
                    {day.blocks.filter(
                      (b) => state.tasks[b.id]?.status === "retry",
                    ).length > 0
                      ? "Los intentos por repetir quedan pendientes."
                      : "Avance basado en lo que registras como completado."}
                  </p>
                  <div className="overall">
                    <span>Sprint completo</span>
                    <strong>
                      {totalDone} / {all.length} bloques
                    </strong>
                  </div>
                </section>
                <section className="practice-note">
                  <h3>
                    <MessageCircle size={17} /> Practica en voz alta
                  </h3>
                  <p>
                    “What did I observe? Why this change? What evidence shows it
                    works?”
                  </p>
                  <span>El razonamiento forma parte del ejercicio.</span>
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
                <Clock3 size={16} /> Temporizador activo:{" "}
                {running[1].timer?.phase}
                <ChevronRight size={16} />
              </button>
            )}
            {!!previous.length && (
              <details className="previous">
                <summary>
                  {previous.length} bloques anteriores pendientes{" "}
                  <ChevronRight size={16} />
                </summary>
                <p>
                  Se conservan aquí; no se añaden automáticamente a las cuatro
                  horas de hoy.
                </p>
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
                Día anterior
              </button>
              <span>Horario de Tijuana · {dateLabel(day.date, true)}</span>
              <button
                className="text-button"
                disabled={selected === plan.days.length - 1}
                onClick={() => selectDay(selected + 1)}
              >
                Día siguiente
              </button>
            </div>
          </>
        ) : view === "resources" ? (
          <section className="resource-page">
            <p className="date-heading">Investigar con contexto</p>
            <h1>Fuentes y formato</h1>
            <p className="day-focus">
              Los testimonios orientan la práctica. Tu invitación y las
              instrucciones del entrevistador determinan el formato real.
            </p>
            <div className="callout">
              El formato de 20 minutos + 5 de explicación es una referencia de
              entrenamiento. La herramienta, el lenguaje y los tiempos de tu
              convocatoria aún no están confirmados.
            </div>
            {plan.sources.map((s) => (
              <article className="source-row" key={s.id}>
                <span className={`source-level ${s.level}`}>
                  {
                    {
                      official: "Documentación oficial",
                      testimony: "Testimonio",
                      practice: "Práctica creada",
                      repository: "Repositorio",
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
        ) : view === "behavioral" ? (
          <section className="resource-page">
            <p className="date-heading">Hechos, decisiones y resultados</p>
            <h1>Tu práctica behavioral</h1>
            <p className="day-focus">
              Construye seis a ocho historias reales y adapta su énfasis a la
              pregunta. Las notas se guardan solo en este navegador.
            </p>
            <div className="callout">
              No inventes conflictos, resultados ni cifras. Si no recuerdas un
              detalle, déjalo pendiente. Practica una respuesta de unos dos
              minutos y después preguntas de seguimiento.
            </div>
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
                          ? "Tienes notas guardadas"
                          : "Abrir preguntas y preparar mi historia"}
                      </span>
                    </span>
                    <ChevronRight size={18} />
                  </button>
                )),
            )}
          </section>
        ) : (
          <Tutorial firstDay={plan.days[0]} openFirstDay={() => selectDay(0)} />
        )}
        <footer className="page-footer">
          Capital One Prep · Preparación independiente · Material ficticio para
          practicar
        </footer>
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

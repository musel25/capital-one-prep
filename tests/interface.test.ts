import test, { afterEach } from "node:test";
import assert from "node:assert/strict";
import { JSDOM } from "jsdom";
import { createElement, useState } from "react";
import type { Block, Progress } from "../web/types";
import {
  emptyProgress,
  freshState,
  replaceProgress,
  STORAGE_KEY,
} from "../web/model";
import plan from "../curriculum/plan.json";

const dom = new JSDOM("<!doctype html><html><body></body></html>", {
  url: "https://prep.example/grind/capital-one/?day=2026-10-23",
  pretendToBeVisual: true,
});
for (const key of [
  "window",
  "document",
  "navigator",
  "HTMLElement",
  "HTMLDialogElement",
  "Event",
  "StorageEvent",
  "localStorage",
  "location",
  "history",
] as const) {
  Object.defineProperty(globalThis, key, {
    configurable: true,
    value: dom.window[key],
  });
}
Object.assign(globalThis, {
  IS_REACT_ACT_ENVIRONMENT: true,
  confirm: () => true,
});
dom.window.HTMLDialogElement.prototype.showModal = function () {
  this.open = true;
};
const { render, screen, cleanup, fireEvent, act } =
  await import("@testing-library/react");
const { default: userEvent } = await import("@testing-library/user-event");
const { default: App } = await import("../web/App");
const { TaskDialog } = await import("../web/TaskDialog");
const user = userEvent.setup({ document: dom.window.document });
afterEach(() => {
  cleanup();
  localStorage.clear();
  history.replaceState(null, "", "/grind/capital-one/?day=2026-10-23");
});

test("Python setup prompt can be copied with the full contract without changing progress", async () => {
  const block = plan.days[0].blocks.find((b) => b.kind === "python") as Block;
  let saves = 0;
  render(
    createElement(TaskDialog, {
      block,
      sources: [],
      close: () => {},
      save: () => {
        saves++;
        return true;
      },
    }),
  );
  assert.ok(
    screen.getByRole("heading", { name: "Preparar el ejercicio local" }),
  );
  await user.click(screen.getByRole("button", { name: "Copiar prompt" }));
  const copied = await navigator.clipboard.readText();
  assert.match(copied, /ordered_ids\(rows\)/);
  assert.match(copied, /Do not implement/);
  assert.match(copied, /Never overwrite/);
  assert.match(copied, /uv run python/);
  assert.equal(saves, 0);
});

test("tutorial deep link returns to day one without changing saved practice", async () => {
  const id = plan.days[0].blocks[0].id;
  const raw = JSON.stringify(
    replaceProgress(freshState(), id, { notes: "Keep my actual practice." }),
  );
  localStorage.setItem(STORAGE_KEY, raw);
  history.replaceState(null, "", "/grind/capital-one/?view=guide");
  const mounted = render(createElement(App));
  assert.ok(screen.getByRole("heading", { name: "Empieza aquí" }));
  await user.click(screen.getByRole("button", { name: "Abrir el día 1" }));
  assert.equal(new URLSearchParams(location.search).get("day"), "2026-10-23");
  assert.equal(new URLSearchParams(location.search).has("view"), false);
  assert.ok(screen.getByRole("heading", { name: plan.days[0].title }));
  assert.equal(localStorage.getItem(STORAGE_KEY), raw);
  mounted.unmount();
  render(createElement(App));
  assert.ok(screen.getByRole("heading", { name: plan.days[0].title }));
  await user.click(screen.getByRole("button", { name: "Ver tutorial" }));
  assert.equal(new URLSearchParams(location.search).get("view"), "guide");
  assert.ok(screen.getByRole("heading", { name: "Empieza aquí" }));
  assert.equal(localStorage.getItem(STORAGE_KEY), raw);
});

test("case review needs saved prediction and finished attempt; closing preserves a draft", async () => {
  let saved: Progress = emptyProgress();
  let closed = false;
  const block: Block = {
    id: "case",
    title: "Case test",
    kind: "case",
    minutes: 60,
    summary: "Practice",
    content: "Rules",
    deliverables: ["Prediction"],
    rubric: ["Evidence"],
    solution: "The worked explanation.",
  };
  function Harness() {
    const [progress, update] = useState(saved);
    return createElement(TaskDialog, {
      block,
      sources: [],
      progress,
      close: () => {
        closed = true;
      },
      save: (patch) => {
        saved = { ...saved, ...patch };
        update(saved);
        return true;
      },
    });
  }
  render(createElement(Harness));
  await user.click(
    screen.getByRole("button", { name: "Mi intento y revisión" }),
  );
  const reveal = screen.getByRole("button", {
    name: "He terminado: abrir explicación",
  }) as HTMLButtonElement;
  assert.equal(reveal.disabled, true);
  await user.type(
    screen.getByLabelText("Mi predicción"),
    "Approve at the inclusive limit.",
  );
  await user.click(screen.getByRole("button", { name: "Guardar predicción" }));
  assert.equal(reveal.disabled, true);
  await user.click(screen.getByRole("button", { name: "Completado" }));
  assert.equal(reveal.disabled, false);
  await user.click(reveal);
  assert.ok(screen.getByText("The worked explanation."));
  await user.type(screen.getByLabelText("Mi predicción"), " Updated evidence.");
  await user.click(screen.getByRole("button", { name: "Cerrar ejercicio" }));
  assert.equal(closed, true);
  assert.match(saved.prediction, /Updated evidence/);
  assert.equal(saved.reviewed, true);
});

test("daily task notes, checklist and running timer restore after remount", async () => {
  const technical = plan.days[0].blocks[0];
  const mounted = render(createElement(App));
  await user.click(screen.getByRole("button", { name: "Empezar bloque" }));
  await user.click(screen.getByRole("button", { name: "Iniciar" }));
  await user.click(
    screen.getByRole("button", { name: "Mi intento y revisión" }),
  );
  await user.type(
    screen.getByLabelText("Notas, evidencia y preguntas pendientes"),
    "My local test evidence.",
  );
  await user.click(screen.getAllByRole("checkbox")[0]);
  const before = JSON.parse(localStorage.getItem(STORAGE_KEY)!);
  assert.equal(before.tasks[technical.id].notes, "My local test evidence.");
  assert.equal(before.tasks[technical.id].checked.length, 1);
  assert.ok(before.tasks[technical.id].timer.startedAt);
  mounted.unmount();
  render(createElement(App));
  await user.click(screen.getByRole("button", { name: "Continuar" }));
  assert.ok(screen.getByRole("button", { name: "Pausar" }));
  await user.click(
    screen.getByRole("button", { name: "Mi intento y revisión" }),
  );
  assert.equal(
    (
      screen.getByLabelText(
        "Notas, evidencia y preguntas pendientes",
      ) as HTMLTextAreaElement
    ).value,
    "My local test evidence.",
  );
  assert.equal(
    (screen.getAllByRole("checkbox")[0] as HTMLInputElement).checked,
    true,
  );
});

test("invalid import preserves progress and another tab cannot silently overwrite it", async () => {
  const id = plan.days[0].blocks[0].id;
  const state = replaceProgress(freshState(), id, { notes: "Keep this note." });
  localStorage.setItem(STORAGE_KEY, JSON.stringify(state));
  render(createElement(App));
  await act(async () => {
    fireEvent.change(screen.getByLabelText("Importar progreso"), {
      target: { files: [{ size: 20, text: async () => '{"version":99}' }] },
    });
  });
  assert.match(
    screen.getByRole("alert").textContent!,
    /no es un respaldo válido/,
  );
  assert.equal(
    JSON.parse(localStorage.getItem(STORAGE_KEY)!).tasks[id].notes,
    "Keep this note.",
  );
  const changed = replaceProgress(state, id, { notes: "Newer tab note." });
  const raw = JSON.stringify(changed);
  localStorage.setItem(STORAGE_KEY, raw);
  act(() =>
    window.dispatchEvent(
      new StorageEvent("storage", { key: STORAGE_KEY, newValue: raw }),
    ),
  );
  assert.match(screen.getByRole("alert").textContent!, /otra pestaña/);
  await user.click(screen.getByRole("button", { name: "Empezar bloque" }));
  await user.click(screen.getByRole("button", { name: "Iniciar" }));
  assert.equal(localStorage.getItem(STORAGE_KEY), raw);
});

test("a storage failure preserves the note draft and prevents closing away unsaved work", async () => {
  const id = plan.days[0].blocks[0].id;
  localStorage.setItem(
    STORAGE_KEY,
    JSON.stringify(replaceProgress(freshState(), id, { notes: "Saved note." })),
  );
  render(createElement(App));
  await user.click(screen.getByRole("button", { name: "Empezar bloque" }));
  await user.click(
    screen.getByRole("button", { name: "Mi intento y revisión" }),
  );
  const field = screen.getByLabelText(
    "Notas, evidencia y preguntas pendientes",
  ) as HTMLTextAreaElement;
  const originalSetItem = dom.window.Storage.prototype.setItem;
  try {
    dom.window.Storage.prototype.setItem = () => {
      throw new dom.window.DOMException("Quota exceeded", "QuotaExceededError");
    };
    fireEvent.change(field, {
      target: { value: "Saved note. My long new story." },
    });
    assert.equal(field.value, "Saved note. My long new story.");
    assert.ok(document.querySelector("dialog [role=alert]"));
    await user.click(screen.getByRole("button", { name: "Cerrar ejercicio" }));
    assert.ok(document.querySelector("dialog"));
    assert.equal(field.value, "Saved note. My long new story.");
  } finally {
    dom.window.Storage.prototype.setItem = originalSetItem;
  }
  await user.click(screen.getByRole("button", { name: "Cerrar ejercicio" }));
  assert.equal(document.querySelector("dialog"), null);
  assert.equal(
    JSON.parse(localStorage.getItem(STORAGE_KEY)!).tasks[id].notes,
    "Saved note. My long new story.",
  );
});

import test, { afterEach } from "node:test";
import assert from "node:assert/strict";
import { JSDOM } from "jsdom";
import { createElement, useState } from "react";
import type { Block, Plan, Progress } from "../web/types";
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
  const block = ((plan as Plan).archivedBlocks ?? plan.days[0].blocks).find(
    (b) => b.id === "d01-python",
  ) as Block;
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
  assert.ok(screen.getByRole("heading", { name: "Local setup" }));
  await user.click(screen.getByRole("button", { name: "Copy prompt" }));
  const copied = await navigator.clipboard.readText();
  assert.match(copied, /ordered_ids\(rows\)/);
  assert.match(copied, /Do not implement/);
  assert.match(copied, /Never overwrite/);
  assert.match(copied, /uv run python/);
  assert.equal(saves, 0);
});

test("replacement LeetCode assignment stays pending and old Python notes remain accessible", async () => {
  const old = replaceProgress(freshState(), "d01-python", {
    status: "done",
    notes: "My earlier sorting solution.",
    checked: ["rubric-0"],
  });
  const raw = JSON.stringify(old);
  localStorage.setItem(STORAGE_KEY, raw);
  render(createElement(App));
  assert.equal(screen.queryByRole("alert"), null);
  assert.ok(screen.getByText("0 / 40 tasks"));
  assert.equal(localStorage.getItem(STORAGE_KEY), raw);
  await user.click(screen.getByRole("button", { name: "Previous exercises" }));
  await user.click(
    screen.getByRole("button", { name: /Python: sort without mutation/ }),
  );
  await user.click(screen.getByRole("button", { name: "My attempt" }));
  assert.equal(
    (
      screen.getByLabelText(
        "Notes, evidence, and open questions",
      ) as HTMLTextAreaElement
    ).value,
    "My earlier sorting solution.",
  );
});

test("archived authorization notes cannot unlock the new number-validation answer", async () => {
  const old = replaceProgress(freshState(), "d06-case-v2", {
    status: "done",
    reviewed: true,
    prediction: "My previous authorization trace.",
    notes: "Keep this earlier work.",
  });
  const raw = JSON.stringify(old);
  localStorage.setItem(STORAGE_KEY, raw);
  history.replaceState(null, "", "/grind/capital-one/?day=2026-10-28");
  render(createElement(App));
  await user.click(
    screen.getByRole("button", {
      name: /Case: digital card-number validation/,
    }),
  );
  await user.click(screen.getByRole("button", { name: "My attempt" }));
  assert.equal(
    (screen.getByLabelText("My prediction") as HTMLTextAreaElement).value,
    "",
  );
  assert.equal(
    (
      screen.getByRole("button", {
        name: "Reveal explanation",
      }) as HTMLButtonElement
    ).disabled,
    true,
  );
  await user.click(screen.getByRole("button", { name: "Close exercise" }));
  await user.click(screen.getByRole("button", { name: "Previous exercises" }));
  await user.click(
    screen.getByRole("button", { name: /Case: virtual-card authorization/ }),
  );
  await user.click(screen.getByRole("button", { name: "My attempt" }));
  assert.equal(
    (screen.getByLabelText("My prediction") as HTMLTextAreaElement).value,
    "My previous authorization trace.",
  );
  assert.equal(localStorage.getItem(STORAGE_KEY), raw);
});

test("focused behavioral mock draws all three themes before ending the round", async () => {
  const block = (plan as Plan).days[7].blocks[2];
  render(
    createElement(TaskDialog, {
      block,
      sources: [],
      close: () => {},
      save: () => true,
    }),
  );
  const questions = new Set<string>();
  for (let i = 0; i < 3; i++) {
    await user.click(screen.getByRole("button", { name: "Draw a question" }));
    questions.add(screen.getByTestId("drawn-question").textContent ?? "");
    await user.click(screen.getByRole("button", { name: "Show follow-ups" }));
  }
  assert.equal(questions.size, 3);
  assert.ok([...questions].some((q) => /team.*deliver/i.test(q)));
  assert.ok([...questions].some((q) => /challenged.*process/i.test(q)));
  assert.ok([...questions].some((q) => /obstacle.*programming/i.test(q)));
  assert.equal(
    (
      screen.getByRole("button", {
        name: "Draw a question",
      }) as HTMLButtonElement
    ).disabled,
    true,
  );
});

test("progressive technical exercise reveals one coding stage at a time", async () => {
  const block = (plan as Plan).days[6].blocks[0];
  render(
    createElement(TaskDialog, {
      block,
      sources: [],
      close: () => {},
      save: () => true,
    }),
  );
  assert.ok(screen.getByRole("region", { name: "Coding stages" }));
  assert.ok(screen.getByRole("heading", { name: /Aggregate purchases/ }));
  assert.equal(
    screen.queryByRole("heading", { name: /Partial refunds/ }),
    null,
  );
  await user.click(screen.getByRole("button", { name: "Reveal next stage" }));
  assert.ok(
    screen.getByRole("heading", { name: /Replayed and conflicting IDs/ }),
  );
  await user.click(screen.getByRole("button", { name: "Reveal next stage" }));
  assert.ok(screen.getByRole("heading", { name: /Partial refunds/ }));
  assert.equal(
    screen.queryByRole("heading", { name: "Open in your editor" }),
    null,
  );
});

test("problem cards link to the official exercise without changing progress", () => {
  let saves = 0;
  const block = {
    id: "lc",
    title: "Bank practice",
    kind: "python",
    minutes: 60,
    summary: "Practice",
    content: "Solve independently.",
    deliverables: [],
    rubric: [],
    problems: [
      {
        number: 2043,
        title: "Simple Bank System",
        difficulty: "Medium",
        url: "https://leetcode.com/problems/simple-bank-system/",
        focus: "State across calls",
      },
    ],
  } as Block;
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
  const link = screen.getByRole("link", { name: /2043. Simple Bank System/ });
  assert.equal(
    link.getAttribute("href"),
    "https://leetcode.com/problems/simple-bank-system/",
  );
  assert.equal(saves, 0);
  assert.equal(screen.queryByRole("heading", { name: "Local setup" }), null);
});

test("case stages reveal progressively without revealing the answer key", async () => {
  const block = {
    id: "staged",
    title: "Staged case",
    kind: "case",
    minutes: 60,
    summary: "Practice",
    content: "Ask questions first.",
    deliverables: [],
    rubric: [],
    stages: [
      { title: "Business", content: "Discuss customer impact." },
      { title: "Rules", content: "Trace rule table." },
    ],
    solution: "Secret answer.",
  } as Block;
  render(
    createElement(TaskDialog, {
      block,
      sources: [],
      close: () => {},
      save: () => true,
    }),
  );
  assert.ok(screen.getByText("Discuss customer impact."));
  assert.equal(screen.queryByText("Trace rule table."), null);
  await user.click(screen.getByRole("button", { name: "Reveal next stage" }));
  assert.ok(screen.getByText("Trace rule table."));
  assert.equal(screen.queryByText("Secret answer."), null);
});

test("behavioral rehearsal draws unseen questions and reveals their follow-ups on demand", async () => {
  const block = {
    id: "draw",
    title: "Rehearsal",
    kind: "behavioral",
    minutes: 30,
    summary: "Practice",
    content: "Answer aloud.",
    deliverables: [],
    rubric: [],
    promptGroups: [
      {
        question: "Explain a disagreement.",
        followUps: ["Why was their position reasonable?"],
      },
      {
        question: "Explain a mistake.",
        followUps: ["When did you tell the team?"],
      },
    ],
  } as Block;
  render(
    createElement(TaskDialog, {
      block,
      sources: [],
      close: () => {},
      save: () => true,
    }),
  );
  assert.equal(screen.queryByText("Explain a disagreement."), null);
  await user.click(screen.getByRole("button", { name: "Draw a question" }));
  const first = screen.getByTestId("drawn-question").textContent;
  assert.equal(screen.queryByText("Why was their position reasonable?"), null);
  assert.equal(screen.queryByText("When did you tell the team?"), null);
  await user.click(screen.getByRole("button", { name: "Show follow-ups" }));
  assert.ok(
    screen.getByText(
      first === "Explain a disagreement."
        ? "Why was their position reasonable?"
        : "When did you tell the team?",
    ),
  );
  await user.click(screen.getByRole("button", { name: "Draw a question" }));
  assert.notEqual(screen.getByTestId("drawn-question").textContent, first);
});

test("removed closing blocks stay in saved progress without appearing in the agenda or timers", async () => {
  const old = replaceProgress(freshState(), "d01-reflection", {
    notes: "Keep this older closing note.",
    status: "done",
    timer: {
      elapsed: 0,
      startedAt: Date.now(),
      duration: 900,
      phase: "Old closing",
    },
  });
  const raw = JSON.stringify(old);
  localStorage.setItem(STORAGE_KEY, raw);
  render(createElement(App));
  assert.equal(screen.queryByRole("alert"), null);
  assert.ok(
    screen.queryByText("Closing reflection") === null,
    "Closing block must not appear",
  );
  assert.ok(
    screen.queryByRole("button", { name: /Timer running/ }) === null,
    "Archived timers must not appear",
  );
  assert.ok(screen.getByText("0 / 40 tasks"));
  assert.ok(screen.getByText("0 min / 3 h 45 min"));
  assert.equal(localStorage.getItem(STORAGE_KEY), raw);
  await user.click(screen.getByRole("button", { name: "Start task" }));
  await user.click(screen.getByRole("button", { name: "Start" }));
  assert.equal(
    JSON.parse(localStorage.getItem(STORAGE_KEY)!).tasks["d01-reflection"]
      .notes,
    "Keep this older closing note.",
  );
});

test("older backups with closing notes can still be imported", async () => {
  const old = replaceProgress(freshState(), "d10-reflection", {
    notes: "Old final notes.",
  });
  render(createElement(App));
  await act(async () => {
    fireEvent.change(screen.getByLabelText("Import progress"), {
      target: {
        files: [{ size: 1000, text: async () => JSON.stringify(old) }],
      },
    });
  });
  assert.equal(screen.queryByRole("alert"), null);
  assert.equal(
    JSON.parse(localStorage.getItem(STORAGE_KEY)!).tasks["d10-reflection"]
      .notes,
    "Old final notes.",
  );
});

test("a saved Spanish timer keeps its phase and elapsed time in the English UI", async () => {
  const id = "d01-technical";
  const raw = JSON.stringify(
    replaceProgress(freshState(), id, {
      status: "in-progress",
      notes: "Keep my notes.",
      prediction: "Keep my prediction.",
      checked: ["rubric-1"],
      timer: {
        elapsed: 123,
        startedAt: Date.now(),
        duration: 1200,
        phase: "Bug: trabajo",
      },
    }),
  );
  localStorage.setItem(STORAGE_KEY, raw);
  render(createElement(App));
  assert.equal(localStorage.getItem(STORAGE_KEY), raw);
  await user.click(
    screen.getByRole("button", { name: /Timer running: Bug: implement/ }),
  );
  assert.equal(
    (screen.getByRole("combobox", { name: "Timer phase" }) as HTMLSelectElement)
      .value,
    "Bug: implement",
  );
  await user.click(screen.getByRole("button", { name: "Pause" }));
  const paused = JSON.parse(localStorage.getItem(STORAGE_KEY)!).tasks[id];
  assert.ok(paused.timer.elapsed >= 123);
  assert.equal(paused.timer.startedAt, null);
  await user.click(screen.getByRole("button", { name: "Start" }));
  const resumed = JSON.parse(localStorage.getItem(STORAGE_KEY)!).tasks[id];
  assert.equal(resumed.timer.phase, "Bug: implement");
  assert.equal(resumed.timer.elapsed, paused.timer.elapsed);
  assert.equal(resumed.timer.duration, 1200);
  assert.ok(resumed.timer.startedAt);
  assert.equal(resumed.notes, "Keep my notes.");
  assert.equal(resumed.prediction, "Keep my prediction.");
  assert.deepEqual(resumed.checked, ["rubric-1"]);
});

test("old tutorial links open the agenda without changing saved practice", () => {
  const id = plan.days[0].blocks[0].id;
  const raw = JSON.stringify(
    replaceProgress(freshState(), id, { notes: "Keep my actual practice." }),
  );
  localStorage.setItem(STORAGE_KEY, raw);
  history.replaceState(
    null,
    "",
    "/grind/capital-one/?view=guide&day=2026-10-23",
  );
  const mounted = render(createElement(App));
  assert.ok(screen.getByRole("heading", { name: plan.days[0].title }));
  assert.ok(screen.queryByRole("button", { name: /tutorial/i }) === null);
  assert.equal(localStorage.getItem(STORAGE_KEY), raw);
  mounted.unmount();
  render(createElement(App));
  assert.ok(screen.getByRole("heading", { name: plan.days[0].title }));
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
  await user.click(screen.getByRole("button", { name: "My attempt" }));
  const reveal = screen.getByRole("button", {
    name: "Reveal explanation",
  }) as HTMLButtonElement;
  assert.equal(reveal.disabled, true);
  await user.type(
    screen.getByLabelText("My prediction"),
    "Approve at the inclusive limit.",
  );
  await user.click(screen.getByRole("button", { name: "Save prediction" }));
  assert.equal(reveal.disabled, true);
  await user.click(screen.getByRole("button", { name: "Completed" }));
  assert.equal(reveal.disabled, false);
  await user.click(reveal);
  assert.ok(screen.getByText("The worked explanation."));
  await user.type(screen.getByLabelText("My prediction"), " Updated evidence.");
  await user.click(screen.getByRole("button", { name: "Close exercise" }));
  assert.equal(closed, true);
  assert.match(saved.prediction, /Updated evidence/);
  assert.equal(saved.reviewed, true);
});

test("daily task notes, checklist and running timer restore after remount", async () => {
  const technical = plan.days[0].blocks[0];
  const mounted = render(createElement(App));
  await user.click(screen.getByRole("button", { name: "Start task" }));
  await user.click(screen.getByRole("button", { name: "Start" }));
  await user.click(screen.getByRole("button", { name: "My attempt" }));
  await user.type(
    screen.getByLabelText("Notes, evidence, and open questions"),
    "My local test evidence.",
  );
  await user.click(screen.getByText("Review checklist"));
  await user.click(screen.getAllByRole("checkbox")[0]);
  const before = JSON.parse(localStorage.getItem(STORAGE_KEY)!);
  assert.equal(before.tasks[technical.id].notes, "My local test evidence.");
  assert.equal(before.tasks[technical.id].checked.length, 1);
  assert.ok(before.tasks[technical.id].timer.startedAt);
  mounted.unmount();
  render(createElement(App));
  await user.click(screen.getByRole("button", { name: "Continue" }));
  assert.ok(screen.getByRole("button", { name: "Pause" }));
  await user.click(screen.getByRole("button", { name: "My attempt" }));
  assert.equal(
    (
      screen.getByLabelText(
        "Notes, evidence, and open questions",
      ) as HTMLTextAreaElement
    ).value,
    "My local test evidence.",
  );
  await user.click(screen.getByText("Review checklist"));
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
    fireEvent.change(screen.getByLabelText("Import progress"), {
      target: { files: [{ size: 20, text: async () => '{"version":99}' }] },
    });
  });
  assert.match(screen.getByRole("alert").textContent!, /not a valid backup/);
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
  assert.match(screen.getByRole("alert").textContent!, /another tab/);
  await user.click(screen.getByRole("button", { name: "Start task" }));
  await user.click(screen.getByRole("button", { name: "Start" }));
  assert.equal(localStorage.getItem(STORAGE_KEY), raw);
});

test("a storage failure preserves the note draft and prevents closing away unsaved work", async () => {
  const id = plan.days[0].blocks[0].id;
  localStorage.setItem(
    STORAGE_KEY,
    JSON.stringify(replaceProgress(freshState(), id, { notes: "Saved note." })),
  );
  render(createElement(App));
  await user.click(screen.getByRole("button", { name: "Start task" }));
  await user.click(screen.getByRole("button", { name: "My attempt" }));
  const field = screen.getByLabelText(
    "Notes, evidence, and open questions",
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
    await user.click(screen.getByRole("button", { name: "Close exercise" }));
    assert.ok(document.querySelector("dialog"));
    assert.equal(field.value, "Saved note. My long new story.");
  } finally {
    dom.window.Storage.prototype.setItem = originalSetItem;
  }
  await user.click(screen.getByRole("button", { name: "Close exercise" }));
  assert.equal(document.querySelector("dialog"), null);
  assert.equal(
    JSON.parse(localStorage.getItem(STORAGE_KEY)!).tasks[id].notes,
    "Saved note. My long new story.",
  );
});

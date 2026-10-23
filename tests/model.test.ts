import test from "node:test";
import assert from "node:assert/strict";
import {
  dayIn,
  dayIndex,
  freshState,
  validateState,
  elapsedSeconds,
  canReview,
  replaceProgress,
} from "../web/model.ts";
const dates = ["2026-10-23", "2026-10-24", "2026-11-01"];
test("Tijuana day and bounded calendar selection", () => {
  assert.equal(dayIn(new Date("2026-10-23T01:00:00Z")), "2026-10-22");
  assert.equal(dayIndex(dates, "2026-10-22"), 0);
  assert.equal(dayIndex(dates, "2026-10-24"), 1);
  assert.equal(dayIndex(dates, "2026-11-02"), 2);
});
test("progress import rejects malformed data before replacement", () => {
  const s = freshState();
  assert.throws(() =>
    validateState({ ...s, tasks: { x: { status: "done" } } }, ["x"]),
  );
  assert.throws(() => validateState({ ...s, version: 2 }, ["x"]));
  assert.throws(() =>
    validateState(
      {
        ...s,
        tasks: {
          unknown: {
            status: "pending",
            notes: "",
            prediction: "",
            checked: [],
            minutes: 0,
            reviewed: false,
            timer: null,
          },
        },
      },
      ["x"],
    ),
  );
  assert.throws(() =>
    validateState(
      {
        ...s,
        tasks: {
          x: {
            status: "done",
            notes: "",
            prediction: "",
            checked: [],
            minutes: -1,
            reviewed: false,
            timer: null,
          },
        },
      },
      ["x"],
    ),
  );
});
test("saved answers, notes, timers and outcomes survive export", () => {
  const s = replaceProgress(freshState(), "x", {
    notes: "Test evidence",
    prediction: "Reject because expired",
    status: "assisted",
    minutes: 35,
  });
  assert.deepEqual(validateState(JSON.parse(JSON.stringify(s)), ["x"]), s);
  assert.equal(s.tasks.x.notes, "Test evidence");
});
test("timer survives refresh and pause using elapsed wall time", () => {
  assert.equal(
    elapsedSeconds(
      { elapsed: 10, startedAt: 1000, duration: 1200, phase: "Bug" },
      6000,
    ),
    15,
  );
  assert.equal(
    elapsedSeconds(
      { elapsed: 10, startedAt: null, duration: 1200, phase: "Bug" },
      9000,
    ),
    10,
  );
  assert.equal(
    elapsedSeconds(
      { elapsed: 10, startedAt: 10000, duration: 1200, phase: "Bug" },
      9000,
    ),
    10,
  );
});
test("case answer reveal requires saved prediction and completed attempt", () => {
  const s = replaceProgress(freshState(), "x", { prediction: "Approve" });
  assert.equal(canReview(s.tasks.x), false);
  s.tasks.x.status = "retry";
  assert.equal(canReview(s.tasks.x), true);
  s.tasks.x.prediction = " ";
  assert.equal(canReview(s.tasks.x), false);
});

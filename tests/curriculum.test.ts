import test from "node:test";
import assert from "node:assert/strict";
import { readFileSync } from "node:fs";
import type { Plan } from "../web/types";
const plan = JSON.parse(
  readFileSync(new URL("../curriculum/plan.json", import.meta.url), "utf8"),
) as Plan;
test("archived mock instructions and timer phases retain their original definitions", () => {
  const originalBlocks = JSON.parse(
    readFileSync(
      new URL("./fixtures/archived-mocks.json", import.meta.url),
      "utf8",
    ),
  ) as Plan["archivedBlocks"];
  for (const original of originalBlocks ?? []) {
    assert.deepEqual(
      plan.archivedBlocks?.find((b) => b.id === original.id),
      original,
    );
  }
});

test("all ten days have four actionable blocks totaling 225 minutes", () => {
  assert.equal(plan.days.length, 10);
  assert.equal(plan.timezone, "America/Tijuana");
  assert.equal(plan.dailyMinutes, 225);
  const blockIds = new Set<string>();
  const labIds = new Set<string>();
  const sources = new Set(plan.sources.map((s) => s.id));
  for (let i = 0; i < 10; i++) {
    const day = plan.days[i];
    const expected = new Date(Date.UTC(2026, 9, 23 + i))
      .toISOString()
      .slice(0, 10);
    assert.equal(day.date, expected);
    assert.equal(
      day.blocks.reduce((n, b) => n + b.minutes, 0),
      225,
      day.date,
    );
    assert.equal(day.blocks.length, 4);
    assert.deepEqual(
      day.blocks.map((b) => b.kind),
      ["technical", "case", "behavioral", "python"],
    );
    for (const b of day.blocks) {
      assert.ok(!blockIds.has(b.id));
      blockIds.add(b.id);
      assert.ok(b.content.length >= 150, `${b.id} needs actual instructions`);
      assert.ok(b.deliverables.length >= 1);
      assert.ok(b.rubric.length >= 1);
      for (const s of b.sources ?? [])
        assert.ok(sources.has(s), `${b.id}: unknown source ${s}`);
      for (const l of b.labs ?? []) labIds.add(l);
      if (b.kind === "technical") {
        if (b.stages?.length) assert.equal(b.stages.length, 3);
        else assert.equal(b.labs?.length, 2);
      }
      if (b.phases?.length)
        assert.equal(
          b.phases.reduce((n, p) => n + p.minutes, 0),
          b.minutes,
          `${b.id} phase duration`,
        );
      if (b.kind === "case")
        assert.ok(
          b.solution && b.solution.length > 100,
          `${b.id} needs reasoned case key`,
        );
    }
  }
  assert.equal(labIds.size, 18);
});

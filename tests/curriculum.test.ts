import test from "node:test";
import assert from "node:assert/strict";
import { readFileSync } from "node:fs";
import type { Plan } from "../web/types";
const plan = JSON.parse(
  readFileSync(new URL("../curriculum/plan.json", import.meta.url), "utf8"),
) as Plan;
test("all ten days have exactly four hours and complete actionable content", () => {
  assert.equal(plan.days.length, 10);
  assert.equal(plan.timezone, "America/Tijuana");
  assert.equal(plan.dailyMinutes, 240);
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
      240,
      day.date,
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
  for (let i = 1; i <= 10; i++)
    for (const kind of ["bug", "feature"])
      assert.ok(labIds.has(`d${String(i).padStart(2, "0")}-${kind}`));
});

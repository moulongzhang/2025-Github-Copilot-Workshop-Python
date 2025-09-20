import { test } from 'node:test';
import assert from 'node:assert/strict';
import { createTimer } from '../timer-core.js';

test('create/pause/reset sequence behaves as expected', () => {
  const nowStart = 1000;
  let now = nowStart;
  const nowProvider = () => now;

  const t = createTimer(1000, nowProvider);
  // initial remaining should be plannedMs
  assert.strictEqual(t.getRemaining(), 1000);

  // start at now=1000
  t.start();
  now += 400; // 400ms later
  const rem1 = t.getRemaining();
  assert(rem1 <= 600 && rem1 >= 580, `unexpected rem1=${rem1}`);

  // pause
  t.pause();
  now += 200; // time passes during pause
  const remPaused = t.getRemaining();
  assert.strictEqual(remPaused, rem1, `expected paused remaining to be stable, got ${remPaused}`);

  // resume
  t.start();
  now += 500; // 500ms after resume
  const remAfterResume = t.getRemaining();
  // should be roughly rem1 - 500
  assert(remAfterResume <= rem1 - 480 && remAfterResume >= rem1 - 520, `unexpected remAfterResume=${remAfterResume}`);

  // reset
  t.reset();
  assert.strictEqual(t.getRemaining(), 1000);
});

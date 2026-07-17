import assert from "node:assert/strict";
import fs from "node:fs";
import test from "node:test";
import vm from "node:vm";


function makeElement(overrides = {}) {
  const listeners = {};
  return {
    addEventListener(name, handler) {
      listeners[name] = handler;
    },
    classList: {
      add() {},
      remove() {},
      toggle() {}
    },
    contains() {
      return false;
    },
    dataset: { maxBytes: String(2 * 1024 * 1024) },
    disabled: false,
    files: [],
    hidden: true,
    setCustomValidity() {},
    textContent: "",
    value: "",
    _listeners: listeners,
    ...overrides
  };
}


test("back navigation resets transient simulation progress", () => {
  const form = makeElement();
  const elements = {
    "sim-form": form,
    fight_style: makeElement({ value: "patchwerk" }),
    desired_targets: makeElement(),
    max_time: makeElement(),
    "desired-targets-field": makeElement(),
    "max-time-field": makeElement(),
    "fight-style-help": makeElement(),
    "desired-targets-note": makeElement(),
    "max-time-note": makeElement(),
    simc_file: makeElement(),
    "file-zone": makeElement(),
    "file-label": makeElement(),
    "file-hint": makeElement(),
    simc_text: makeElement({ value: "mage=example" }),
    "run-button": makeElement({ textContent: "Run simulation" }),
    "run-status": makeElement({ hidden: true }),
    "elapsed-time": makeElement({ textContent: "0:00 elapsed" })
  };
  const windowListeners = {};
  const clearedTimers = [];
  const context = {
    DataTransfer: class {},
    Date,
    document: {
      getElementById(id) {
        return elements[id];
      },
      querySelectorAll() {
        return [];
      }
    },
    window: {
      addEventListener(name, handler) {
        windowListeners[name] = handler;
      },
      clearInterval(timer) {
        clearedTimers.push(timer);
      },
      setInterval() {
        return 42;
      }
    }
  };

  const source = fs.readFileSync("app/static/app.js", "utf8");
  vm.runInNewContext(source, context);

  form._listeners.submit({ preventDefault() {} });
  assert.equal(elements["run-button"].disabled, true);
  assert.equal(elements["run-button"].textContent, "Simulation running");
  assert.equal(elements["run-status"].hidden, false);

  windowListeners.pageshow();

  assert.deepEqual(clearedTimers, [42]);
  assert.equal(elements["run-button"].disabled, false);
  assert.equal(elements["run-button"].textContent, "Run simulation");
  assert.equal(elements["run-status"].hidden, true);
  assert.equal(elements["elapsed-time"].textContent, "0:00 elapsed");
});

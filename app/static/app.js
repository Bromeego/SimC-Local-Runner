(function () {
  const form = document.getElementById("sim-form");
  const fightStyle = document.getElementById("fight_style");
  const desiredTargets = document.getElementById("desired_targets");
  const maxTime = document.getElementById("max_time");
  const desiredTargetsField = document.getElementById("desired-targets-field");
  const maxTimeField = document.getElementById("max-time-field");
  const fightStyleHelp = document.getElementById("fight-style-help");
  const desiredTargetsNote = document.getElementById("desired-targets-note");
  const maxTimeNote = document.getElementById("max-time-note");
  const fileInput = document.getElementById("simc_file");
  const fileZone = document.getElementById("file-zone");
  const fileLabel = document.getElementById("file-label");
  const fileHint = document.getElementById("file-hint");
  const profileText = document.getElementById("simc_text");
  const runButton = document.getElementById("run-button");
  const runStatus = document.getElementById("run-status");
  const elapsedTime = document.getElementById("elapsed-time");
  let elapsedTimer = null;

  const styleCopy = {
    patchwerk: {
      help: "A clean stand-still fight for direct comparisons.",
      targets: "Use a fixed target count for direct comparisons.",
      time: "Controls the simulated encounter length."
    },
    hecticaddcleave: {
      help: "Movement and recurring adds for cleave-focused testing.",
      targets: "Use this as a tuning input for the cleave comparison.",
      time: "Controls the simulated encounter length."
    },
    dungeonslice: {
      help: "A built-in sequence of boss and trash phases.",
      targets: "DungeonSlice manages its own target flow.",
      time: "DungeonSlice manages its own timing."
    }
  };

  function updateFightStyle() {
    const selected = fightStyle.value;
    const copy = styleCopy[selected];
    const dungeonSlice = selected === "dungeonslice";

    fightStyleHelp.textContent = copy.help;
    desiredTargetsNote.textContent = copy.targets;
    maxTimeNote.textContent = copy.time;
    desiredTargets.disabled = dungeonSlice;
    maxTime.disabled = dungeonSlice;
    desiredTargetsField.classList.toggle("is-disabled", dungeonSlice);
    maxTimeField.classList.toggle("is-disabled", dungeonSlice);
  }

  fightStyle.addEventListener("change", updateFightStyle);
  updateFightStyle();

  function showFile(file) {
    const extension = file.name.toLowerCase().split(".").pop();
    const allowed = extension === "simc" || extension === "txt";
    const maxBytes = Number(fileZone.dataset.maxBytes);

    if (!allowed) {
      fileInput.value = "";
      fileZone.classList.add("is-error");
      fileLabel.textContent = "That file type is not supported";
      fileHint.textContent = "Choose a .simc or .txt file.";
      return false;
    }

    if (file.size > maxBytes) {
      fileInput.value = "";
      fileZone.classList.add("is-error");
      fileLabel.textContent = "That profile is too large";
      fileHint.textContent = `The maximum upload size is ${Math.round(maxBytes / 1024 / 1024)} MB.`;
      return false;
    }

    fileZone.classList.remove("is-error");
    fileLabel.textContent = file.name;
    fileHint.textContent = "Ready to simulate. Drop another file to replace it.";
    profileText.setCustomValidity("");
    return true;
  }

  fileInput.addEventListener("change", function () {
    if (fileInput.files.length) showFile(fileInput.files[0]);
  });

  ["dragenter", "dragover"].forEach(function (eventName) {
    fileZone.addEventListener(eventName, function (event) {
      event.preventDefault();
      event.stopPropagation();
      fileZone.classList.add("is-dragging");
    });
  });

  ["dragleave", "drop"].forEach(function (eventName) {
    fileZone.addEventListener(eventName, function (event) {
      event.preventDefault();
      event.stopPropagation();
      if (eventName === "dragleave" && fileZone.contains(event.relatedTarget)) return;
      fileZone.classList.remove("is-dragging");
    });
  });

  fileZone.addEventListener("drop", function (event) {
    const file = event.dataTransfer.files[0];
    if (!file || !showFile(file)) return;

    const transfer = new DataTransfer();
    transfer.items.add(file);
    fileInput.files = transfer.files;
  });

  profileText.addEventListener("input", function () {
    profileText.setCustomValidity("");
  });

  function resetRunState() {
    if (elapsedTimer !== null) {
      window.clearInterval(elapsedTimer);
      elapsedTimer = null;
    }

    runButton.disabled = false;
    runButton.textContent = "Run simulation";
    runStatus.hidden = true;
    elapsedTime.textContent = "0:00 elapsed";
  }

  // Browsers may restore this page from their back-forward cache exactly as it
  // looked during submission. Reset transient progress UI whenever it returns.
  window.addEventListener("pageshow", resetRunState);
  window.addEventListener("pagehide", function () {
    if (elapsedTimer !== null) {
      window.clearInterval(elapsedTimer);
      elapsedTimer = null;
    }
  });

  form.addEventListener("submit", function (event) {
    if (!fileInput.files.length && !profileText.value.trim()) {
      event.preventDefault();
      profileText.setCustomValidity("Upload a profile or paste profile contents.");
      profileText.reportValidity();
      return;
    }

    runButton.disabled = true;
    runButton.textContent = "Simulation running";
    runStatus.hidden = false;

    const startedAt = Date.now();
    elapsedTimer = window.setInterval(function () {
      const totalSeconds = Math.floor((Date.now() - startedAt) / 1000);
      const minutes = Math.floor(totalSeconds / 60);
      const seconds = String(totalSeconds % 60).padStart(2, "0");
      elapsedTime.textContent = `${minutes}:${seconds} elapsed`;
    }, 1000);
  });

  document.querySelectorAll("[data-delete-report]").forEach(function (deleteForm) {
    deleteForm.addEventListener("submit", function (event) {
      if (!window.confirm("Delete this report and its saved input profile?")) {
        event.preventDefault();
      }
    });
  });
})();

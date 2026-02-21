(function (global) {
    "use strict";

    const DEFAULT_FILE_MESSAGE =
        "Please serve this file over HTTP (e.g. python -m http.server) so Pyodide can fetch resources.";

    function ensureHttp(statusElement, message = DEFAULT_FILE_MESSAGE) {
        if (global.location && global.location.protocol === "file:") {
            if (statusElement) {
                statusElement.textContent = message;
            }
            return false;
        }
        return true;
    }

    async function fetchTextOrThrow(path, label = path) {
        const response = await fetch(path);
        if (!response.ok) {
            throw new Error(`Failed to fetch ${label} (${response.status})`);
        }
        return response.text();
    }

    async function loadPyodideAndDisplayio({ statusElement, displayioPath }) {
        if (statusElement) {
            statusElement.textContent = "Loading Pyodide\u2026";
        }
        const pyodide = await loadPyodide();

        if (statusElement) {
            statusElement.textContent = "Loading displayio module\u2026";
        }
        const moduleCode = await fetchTextOrThrow(displayioPath, displayioPath);
        pyodide.FS.writeFile("/home/pyodide/displayio.py", moduleCode);

        return pyodide;
    }

    async function loadPythonFile(pyodide, { sourcePath, targetPath, label }) {
        const code = await fetchTextOrThrow(sourcePath, label || sourcePath);
        pyodide.FS.writeFile(targetPath, code);
    }

    global.beadyeyePyodide = {
        ensureHttp,
        fetchTextOrThrow,
        loadPyodideAndDisplayio,
        loadPythonFile,
    };
})(window);

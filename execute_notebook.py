"""Execute the assignment notebook and save measured results from that execution."""

from __future__ import annotations

import base64
import asyncio
import hashlib
import json
import os
import sys
from pathlib import Path

import nbformat
from nbclient import NotebookClient

ROOT = Path(__file__).resolve().parent
NOTEBOOK = ROOT / "Assignment3.ipynb"

# This temporary cell reads runtime variables. It is removed before the notebook
# is saved; no sampled counts are typed into the notebook or this script.
CAPTURE = '''import json, platform, sys, qiskit, qiskit_aer
matrices = {"a": np.kron(X, X), "b": np.kron(I2, X),
            "c": np.kron(H, H), "d": np.kron(Y, Z)}
counts_by_part = {"a": counts_q1a, "b": counts_q1b,
                  "c": counts_q1c, "d": counts_q1d}
captured = {"shots": SHOTS, "seed": SEED, "backend": "ideal AerSimulator",
            "provenance": {"data_origin": "executed Assignment3.ipynb",
                           "python_executable": sys.executable,
                           "noise_model": None,
                           "versions": {"python": platform.python_version(),
                                        "qiskit": qiskit.__version__,
                                        "qiskit_aer": qiskit_aer.__version__}},
            "q1": {}, "q2": {}}
for key, matrix in matrices.items():
    captured["q1"][key] = {
        "matrix": [[[float(z.real), float(z.imag)] for z in row] for row in matrix],
        "probabilities": {b: float(abs(matrix[k, 0]) ** 2) for k, b in enumerate(BASIS)},
        "counts": counts_by_part[key]}
captured["q2"]["statevector"] = [[float(z.real), float(z.imag)] for z in psi_out.data]
print(json.dumps(captured))
'''


class InterpreterNotebookClient(NotebookClient):
    """Start the kernel with the interpreter that launched this script."""

    def create_kernel_manager(self):
        manager = super().create_kernel_manager()
        manager.kernel_spec.argv[0] = sys.executable
        return manager


def histogram_comment(key, result, shots):
    counts = result["counts"]
    listing = "; ".join(f"{bits}: {counts[bits]}" for bits in ["00", "01", "10", "11"])
    if key == "c":
        explanation = (f"The prediction is probability 1/4 for every outcome, or {shots / 4:g} "
                       "counts per outcome on average. The observed bars are approximately equal; "
                       "their small differences arise from finite-shot sampling in the ideal simulator.")
    else:
        bits = {"a": "11", "b": "01", "d": "10"}[key]
        explanation = (f"All {shots} shots give {bits}, matching P({bits}) = 1 and probability 0 "
                       "for the other outcomes.")
        if key == "d":
            explanation += " The global phase i in i|10⟩ does not change measurement probabilities."
    return f"Actual simulator counts: {listing}. {explanation}"


def execute():
    if os.name == "nt":
        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
    kernel_environment = os.environ.copy()
    for variable, directory in [("IPYTHONDIR", "ipython"), ("JUPYTER_RUNTIME_DIR", "jupyter"),
                                ("MPLCONFIGDIR", "matplotlib")]:
        directory = ROOT / "report_assets" / "runtime" / directory
        directory.mkdir(parents=True, exist_ok=True)
        kernel_environment[variable] = str(directory)
    notebook = nbformat.read(NOTEBOOK, as_version=4)
    notebook.metadata.kernelspec = {
        "display_name": f"Python {sys.version_info.major}.{sys.version_info.minor} (Assignment 3)",
        "language": "python",
        "name": "python3",
    }
    for cell in notebook.cells:
        cell.metadata.pop("execution", None)
        if cell.cell_type == "code":
            cell.outputs = []
            cell.execution_count = None
    notebook.cells.append(nbformat.v4.new_code_cell(CAPTURE))
    InterpreterNotebookClient(
        notebook, timeout=120, kernel_name="python3", record_timing=False,
        resources={"metadata": {"path": str(ROOT)}},
    ).execute(env=kernel_environment)
    capture_cell = notebook.cells.pop()
    text = "".join(o.get("text", "") for o in capture_cell.outputs if o.output_type == "stream")
    results = json.loads(text)
    sections = {c.metadata.get("assignment_section"): c for c in notebook.cells}
    for key, result in results["q1"].items():
        if sum(result["counts"].values()) != results["shots"]:
            raise ValueError(f"Question 1({key}): inconsistent shot total")
        sections[f"histogram_comment_q1{key}"].source = histogram_comment(key, result, results["shots"])
    figures = ROOT / "figures"
    figures.mkdir(exist_ok=True)
    for section, cell in sections.items():
        if not section or cell.cell_type != "code":
            continue
        if section == "verification_q2":
            filename = "q2_circuit.png"
        elif section.startswith("histogram_plot_"):
            filename = section.removeprefix("histogram_plot_") + "_histogram.png"
        else:
            continue
        images = [o.data["image/png"] for o in cell.outputs if "image/png" in o.get("data", {})]
        if len(images) != 1:
            raise ValueError(f"Expected one generated image in {section}; found {len(images)}")
        (figures / filename).write_bytes(base64.b64decode(images[0]))
    nbformat.validate(notebook)
    nbformat.write(notebook, NOTEBOOK)
    results["provenance"]["notebook_sha256"] = hashlib.sha256(NOTEBOOK.read_bytes()).hexdigest()
    (ROOT / "results.json").write_text(json.dumps(results, indent=2) + "\n", encoding="utf-8", newline="\n")
    print(f"Executed {sum(c.cell_type == 'code' for c in notebook.cells)} notebook code cells successfully.")
    for key, result in results["q1"].items():
        print(f"Q1({key}): actual simulator counts {result['counts']}")
    print("Saved the executed notebook, its figure images, and results.json with execution provenance.")


if __name__ == "__main__":
    execute()

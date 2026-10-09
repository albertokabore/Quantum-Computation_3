"""Assignment 3: two-qubit operators, ket actions, measurement predictions and
Qiskit simulations.

Qiskit uses little-endian ordering: a basis ket is written |q1 q0>, so a gate
G applied to qubit 0 of a 2-qubit circuit has the operator I (x) G, and a gate
applied to qubit 1 has G (x) I.

Run:  python quantum_hw3.py   -> writes figures/ and results.json
"""

from __future__ import annotations

import json
from dataclasses import dataclass, field
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402
import numpy as np  # noqa: E402
from qiskit import QuantumCircuit, transpile  # noqa: E402
from qiskit.quantum_info import Operator, Statevector  # noqa: E402
from qiskit.visualization import plot_histogram  # noqa: E402
from qiskit_aer import AerSimulator  # noqa: E402

SHOTS = 1024
SEED = 2026
ROOT = Path(__file__).resolve().parent
FIG_DIR = ROOT / "figures"
BASIS = ["00", "01", "10", "11"]  # |q1 q0>

# Single-qubit gates
I2 = np.eye(2, dtype=complex)
X = np.array([[0, 1], [1, 0]], dtype=complex)
Y = np.array([[0, -1j], [1j, 0]], dtype=complex)
Z = np.array([[1, 0], [0, -1]], dtype=complex)
H = np.array([[1, 1], [1, -1]], dtype=complex) / np.sqrt(2)
# In |q1 q0> order, q0 controls the X on q1. The projectors act on q0.
P0 = np.diag([1, 0])
P1 = np.diag([0, 1])
CX_0_1 = np.kron(I2, P0) + np.kron(X, P1)
Q2_OPERATOR = CX_0_1 @ np.kron(I2, H)


@dataclass
class Part:
    key: str
    code: list[str]
    circuit: QuantumCircuit
    kron: tuple[str, str]  # (gate on q1, gate on q0) names
    expected: np.ndarray  # hand-derived Kronecker product
    results: dict = field(default_factory=dict)


def q1_parts() -> list[Part]:
    """Question 1 circuits with the Kronecker-product operator derived by hand."""
    a = QuantumCircuit(2)
    a.x(0)
    a.x(1)

    b = QuantumCircuit(2)
    b.x(0)

    c = QuantumCircuit(2)
    c.h(0)
    c.h(1)

    d = QuantumCircuit(2)
    d.z(0)
    d.y(1)

    return [
        Part("a", ["qc = QuantumCircuit(2)", "qc.x(0)", "qc.x(1)"], a, ("X", "X"), np.kron(X, X)),
        Part("b", ["qc = QuantumCircuit(2)", "qc.x(0)"], b, ("I", "X"), np.kron(I2, X)),
        Part("c", ["qc = QuantumCircuit(2)", "qc.h(0)", "qc.h(1)"], c, ("H", "H"), np.kron(H, H)),
        Part("d", ["qc = QuantumCircuit(2)", "qc.z(0)", "qc.y(1)"], d, ("Y", "Z"), np.kron(Y, Z)),
    ]


def q2_circuit() -> QuantumCircuit:
    """Figure 1: H on q0, then controlled-X with q0 control and q1 target."""
    qc = QuantumCircuit(2, 2)
    qc.barrier()
    qc.h(0)
    qc.cx(0, 1)
    qc.barrier()
    qc.measure([0, 1], [0, 1])
    return qc


def simulate(qc: QuantumCircuit) -> dict[str, int]:
    """Sample the circuit on the Aer simulator; adds measurements if missing."""
    circ = qc.copy()
    if circ.num_clbits == 0:
        circ.measure_all()
    sim = AerSimulator(seed_simulator=SEED)
    counts = sim.run(transpile(circ, sim), shots=SHOTS).result().get_counts()
    return {k: counts.get(k, 0) for k in BASIS}


def probabilities(qc: QuantumCircuit) -> dict[str, float]:
    """Exact |<b|psi_f>|^2 for psi_i = |00>."""
    sv = Statevector.from_label("00").evolve(qc.remove_final_measurements(inplace=False))
    return {b: float(abs(sv.data[int(b, 2)]) ** 2) for b in BASIS}


def save_figures(name: str, title: str, qc: QuantumCircuit, counts: dict[str, int]) -> dict[str, str]:
    FIG_DIR.mkdir(exist_ok=True)
    circ_path = FIG_DIR / f"{name}_circuit.png"
    hist_path = FIG_DIR / f"{name}_histogram.png"

    fig = qc.draw("mpl")
    fig.savefig(circ_path, dpi=200, bbox_inches="tight")
    plt.close(fig)

    fig = plot_histogram(counts, title=f"{title}: {SHOTS} shots (AerSimulator)", figsize=(6, 3.6))
    fig.savefig(hist_path, dpi=200, bbox_inches="tight")
    plt.close(fig)
    return {"circuit": str(circ_path.relative_to(ROOT)), "histogram": str(hist_path.relative_to(ROOT))}


def main() -> dict:
    out: dict = {"shots": SHOTS, "seed": SEED, "q1": {}, "q2": {}}

    for p in q1_parts():
        op = Operator(p.circuit).data
        if not np.allclose(op, p.expected):
            raise AssertionError(f"Q1({p.key}): hand-derived operator does not match Qiskit")
        predicted = {b: float(abs(p.expected[k, 0]) ** 2) for k, b in enumerate(BASIS)}
        exact = probabilities(p.circuit)
        if not all(np.isclose(predicted[b], exact[b]) for b in BASIS):
            raise AssertionError(f"Q1({p.key}): Born-rule prediction does not match Qiskit")
        counts = simulate(p.circuit)
        out["q1"][p.key] = {
            "code": p.code,
            "kron": p.kron,
            "matrix": [[[z.real, z.imag] for z in row] for row in p.expected],
            "probabilities": predicted,
            "counts": counts,
            "figures": save_figures(f"q1{p.key}", f"Question 1({p.key})", p.circuit, counts),
        }

    qc2 = q2_circuit()
    unitary2 = qc2.remove_final_measurements(inplace=False)
    if not np.allclose(Operator(unitary2).data, Q2_OPERATOR):
        raise AssertionError("Q2: controlled-X operator does not match the derivation")
    sv = Statevector.from_label("00").evolve(unitary2)
    counts = simulate(qc2)
    out["q2"] = {
        "statevector": [[z.real, z.imag] for z in sv.data],
        "probabilities": probabilities(qc2),
        "counts": counts,
        "figures": save_figures("q2", "Question 2", qc2, counts),
    }

    (ROOT / "results.json").write_text(json.dumps(out, indent=2))
    return out


if __name__ == "__main__":
    res = main()
    for k, v in res["q1"].items():
        print(f"Q1({k}) probs={v['probabilities']} counts={v['counts']}")
    print(f"Q2 probs={res['q2']['probabilities']} counts={res['q2']['counts']}")

"""Checks the hand-derived answers against Qiskit.  Run: python -m pytest -q"""

import numpy as np
import pytest
from qiskit.quantum_info import Operator, Statevector, partial_trace

import quantum_hw3 as hw

PARTS = {p.key: p for p in hw.q1_parts()}

# Predicted output (from |00>) and outcome probabilities, derived by hand.
EXPECTED = {
    "a": ({"11": 1.0}, np.array([0, 0, 0, 1])),
    "b": ({"01": 1.0}, np.array([0, 1, 0, 0])),
    "c": ({b: 0.25 for b in hw.BASIS}, np.full(4, 0.5)),
    "d": ({"10": 1.0}, np.array([0, 0, 1j, 0])),
}

# Each row lists the output amplitudes for one of the four input basis kets.
# Explicit answers catch sign/phase errors beyond the default |00> input.
BASIS_OUTPUTS = {
    "a": np.array([[0, 0, 0, 1], [0, 0, 1, 0], [0, 1, 0, 0], [1, 0, 0, 0]]),
    "b": np.array([[0, 1, 0, 0], [1, 0, 0, 0], [0, 0, 0, 1], [0, 0, 1, 0]]),
    "c": np.array([[1, 1, 1, 1], [1, -1, 1, -1],
                   [1, 1, -1, -1], [1, -1, -1, 1]]) / 2,
    "d": np.array([[0, 0, 1j, 0], [0, 0, 0, -1j],
                   [-1j, 0, 0, 0], [0, 1j, 0, 0]]),
}


@pytest.mark.parametrize("key", PARTS)
def test_kronecker_operator_matches_qiskit(key):
    assert np.allclose(Operator(PARTS[key].circuit).data, PARTS[key].expected)


@pytest.mark.parametrize("key", PARTS)
def test_operator_is_unitary(key):
    u = PARTS[key].expected
    assert np.allclose(u.conj().T @ u, np.eye(4))


@pytest.mark.parametrize("key", PARTS)
def test_output_state_and_probabilities(key):
    probs, psi = EXPECTED[key]
    out = Statevector.from_label("00").evolve(PARTS[key].circuit)
    assert np.allclose(out.data, psi)
    got = hw.probabilities(PARTS[key].circuit)
    for b in hw.BASIS:
        assert got[b] == pytest.approx(probs.get(b, 0.0))


@pytest.mark.parametrize("key", PARTS)
@pytest.mark.parametrize("input_index", range(4))
def test_action_on_every_basis_ket(key, input_index):
    expected = BASIS_OUTPUTS[key][input_index]
    basis = Statevector.from_label(hw.BASIS[input_index])
    assert np.allclose(PARTS[key].expected @ basis.data, expected)
    assert np.allclose(basis.evolve(PARTS[key].circuit).data, expected)


def test_q2_operator_matches_controlled_x_derivation():
    qc = hw.q2_circuit().remove_final_measurements(inplace=False)
    expected = np.array([[1, 1, 0, 0], [0, 0, 1, -1],
                         [0, 0, 1, 1], [1, -1, 0, 0]]) / np.sqrt(2)
    assert np.allclose(Operator(qc).data, expected)
    assert np.allclose(hw.Q2_OPERATOR, expected)


def test_q2_output_state():
    qc = hw.q2_circuit().remove_final_measurements(inplace=False)
    out = Statevector.from_label("00").evolve(qc)
    assert np.allclose(out.data, np.array([1, 0, 0, 1]) / np.sqrt(2))
    assert partial_trace(out, [1]).purity() == pytest.approx(0.5)


def test_q2_measurement_probabilities_and_correlations():
    qc = hw.q2_circuit()
    assert hw.probabilities(qc) == pytest.approx({"00": 0.5, "01": 0, "10": 0, "11": 0.5})
    counts = hw.simulate(qc)
    assert sum(counts.values()) == hw.SHOTS
    assert counts["01"] == counts["10"] == 0


@pytest.mark.parametrize("key", PARTS)
def test_simulation_only_hits_allowed_outcomes(key):
    probs, _ = EXPECTED[key]
    counts = hw.simulate(PARTS[key].circuit)
    assert sum(counts.values()) == hw.SHOTS
    assert all(counts[b] == 0 for b in hw.BASIS if probs.get(b, 0) == 0)

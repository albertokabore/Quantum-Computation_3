# Assignment 3 review

The original Question 1 calculations were correct. Question 2 contained a substantive
circuit-reading error that affected the code, tests, notebook, PDF, and histogram.
That error is corrected throughout. Question 3 now explains the physical qubit more
precisely and distinguishes hardware measurements from the ideal simulator used here.

## Check against the attached instructions

| Requirement | Reviewed result |
|---|---|
| Derive a 4 by 4 operator for each Q1 circuit using Kronecker products | All four are correct. The PDF now explains the general block construction, tensor-factor ordering, and gate multiplication order. |
| Predict each operator's action on 00, 01, 10, 11 | All 16 actions are included, with intermediate product steps. The tests check every action against independent expected amplitudes. |
| Predict all four measurement probabilities | Each Q1 part lists amplitudes, their squared magnitudes, expected counts, and observed frequencies for the default input 00. The actions also determine probabilities for other basis inputs. |
| Include Qiskit histogram snapshots | All four Q1 histograms are embedded in the PDF, with 1024 shots, simulator name, and all four outcome labels. Q2 also has a corrected circuit and histogram. |
| Find Q2's output state for input 00 | Corrected to the entangled Bell state `(00 + 11)/sqrt(2)`, with a step-by-step derivation and explicit operator. |
| Brief research on IBM's representation of qubits | Two paragraphs describe transmons, energy levels, control, readout, and practical imperfections, followed by four linked primary references. |
| Submit one PDF to Canvas | `Assignment3.pdf` contains all answers and figures. The student name still needs to be filled in. No Canvas upload was performed. |

## Question 1: verified answers

The basis is ordered `|00>, |01>, |10>, |11>`, with each ket written `|q1 q0>`.
Thus qubit 0 is the right tensor factor: `x(0)` has operator `I tensor X`.
This matches [IBM's bit-ordering documentation](https://quantum.cloud.ibm.com/docs/en/guides/bit-ordering).

The following table lists probabilities in that same basis order, for input `|00>`.

| Part | Operator | Output | P(00), P(01), P(10), P(11) |
|---|---|---|---|
| (a) `x(0); x(1)` | X tensor X | `|11>` | 0, 0, 0, 1 |
| (b) `x(0)` | I tensor X | `|01>` | 0, 1, 0, 0 |
| (c) `h(0); h(1)` | H tensor H | `( |00> + |01> + |10> + |11> ) / 2` | 1/4, 1/4, 1/4, 1/4 |
| (d) `z(0); y(1)` | Y tensor Z | `i|10>` | 0, 0, 1, 0 |

For (a), the basis actions are `00 -> 11`, `01 -> 10`, `10 -> 01`, and `11 -> 00`.
For (b), they are `00 -> 01`, `01 -> 00`, `10 -> 11`, and `11 -> 10`.

For (c), the four columns of the operator give these outputs:

```text
00 -> ( |00> + |01> + |10> + |11> ) / 2
01 -> ( |00> - |01> + |10> - |11> ) / 2
10 -> ( |00> + |01> - |10> - |11> ) / 2
11 -> ( |00> - |01> - |10> + |11> ) / 2
```

Each amplitude has magnitude 1/2, so its squared magnitude is 1/4 for every input.
The signs affect relative phases while leaving these computational-basis probabilities unchanged.

For (d), the phase-sensitive actions are:

```text
00 ->  i|10>
01 -> -i|11>
10 -> -i|00>
11 ->  i|01>
```

These follow from `Y|0> = i|1>`, `Y|1> = -i|0>`, and `Z|1> = -|1>`.
The coefficient `i` on the output for input 00 is a global phase and has magnitude 1.
For a superposition input, the relative signs in the full operator must still be retained.

The part (c) simulation gives counts `264, 275, 252, 233`. Each outcome has expected
count 256 and marginal standard deviation `sqrt(1024 * 1/4 * 3/4) = 13.86`.
The largest observed deviation is 23 counts, about 1.66 standard deviations.
These results are consistent with finite-shot sampling of a uniform distribution.
The other Q1 circuits give exactly 1024 counts at their one allowed outcome on the ideal simulator.

## Question 2: corrected control gate

The attached diagram contains a filled control dot on the q0 wire, connected vertically
to the X on q1. This is CNOT, with q0 as control and q1 as target.
The original `qc.x(1)` treated the target flip as unconditional and therefore solved
a different circuit. Its answer `( |10> + |11> ) / sqrt(2)` was incorrect for the assignment.
The original Q2 test expected that same answer, so it could not detect the interpretation error.

The corrected sequence is:

```python
qc = QuantumCircuit(2, 2)
qc.barrier()
qc.h(0)
qc.cx(0, 1)
qc.barrier()
qc.measure([0, 1], [0, 1])
```

The state before measurement evolves as follows:

```text
|00> --H on q0--> ( |00> + |01> ) / sqrt(2)
     --CX(0,1)--> ( |00> + |11> ) / sqrt(2)
```

CNOT leaves the branch with q0 = 0 unchanged and flips q1 on the branch with q0 = 1.
The final vector is `(1, 0, 0, 1)^T / sqrt(2)`, in the stated basis.
It is a Bell state: each qubit separately has equal probabilities for 0 and 1,
and their measurement results are perfectly correlated. The corrected histogram contains
516 counts for 00 and 508 for 11, with zero counts for 01 and 10.
Each allowed outcome has expected count 512 and marginal standard deviation 16.

Because the diagram includes measurement, the report distinguishes the coherent vector
before measurement from the result after measurement. A single ideal run ends in 00 or 11;
discarding the outcome record gives the mixture `diag(1/2, 0, 0, 1/2)`.
A histogram in this basis verifies the probabilities but does not by itself certify entanglement;
the ideal statevector calculation establishes coherence for this circuit.

## Question 3: scientific corrections and sources

The original text correctly identified superconducting transmons, but several statements
needed qualification:

- Frequency selectivity and pulse shaping suppress leakage into higher levels; they do not
  guarantee that leakage is zero.
- Hardware readout returns a classified bit. One measurement does not determine both complex
  amplitudes of an unknown qubit state.
- The assignment's counts come from an ideal Aer simulator, rather than an IBM device's physical
  readout resonators. The simulator here includes no hardware noise model.
- The broad claim that all virtual Z rotations add no error and the claim that every nonadjacent
  gate necessarily requires SWAP insertion were removed. Neither is needed to explain the
  physical representation of a qubit.

The revised two-paragraph answer focuses on the circuit's two lowest energy states,
normalized superpositions, charge-noise suppression, cooling, microwave control, and readout.
Its linked references are
[IBM's hardware course](https://quantum.cloud.ibm.com/learning/en/courses/quantum-computing-in-practice/running-quantum-circuits),
[Koch et al.'s transmon paper](https://doi.org/10.1103/PhysRevA.76.042319),
[Blais et al.'s circuit-QED review](https://doi.org/10.1103/RevModPhys.93.025005), and
[IBM's account of its cryogenic systems](https://www.ibm.com/quantum/blog/quantum-five-years).

## Validation

- `python -m pytest -q`: **35 tests passed**. Checks cover all Q1 operators, unitarity,
  all 16 Q1 basis actions, output states, measurement probabilities, and allowed sampled outcomes.
  Q2 checks cover its full operator, Bell amplitudes, reduced-state purity, and measurement correlations.
- `python make_report.py`: regenerated the PDF, JSON results, circuit diagrams, and histograms.
- Executed all six code cells in `Assignment3.ipynb` and saved their fresh outputs.
- Inspected the generated PDF pages for readable equations, tables, figures, and complete answers.

Only the single PDF is required for submission. The notebook, JSON, source, tests, and this review
support reproducibility and explanation.

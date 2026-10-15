# Assignment 3 — assignment instructions

Source: the two-page assignment image supplied in this conversation. This is a
text transcription of the instructions and circuit, not the original image file.

## Instructions

You may use lecture times during Midterm week Mon 10/12 - Fri 10/16 week to work
on this assignment.

- Upload your assignment to Canvas assignments in one single PDF file.

## Questions

1. Given the Qiskit code below, for each circuit:

   - Derive the 4×4 operator by applying the Kronecker product formulation
     discussed in class.
   - Predict the action of the operator on the kets: |00⟩, |01⟩, |10⟩, |11⟩.
   - Predict the probability measurements: |⟨ψ_f|00⟩|², |⟨ψ_f|01⟩|²,
     |⟨ψ_f|10⟩|² and |⟨ψ_f|11⟩|², where ψ_f is the state vector at the circuit output.
   - Include a snapshot of the Qiskit histograms that verify your measurement
     predictions.

   **(a)**

   ```python
   qc = QuantumCircuit(2)
   qc.x(0)
   qc.x(1)
   ```

   **(b)**

   ```python
   qc = QuantumCircuit(2)
   qc.x(0)
   ```

   **(c)**

   ```python
   qc = QuantumCircuit(2)
   qc.h(0)
   qc.h(1)
   ```

   **(d)**

   ```python
   qc = QuantumCircuit(2)
   qc.z(0)
   qc.y(1)
   ```

2. Consider the following two qubit circuit with input state vector
   |ψ_i⟩ = |00⟩. Determine the output state vector for this circuit.

   **Figure 1: Question 2 Circuit Diagram — text transcription**

   ```text
   q0: |0⟩ ── barrier ── H ── ● ── barrier ── Measure → c0
                              │
   q1: |0⟩ ── barrier ──────── X ── barrier ── Measure → c1
   ```

   The connected control on q0 and X on q1 represent `cx(0, 1)`.

3. Perform a brief piece of research to explain how qubits are represented on an
   IBM quantum computer. Write 1–2 paragraphs and include references to support
   your statements.

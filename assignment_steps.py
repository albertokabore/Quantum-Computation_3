"""Worked calculations for the assigned circuits, shared by the PDF and notebook."""

from __future__ import annotations

import re

import numpy as np

import quantum_hw3 as hw

GATES = {"I": hw.I2, "X": hw.X, "Y": hw.Y, "Z": hw.Z, "H": hw.H}

INTRO = [
    ("Basis and bit order", "A ket is a column vector: |0⟩ = (1,0)ᵀ and |1⟩ = (0,1)ᵀ. "
     "Qiskit writes two-qubit kets as |q1 q0⟩ = |q1⟩ ⊗ |q0⟩. Therefore q0 is the rightmost "
     "bit and the right tensor factor. We use the order |00⟩, |01⟩, |10⟩, |11⟩ throughout. "
     "Their vectors are (1,0,0,0)ᵀ, (0,1,0,0)ᵀ, (0,0,1,0)ᵀ, and (0,0,0,1)ᵀ, respectively. "
     "The superscript T means transpose: these lists are written horizontally to save space, "
     "but represent columns."),
    ("From gates to the 4×4 operator", "I means leave a qubit unchanged. A gate G on q0 "
     "has operator I ⊗ G; a gate on q1 has operator G ⊗ I. The symbol ⊗ denotes the "
     "Kronecker product. For A = [[a,b],[c,d]], A ⊗ B = [[aB,bB],[cB,dB]]: multiply "
     "every entry of B by a, then by b, then by c, then by d, and place these four 2×2 "
     "blocks at upper-left, upper-right, lower-left, and lower-right. Two 2×2 factors "
     "therefore produce a 4×4 matrix. For successive gates, the later gate multiplies on "
     "the left. Gates acting on different qubits combine as (G1 ⊗ I)(I ⊗ G0) = G1 ⊗ G0."),
    ("From the operator to the state", "The output is |ψf⟩ = U|ψi⟩. Each output entry "
     "is a row of U dotted with the input: multiply each of the four row entries by the "
     "corresponding input entry, then add all four products. A basis input has one entry "
     "equal to 1 and the other three equal to 0, so it selects one column of U. Column 1 "
     "belongs to |00⟩, column 2 to |01⟩, column 3 to |10⟩, and column 4 to |11⟩. For the "
     "basis-action calculations, (A ⊗ B)(|a⟩ ⊗ |b⟩) = (A|a⟩) ⊗ (B|b⟩). Expand products "
     "by distributing each term; |a⟩ ⊗ |b⟩ is then written |ab⟩."),
    ("From amplitudes to probabilities", "Write |ψf⟩ = a00|00⟩ + a01|01⟩ + a10|10⟩ + "
     "a11|11⟩. The amplitude a_b = ⟨b|ψf⟩ is the vector entry for outcome b. The Born "
     "rule gives P(b) = |a_b|² = a_b* a_b, where * means complex conjugation. The "
     "imaginary unit satisfies i² = −1 and i* = −i. The four probabilities must sum "
     "to 1. Qiskit initializes QuantumCircuit(2) to |00⟩; the detailed probability "
     "calculations use that input. The assignment's other three basis inputs are also "
     "worked out for each operator."),
    ("Reading the histogram", "Each shot prepares the input again, applies the circuit, "
     "and measures it once. With N = 1024 shots, the expected count is N×P(b), whereas "
     "the observed frequency is n_b/N. The horizontal axis labels outcomes q1q0 and "
     "the vertical axis shows counts. Random sampling can make n_b differ from N×P(b); "
     "the count standard deviation for one outcome is √(NP(b)(1−P(b))). All four labels "
     "are retained, including outcomes with zero counts. These are ideal AerSimulator "
     "results (seed 2026), without a hardware noise model."),
]

OPERATOR_STEPS = {
    "a": ["The first gate is X on q0: I ⊗ X.\n\n"
          "The second gate is X on q1: X ⊗ I.\n\n"
          r"$$ U=(X\otimes I)(I\otimes X)=(XI)\otimes(IX)=X\otimes X. $$",
          "The entries of the left X are 0,1,1,0. They scale the four blocks in that order."],
    "b": ["Only q0 receives X; q1 receives I. Thus U = I ⊗ X.",
          "The entries of I are 1,0,0,1. They scale the four blocks in that order."],
    "c": ["The first gate is H on q0: I ⊗ H. The second is H on q1: H ⊗ I. "
          "Thus U = (H ⊗ I)(I ⊗ H) = H ⊗ H.",
          "Each H contains a factor 1/√2. Their product is (1/√2)(1/√2) = "
          "1/(√2×√2) = 1/2. "
          "In the block table, the minus sign in the lower-right block multiplies every entry."],
    "d": ["The first gate is Z on q0: I ⊗ Z. The second is Y on q1: Y ⊗ I. "
          "Thus U = (Y ⊗ I)(I ⊗ Z) = (YI) ⊗ (IZ) = Y ⊗ Z.",
          "The entries of Y are 0,−i,i,0. They scale the four blocks in that order. "
          "In particular, (−i)(−1) = i and i(−1) = −i; retain these signs."],
}


def common_scale(array: np.ndarray) -> float:
    values = np.abs(array[np.abs(array) > 1e-9])
    if not len(values):
        return 1.0
    if not np.allclose(values, values[0]):
        raise ValueError("Expected a common nonzero magnitude")
    return float(values[0])


def scalar(z: complex) -> str:
    for value, label in [(0, "0"), (1, "1"), (-1, "−1"), (1j, "i"), (-1j, "−i"),
                         (.5, "1/2"), (-.5, "−1/2"),
                         (1 / np.sqrt(2), "1/√2"), (-1 / np.sqrt(2), "−1/√2")]:
        if abs(z - value) < 1e-9:
            return label
    raise ValueError(f"Unsupported coefficient: {z}")


def matrix_text(matrix: np.ndarray) -> str:
    scale = common_scale(matrix)
    inside = "[" + ", ".join("[" + ", ".join(scalar(z / scale) for z in row) + "]"
                              for row in matrix) + "]"
    return inside if np.isclose(scale, 1) else f"({scalar(scale)}){inside}"


def tex(text: str) -> str:
    """Convert the assignment's short Unicode equations to notebook math."""
    text = re.sub(r"\|([01ab]+)⟩", r"|\1\\rangle", text)
    for old, new in [("⊗", r"\otimes"), ("×", r"\cdot"), ("−", "-"),
                     ("→", r"\longrightarrow"), ("√2", r"\sqrt{2}"),
                     ("²", "^2"), ("ᵀ", "^T")]:
        text = text.replace(old, new)
    return text


def matrix_tex(matrix: np.ndarray) -> str:
    scale = common_scale(matrix)
    inside = r"\begin{bmatrix}" + r"\\".join(
        " & ".join(tex(scalar(z / scale)) for z in row) for row in matrix) + r"\end{bmatrix}"
    prefix = "" if np.isclose(scale, 1) else (r"\frac12" if np.isclose(scale, .5)
                                               else r"\frac1{\sqrt2}")
    return prefix + inside


def gate_actions(gate_names: tuple[str, ...]) -> list[list[str]]:
    """Show both row products of every single-qubit gate needed by this part."""
    rows = []
    for name in dict.fromkeys(gate_names):
        gate = GATES[name]
        for bit in range(2):
            vector = np.eye(2)[:, bit]
            work = row_products(gate, vector)
            result = gate @ vector
            if name == "H":
                ket = "(|0⟩ + |1⟩)/√2" if bit == 0 else "(|0⟩ − |1⟩)/√2"
            else:
                index = int(np.argmax(abs(result)))
                coefficient = scalar(result[index])
                ket = ("" if coefficient == "1" else coefficient) + f"|{index}⟩"
            rows.append([f"{name}|{bit}⟩", "; ".join(row[1] for row in work), ket])
    return rows


def block_steps(part: hw.Part) -> list[list[str]]:
    left, right = (GATES[name] for name in part.kron)
    rows = []
    for r, vertical in enumerate(["Upper", "Lower"]):
        for c, horizontal in enumerate(["left", "right"]):
            coefficient = scalar(left[r, c])
            products = "[" + ", ".join("[" + ", ".join(
                f"({coefficient})×({scalar(value)})" for value in row) + "]"
                for row in right) + "]"
            rows.append([f"{vertical}-{horizontal}",
                         f"({coefficient}){part.kron[1]}",
                         products + " = " + matrix_text(left[r, c] * right)])
    return rows


def basis_steps(part: hw.Part) -> list[tuple[str, list[str]]]:
    """Expand each of the four assigned basis inputs without a sign-rule shortcut."""
    chains = []
    g1, g0 = part.kron
    for k, bits in enumerate(hw.BASIS):
        a, b = map(int, bits)
        first = f"({g1}|{a}⟩) ⊗ ({g0}|{b}⟩)"
        if part.key == "c":
            sign_a, sign_b = ("+" if a == 0 else "−"), ("+" if b == 0 else "−")
            factor = f"[(|0⟩ {sign_a} |1⟩)/√2] ⊗ [(|0⟩ {sign_b} |1⟩)/√2]"
            # Distribute all four terms in the same order as the computational basis.
            s01, s10, s11 = sign_b, sign_a, ("+" if a == b else "−")
            distributed = (f"(1/2)[(|0⟩ ⊗ |0⟩) {s01} (|0⟩ ⊗ |1⟩) "
                           f"{s10} (|1⟩ ⊗ |0⟩) {s11} (|1⟩ ⊗ |1⟩)]")
            final = f"(1/2)(|00⟩ {s01} |01⟩ {s10} |10⟩ {s11} |11⟩)"
            steps = [first, factor, distributed, final]
        elif part.key == "d":
            phase_y, phase_z = ("i" if a == 0 else "−i"), ("1" if b == 0 else "−1")
            coefficient = scalar(part.expected[:, k][int((1 - a) * 2 + b)])
            steps = [first, f"({phase_y}|{1-a}⟩) ⊗ ({phase_z}|{b}⟩)",
                     f"({phase_y})({phase_z})|{1-a}{b}⟩", f"{coefficient}|{1-a}{b}⟩"]
        else:
            out_a = 1 - a if part.key == "a" else a
            steps = [first, f"|{out_a}⟩ ⊗ |{1-b}⟩", f"|{out_a}{1-b}⟩"]
        chains.append((bits, steps))
    return chains


def row_products(matrix: np.ndarray, vector: np.ndarray) -> list[list[str]]:
    matrix_scale, vector_scale = common_scale(matrix), common_scale(vector)
    scale = matrix_scale * vector_scale
    rows = []
    for index, row in enumerate(matrix / matrix_scale):
        terms = []
        for coefficient, entry in zip(row, vector / vector_scale):
            a, b = scalar(coefficient), scalar(entry)
            if a.startswith("−"):
                a = f"({a})"
            if b.startswith("−"):
                b = f"({b})"
            terms.append(f"{a}×{b}")
        expression = " + ".join(terms)
        if not np.isclose(scale, 1):
            expression = f"({scalar(scale)})[{expression}]"
        value = scalar((matrix @ vector)[index])
        rows.append([f"Row {index+1}", expression + f" = {value}", value])
    return rows


def probability_steps(vector: np.ndarray) -> list[list[str]]:
    rows = []
    for bits, amplitude in zip(hw.BASIS, vector):
        a = scalar(amplitude)
        if np.isclose(abs(amplitude), 0):
            arithmetic = "|0|² = 0×0 = 0"
        elif np.isclose(amplitude, 1j):
            arithmetic = "|i|² = (−i)i = −i² = −(−1) = 1"
        elif np.isclose(abs(amplitude), 1):
            arithmetic = f"|{a}|² = ({a})({a}) = 1"
        elif np.isclose(abs(amplitude), .5):
            arithmetic = "|1/2|² = (1/2)(1/2) = 1/4"
        else:
            arithmetic = "|1/√2|² = (1/√2)(1/√2) = 1/(√2×√2) = 1/2"
        rows.append([bits, a, arithmetic, scalar(abs(amplitude) ** 2)
                     if not np.isclose(abs(amplitude) ** 2, .25) else "1/4"])
    return rows


def normalization(vector: np.ndarray) -> str:
    probabilities = [row[3] for row in probability_steps(vector)]
    return " + ".join(probabilities) + " = 1"


def row_markdown(matrix: np.ndarray, vector: np.ndarray) -> str:
    return "\n\n".join(f"**{row[0]}:** $ {tex(row[1])} $." for row in row_products(matrix, vector))


def probability_markdown(vector: np.ndarray) -> str:
    return "\n\n".join(f"$P({bits}) = {tex(work)}$." for bits, _, work, _ in probability_steps(vector))


def q1a_handwritten_markdown() -> str:
    """Use the actual scanned answers and retain the block omitted by the user."""
    return r"""## Question 1(a)

### 4×4 Operator Using the Kronecker Product Formulation

![Question 1(a), handwritten page 1](report_assets/handwritten_q1a/page_1.jpeg)

---

![Question 1(a), handwritten page 2](report_assets/handwritten_q1a/page_2.jpeg)

**Upper-right block:**

$$ (1)X = \begin{bmatrix}(1)\cdot(0) & (1)\cdot(1)\\(1)\cdot(1) & (1)\cdot(0)\end{bmatrix} $$

$$ = \begin{bmatrix}0 & 1\\1 & 0\end{bmatrix}. $$

---

### Action of the Operator on the Kets: |00⟩, |01⟩, |10⟩, |11⟩

![Question 1(a), handwritten page 3](report_assets/handwritten_q1a/page_3.jpeg)

---

### Probability Measurements

![Question 1(a), handwritten page 4](report_assets/handwritten_q1a/page_4.jpeg)

---"""


def q1b_handwritten_markdown() -> str:
    """Use the four actual handwritten Question 1(b) page images."""
    return r"""## Question 1(b)

### 4×4 Operator Using the Kronecker Product Formulation

![Question 1(b), handwritten page 1](report_assets/handwritten_q1b/page_1.jpeg)

---

![Question 1(b), handwritten page 2](report_assets/handwritten_q1b/page_2.jpeg)

---

### Action of the Operator on the Kets: |00⟩, |01⟩, |10⟩, |11⟩

![Question 1(b), handwritten page 3](report_assets/handwritten_q1b/page_3.jpeg)

---

### Probability Measurements

![Question 1(b), handwritten page 4](report_assets/handwritten_q1b/page_4.jpeg)

---"""


def q1c_handwritten_markdown() -> str:
    """Keep all five handwritten pages and all six steps for Question 1(c)."""
    return r"""## Question 1(c)

### 4×4 Operator Using the Kronecker Product Formulation

![Question 1(c), handwritten page 1](report_assets/handwritten_q1c/page_1.jpeg)

---

![Question 1(c), handwritten page 2](report_assets/handwritten_q1c/page_2.jpeg)

For clarity, the bottom-right entry of the lower-right block uses two negative factors:

$$ \left(-\frac{1}{\sqrt{2}}\right)\left(-\frac{1}{\sqrt{2}}\right)=\frac{1}{2}. $$

---

### Action of the Operator on the Kets: |00⟩, |01⟩, |10⟩, |11⟩

![Question 1(c), handwritten page 3](report_assets/handwritten_q1c/page_3.jpeg)

---

![Question 1(c), handwritten page 4](report_assets/handwritten_q1c/page_4.jpeg)

---

### Probability Measurements

![Question 1(c), handwritten page 5](report_assets/handwritten_q1c/page_5.jpeg)

---"""


def q1_markdown(part: hw.Part) -> str:
    if part.key == "a":
        return q1a_handwritten_markdown()
    if part.key == "b":
        return q1b_handwritten_markdown()
    if part.key == "c":
        return q1c_handwritten_markdown()
    g1, g0 = part.kron
    output = part.expected[:, 0]
    chunks = [f"## Question 1({part.key})",
              "### 4×4 Operator Using the Kronecker Product Formulation", *OPERATOR_STEPS[part.key],
              "$$ " + r", \qquad ".join(f"{name} = {matrix_tex(GATES[name])}"
                                               for name in dict.fromkeys(part.kron)) + ". $$",
              "**Single-qubit actions:**",
              "Multiply the two matrix rows by the input column. These are the only single-qubit actions needed for this part."]
    for action_index, (label, work, ket) in enumerate(gate_actions(part.kron)):
        chunks.append(f"**Input ${tex(label)}$:**")
        if part.key == "a":
            # The user's handwritten page 1 explicitly multiplies X by each
            # input column before calculating the two row products.
            input_column = np.eye(2)[:, action_index:action_index + 1]
            chunks.append(f"$$ {tex(label)} = {matrix_tex(hw.X)}"
                          f"{matrix_tex(input_column)}. $$")
        chunks.extend(f"$$ {tex(row)} $$" for row in work.split("; "))
        chunks.append(f"Therefore $ {tex(label + ' = ' + ket)} $.")
    chunks += ["**Kronecker product expansion:**",
               "Each entry of the left factor multiplies **every** entry of the right factor."]
    left, right = (GATES[name] for name in part.kron)
    for index, (position, block, _) in enumerate(block_steps(part)):
        coefficient = left[index // 2, index % 2]
        products = (r"\begin{bmatrix}" + r"\\".join(
            " & ".join(tex(f"({scalar(coefficient)})×({scalar(value)})") for value in row)
            for row in right) + r"\end{bmatrix}")
        if part.key == "a" and index in {0, 2, 3}:
            # Transcribe the three blocks present on handwritten page 2.
            # The omitted upper-right block retains its existing calculation.
            expansion = f"{tex(block)} = "
            if index in {0, 2}:
                expansion += f"({tex(scalar(coefficient))}){matrix_tex(right)} = "
            expansion += products
            result = matrix_tex(coefficient * right)
            chunks.append(f"**{position} block:**")
            if index == 0:
                chunks += [f"$$ {expansion} $$", f"$$ {tex(block)} = {result}. $$"]
            else:
                chunks.append(f"$$ {expansion} = {result}. $$")
        else:
            chunks += [f"**{position} block:**", f"$$ {tex(block)} = {products} $$",
                       f"$$ = {matrix_tex(coefficient * right)}. $$"]
    chunks += ["Place the upper two blocks side by side, then the lower two blocks:",
               f"$$ U = {g1} \\otimes {g0} = {matrix_tex(part.expected)}. $$",
               "### Action of the Operator on the Kets: |00⟩, |01⟩, |10⟩, |11⟩",
               "Use the single-qubit actions above. Multiply any scalar phases and distribute tensor products before combining the two bits."]
    for bits, steps in basis_steps(part):
        chunks.append(f"**Input $|{bits}\\rangle$:**")
        chunks.extend(f"$$ {tex('U|' + bits + '⟩' if j == 0 else '')} "
                      f"{'=' if j == 0 else '='} {tex(step)} $$" for j, step in enumerate(steps))
    chunks += ["### Probability Measurements",
               "The initialized input is $|00\\rangle=(1,0,0,0)^T$. Keep all four row products visible:",
               f"$$ U|00\\rangle = {matrix_tex(part.expected)}{matrix_tex(np.eye(4)[:, :1])}. $$",
               row_markdown(part.expected, np.eye(4)[:, 0]),
               f"$$ |\\psi_f\\rangle = {matrix_tex(output.reshape(-1, 1))} "
               f"= {tex(basis_steps(part)[0][1][-1])}. $$",
               "**Probability measurements and normalization:**",
               "Take the squared magnitude of each output amplitude, rather than the amplitude itself:",
               probability_markdown(output), f"$$ {tex(normalization(output))}. $$",
               "For the other basis inputs above, " +
               ("each of the four coefficients is +1/2 or −1/2. Squaring either sign gives (±1/2)² = 1/4, so every input has the same four basis probabilities."
                if part.key == "c" else "there is exactly one nonzero coefficient, of magnitude 1. Its output ket has probability 1 and the other three outcomes have probability 0.")]
    return "\n\n".join(chunks)


Q2_READING = ("Read the assigned diagram from left to right. The input is |00⟩. H acts on q0. "
              "The filled dot on q0 joined to X on q1 is one controlled-X (CNOT), written "
              "qc.cx(0, 1): q0 controls whether q1 flips. Barriers leave the state unchanged. "
              "The final measurement sends q0 to c0 and q1 to c1. We first calculate the "
              "coherent state immediately before measurement, then explain the possible measured results.")

CNOT_ROWS = [["00", "0: leave q1 = 0", "00"], ["01", "1: flip q1 from 0 to 1", "11"],
             ["10", "0: leave q1 = 1", "10"], ["11", "1: flip q1 from 1 to 0", "01"]]


def q2_markdown() -> str:
    """Use both handwritten Question 2 pages, including all three steps."""
    return r"""## Question 2: Output State Vector

![Question 2, handwritten page 1](report_assets/handwritten_q2/page_1.jpeg)

---

![Question 2, handwritten page 2](report_assets/handwritten_q2/page_2.jpeg)

---"""

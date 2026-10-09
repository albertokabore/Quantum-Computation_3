"""Build the single-PDF submission (Assignment3.pdf) from quantum_hw3.py results.

Run:  python make_report.py
"""

from __future__ import annotations

import os
from datetime import date
from pathlib import Path

import matplotlib
import numpy as np
from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import inch
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import (Image, KeepTogether, PageBreak, Paragraph, Preformatted,
                                SimpleDocTemplate, Spacer, Table, TableStyle)

import quantum_hw3 as hw

ROOT = Path(__file__).resolve().parent
OUT = ROOT / "Assignment3.pdf"

# DejaVu ships with matplotlib and covers the ⊗ ψ ⟨ ⟩ √ ½ glyphs used below.
_FONT_DIR = Path(matplotlib.get_data_path()) / "fonts" / "ttf"
pdfmetrics.registerFont(TTFont("DV", os.fspath(_FONT_DIR / "DejaVuSans.ttf")))
pdfmetrics.registerFont(TTFont("DV-B", os.fspath(_FONT_DIR / "DejaVuSans-Bold.ttf")))
pdfmetrics.registerFont(TTFont("DV-I", os.fspath(_FONT_DIR / "DejaVuSans-Oblique.ttf")))
pdfmetrics.registerFont(TTFont("DVM", os.fspath(_FONT_DIR / "DejaVuSansMono.ttf")))
pdfmetrics.registerFontFamily("DV", normal="DV", bold="DV-B", italic="DV-I", boldItalic="DV-B")

_ss = getSampleStyleSheet()
BODY = ParagraphStyle("body", _ss["BodyText"], fontName="DV", fontSize=9.5, leading=14, spaceAfter=5)
SMALL = ParagraphStyle("small", BODY, fontSize=8.5, leading=11.5)
CELL = ParagraphStyle("cell", SMALL, spaceBefore=0, spaceAfter=0)
H1 = ParagraphStyle("h1", BODY, fontName="DV-B", fontSize=14, leading=18, spaceBefore=8, spaceAfter=6)
H2 = ParagraphStyle("h2", BODY, fontName="DV-B", fontSize=11.5, leading=15, spaceBefore=8, spaceAfter=4)
TITLE = ParagraphStyle("title", H1, fontSize=17, alignment=TA_CENTER, spaceAfter=2)
CENTER = ParagraphStyle("center", BODY, alignment=TA_CENTER)
CAPTION = ParagraphStyle("caption", SMALL, alignment=TA_CENTER, textColor=colors.HexColor("#444444"))
CODE = ParagraphStyle("code", fontName="DVM", fontSize=8.5, leading=11,
                      backColor=colors.HexColor("#F3F4F6"), borderPadding=5, leftIndent=6)

KET = {b: f"|{b}⟩" for b in hw.BASIS}


# ---------------------------------------------------------------- formatting
def _unit(z: complex) -> str:
    """Format a unit-magnitude coefficient in {1, -1, i, -i}."""
    for val, s in ((1, "1"), (-1, "−1"), (1j, "i"), (-1j, "−i")):
        if abs(z - val) < 1e-9:
            return s
    raise ValueError(z)


def _scale_name(m: float) -> str:
    for val, s in ((1.0, ""), (0.5, "½"), (1 / np.sqrt(2), "1/√2")):
        if abs(m - val) < 1e-9:
            return s
    return f"{m:.4g}"


def _common_scale(v: np.ndarray) -> float:
    mags = np.abs(v[np.abs(v) > 1e-9])
    if not np.allclose(mags, mags[0]):
        raise ValueError("entries do not share a common magnitude")
    return float(mags[0])


def ket_expr(vec: np.ndarray) -> str:
    """e.g. [0,0,i,0] -> 'i|10⟩';  ½[1,-1,1,-1] -> '½(|00⟩ − |01⟩ + |10⟩ − |11⟩)'."""
    m = _common_scale(vec)
    terms = []
    for k, z in enumerate(vec):
        if abs(z) < 1e-9:
            continue
        c = _unit(z / m)
        neg = c.startswith("−")
        mag = c.lstrip("−")
        body = f"{'' if mag == '1' else mag}{KET[hw.BASIS[k]]}"
        if not terms:
            terms.append(("−" if neg else "") + body)
        else:
            terms.append(("− " if neg else "+ ") + body)
    expr = " ".join(terms)
    scale = _scale_name(m)
    if not scale:
        return expr
    if "/" in scale:
        scale = f"({scale})"
    return f"{scale}({expr})" if len(terms) > 1 else f"{scale}{expr}"


def matrix_flowable(label: str, mat: np.ndarray) -> Table:
    """Render 'label = scale · [matrix]' with bracket-style side rules."""
    m = _common_scale(mat)
    cells = [[_unit(z / m) if abs(z) > 1e-9 else "0" for z in row] for row in mat]
    inner = Table(cells, colWidths=[0.36 * inch] * mat.shape[1], rowHeights=0.21 * inch)
    inner.setStyle(TableStyle([
        ("FONT", (0, 0), (-1, -1), "DV", 10),
        ("ALIGN", (0, 0), (-1, -1), "CENTER"),
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
        ("LINEBEFORE", (0, 0), (0, -1), 1.1, colors.black),
        ("LINEAFTER", (-1, 0), (-1, -1), 1.1, colors.black),
        # short horizontal serifs to make the rules read as square brackets
        ("LINEABOVE", (0, 0), (0, 0), 1.1, colors.black),
        ("LINEABOVE", (-1, 0), (-1, 0), 1.1, colors.black),
        ("LINEBELOW", (0, -1), (0, -1), 1.1, colors.black),
        ("LINEBELOW", (-1, -1), (-1, -1), 1.1, colors.black),
    ]))
    scale = _scale_name(m)
    label_width = (0.45 if len(label) < 3 else 1.3) * inch
    scale_width = (0.55 if "/" in scale else 0.3 if scale else 0.05) * inch
    outer = Table([[Paragraph(label + " =", BODY), Paragraph(scale, BODY) if scale else "", inner]],
                  colWidths=[label_width, scale_width, mat.shape[1] * 0.36 * inch + 12], hAlign="LEFT")
    outer.setStyle(TableStyle([("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
                               ("ALIGN", (0, 0), (0, 0), "RIGHT")]))
    return outer


def grid(rows: list[list], widths: list[float], header: bool = True) -> Table:
    # Paragraph cells wrap long ket expressions instead of spilling into neighbors.
    wrapped = [[Paragraph(f"<b>{cell}</b>" if header and i == 0 else cell, CELL)
                if isinstance(cell, str) else cell for cell in row] for i, row in enumerate(rows)]
    t = Table(wrapped, colWidths=widths, hAlign="LEFT", repeatRows=1 if header else 0)
    style = [
        ("FONT", (0, 0), (-1, -1), "DV", 9),
        ("GRID", (0, 0), (-1, -1), 0.4, colors.HexColor("#9CA3AF")),
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
        ("ALIGN", (1, 0), (-1, -1), "CENTER"),
        ("TOPPADDING", (0, 0), (-1, -1), 3),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 3),
    ]
    if header:
        style += [("FONT", (0, 0), (-1, 0), "DV-B", 9),
                  ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#E5E7EB"))]
    t.setStyle(TableStyle(style))
    return t


def fig(path: str, width: float) -> Image:
    img = Image(os.fspath(ROOT / path))
    img.drawWidth, img.drawHeight = width, width * img.imageHeight / img.imageWidth
    return img


def frac(p: float) -> str:
    for val, s in ((0.0, "0"), (1.0, "1"), (0.5, "1/2"), (0.25, "1/4")):
        if abs(p - val) < 1e-9:
            return s
    return f"{p:.4f}"


# ---------------------------------------------------------------- content
GATES = {"I": hw.I2, "X": hw.X, "Y": hw.Y, "Z": hw.Z, "H": hw.H}

DERIVATION = {
    "a": ("<font face='DVM'>qc.x(0)</font> flips q0 and <font face='DVM'>qc.x(1)</font> flips q1. "
          "The two gates act on different qubits, so they form one layer and the 4×4 operator is the "
          "Kronecker product U = X<sub>q1</sub> ⊗ X<sub>q0</sub> = X ⊗ X. Writing X ⊗ X in 2×2 blocks, "
          "X ⊗ X = [[0·X, 1·X], [1·X, 0·X]], gives an anti-diagonal of ones:"),
    "b": ("Only q0 receives a gate; q1 is left alone, which is the identity. Hence "
          "U = I<sub>q1</sub> ⊗ X<sub>q0</sub> = I ⊗ X = [[1·X, 0·X], [0·X, 1·X]], i.e. X repeated "
          "down the block diagonal:"),
    "c": ("A Hadamard acts on each qubit, so U = H<sub>q1</sub> ⊗ H<sub>q0</sub> = H ⊗ H = "
          "(1/√2)[[H, H], [H, −H]]. Each entry is (1/√2)(1/√2)(±1) = ±½, and the sign is "
          "(−1)<super>x·y</super> (bitwise dot product of row and column labels):"),
    "d": ("Z acts on q0 and Y on q1. Because they act on different qubits the order in which they are "
          "written does not matter, and U = Y<sub>q1</sub> ⊗ Z<sub>q0</sub> = Y ⊗ Z = "
          "[[0·Z, −i·Z], [i·Z, 0·Z]]:"),
}

COMMENT = {
    "a": "Both qubits are flipped, so the circuit deterministically outputs |11⟩.",
    "b": ("Only q0 is flipped. In Qiskit's bit-string convention (q1 on the left) the outcome is "
          "<b>01</b>, not 10."),
    "c": ("H ⊗ H maps |00⟩ to an equal superposition of all four basis states, so each outcome has "
          "probability ¼. With 1024 shots each bar should be close to 256; the spread seen in the "
          "histogram is ordinary shot noise (standard deviation √(1024·¼·¾) ≈ 13.9 counts)."),
    "d": ("Z leaves |0⟩ unchanged and Y|0⟩ = i|1⟩, so ψ<sub>f</sub> = i|10⟩. The global phase i is not "
          "observable: |⟨10|ψ<sub>f</sub>⟩|² = |i|² = 1."),
}

ACTION_STEPS = {
    "a": ["X|0⟩ ⊗ X|0⟩", "X|0⟩ ⊗ X|1⟩", "X|1⟩ ⊗ X|0⟩", "X|1⟩ ⊗ X|1⟩"],
    "b": ["I|0⟩ ⊗ X|0⟩", "I|0⟩ ⊗ X|1⟩", "I|1⟩ ⊗ X|0⟩", "I|1⟩ ⊗ X|1⟩"],
    "c": ["H|0⟩ ⊗ H|0⟩ = |+⟩ ⊗ |+⟩", "H|0⟩ ⊗ H|1⟩ = |+⟩ ⊗ |−⟩",
          "H|1⟩ ⊗ H|0⟩ = |−⟩ ⊗ |+⟩", "H|1⟩ ⊗ H|1⟩ = |−⟩ ⊗ |−⟩"],
    "d": ["(i|1⟩) ⊗ |0⟩", "(i|1⟩) ⊗ (−|1⟩)",
          "(−i|0⟩) ⊗ |0⟩", "(−i|0⟩) ⊗ (−|1⟩)"],
}

Q3_PARAS = [
    "IBM represents each physical qubit using a superconducting <i>transmon</i>: an electrical "
    "circuit with a Josephson junction connected in parallel with a capacitor [1]. The junction "
    "contains a thin insulating barrier between superconductors and supplies a nonlinear "
    "inductance. Together with the capacitance, it produces a quantum oscillator with unequal "
    "energy-level spacings. Its ground and first excited energy eigenstates define the computational "
    "states |0⟩ and |1⟩ [2, 3]. Within this two-level subspace, a pure state is "
    "|ψ⟩ = α|0⟩ + β|1⟩, with complex amplitudes satisfying |α|² + |β|² = 1; their relative phase "
    "also carries quantum information. The large capacitance reduces sensitivity to charge noise, "
    "while the remaining anharmonicity permits selective control [2]. IBM cools its processors "
    "in dilution refrigerators to temperatures of roughly 15–20 mK to reduce thermal excitation [4].",

    "Shaped microwave pulses manipulate the amplitudes and relative phase to implement "
    "single-qubit gates, while interactions between coupled qubits implement entangling gates [1, 3]. "
    "A transmon has higher energy levels, so pulse calibration and shaping suppress unwanted "
    "population leakage outside |0⟩ and |1⟩; leakage is not automatically zero [3]. For dispersive "
    "readout, a transmon couples to a microwave resonator whose response depends on the qubit "
    "state. A probe signal is amplified and classified to return a classical 0 or 1 [1, 3]. Ideally, "
    "a computational-basis measurement of α|0⟩ + β|1⟩ returns 0 with probability |α|² and 1 with "
    "probability |β|². One such measurement does not reveal both complex amplitudes; repeated "
    "preparations and measurements estimate probabilities. Physical devices also experience "
    "relaxation, dephasing, control imperfections, and readout errors [3]. The histograms in this "
    "assignment instead use an ideal AerSimulator without a hardware noise model: their random "
    "variation comes from finite-shot sampling of the predicted probabilities.",
]

REFERENCES = [
    "IBM Quantum Learning, “Running quantum circuits,” "
    "<link href='https://quantum.cloud.ibm.com/learning/en/courses/quantum-computing-in-practice/running-quantum-circuits' "
    "color='blue'>IBM Quantum course</link> (accessed Oct. 9, 2026).",
    "J. Koch <i>et al.</i>, “Charge-insensitive qubit design derived from the Cooper "
    "pair box,” <i>Phys. Rev. A</i> 76, 042319 (2007). "
    "<link href='https://doi.org/10.1103/PhysRevA.76.042319' color='blue'>doi:10.1103/PhysRevA.76.042319</link>.",
    "A. Blais, A. L. Grimsmo, S. M. Girvin, and A. Wallraff, “Circuit quantum electrodynamics,” "
    "<i>Rev. Mod. Phys.</i> 93, 025005 (2021). "
    "<link href='https://doi.org/10.1103/RevModPhys.93.025005' color='blue'>doi:10.1103/RevModPhys.93.025005</link>.",
    "IBM Quantum, “Five years ago today, we put the first quantum computer on the cloud. "
    "Here’s how we did it,” May 4, 2021. "
    "<link href='https://www.ibm.com/quantum/blog/quantum-five-years' color='blue'>IBM Quantum blog</link> "
    "(accessed Oct. 9, 2026).",
]


def question1(story: list, results: dict) -> None:
    story.append(Paragraph("Question 1", H1))
    story.append(Paragraph(
        "<b>Convention.</b> Qiskit orders qubits little-endian: a two-qubit basis ket is written "
        "|q1 q0⟩, so qubit 0 is the <i>rightmost</i> bit and the rightmost factor of every Kronecker "
        "product. A gate G on qubit 0 is therefore I ⊗ G, and on qubit 1 it is G ⊗ I. The basis is "
        "ordered |00⟩, |01⟩, |10⟩, |11⟩ (rows/columns 0–3). Every circuit starts in "
        "ψ<sub>i</sub> = |00⟩. Each hand-derived matrix below was checked against "
        "<font face='DVM'>qiskit.quantum_info.Operator(qc)</font> (within floating-point precision), and each circuit "
        f"was sampled with {hw.SHOTS} shots on <font face='DVM'>AerSimulator</font> "
        f"(seed {hw.SEED}). Single-qubit matrices used: I = [[1,0],[0,1]], X = [[0,1],[1,0]], "
        "Y = [[0,−i],[i,0]], Z = [[1,0],[0,−1]], H = (1/√2)[[1,1],[1,−1]].", SMALL))

    story.append(Paragraph("How the calculations are obtained", H2))
    story.append(Paragraph(
        "For A = [[a,b],[c,d]], the Kronecker product replaces every scalar entry with a scaled "
        "copy of B: A ⊗ B = [[aB,bB],[cB,dB]]. Thus two 2×2 matrices give one 4×4 matrix. "
        "For successive gates, the later gate multiplies on the left. In these four circuits, "
        "gates on different qubits combine as (G1 ⊗ I)(I ⊗ G0) = G1 ⊗ G0.", BODY))
    story.append(Paragraph(
        "The ordered basis vectors are |00⟩ = (1,0,0,0)<super>T</super>, "
        "|01⟩ = (0,1,0,0)<super>T</super>, |10⟩ = (0,0,1,0)<super>T</super>, and "
        "|11⟩ = (0,0,0,1)<super>T</super>. Multiplying U by a basis vector selects its "
        "corresponding column. Equivalently, (A ⊗ B)(|a⟩ ⊗ |b⟩) = A|a⟩ ⊗ B|b⟩; "
        "the action tables below show both methods through the product step and final ket.", BODY))
    story.append(Paragraph(
        "Useful identities are X|0⟩ = |1⟩, X|1⟩ = |0⟩; Y|0⟩ = i|1⟩, "
        "Y|1⟩ = −i|0⟩; Z|0⟩ = |0⟩, Z|1⟩ = −|1⟩; and "
        "H|0⟩ = |+⟩ = (|0⟩ + |1⟩)/√2, H|1⟩ = |−⟩ = (|0⟩ − |1⟩)/√2.", BODY))
    story.append(Paragraph(
        "<b>Born rule.</b> Write |ψf⟩ = a00|00⟩ + a01|01⟩ + a10|10⟩ + a11|11⟩. "
        "The amplitude for outcome b is ab = ⟨b|ψf⟩, and its probability is "
        "P(b) = |ab|² = ab*ab. Normalization requires the four probabilities to sum to 1. "
        "The predictions below use the default Qiskit input |00⟩. Actions on the other three "
        "basis inputs are included separately, as the assignment requests.", BODY))
    story.append(Paragraph(
        "For N independent shots, the expected count is NP(b), and the marginal count standard "
        "deviation is √(NP(b)(1−P(b))). With N = 1024, a probability of 1/4 gives an expected "
        "256 counts with a standard deviation of about 13.9. An ideal simulator's observed "
        "frequencies need not equal the exact probabilities; zero-probability outcomes remain "
        "absent. All four outcome labels are retained in each histogram.", BODY))
    story.append(Paragraph(
        "The bit order and controlled-gate convention follow "
        "<link href='https://quantum.cloud.ibm.com/docs/en/guides/bit-ordering' color='blue'>"
        "IBM's Qiskit bit-ordering documentation</link> (accessed Oct. 9, 2026).", SMALL))

    for part in hw.q1_parts():
        r = results["q1"][part.key]
        g1, g0 = part.kron
        U = part.expected
        story.append(PageBreak())
        story.append(Paragraph(f"Question 1({part.key})", H1))
        top = Table([[Preformatted("\n".join(part.code), CODE), fig(r["figures"]["circuit"], 1.2 * inch)]],
                    colWidths=[2.6 * inch, 1.6 * inch], hAlign="LEFT")
        top.setStyle(TableStyle([("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
                                 ("LEFTPADDING", (0, 0), (-1, -1), 0)]))
        story.append(top)
        story.append(Spacer(1, 2))

        story.append(Paragraph("<b>4×4 operator (Kronecker product).</b> " + DERIVATION[part.key], BODY))
        hist = [fig(r["figures"]["histogram"], 3.0 * inch),
                Paragraph(f"Figure 1({part.key}). Qiskit histogram, {hw.SHOTS} shots "
                          "(measure_all() appended to the circuit shown above).", CAPTION)]
        mid = Table([[matrix_flowable(f"U = {g1} ⊗ {g0}", U), hist]],
                    colWidths=[3.5 * inch, 3.5 * inch], hAlign="LEFT")
        mid.setStyle(TableStyle([("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
                                 ("LEFTPADDING", (0, 0), (-1, -1), 0)]))
        story.append(mid)
        story.append(Spacer(1, 2))

        action_rows = [["Input", "Product rule step (q1 ⊗ q0)", "U |input⟩"]]
        for k, b in enumerate(hw.BASIS):
            action_rows.append([KET[b], ACTION_STEPS[part.key][k], ket_expr(U[:, k])])
        prob_rows = [["Outcome b", "Amplitude ⟨b|ψf⟩", "P(b) = |amplitude|²", "Expected count", "Observed count (fraction)"]]
        psi = U[:, 0]
        for k, b in enumerate(hw.BASIS):
            p = r["probabilities"][b]
            n = r["counts"][b]
            amp = "0" if abs(psi[k]) < 1e-9 else _scale_name(abs(psi[k])) or _unit(psi[k])
            prob_rows.append([b, amp, frac(p), f"{hw.SHOTS * p:.0f}", f"{n}  ({n / hw.SHOTS:.3f})"])

        psi_f = ket_expr(U[:, 0])
        story.append(Paragraph(
            "<b>Action on all four basis kets.</b> Each row is the corresponding column of U "
            "written as a ket. " + ("The middle column explicitly multiplies the Y and Z phases."
                                   if part.key == "d" else "Apply each gate to its own qubit, then expand the product."), BODY))
        story.append(grid(action_rows, [0.6 * inch, 2.8 * inch, 3.6 * inch]))
        story.append(Spacer(1, 6))
        story.append(Paragraph(
            f"<b>Measurement prediction for |00⟩.</b> The output is ψ<sub>f</sub> = U|00⟩ = {psi_f}. "
            + COMMENT[part.key], BODY))
        story.append(grid(prob_rows, [0.95 * inch, 1.25 * inch, 1.4 * inch, 1.2 * inch, 2.2 * inch]))
        story.append(Paragraph(
            "For any other basis input, square the magnitudes in its action-table row. "
            + ("Every input in part (c) gives probability 1/4 for every outcome; the signs affect phases."
               if part.key == "c" else "The one nonzero coefficient has magnitude 1, so that row's output ket occurs with certainty."), SMALL))


def question2(story: list, results: dict) -> None:
    r = results["q2"]
    story.append(PageBreak())
    story.append(Paragraph("Question 2", H1))
    story.append(Paragraph(
        "Read Figure 1 from left to right. After the initial barrier, H acts on q0. "
        "The filled dot on q0 is connected vertically to the X on q1: together they denote "
        "a <b>controlled-X (CNOT)</b>, implemented by <font face='DVM'>qc.cx(0, 1)</font>. "
        "q0 is the control and q1 the target. A second barrier precedes measurement of "
        "q0 into c0 and q1 into c1. Barriers constrain compilation but leave the state unchanged.", BODY))
    story.append(Paragraph(
        "In the basis |q1 q0⟩, CNOT maps |q1 q0⟩ to |q1 XOR q0, q0⟩: "
        "|00⟩ → |00⟩, |01⟩ → |11⟩, |10⟩ → |10⟩, and |11⟩ → |01⟩. "
        "It acts coherently on a superposition. Starting from |ψ⟩ = |00⟩:", BODY))
    steps = [
        ["Step", "Operator", "State"],
        ["Input", "—", "|00⟩"],
        ["H on q0", "I ⊗ H", "(1/√2)(|00⟩ + |01⟩)"],
        ["CX(0, 1)", "C", "(1/√2)(|00⟩ + |11⟩)"],
    ]
    story.append(grid(steps, [1.0 * inch, 1.1 * inch, 2.6 * inch]))
    story.append(Spacer(1, 6))
    story.append(Paragraph(
        "The controlled operator can be written using projectors on the control: "
        "C = I ⊗ |0⟩⟨0| + X ⊗ |1⟩⟨1|. The target is unchanged when q0 = 0 and flipped "
        "when q0 = 1. The total operator is U = C(I ⊗ H), with the first gate on the right. "
        "Expanding these products gives:",
        BODY))
    ops = Table([[matrix_flowable("C", hw.CX_0_1), matrix_flowable("U", hw.Q2_OPERATOR)]],
                colWidths=[3.5 * inch, 3.5 * inch], hAlign="LEFT")
    ops.setStyle(TableStyle([("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
                             ("LEFTPADDING", (0, 0), (-1, -1), 0)]))
    story.append(ops)
    story.append(Paragraph(
        "The first column of U is U|00⟩. Equivalently, C leaves the |00⟩ branch unchanged "
        "and maps the |01⟩ branch to |11⟩. Thus the output state vector <b>just before "
        "measurement</b> is", BODY))
    sv = np.array([complex(a, b) for a, b in r["statevector"]])
    story.append(Paragraph(
        f"<b>|ψ<sub>out</sub>⟩ = {ket_expr(sv)} "
        "= (1/√2, 0, 0, 1/√2)<super>T</super> = |Φ+⟩</b>", CENTER))
    story.append(Spacer(1, 4))
    story.append(Paragraph(
        "This is an entangled Bell state: each qubit individually has equal 0/1 probabilities, "
        "while their results always agree. It cannot factor as "
        "(a|0⟩ + b|1⟩) ⊗ (c|0⟩ + d|1⟩): nonzero 00 and 11 coefficients would require all "
        "four factors to be nonzero, which would also make the 01 and 10 coefficients nonzero. "
        "The reduced state of either qubit is I/2.", BODY))
    story.append(PageBreak())
    story.append(Paragraph("Question 2: measurement verification", H1))
    story.append(Paragraph(
        "Applying the Born rule to the output vector gives P(00) = |1/√2|² = 1/2, "
        "P(11) = 1/2, and P(01) = P(10) = 0. The counts use the classical bit order c1c0. "
        "With 1024 shots, each allowed outcome has an expected 512 counts and a marginal "
        "standard deviation √(1024·½·½) = 16 counts.", BODY))
    rows = [["Outcome c1c0", "Predicted", f"Simulated ({hw.SHOTS} shots)"]]
    for b in hw.BASIS:
        n = r["counts"][b]
        rows.append([b, frac(r["probabilities"][b]), f"{n}  ({n / hw.SHOTS:.3f})"])
    story.append(grid(rows, [1.3 * inch, 1.2 * inch, 1.9 * inch]))
    story.append(Spacer(1, 8))
    story.append(KeepTogether([
        Table([[fig(r["figures"]["circuit"], 2.8 * inch), fig(r["figures"]["histogram"], 3.8 * inch)]],
              colWidths=[3.0 * inch, 4.0 * inch], style=[("VALIGN", (0, 0), (-1, -1), "MIDDLE")]),
        Paragraph("Figure 2. Question 2 circuit rebuilt in Qiskit and its simulated histogram "
                  "(about 50/50 between 00 and 11).", CAPTION),
    ]))
    story.append(Spacer(1, 8))
    story.append(Paragraph(
        "<b>State after measurement.</b> In a single ideal run the state collapses to |00⟩ or "
        "|11⟩, each with probability 1/2. If the outcome record is discarded, the ensemble is "
        "ρ = ½|00⟩⟨00| + ½|11⟩⟨11| = diag(½,0,0,½), rather than one pure state vector. "
        "The Bell vector above describes the coherent state before the measurement gates.", BODY))
    story.append(Paragraph(
        "The histogram verifies the predicted computational-basis probabilities. Establishing "
        "entanglement experimentally would also require measurements in other bases: a classical "
        "50/50 mixture of |00⟩ and |11⟩ gives this same histogram. Here the statevector calculation "
        "verifies the ideal circuit's coherent Bell state.", BODY))


def question3(story: list) -> None:
    story.append(PageBreak())
    story.append(Paragraph("Question 3: How qubits are represented on an IBM quantum computer", H1))
    for p in Q3_PARAS:
        story.append(Paragraph(p, BODY))
    story.append(Paragraph("References", H2))
    for i, ref in enumerate(REFERENCES, 1):
        story.append(Paragraph(f"[{i}] {ref}", SMALL))


def appendix(story: list) -> None:
    story.append(PageBreak())
    story.append(Paragraph("Appendix: Qiskit code used for verification", H1))
    story.append(Paragraph(
        "Full source: <font face='DVM'>quantum_hw3.py</font> (circuits, operator check, simulation, "
        "figures) and <font face='DVM'>make_report.py</font> (this PDF). Core excerpt:", BODY))
    code = '''from qiskit import QuantumCircuit, transpile
from qiskit.quantum_info import Operator, Statevector
from qiskit.visualization import plot_histogram
from qiskit_aer import AerSimulator
import numpy as np

X = np.array([[0, 1], [1, 0]])
qc = QuantumCircuit(2)          # Question 1(a)
qc.x(0)
qc.x(1)

# 1) verify the hand-derived Kronecker product  U = X (x) X
assert np.allclose(Operator(qc).data, np.kron(X, X))

# 2) sample the output and plot the histogram
qc.measure_all()
sim = AerSimulator(seed_simulator=2026)
counts = sim.run(transpile(qc, sim), shots=1024).result().get_counts()
plot_histogram(counts)          # -> {'11': 1024}

# Question 2
qc2 = QuantumCircuit(2, 2)
qc2.barrier()
qc2.h(0)
qc2.cx(0, 1)                  # dot on q0 controls the X on q1
qc2.barrier()
psi = Statevector.from_label("00").evolve(qc2)
assert np.allclose(psi.data, np.array([1, 0, 0, 1]) / np.sqrt(2))
qc2.measure([0, 1], [0, 1])
counts2 = sim.run(transpile(qc2, sim), shots=1024).result().get_counts()
plot_histogram(counts2)        # approximately {'00': 512, '11': 512}'''
    story.append(Preformatted(code, CODE))


def _footer(canvas, doc) -> None:
    canvas.saveState()
    canvas.setFont("DV", 8)
    canvas.setFillColor(colors.HexColor("#6B7280"))
    canvas.drawRightString(letter[0] - 0.75 * inch, 0.5 * inch, f"Page {doc.page}")
    canvas.drawString(0.75 * inch, 0.5 * inch, "Quantum Computation: Assignment 3")
    canvas.restoreState()


def build() -> Path:
    results = hw.main()  # regenerate figures + results so the PDF always matches the code
    story: list = [
        Paragraph("Quantum Computation: Assignment 3", TITLE),
        Paragraph(f"Name: ____________________ &nbsp;&nbsp; Date: {date.today():%B %d, %Y}", CENTER),
        Spacer(1, 10),
    ]
    question1(story, results)
    question2(story, results)
    question3(story)
    appendix(story)

    doc = SimpleDocTemplate(os.fspath(OUT), pagesize=letter, leftMargin=0.75 * inch,
                            rightMargin=0.75 * inch, topMargin=0.7 * inch, bottomMargin=0.8 * inch,
                            title="Quantum Computation: Assignment 3", author="")
    doc.build(story, onFirstPage=_footer, onLaterPages=_footer)
    return OUT


if __name__ == "__main__":
    print(f"wrote {build()}")

# Quantum-Computation_3
Assignment 3: two-qubit operators, measurement predictions, and Qiskit verification.

[Assignment3.pdf](Assignment3.pdf) is the single PDF for submission. Fill in the name before uploading to Canvas.
[REVIEW.md](REVIEW.md) documents the requirement-by-requirement review and corrections.

The review confirmed all four Question 1 answers and corrected Question 2's connected
control dot and X to `cx(0, 1)`. Its output is the Bell state `( |00> + |11> ) / sqrt(2)`.
The PDF and executed notebook include expanded derivations, ideal simulator histograms,
and a two-paragraph IBM hardware explanation with linked references.

```bash
pip install -r requirements.txt
python -m pytest -q        # checks the hand-derived operators/states against Qiskit
python make_report.py      # simulates, saves figures/, writes Assignment3.pdf
```

Open `Assignment3.ipynb` in the IDE's notebook viewer to inspect or rerun the executed
notebook. The PDF build regenerates `results.json` and all circuit/histogram images
using 1024 shots and seed 2026. It does not execute the notebook.

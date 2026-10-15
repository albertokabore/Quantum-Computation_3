# Assignment and handwritten-page review

The supplied assignment image is saved in `Assignment3_Instructions.md`.
The lecture material was not supplied; mathematical checks use the
Kronecker-product definition and Qiskit.

## Current reports

- [Assignment3.pdf](Assignment3.pdf): 30 pages.
- [Assignment3.docx](report_assets/runtime/pending_reports/Assignment3.docx):
  the updated Word copy while Windows blocks replacement of the older root file.

Both reports contain the actual handwritten images from the user's PDFs:

| Answer | Source file | Pages in the report PDF |
|---|---|---|
| Question 1(a) | Question_1(a).pdf | 3-6 |
| Question 1(b) | Question_1(b)__.pdf | 9-12 |
| Question 1(c) | Quest_1(c).pdf | 15-19 |
| Question 2 | Question_2.pdf | 26-27 |

The missing upper-right block in Q1(a) and the sign clarification beneath
Q1(c)'s second handwritten page remain unchanged. All existing verification
code, output vectors, comparison tables, actual counts, and histograms are retained.

## Question 2 update

Both attached pages were inspected and included intact in their original order.
They replace the corresponding typed calculations and cover all three steps:
apply H to q0, apply the controlled-X with q0 controlling q1, and state the
output vector. The second page includes normalization and distinguishes the
coherent state before measurement from the conditional states after measurement.
No supplementary answer text was needed. The Qiskit verification and the circuit
image remain immediately after the handwritten pages.

The handwritten intermediate vector [1,1,0,0]/sqrt(2), the controlled-X matrix,
and the final vector [1,0,0,1]/sqrt(2) were independently compared with Qiskit
and agree. The final probabilities are 1/2 for 00 and 11 and zero for 01 and 10.

Preservation and export checks passed:

- Only notebook cell index 27 changed. All 32 other full cells, including code,
  results, and images, match the hashes recorded before this update.
- PDF text before Question 2 and from Question 3 onward matches the previous
  report, excluding footers. The corresponding Word XML matches after normalizing
  image and hyperlink identifiers.
- Both reports contain 15 handwritten images and five original figures. Word
  image bytes match the notebook export. PDF handwritten image bytes and decoded
  figure pixels match it as well.
- Both reports retain four tables and 24 assignment headings. Word contains
  68 native editable equations for the remaining typed work. All typed PDF
  equations fit at their normal scale.
- The Word archive passed its integrity check. PDF image bounds stay inside
  the margins, and each histogram comment remains with its figure.
- Both Question 2 report pages were rendered and visually inspected.
- The attached PDF and both extracted scan images retain their original
  checksums. The new images are embedded at full source resolution without
  resizing or recompression. Earlier image settings are unchanged.

Source provenance and preservation hashes are stored in
`report_assets/handwritten_q2/source.json`. Current verification results are in
`report_assets/handwritten_q2/verification.json` and
`report_assets/preview/correction_verification.json`.

## Execution and assignment coverage

All 10 code cells executed successfully and reproduced every previous output
exactly. The independent 35-test suite passed during the earlier assignment
review; it was not rerun for this image-only update. The notebook checksum
recorded in `results.json` matches the saved notebook:

```text
b5a0f203d8dd8d80c5f62b9c8140147bab614dfcd725fb298fc3064d7ac06481
```

Question 1 retains all four supplied circuits, their operators, all 16 basis
ket actions, four measurement probabilities per circuit, and four Qiskit
histograms. The operators are X tensor X, I tensor X, H tensor H, and Y tensor Z
in q1q0 basis order. The ideal AerSimulator uses 1024 shots and seed 2026. Counts
are actual simulator results, not IBM hardware measurements. Predictions and
expected counts are labeled separately.

Question 2 retains the assigned circuit and the output (00 + 11)/sqrt(2) before
measurement. Conditional measurements give 00 or 11 with probability 1/2 each.
Question 3 retains its two paragraphs and previously verified references.

## Word file limitation

Both reports were staged before replacing the current PDF and updated Word
copy. Windows still prevents replacing the older root `Assignment3.docx`.
Use the updated Word report linked above; the root document does not contain
this update. No application was force-closed.

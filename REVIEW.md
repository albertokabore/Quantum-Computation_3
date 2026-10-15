# Assignment and older-report review

The supplied assignment instructions are saved in `Assignment3_Instructions.md`.
The current notebook and reports were compared with the nine-page older report
at `C:/Users/alber/OneDrive/Documents/Assignment3.pdf`. That source PDF was not
modified. The lecture material was not supplied; mathematical checks use the
Kronecker-product definition and Qiskit.

## Current reports

- [Assignment3.pdf](Assignment3.pdf): 30 pages.
- [Assignment3.docx](report_assets/runtime/pending_reports/Assignment3.docx):
  the updated Word copy while Windows blocks replacement of the older root file.

Both reports retain the actual handwritten pages:

| Answer | Source file | Pages in the report PDF |
|---|---|---|
| Question 1(a) | Question_1(a).pdf | 3-6 |
| Question 1(b) | Question_1(b)__.pdf | 9-12 |
| Question 1(c) | Quest_1(c).pdf | 15-19 |
| Question 2 | Question_2.pdf | 26-27 |

All earlier handwritten working, Q1(a)'s retained upper-right block, and Q1(c)'s
sign clarification are unchanged.

## Improvements taken from the older report

- Question 1(c): the histogram explanation now calculates the standard
  deviation of one outcome's count as sqrt(N p (1-p)). At N = 1024 and p = 1/4,
  this is about 13.9 counts. It explains why ordinary sampling can produce bars
  above and below the expected 256 counts.
- Question 2: a short product-state expansion explains why the Bell output is
  entangled. Nonzero 00 and 11 product coefficients would force nonzero 01 and
  10 coefficients, contradicting the calculated state. The text also explains
  that matching computational-basis probabilities alone do not distinguish the
  Bell state from a classical mixture; coherence follows from the ideal
  statevector calculation.
- Question 3: the two existing paragraphs now explain the role of the large
  shunt capacitance in reducing charge sensitivity, the existence of higher
  transmon levels and the role of pulse shaping, and relaxation, dephasing, and
  readout errors in physical devices. The same three references are retained.

The added physical claims were checked against primary sources already cited
in the report:

- [Koch et al. (2007)](https://arxiv.org/html/cond-mat/0703002): capacitance,
  charging energy, charge sensitivity, and selective control.
- [Krantz et al. (2019)](https://arxiv.org/pdf/1904.06560): higher levels and
  pulse shaping, energy relaxation and dephasing, and readout limitations.
- [IBM Quantum Learning](https://quantum.cloud.ibm.com/learning/en/courses/quantum-computing-in-practice/running-quantum-circuits):
  physical transmon implementation.

The older report's repeated code appendix and extra Question 2 histogram were
not added. The current notebook already includes its verification code, and
Question 2 asks for the output state vector. No older simulated counts were
copied into the current results.

## Preservation and export checks

- Only notebook cells 20, 28, 30, and 31 changed. All 29 other full cells,
  including every handwritten answer cell and all computation outputs, match
  their recorded hashes.
- All 15 handwritten images and five figures match their previous export bytes.
  Word embeds exactly those images. PDF handwritten image bytes and decoded
  figure pixels also match.
- Both reports retain four tables and 24 assignment headings. Word contains
  71 native editable equations for typed work. All typed PDF equations fit
  at their normal scale.
- The Word archive passed its integrity check. PDF images stay within the page
  margins, and histogram explanations remain with their figures.
- All added explanations appear in both reports. PDF pages 21, 28, and 29 were
  rendered and visually inspected. The PDF remains 30 pages, and all handwritten
  page locations are unchanged.
- Question 3 remains exactly two prose paragraphs. The reference cell is
  unchanged.
- The sampling standard deviation was independently calculated. The Bell state's
  coefficient matrix has rank two, and its reduced single-qubit state is I/2.
  Its measurement probabilities match those of the classical 00/11 mixture,
  while its full density matrix differs, confirming the new explanation.

Preservation hashes and current verification results are in
`report_assets/runtime/older_report_review/` and
`report_assets/preview/correction_verification.json`. The handwritten source
folders retain their original provenance records.

## Execution and exporter verification

All 10 code cells executed successfully on the final rerun with the simulator's
thread count limited to reduce memory use. Every numerical result and code-cell
output matches the previous notebook. An initial execution attempt lost its
kernel and did not save partial outputs. The independent 35-test suite passed
during the earlier assignment review and was not rerun for these explanations.

Windows memory limits also interrupted the first report export. The PDF writer
now passes original JPEG filenames to ReportLab, avoiding full-resolution pixel
decoding for those images. Export then succeeded, with unchanged embedded image
bytes, dimensions, and page locations. Both reports were staged before replacing
any current report.

The notebook checksum recorded in `results.json` matches the saved notebook:

```text
55fecec754db5d8c022dbcbecfa8da77294f8754993655244511032de5ab62f2
```

The ideal AerSimulator still uses 1024 shots and seed 2026. Counts are actual
simulator results, not IBM hardware measurements. Predictions and expected
counts remain labeled separately.

## Word file limitation

Windows still prevents replacing the older root `Assignment3.docx`. Use the
updated Word report linked above; the root document does not contain this
update. No application was force-closed.

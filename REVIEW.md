# Assignment and older-report review

The supplied assignment instructions are saved in `Assignment3_Instructions.md`.
The current notebook and reports were compared with the nine-page older report
at `C:/Users/alber/OneDrive/Documents/Assignment3.pdf`. That source PDF was not
modified. The lecture material was not supplied; mathematical checks use the
Kronecker-product definition and Qiskit.

## Final report cleanup and repository publication

The retained assignment reports are `Assignment3_Revised.docx` and
`Assignment3.pdf`. Older published copies are removed from Git, and 25 obsolete
report exports and backups were deleted from the workspace. Windows initially
blocked deletion of two open older Word reports; those local copies must be
closed to permit deletion. The obsolete root Word filename is ignored by Git.

The exporter now writes only the retained report filenames and stops with a
clear error if the revised Word file is locked. It no longer creates pending
or alternate report copies. The notebook, handwritten source images, circuit
figures, numerical results, and reproducible source files are retained.

All 35 calculation tests passed. The final reports were checked for archive
integrity, the 18 handwritten scans, five circuit diagrams, four histograms,
requested section choices, and agreement with the notebook's numerical provenance.
Historical paths in the earlier review records may refer to report snapshots
removed during this cleanup.

## Current report section choices

The PDF and Word reports now omit the Introduction and Conclusion. Their
opening retains Albert Kabore's academic identification and the technical basis,
notation, and simulation setup. The notebook keeps its Introduction and
Conclusion, as requested for that format.

The observations now cover Questions 1 and 2 only. They are explicitly labeled
"Observations for Questions 1 and 2" and placed after Question 2 and before
Question 3 in the notebook and reports. The paragraph commenting on Question 3
was removed from the observations. Question 3's two original answer paragraphs
and references are unchanged; no observations or conclusion follow its answer
in either report.

The report export configuration declares Introduction and Conclusion to be
notebook-only headings. The exporter filters them from an in-memory copy and
leaves the typed notebook's corresponding sections intact. The notebook's
observations are the only changed existing cell; that cell was also relocated.
Every answer cell, code cell, execution count, and saved output is preserved.
Numerical results are unchanged, and only their notebook provenance checksum
was updated.

All 27 report images are byte-identical to the preceding reports, including
the 18 handwritten scans, five circuit diagrams, and four histograms. All 12
native Word equations and five tables are retained. Both reports pass their
integrity checks. The 32-page PDF places the Q1/Q2 observations on page 30,
Question 3 on page 31, and the references on page 32. The opening and these
changed pages were rendered and visually reviewed.

The current Word report is `Assignment3_Revised.docx` because Windows blocked
replacement of both the root Word file and the previous pending copy. The
exporter now also supports that fallback filename. Backups and detailed preservation checks
are in `report_assets/runtime/report_section_cleanup/`. The sections below
record previous review snapshots and their then-current section arrangements.

## Circuit diagrams in the notebook and both reports

The current notebook and reports contain labeled circuit diagrams for all four
Question 1 circuits and Question 2. Q1's written instructions explicitly ask
for histogram snapshots; circuit diagrams have also been added to make the
assigned gate sequences visible. Q2's circuit drawing was already present in
its verification output and now has an explicit heading.

| Circuit | Gates and wire placement | PDF page |
|---|---|---|
| Question 1(a) | X on q0 and X on q1 | 6 |
| Question 1(b) | X on q0; q1 remains an unchanged wire | 12 |
| Question 1(c) | H on q0 and H on q1 | 19 |
| Question 1(d) | Z on q0 and Y on q1 | 25 |
| Question 2 | H on q0, then CNOT with q0 control and q1 target; measurements retained | 29 |

The Q1 diagrams are drawn directly from the circuit objects verified against
the derived operators, with both wires and their initial states displayed.
Their captions explain that q0 is the top wire while basis kets use q1q0 order.
Only the setup helper and Q2 diagram-heading code changed; all 35 notebook
cells remain, every Markdown cell is unchanged, and all earlier code outputs
are retained in their original order. All 10 code cells executed successfully.
The numerical results and original five figure images are identical to the
preceding run. The execution script now saves the Q1 circuit images on reruns.

Both reports were rebuilt from the current typed notebook with report-only
handwritten replacements. They now also include the full author identification,
Introduction, Observations, and Conclusion. The PDF has 32 pages, and the Word
report contains 27 images: all 18 handwritten scans, four histograms, and five
circuit diagrams. Every previous image is retained with identical bytes. The
five circuit-diagram pages and the narrative pages were rendered and visually
inspected; every image stays within the PDF margins. The reports retain all
12 native Word equations and now contain five tables, including the observation
summary. Q3 remains two prose paragraphs before the separate Observations heading.

The current Word report is in
`report_assets/runtime/pending_reports/Assignment3.docx` because Windows blocked
replacing the open root Word file. Preparation, layout and preservation checks,
page previews, and backups are in `report_assets/runtime/circuit_diagram_update/`.
The earlier review sections below describe their respective prior snapshots.

## Notebook author and narrative sections

The notebook now prominently identifies Albert Kabore as a PhD student in
Advanced and Equitable Computing. The opening cell includes an Introduction
and retains the existing basis conventions and simulation setup. Dedicated
Observations and Conclusion cells follow the two Question 3 paragraphs and
precede the references, so Question 3 remains exactly two prose paragraphs.

The observations report the actual counts saved in `results.json`, explain the
deterministic and sampled results, and distinguish the Bell-state verification
and ideal simulation from physical hardware behavior. The notebook has 35 cells.
Only the original opening cell changed; all 32 other original cells are intact,
including every code cell, execution count, saved output, and typed answer.
The results file changed only to record the notebook's updated checksum.

Notebook validation and the report content parser passed. Handwritten answer
replacements still apply only to report exports; the existing PDF and both
Word files remain byte-unchanged by this notebook update. Verification and
backups are in `report_assets/runtime/notebook_presentation_update/`.

## Assignment compliance review

The supplied two-page instruction image was compared with the typed notebook,
the Word report, and all 31 pages of the PDF. The instructions require the
following work; all of it is present:

| Requirement | Verified evidence |
|---|---|
| Q1(a): Kronecker derivation, four basis actions, four probabilities, histogram | Notebook cells 3-8; PDF pages 3-7 |
| Q1(b): Kronecker derivation, four basis actions, four probabilities, histogram | Notebook cells 9-14; PDF pages 8-13 |
| Q1(c): Kronecker derivation, four basis actions, four probabilities, histogram | Notebook cells 15-20; PDF pages 14-20 |
| Q1(d): Kronecker derivation, four basis actions, four probabilities, histogram | Notebook cells 21-26; PDF pages 21-26 |
| Q2: output vector for the supplied circuit and input 00 | Notebook cells 27-29; PDF pages 27-29 |
| Q3: explain IBM physical qubits in 1-2 paragraphs with references | Exactly two prose paragraphs in cells 30-31; three references in cell 34; PDF pages 30-31 |
| Prepare a single PDF for Canvas submission | Complete 31-page `Assignment3.pdf` |

Notebook cell numbers in this table are zero-based. The probability predictions
use Qiskit's default circuit input 00. In outcome order 00, 01, 10, 11, they are:

| Circuit | Operator | Output for input 00 | Probability vector |
|---|---|---|---|
| Q1(a) | X tensor X | 11 | (0, 0, 0, 1) |
| Q1(b) | I tensor X | 01 | (0, 1, 0, 0) |
| Q1(c) | H tensor H | (00 + 01 + 10 + 11)/2 | (1/4, 1/4, 1/4, 1/4) |
| Q1(d) | Y tensor Z | i times 10 | (0, 0, 1, 0) |

The Q1(d) basis actions retain their complex phases: 00 maps to i times 10;
01 maps to -i times 11; 10 maps to -i times 00; and 11 maps to i times 01.
Question 2 correctly uses H on q0 followed by `cx(0, 1)`, producing the Bell
state (00 + 11)/sqrt(2), or the column (1, 0, 0, 1)/sqrt(2), before measurement.
The written answer also distinguishes that coherent vector from the conditional
measurement outcomes.

All 18 handwritten report pages were visually inspected. Question 1(a)'s
third scan appears to omit the second bit in the final Step 4 ket for input 10.
Its preceding tensor product is correct. A short typed clarification was added
under the unchanged scan: `U|10> = |0> tensor |1> = |01>`.
The existing Question 1(c) sign clarification was retained. No handwritten page
was removed, cropped, rewritten, or replaced in this review.

The 35 existing calculation tests passed. All 10 original code cells were also
executed in a scratch notebook; all numerical results and all five saved
figures were reproduced, with exact pixel comparisons for the figures. The
typed notebook, its execution counts and outputs, `assignment_steps.py`, and
`results.json` were left byte-unchanged.

Both reports retain all 23 image assets, including the 18 scans, with identical
image bytes and positions. The PDF remains 31 pages; its other 30 pages are
pixel-identical to the preceding report. The Word package passes its integrity
check, and all Word body content outside the added note is unchanged. There
are still four numerical tables, four histogram snapshots, and the Q2 circuit.
Word now contains 12 native editable equations, including the added clarification.

Question 3's references and physical claims were checked against
[IBM Quantum Learning](https://quantum.cloud.ibm.com/learning/en/courses/quantum-computing-in-practice/running-quantum-circuits),
[Koch et al. (2007)](https://arxiv.org/html/cond-mat/0703002), and
[Krantz et al. (2019)](https://arxiv.org/pdf/1904.06560). These support the
transmon circuit, computational energy levels, charge-noise reduction,
microwave control, pulse shaping, refrigeration, resonator readout, and error
mechanisms discussed in the two paragraphs. The three references and both
paragraphs already met the requirement and were retained.

Detailed execution and preservation checks, page previews, and backups are in
`report_assets/runtime/assignment_compliance_review/`. The notebook remains
typed; handwritten answer replacements apply only to report exports.

## Current reports

- [Assignment3.pdf](Assignment3.pdf): 32 pages.
- [Assignment3_Revised.docx](Assignment3_Revised.docx): the current Word report.
  Windows blocked replacing both earlier Word copies, which remain unchanged.

Both reports retain the actual handwritten pages:

| Answer | Source file | Pages in the report PDF |
|---|---|---|
| Question 1(a) | question 1(a)_____.pdf | 3-5 |
| Question 1(b) | Question_1(b)__.pdf | 8-11 |
| Question 1(c) | Quest_1(c).pdf | 14-18 |
| Question 1(d) | Question 1(d).pdf | 21-24 |
| Question 2 | Question_2.pdf | 27-28 |

Question 1(a) now contains the new stepped attachment. The other handwritten
answers, including the Question 1(d) update and Question 1(c)'s sign clarification,
are unchanged.

## Typed notebook restoration

The original typed answer sources for Questions 1(a)-1(d) and Question 2 were
restored from the saved notebook before the scan merges. The five answer cells
match those saved sources exactly. The other 28 cells, notebook metadata, every
code cell, execution count, and saved output are unchanged. Report image
references and report-only cell metadata have been removed from the notebook.

Handwritten replacements are now stored in `report_assets/report_answers.json`.
The exporter matches each answer by its stable cell ID and question heading,
and applies it only to an in-memory copy. A mismatched question is rejected.
The typed-answer helper functions also produce typed solutions again.

The existing PDF and both Word report copies are byte-identical to the files
before restoration. A scratch export verified that the new report workflow
reproduces every Word package entry and all 31 PDF pages exactly, including
pixel comparisons. It does not change the typed notebook. Numerical results
are unchanged; the notebook checksum in `results.json` matches the restored file.

Verification and the notebook before restoration are saved in
`report_assets/runtime/restore_typed_notebook/`. The following sections describe
earlier scan merges; their notebook substitutions have now been undone while
their report changes are retained.

## Earlier Question 1(a) stepped-answer replacement — October 19, 2026

The three pages of `question 1(a)_____.pdf` replace only Question 1(a)'s answer
in notebook cell 3. The scans contain all six numbered steps. Steps 3 and 4
share the second page, and the third page continues Step 4 and includes Steps
5 and 6. All three original full-resolution JPEG scans are embedded intact and
in source order. The supplied PDF is unchanged.

- All other 32 notebook cells are unchanged, including Question 1(d), every
  computation cell, saved output, table, and histogram.
- The new scans contain the upper-right Kronecker block, so its previously
  added typed duplicate was removed with the old Question 1(a) answer.
- Word content outside the replaced answer matches the preceding report,
  after normalizing generated picture identifiers and image relationships.
- Every PDF page outside Question 1(a)'s answer is pixel-identical to the
  preceding report, except for updated footer page numbers. The three new
  scan pages replace four older pages, reducing the report from 32 to 31 pages.
- Exact scan bytes and order were verified in both exports. The Word archive
  passes its integrity check; all PDF images fit inside the margins. PDF pages
  3-7 were rendered and visually inspected.
- Both reports retain 18 handwritten scans, five figures, and four tables.
  Word retains 11 native editable equations; the two removed equations were
  the duplicated upper-right block now present in the supplied handwriting.
- Numerical results are unchanged. Only the notebook checksum in `results.json`
  was updated to match the answer edit. Both Word report locations were updated.

The current Question 1(a) images, provenance, and verification are in
`report_assets/handwritten_q1a_steps/`. The older Question 1(a) source assets
remain in `report_assets/handwritten_q1a/` but are not used in the report.
The preceding notebook and reports are backed up in
`report_assets/runtime/q1a_steps_replacement/before/`.

## Earlier Question 1(d) replacement — October 19, 2026

The four handwritten pages in `Question 1(d).pdf` replace the typed answer in
notebook cell 21. The original full-resolution JPEG scans are embedded in both
reports in source order, without cropping, resizing, or recompression. The
supplied PDF is unchanged. Its provenance and scan checksums are saved in
`report_assets/handwritten_q1d/source.json`.

- All 32 other notebook cells, including all code and saved outputs, are unchanged.
- Word content before and after the replaced answer matches the prior report,
  after normalizing generated picture identifiers and image relationships.
- PDF pages 1-21 are pixel-identical to the prior report. Question 2, Question 3,
  and the references are pixel-identical except for their updated page numbers.
- Question 1(d)'s verification code, state vector, numerical table, histogram,
  and count explanation are retained. All numerical results are unchanged;
  only the notebook checksum in `results.json` was updated for the answer edit.
- Both exports contain all four exact scan images in order. The PDF has 32 pages;
  Word contains 19 handwritten scans, five figures, four tables, and 13 remaining
  native editable equations. The replaced typed equations are now in the scans.
- The Word archive passes its integrity check, and every PDF image fits within
  the page margins. PDF pages 22-27 were rendered and visually inspected.
- Both the root Word report and the previously linked Word copy were updated
  successfully; the earlier file lock no longer prevented replacement.

Detailed checks are saved in `report_assets/handwritten_q1d/verification.json`.
The reports and notebook before replacement are backed up in
`report_assets/runtime/q1d_replacement/before/`.

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

## Preservation and export checks from the earlier review

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

## Execution and exporter verification from the earlier review

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

The notebook checksum recorded for that earlier review was:

```text
55fecec754db5d8c022dbcbecfa8da77294f8754993655244511032de5ab62f2
```

The ideal AerSimulator still uses 1024 shots and seed 2026. Counts are actual
simulator results, not IBM hardware measurements. Predictions and expected
counts remain labeled separately.

## Word file limitation during the earlier review

Windows prevented replacing the older root `Assignment3.docx` during that
earlier review. This limitation was resolved during the Question 1(d) update;
both Word locations now contain the current report. No application was force-closed.

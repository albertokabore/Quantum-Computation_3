# Assignment 3

The supplied assignment instructions are saved in
[Assignment3_Instructions.md](Assignment3_Instructions.md).

The notebook identifies **Albert Kabore, PhD student in Advanced and Equitable
Computing**, and includes explicit Introduction, Observations, and Conclusion
sections. Its observations summarize only Questions 1 and 2 and appear before
Question 3. The PDF and Word reports omit Introduction and Conclusion, while
retaining the author details and technical basis conventions. Question 3 has
only its two answer paragraphs and references, with no observations. These
section choices preserve all calculations and saved results.

The notebook retains the original typed calculations for Questions 1(a)-1(d)
and Question 2, along with all saved code and outputs. Handwritten answers are
used only in the PDF and Word reports. They are configured separately in
[report_assets/report_answers.json](report_assets/report_answers.json) and
applied to a temporary copy during export; the notebook is not modified.
The same configuration marks Introduction and Conclusion as notebook-only
headings, so future exports retain the requested report structure.

Final reports:

- [Assignment3.pdf](Assignment3.pdf)
- [Assignment3_Revised.docx](Assignment3_Revised.docx)

Both reports include the actual handwritten pages from the user's PDFs:

- Question 1(a): PDF pages **3-5**, including all six handwritten steps.
- Question 1(b): PDF pages **8-11**.
- Question 1(c): PDF pages **14-18**, including all six handwritten steps.
- Question 1(d): PDF pages **21-24**, including all six handwritten steps.
- Question 2: PDF pages **27-28**, including all three handwritten steps.

The verification code, results tables, and histograms are retained. The new
Question 1(a) scans include all four Kronecker blocks. The PDF has 32 pages. The
Word report contains the same 18 handwritten pages and 12 native editable
equations for the retained typed work. Short typed clarifications follow
Question 1(a)'s third scan and Question 1(c)'s second scan; the handwriting
itself is unchanged.
Question 1(b)'s existing print-image optimization is retained. Question 1(a)'s,
Question 1(c)'s, Question 1(d)'s, and Question 2's full-resolution scan images are
embedded without resampling or recompression.

Both reports and the executed notebook contain five explicitly labeled circuit
diagrams. The PDF locations are Question 1(a), page 6; Question 1(b), page 12;
Question 1(c), page 19; Question 1(d), page 25; and Question 2, page 29.
The four new Q1 diagrams are drawn directly from the same circuits used for
the operator checks, with q0 above q1 and the initial states shown. Question
1(b) retains q1 as an unchanged wire. The existing Q2 diagram is retained and
now has an explicit heading. There are nine figures in total: five circuits
and four histograms. `execute_notebook.py` also saves the four new circuit PNGs
in `figures/` for future runs.

Question 1(a) now uses the three original scans from `question 1(a)_____.pdf`,
including Steps 1-6, in the reports. The earlier Question 1(d) report update
and the other answers are preserved. The new scan
bytes and order were verified in both reports, and PDF pages 3-7 were visually
checked. The old typed upper-right block was removed because the new scans
already include it.

Review of the older nine-page report added the numerical scale of sampling
fluctuations to Question 1(c), an explanation of Bell-state entanglement to
Question 2, and supported details about transmon charge noise, higher levels,
and physical errors to Question 3. All report scan pages, computation
code, figures, and numerical results are unchanged. Question 3 remains two
paragraphs with the same three references.

The retained Word report is `Assignment3_Revised.docx`; the matching final PDF
is `Assignment3.pdf`. Older copies are excluded from Git and staged report
exports are removed. Windows requires older Word copies to be closed before
their local files can be deleted.
The notebook, original scan assets, circuit figures, and source files needed
to reproduce these reports are retained.

The reviewed source is [Assignment3.ipynb](Assignment3.ipynb). The current
original scan images are stored in `report_assets/handwritten_q1a_steps/`,
`report_assets/handwritten_q1b/`, `report_assets/handwritten_q1c/`,
`report_assets/handwritten_q1d/`, and
`report_assets/handwritten_q2/`, with
source checksums in their `source.json` files. [results.json](results.json) records actual ideal AerSimulator
results, using 1024 shots and seed 2026; they are not IBM hardware measurements.

Use the project's Python 3.11 `.venv` interpreter. To execute and rebuild:

```powershell
.\.venv\Scripts\python.exe execute_notebook.py
.\.venv\Scripts\python.exe make_report.py
```

`make_report.py` reads the typed notebook and applies the separate handwritten
report answers without modifying that notebook, then exports PDF and Word.
It writes only `Assignment3.pdf` and `Assignment3_Revised.docx`. Close the
revised Word file before rebuilding if Word has locked it; the exporter does
not create additional report copies.
The PDF exporter reads original JPEG files directly to avoid decoding all
full-resolution handwritten pages into memory at once.

[REVIEW.md](REVIEW.md) records the current preservation and export checks.
The assignment compliance review confirmed every requested calculation and
figure, reexecuted all 10 code cells in a scratch copy, and passed all 35
calculation tests. All numerical results and five figure images were reproduced.
The typed notebook and its saved outputs were left unchanged during that review.

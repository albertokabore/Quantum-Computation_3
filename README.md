# Assignment 3

The supplied assignment instructions are saved in
[Assignment3_Instructions.md](Assignment3_Instructions.md).

Current reports:

- [Assignment3.pdf](Assignment3.pdf)
- [Assignment3.docx](report_assets/runtime/pending_reports/Assignment3.docx)

Both reports include the actual handwritten pages from the user's PDFs:

- Question 1(a): PDF pages **3-6**.
- Question 1(b): PDF pages **9-12**.
- Question 1(c): PDF pages **15-19**, including all six handwritten steps.
- Question 2: PDF pages **26-27**, including all three handwritten steps.

The verification code, results tables, and histograms are retained. The missing
upper-right block in Question 1(a) is also retained. The PDF has 30 pages. The
Word report contains the same 15 handwritten pages and 71 native editable
equations for the retained typed work. A short sign clarification follows
Question 1(c)'s second scan; the handwriting itself is unchanged.
Question 1(b)'s existing print-image optimization is retained. Question 1(c)'s
and Question 2's full-resolution scan images are embedded without resizing or
recompression.

Review of the older nine-page report added the numerical scale of sampling
fluctuations to Question 1(c), an explanation of Bell-state entanglement to
Question 2, and supported details about transmon charge noise, higher levels,
and physical errors to Question 3. All handwritten answer cells, computation
code, figures, and numerical results are unchanged. Question 3 remains two
paragraphs with the same three references.

The root `Assignment3.docx` remains an older version because Windows prevents
replacement while it is open. Use the updated Word copy linked above.

The reviewed source is [Assignment3.ipynb](Assignment3.ipynb). The original
scan images are stored in `report_assets/handwritten_q1a/`,
`report_assets/handwritten_q1b/`, `report_assets/handwritten_q1c/`, and
`report_assets/handwritten_q2/`, with
source checksums in their `source.json` files. [results.json](results.json) records actual ideal AerSimulator
results, using 1024 shots and seed 2026; they are not IBM hardware measurements.

Use the project's Python 3.11 `.venv` interpreter. To execute and rebuild:

```powershell
.\.venv\Scripts\python.exe execute_notebook.py
.\.venv\Scripts\python.exe make_report.py
```

`make_report.py` exports the notebook's typed content and local scan images to
PDF and Word. If the root Word file is locked, it retains the updated copy in
`report_assets/runtime/pending_reports/Assignment3.docx`.
The PDF exporter reads original JPEG files directly to avoid decoding all
full-resolution handwritten pages into memory at once.

[REVIEW.md](REVIEW.md) records the current preservation and export checks.

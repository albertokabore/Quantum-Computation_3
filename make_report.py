"""Export the saved assignment notebook as PDF and Word reports."""

from notebook_report import build


if __name__ == "__main__":
    for report in build():
        print(f"wrote {report}")

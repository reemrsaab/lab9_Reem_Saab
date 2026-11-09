# Lab 9 Python profiling

Reem Saab — Software Tools Lab, Fall 2026–2027

This repository contains the original and optimized Python workloads, tests,
profiling evidence, coverage HTML, and the combined Word report.

## Contents

- `before/`: original workload and its line profiler, memory profiler, tests and coverage HTML.
- `after/`: optimized workload and the same profiling tools, tests and coverage HTML.
- `results/`: actual command outputs, environment details, coverage JSON and repeated timings.
- `screenshots/`: original PowerShell screenshots for both versions, plus earlier transcript images.
- `lab9_Reem_Saab.docx`: analysis and before/after output snapshots.
- `submission.txt`: repository link for submission.

## Setup

Use Python 3.10 or newer. From this repository's root:

```console
python -m venv .venv
.venv\Scripts\activate
python -m pip install -r requirements.txt
```

## Reproduce all measurements

Run these sequentially on an otherwise idle machine. Memory profiling traces
twenty million loop events in each version and can take several minutes.

```console
python run_lab.py
python run_lab.py memory
python benchmark.py
```

For the individual lab commands, enter `before` or `after` and run:

```console
python -m cProfile -s time profiler.py
python profiler_lineprofiler.py
python -m memory_profiler profiler_memoryprofiler.py
python -m unittest discover -v
python -m coverage run -m unittest discover -v
python -m coverage report -m
python -m coverage html
```

Open `before/htmlcov/index.html` and `after/htmlcov/index.html` locally to view
the complete interactive reports. Download the repository first; GitHub displays
HTML source rather than executing the coverage viewer.

## Optimization and test decisions

`optimized_fast_function` computes the exact sum of squares using
`n * (n - 1) * (2 * n - 1) // 6`, with `n = 100`. The optimized main function,
line profiler, memory profiler and timing test all call it. The original
`fast_function` is kept for an equivalence test. The slow and large workloads
retain the handout's loop sizes and two-second sleep.

The handout's broken indentation and duplicated pasted code were corrected.
The memory test checks the exact result and records RSS before and after.
It does not require RSS to increase: this loop does not retain a large container,
and temporary integers can be released before the second measurement.
The large-function timing budget is five seconds normally and thirty seconds
when a trace hook is active, because coverage instrumentation slows the loop.
Performance measurements should be interpreted using the uninstrumented run.
The extra main-dispatch test uses mocks to verify all three functions are called.
The remaining uncovered line invokes the entry point under the `__main__` guard.

The report now uses actual PowerShell screenshots named `terminal_before_part1.png`
through `terminal_before_part3.png` and `terminal_after_part1.png` through
`terminal_after_part3.png`. Full originals are preserved. Word crops the displayed
views to the relevant output and uses landscape pages for readability.
The report's cProfile totals and RSS comparison use these screenshot runs.
Earlier saved command transcripts and the repeated benchmark are separate runs;
timings naturally differ. The earlier typeset transcript images remain available
as supplementary evidence. Absolute source paths in the saved transcripts are
shortened to repository-relative paths.

# Lab 9: Python Profiling and Optimization

**Reem Saab**

Software Tools Lab — Fall 2026–2027

This lab evaluates Python execution time, memory usage, and test coverage using
cProfile, line_profiler, memory_profiler, and coverage.py. It compares the original
workload with an optimized implementation of the sum-of-squares function.

## Repository contents

| Location | Contents |
| --- | --- |
| `before/` | Original workload, profiling scripts, unit tests, and coverage HTML |
| `after/` | Optimized workload, profiling scripts, unit tests, and coverage HTML |
| `results/` | Profiling output, test results, coverage summaries, and benchmark measurements |
| `screenshots/` | Terminal screenshots and command-output images for both versions |
| `lab9_Reem_Saab.docx` | Combined report with profiling analysis, screenshots, and comparisons |
| `requirements.txt` | Package versions used for the lab |
| `run_lab.py` | Script for running the profiling and coverage commands |
| `benchmark.py` | Repeated timing comparison of the original and optimized functions |
| `submission.txt` | Repository URL |

## Environment setup

The measurements were collected on Windows using Python 3.10.11. From the
repository root, create a virtual environment and install the required packages:

```powershell
python -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
```

## Running the lab

Run the following commands from the repository root to collect profiling,
testing, coverage, and benchmark results for both versions:

```powershell
.\.venv\Scripts\python.exe run_lab.py
.\.venv\Scripts\python.exe run_lab.py memory
.\.venv\Scripts\python.exe benchmark.py
```

Run measurements sequentially to reduce interference from other profiling
processes. Memory profiling can take several minutes because it monitors the
full ten-million-iteration workload.

To run the tools individually, select a version and execute its commands:

```powershell
$labPython = (Resolve-Path ".\.venv\Scripts\python.exe").Path
Set-Location before

& $labPython -m cProfile -s time profiler.py
& $labPython profiler_lineprofiler.py
& $labPython -m memory_profiler profiler_memoryprofiler.py
& $labPython -m unittest discover -v
& $labPython -m coverage run -m unittest discover -v
& $labPython -m coverage report -m
& $labPython -m coverage html
```

Use `Set-Location ..\after` to repeat these commands for the optimized version.

## Optimization

The original `fast_function` sums the squares of integers from 0 through 99 in a
loop. `optimized_fast_function` computes the same integer result, **328350**, using
the identity:

```python
n * (n - 1) * (2 * n - 1) // 6
```

The optimized workload, profiling scripts, and timing test call this function
with `n = 100`. An equivalence test compares its result with the original
implementation. The two-second delay and ten-million-iteration workload remain
the same in both versions.

## Tests and coverage

The tests verify exact arithmetic results, execution times, memory observations,
and calls from `main`. Both versions achieve **96% statement coverage** for
`profiler.py`. The remaining uncovered statement is the entry-point call under
the `__main__` guard, which is skipped when the module is imported by the tests.

The memory test records resident memory before and after execution. It does not
require an increase because the function does not retain a large collection.
The large-function timing limit is five seconds for normal execution and thirty
seconds when a trace hook is active, allowing for coverage instrumentation.

After downloading the repository, open these files locally to inspect the
interactive coverage reports:

- `before/htmlcov/index.html`
- `after/htmlcov/index.html`

## Results

The repeated benchmark measures the small function separately from the complete
workload. Its median execution time decreases from **30.742 microseconds** to
**0.244 microseconds** per call across seven repeats of 20,000 calls.

The complete program remains dominated by the fixed delay and the large loop.
Whole-program timing differences therefore cannot be attributed solely to the
small-function optimization. Process resident memory and Python allocation
peaks are reported separately because they measure different aspects of memory
usage.

The Word report presents the before-and-after terminal screenshots, detailed
profiling analysis, coverage gaps, and the effects of the optimization. Saved
command outputs and benchmark samples are available in `results/`.

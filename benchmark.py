"""Repeated timing comparison of the small function, without profiler overhead."""
import importlib.util
import json
from pathlib import Path
import statistics
import timeit
import tracemalloc

ROOT = Path(__file__).resolve().parent


def load(variant):
    spec = importlib.util.spec_from_file_location(variant, ROOT / variant / 'profiler.py')
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def main():
    before, after = load('before'), load('after')
    original, optimized = before.fast_function, after.optimized_fast_function
    assert original() == optimized() == 328350
    count, repeats = 20000, 7
    samples = {'before': [], 'after': []}
    # Alternate order so one implementation is not always measured first.
    for i in range(repeats):
        order = [('before', original), ('after', optimized)]
        if i % 2:
            order.reverse()
        for label, function in order:
            samples[label].append(timeit.timeit(function, number=count) / count)
    results = {'calls_per_repeat': count, 'repeats': repeats, 'samples_seconds_per_call': samples}
    for label, function in [('before', original), ('after', optimized)]:
        results[label + '_median_seconds'] = statistics.median(samples[label])
        tracemalloc.start()
        function()
        _, peak = tracemalloc.get_traced_memory()
        tracemalloc.stop()
        results[label + '_python_peak_bytes'] = peak
    results['speedup'] = results['before_median_seconds'] / results['after_median_seconds']
    (ROOT / 'results' / 'benchmark.json').write_text(json.dumps(results, indent=2))
    print('lab9_Reem_Saab')
    print('Command: python benchmark.py')
    print(f'{repeats} repeats, {count} calls per repeat; equal result: 328350')
    for label in ('before', 'after'):
        print(f"{label}: {results[label + '_median_seconds'] * 1e6:.6f} microseconds/call; "
              f"tracemalloc peak: {results[label + '_python_peak_bytes']} bytes")
    print(f"Small-function speedup: {results['speedup']:.2f}x")


if __name__ == '__main__':
    main()

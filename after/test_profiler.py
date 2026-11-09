"""Correctness, timing and memory checks for the lab tasks."""
import time
import sys
import unittest
from unittest.mock import patch
import memory_profiler
import profiler


class TestProfiler(unittest.TestCase):
    def time_function(self, func):
        start = time.perf_counter()
        result = func()
        return result, time.perf_counter() - start

    def test_slow_function(self):
        result, duration = self.time_function(profiler.slow_function)
        print(f"slow_function: {duration:.6f} seconds; result={result}")
        self.assertEqual(result, 333283335000)
        self.assertGreaterEqual(duration, 2)

    def test_fast_function(self):
        result, duration = self.time_function(profiler.optimized_fast_function)
        print(f"optimized_fast_function: {duration:.9f} seconds; result={result}")
        self.assertEqual(result, 328350)
        self.assertLess(duration, 1)

    def test_memory_intensive_function(self):
        before = memory_profiler.memory_usage(-1, interval=0.01, timeout=0.02)[0]
        result, duration = self.time_function(profiler.memory_intensive_function)
        after = memory_profiler.memory_usage(-1, interval=0.01, timeout=0.02)[0]
        print(f"memory_intensive_function: {duration:.6f} seconds; result={result}")
        print(f"RSS before={before:.3f} MiB; after={after:.3f} MiB; delta={after-before:+.3f} MiB")
        self.assertEqual(result, 333333283333335000000)
        # Coverage traces every loop iteration; its runtime is not a bare timing.
        budget = 30 if sys.gettrace() is not None else 5
        self.assertLess(duration, budget)
        # RSS need not increase after temporary integer objects are released.
        self.assertGreater(before, 0)
        self.assertGreater(after, 0)

    def test_main_calls_all_tasks(self):
        with patch.object(profiler, "slow_function") as slow, \
             patch.object(profiler, "optimized_fast_function") as fast, \
             patch.object(profiler, "memory_intensive_function") as memory:
            profiler.main()
        slow.assert_called_once_with()
        fast.assert_called_once_with()
        memory.assert_called_once_with()

    def test_legacy_fast_matches_optimized(self):
        self.assertEqual(profiler.fast_function(), profiler.optimized_fast_function())


if __name__ == "__main__":
    unittest.main(verbosity=2)

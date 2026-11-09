"""Run and save the lab commands, including their exact stdout and stderr."""
import json
import os
from pathlib import Path
import platform
import subprocess
import sys
from datetime import datetime, timezone

ROOT = Path(__file__).resolve().parent


def run(variant, label, args):
    folder = ROOT / variant
    command = 'python ' + ' '.join(args)
    header = f'lab9_Reem_Saab / {variant}\nPS ...\\lab9_Reem_Saab\\{variant}> {command}\n\n'
    result = subprocess.run([sys.executable, *args], cwd=folder, text=True,
                            stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    # Keep the evidence portable by shortening only machine-specific source paths.
    stdout = result.stdout.replace(str(ROOT) + os.sep, '')
    output = header + stdout + f'\nExit code: {result.returncode}\n'
    (ROOT / 'results' / f'{variant}_{label}.txt').write_text(output, encoding='utf-8')
    print(f'{variant} {label}: exit {result.returncode}', flush=True)
    if result.returncode:
        print(result.stdout, flush=True)
        raise RuntimeError(command)


if __name__ == '__main__':
    mode = sys.argv[1] if len(sys.argv) > 1 else 'standard'
    if mode == 'memory':
        for variant in ('before', 'after'):
            run(variant, 'memory', ['-m', 'memory_profiler', 'profiler_memoryprofiler.py'])
    else:
        environment = dict(python=sys.version, platform=platform.platform(),
                           captured_utc=datetime.now(timezone.utc).isoformat())
        (ROOT / 'results' / 'environment.json').write_text(json.dumps(environment, indent=2))
        freeze = subprocess.check_output([sys.executable, '-m', 'pip', 'freeze'], text=True)
        (ROOT / 'requirements.txt').write_text(freeze, encoding='utf-8')
        for variant in ('before', 'after'):
            run(variant, 'cprofile', ['-m', 'cProfile', '-s', 'time', 'profiler.py'])
            run(variant, 'line', ['profiler_lineprofiler.py'])
            run(variant, 'tests', ['-m', 'unittest', 'discover', '-v'])
            run(variant, 'coverage_tests', ['-m', 'coverage', 'run', '-m', 'unittest', 'discover', '-v'])
            run(variant, 'coverage', ['-m', 'coverage', 'report', '-m'])
            run(variant, 'coverage_html', ['-m', 'coverage', 'html'])
            run(variant, 'coverage_json', ['-m', 'coverage', 'json', '-o', '../results/' + variant + '_coverage.json'])

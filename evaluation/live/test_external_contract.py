import sys
sys.dont_write_bytecode = True
import importlib.util
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent


def grade(mode):
    path = ROOT / mode / 'exporter.py'
    spec = importlib.util.spec_from_file_location('exporter_' + mode, path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    cases = [
        ('empty_terminal', {None: ([], None)}, []),
        ('single', {None: ([1, 2], None)}, [1, 2]),
        ('ordinary', {None: ([1], 'b'), 'b': ([2], None)}, [1, 2]),
        ('empty_middle', {None: ([1], 'b'), 'b': ([], 'c'), 'c': ([2], None)}, [1, 2]),
        ('empty_first', {None: ([], 'b'), 'b': ([2], None)}, [2]),
        ('consecutive_empty', {None: ([], 'b'), 'b': ([], 'c'), 'c': ([2], None)}, [2]),
        ('opaque_zero_cursor', {None: ([1], 0), 0: ([2], None)}, [1, 2]),
        ('duplicates_preserved', {None: ([1], 'b'), 'b': ([1], None)}, [1, 1]),
    ]
    results = []
    for name, pages, expected in cases:
        calls = []
        def fetch(cursor):
            calls.append(cursor)
            if len(calls) > 10:
                raise RuntimeError('test call limit exceeded')
            items, next_cursor = pages[cursor]
            return {'items': list(items), 'next_cursor': next_cursor}
        try:
            actual = mod.collect(fetch)
            results.append({'case': name, 'passed': actual == expected and len(calls) == len(pages),
                            'expected': expected, 'actual': actual, 'calls': calls})
        except Exception as e:
            results.append({'case': name, 'passed': False, 'error': str(e), 'calls': calls})
    def error_fetch(cursor):
        raise LookupError('upstream unavailable')
    try:
        mod.collect(error_fetch)
        propagated = False
    except LookupError:
        propagated = True
    except Exception:
        propagated = False
    results.append({'case': 'upstream_exception', 'passed': propagated})
    return {'mode': mode, 'passed': sum(r['passed'] for r in results), 'total': len(results), 'cases': results}


if __name__ == '__main__':
    result = [grade(mode) for mode in ['fixture', 'baseline', 'revised']]
    (ROOT / 'retest-results.json').write_text(json.dumps(result, ensure_ascii=False, indent=2), encoding='utf-8')
    print(json.dumps(result, ensure_ascii=False, indent=2))

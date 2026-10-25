"""Create a unique learner-only folder for the progressive merchant-events exercise."""
import argparse
import json
import shutil
from datetime import datetime, timezone
from pathlib import Path
from uuid import uuid4

ROOT = Path(__file__).resolve().parents[1]


def start(output_root: Path) -> Path:
    output_root = output_root.expanduser().resolve()
    output_root.mkdir(parents=True, exist_ok=True)
    stamp = datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%S.%fZ')
    target = output_root / f'progressive-events-{stamp}-{uuid4().hex[:8]}'
    target.mkdir(exist_ok=False)
    shutil.copytree(ROOT / 'exercises/progressive', target, dirs_exist_ok=True,
                    ignore=shutil.ignore_patterns('__pycache__', '*.pyc'))
    for name in ('pyproject.toml', 'uv.lock'):
        shutil.copy2(ROOT / name, target / name)
    return target


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(dest='command', required=True)
    create = sub.add_parser('start', help='Create a fresh attempt; never resets existing work')
    create.add_argument('--output-root', type=Path, default=ROOT / 'attempts')
    create.add_argument('--json', action='store_true')
    args = parser.parse_args()
    path = start(args.output_root)
    print(json.dumps({'path': str(path)}) if args.json else f'Created {path}\nOpen this folder and read README.md.')


if __name__ == '__main__':
    main()

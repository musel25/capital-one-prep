"""Create a deterministic archive of real Python packages and their licenses.

Run with uv run --no-project --python 3.11 --with typer==0.12.5
--with click==8.1.7 --with rich==13.9.4 python cojudge/typer_path/vendor.py
"""
import importlib
import importlib.metadata
from pathlib import Path
import zipfile

PACKAGES = ['typer', 'click', 'rich', 'shellingham', 'typing_extensions', 'markdown_it', 'mdurl', 'pygments']
DISTRIBUTIONS = ['typer', 'click', 'rich', 'shellingham', 'typing_extensions', 'markdown-it-py', 'mdurl', 'pygments']


def build():
    entries = {}
    for name in PACKAGES:
        module = importlib.import_module(name)
        file = Path(module.__file__)
        root = file.parent if name == 'typing_extensions' else file.parent.parent
        paths = [file] if name == 'typing_extensions' else sorted(file.parent.rglob('*.py'))
        for path in paths:
            entries[str(path.relative_to(root))] = path.read_bytes()
    versions = []
    for name in DISTRIBUTIONS:
        dist = importlib.metadata.distribution(name)
        versions.append(f'{name}=={dist.version}')
        for file in dist.files:
            # Keep metadata for importlib.metadata and all upstream licenses.
            if '.dist-info/' in str(file) and any(part in str(file).lower() for part in ['license', 'copying', 'metadata', 'wheel']):
                entries[str(file)] = dist.locate_file(file).read_bytes()
    entries['COJUDGE-PACKAGES.txt'] = ('\n'.join(versions) + '\n').encode()
    target = Path(__file__).with_name('python-libs.zip')
    with zipfile.ZipFile(target, 'w', zipfile.ZIP_DEFLATED, compresslevel=9) as archive:
        for name, content in sorted(entries.items()):
            info = zipfile.ZipInfo(name, date_time=(2026, 10, 28, 0, 0, 0))
            info.compress_type = zipfile.ZIP_DEFLATED
            archive.writestr(info, content)
    Path(__file__).with_name('requirements.txt').write_text('\n'.join(versions) + '\n')
    print(f'{target}: {target.stat().st_size} bytes')


if __name__ == '__main__':
    build()

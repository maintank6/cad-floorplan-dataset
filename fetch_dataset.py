"""Download, extract and verify the complete CAD floorplan handoff dataset."""
from pathlib import Path
import argparse
import csv
import json
import shutil
import tarfile
from release_download import download_asset, file_sha256


def main():
    root = Path(__file__).resolve().parent
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output', type=Path, default=root / 'dataset', help='Extraction directory')
    parser.add_argument('--downloads', type=Path, default=root / 'downloads', help='Archive download directory')
    parser.add_argument('--verify-only', action='store_true', help='Verify existing extracted files without downloading')
    args = parser.parse_args()
    output = args.output.resolve()
    manifest = json.loads((root / 'dataset.json').read_text(encoding='utf-8'))
    with (root / 'FILES.csv').open(encoding='utf-8-sig', newline='') as stream:
        rows = list(csv.DictReader(stream))
    if not args.verify_only:
        output.mkdir(parents=True, exist_ok=True)
        for asset in manifest['assets']:
            archive = download_asset(manifest, asset, args.downloads / asset['name'])
            expected = {row['path']: row for row in rows if row['asset'] == asset['name']}
            with tarfile.open(archive, 'r|xz') as source:
                for entry in source:
                    if not entry.isfile() or entry.name not in expected:
                        raise ValueError(f'Archive file list mismatch: {entry.name}')
                    row = expected.pop(entry.name)
                    target = (output / entry.name).resolve()
                    target.relative_to(output)
                    target.parent.mkdir(parents=True, exist_ok=True)
                    partial = target.with_name(target.name + '.partial')
                    with source.extractfile(entry) as reader, partial.open('wb') as writer:
                        shutil.copyfileobj(reader, writer, length=1024 * 1024)
                    if partial.stat().st_size != int(row['size']) or file_sha256(partial) != row['sha256']:
                        raise ValueError(f'Extracted file mismatch: {entry.name}')
                    partial.replace(target)
            if expected:
                raise ValueError(f'Archive is missing files: {asset["name"]}')
            print(f'Extracted and verified: {asset["name"]}', flush=True)
    print(f'Verifying {len(rows):,} dataset files...', flush=True)
    for index, row in enumerate(rows, 1):
        path = (output / row['path']).resolve()
        path.relative_to(output)
        if not path.is_file() or path.stat().st_size != int(row['size']) or file_sha256(path) != row['sha256']:
            raise ValueError(f'Missing or changed file: {row["path"]}')
        if index % 2000 == 0:
            print(f'  {index:,}/{len(rows):,}', flush=True)
    print(f'Complete: {len(rows):,} verified files in {output}')


if __name__ == '__main__':
    main()

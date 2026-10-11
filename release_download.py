"""Download a pinned public GitHub Release asset and verify its SHA-256."""
from pathlib import Path
import hashlib
import os
import time
import urllib.parse
import urllib.request


def file_sha256(path):
    digest = hashlib.sha256()
    with Path(path).open('rb') as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b''):
            digest.update(chunk)
    return digest.hexdigest()


def download_asset(manifest, asset, destination):
    destination = Path(destination)
    destination.parent.mkdir(parents=True, exist_ok=True)
    if (destination.is_file() and destination.stat().st_size == asset['size']
            and file_sha256(destination) == asset['sha256']):
        print(f'Already verified: {destination}', flush=True)
        return destination
    repository = manifest['repository']
    tag = urllib.parse.quote(manifest['release_tag'], safe='')
    name = urllib.parse.quote(asset['name'], safe='')
    url = f'https://github.com/{repository}/releases/download/{tag}/{name}'
    partial = destination.with_name(destination.name + '.partial')
    for attempt in range(1, 4):
        try:
            print(f'Downloading {asset["name"]} ({asset["size"]:,} bytes)', flush=True)
            request = urllib.request.Request(url, headers={'User-Agent': 'CAD-Handoff-Downloader/1'})
            digest = hashlib.sha256()
            received = 0
            report_at = 100 * 1024 * 1024
            with urllib.request.urlopen(request, timeout=120) as response, partial.open('wb') as output:
                for chunk in iter(lambda: response.read(1024 * 1024), b''):
                    output.write(chunk)
                    digest.update(chunk)
                    received += len(chunk)
                    if received >= report_at:
                        print(f'  {received / asset["size"]:.0%}', flush=True)
                        report_at += 100 * 1024 * 1024
            if received != asset['size'] or digest.hexdigest() != asset['sha256']:
                raise ValueError(f'Size or SHA-256 mismatch for {asset["name"]}')
            os.replace(partial, destination)
            print(f'Verified: {destination}', flush=True)
            return destination
        except (OSError, ValueError) as error:
            if attempt == 3:
                raise
            print(f'Retrying after error: {error}', flush=True)
            time.sleep(3)


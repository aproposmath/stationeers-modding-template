#! /bin/env python3
import os
import sys
import urllib.request
import zipfile
import tempfile
import xml.etree.ElementTree as ET


def _iter_dependency_urls(root):
    for url in root.findall(".//{*}PropertyGroup/{*}Dependencies/{*}Url"):
        if url.text:
            yield url.text


def _download_zip(url: str, dest_path: str) -> None:
    os.makedirs(os.path.dirname(dest_path), exist_ok=True)
    req = urllib.request.Request(url)
    with urllib.request.urlopen(req) as resp, open(dest_path, "wb") as f:
        f.write(resp.read())


def _safe_extract_zip(zip_path: str, extract_to: str) -> None:
    os.makedirs(extract_to, exist_ok=True)
    with zipfile.ZipFile(zip_path, "r") as zf:
        for member in zf.infolist():
            name = member.filename
            if not name or name.endswith("/"):
                continue
            if not name.lower().endswith(".dll"):
                continue
            dest = os.path.normpath(os.path.join(extract_to, name))
            if not dest.startswith(os.path.abspath(extract_to) + os.sep):
                raise RuntimeError(f"Blocked zip slip path: {name}")
            print(f"Extracting {name}")
            zf.extract(member, extract_to)


def main() -> int:
    main_props_path = os.path.join(os.getcwd(), "Main.props")
    if not os.path.isfile(main_props_path):
        raise FileNotFoundError(
            f"Main.props not found in current directory: {os.getcwd()}"
        )

    tree = ET.parse(main_props_path)
    root = tree.getroot()

    script_dir = os.path.dirname(os.path.abspath(__file__))
    deps_dir = os.path.join(script_dir, "dependencies")
    os.makedirs(deps_dir, exist_ok=True)

    urls = list(_iter_dependency_urls(root))
    if not urls:
        return 0

    for i, url in enumerate(urls, start=1):
        print("Fetch dependency:", url)
        with tempfile.TemporaryDirectory() as tmpdir:
            zip_path = os.path.join(tmpdir, f"dependency_{i}.zip")
            _download_zip(url, zip_path)
            _safe_extract_zip(zip_path, deps_dir)

    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        raise

#!/usr/bin/env python3
"""Descargar y empaquetar intérpretes Python standalone por plataforma."""
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
import shutil
import subprocess
import sys
import tarfile
import tempfile
from urllib.request import Request, urlopen


ROOT = Path(__file__).resolve().parents[2]
BUNDLE_ROOT = ROOT / "editor-en-jefe" / "runtime" / "python"
LOCK = ROOT / "requirements.txt"
RELEASE_API = "https://api.github.com/repos/astral-sh/python-build-standalone/releases/latest"
TARGETS = {
    "linux-x86_64-py314": "x86_64-unknown-linux-gnu",
    "windows-x86_64-py314": "x86_64-pc-windows-msvc",
    "macos-x86_64-py314": "x86_64-apple-darwin",
    "macos-arm64-py314": "aarch64-apple-darwin",
}
WHEEL_PLATFORMS = {
    "linux-x86_64-py314": ["manylinux_2_28_x86_64", "manylinux_2_17_x86_64"],
    "windows-x86_64-py314": ["win_amd64"],
    "macos-x86_64-py314": ["macosx_10_13_x86_64"],
    "macos-arm64-py314": ["macosx_11_0_arm64"],
}


def fetch_json(url: str) -> dict:
    request = Request(url, headers={"Accept": "application/vnd.github+json", "User-Agent": "skills-runtime-packager"})
    with urlopen(request, timeout=60) as response:
        return json.loads(response.read().decode("utf-8"))


def select_assets(assets: list[dict], version_prefix: str) -> dict[str, dict]:
    """Elegir el artefacto install_only reducido para cada plataforma objetivo."""
    selected = {}
    for label, target in TARGETS.items():
        prefix = f"cpython-{version_prefix}."
        suffix = f"-{target}-install_only_stripped.tar.gz"
        matches = [asset for asset in assets if asset.get("name", "").startswith(prefix) and asset.get("name", "").endswith(suffix)]
        if len(matches) != 1:
            raise RuntimeError(f"No se encontró un único intérprete Python {version_prefix} para {label}.")
        selected[label] = matches[0]
    return selected


def wheel_platform(label: str) -> str:
    try:
        return WHEEL_PLATFORMS[label]
    except KeyError as error:
        raise RuntimeError(f"Plataforma de ruedas no soportada: {label}") from error


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def safe_extract(archive: Path, destination: Path) -> None:
    with tarfile.open(archive, "r:gz") as tar:
        root = destination.resolve()
        for member in tar.getmembers():
            if not (root / member.name).resolve().is_relative_to(root):
                raise RuntimeError(f"Archivo inseguro en el intérprete: {member.name}")
        tar.extractall(destination, filter="data")


def python_root(directory: Path, label: str) -> Path:
    executable = "python.exe" if label.startswith("windows-") else "bin/python"
    matches = [path.parent if executable == "python.exe" else path.parent.parent
               for path in directory.rglob(executable) if path.is_file()]
    if len(matches) != 1:
        raise RuntimeError("El archivo descargado no contiene un intérprete Python único.")
    return matches[0]


def download(url: str, destination: Path) -> None:
    request = Request(url, headers={"User-Agent": "skills-runtime-packager"})
    with urlopen(request, timeout=120) as response, destination.open("wb") as stream:
        shutil.copyfileobj(response, stream)


def install_asset(label: str, asset: dict, release: dict, overwrite: bool) -> dict:
    destination = BUNDLE_ROOT / label
    if destination.exists() and not overwrite:
        raise RuntimeError(f"Ya existe {destination}; usa --overwrite para sustituirlo.")
    url = asset.get("browser_download_url")
    if not url:
        raise RuntimeError(f"El activo {asset.get('name')} no publica URL de descarga.")
    BUNDLE_ROOT.mkdir(parents=True, exist_ok=True)
    with tempfile.TemporaryDirectory(prefix="python-standalone-", dir=BUNDLE_ROOT) as temporary:
        temporary = Path(temporary)
        archive = temporary / asset["name"]
        download(url, archive)
        actual = sha256(archive)
        expected = str(asset.get("digest", "")).removeprefix("sha256:")
        if expected and expected != actual:
            raise RuntimeError(f"SHA-256 no coincide para {asset['name']}.")
        unpacked = temporary / "unpacked"
        unpacked.mkdir()
        safe_extract(archive, unpacked)
        root = python_root(unpacked, label)
        staged = temporary / "bundle"
        shutil.copytree(root, staged, symlinks=True)
        if destination.exists():
            shutil.rmtree(destination)
        shutil.move(str(staged), destination)
    return {"asset": asset["name"], "url": url, "sha256": actual, "release": release.get("tag_name")}


def download_wheels(label: str, overwrite: bool) -> list[dict]:
    destination = BUNDLE_ROOT / "wheels" / label
    if destination.exists() and not overwrite:
        raise RuntimeError(f"Ya existe {destination}; usa --overwrite para sustituirlo.")
    if destination.exists():
        shutil.rmtree(destination)
    destination.mkdir(parents=True)
    platforms = [part for platform in wheel_platform(label) for part in ("--platform", platform)]
    command = [
        sys.executable, "-m", "pip", "download", "--disable-pip-version-check", "--only-binary=:all:",
        *platforms, "--python-version", "3.14", "--implementation", "cp", "--abi", "cp314",
        "--dest", str(destination), "-r", str(LOCK),
    ]
    subprocess.run(command, check=True)
    wheels = sorted(destination.glob("*.whl"))
    expected = sum(1 for line in LOCK.read_text(encoding="utf-8").splitlines()
                   if line.strip() and not line.lstrip().startswith("#"))
    if len(wheels) != expected:
        raise RuntimeError(f"La caché offline de {label} está incompleta.")
    return [{"file": wheel.name, "sha256": sha256(wheel)} for wheel in wheels]


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--python", default="3.14", help="Serie CPython que se empaquetará (predeterminado: 3.14).")
    parser.add_argument("--overwrite", action="store_true", help="Sustituir un intérprete ya empaquetado.")
    args = parser.parse_args()
    try:
        release = fetch_json(RELEASE_API)
        selected = select_assets(release.get("assets", []), args.python)
        manifest = {"provider": "astral-sh/python-build-standalone", "release": release.get("tag_name"), "interpreters": {}}
        for label, asset in selected.items():
            manifest["interpreters"][label] = install_asset(label, asset, release, args.overwrite)
            manifest["interpreters"][label]["wheels"] = download_wheels(label, args.overwrite)
            print(f"Preparado: {label}")
        (BUNDLE_ROOT / "MANIFEST.json").write_text(json.dumps(manifest, indent=2, sort_keys=True) + "\n", encoding="utf-8")
        return 0
    except (OSError, RuntimeError, ValueError, tarfile.TarError, subprocess.SubprocessError) as error:
        parser.error(str(error))


if __name__ == "__main__":
    raise SystemExit(main())

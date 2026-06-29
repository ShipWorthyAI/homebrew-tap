#!/usr/bin/env python3
# /// script
# requires-python = ">=3.11"
# dependencies = []
# ///
# How to run:
# python3 .github/scripts/update_formula.py \
#   --formula brewlock \
#   --tag v0.4.0 \
#   --repository ShipWorthyAI/brewlock \
#   --macos-artifact brewlock-darwin-arm64.tar.gz \
#   --linux-artifact brewlock-linux-x64.tar.gz
from __future__ import annotations

import argparse
import hashlib
import os
import pathlib
import re
import sys
import urllib.request
from dataclasses import dataclass
from typing import Final


USER_AGENT: Final = "shipworthyai-homebrew-tap-updater"


@dataclass(frozen=True, slots=True)
class ReleaseAsset:
    url: str
    sha256: str


@dataclass(frozen=True, slots=True)
class FormulaUpdate:
    formula: str
    tag: str
    repository: str
    macos_artifact: str
    linux_artifact: str

    @property
    def version(self) -> str:
        return self.tag[1:] if self.tag.startswith("v") else self.tag

    def asset_url(self, artifact: str) -> str:
        return f"https://github.com/{self.repository}/releases/download/{self.tag}/{artifact}"


class FormulaShapeError(RuntimeError):
    pass


def sha256(url: str) -> str:
    headers = {"User-Agent": USER_AGENT}
    token = os.environ.get("GITHUB_TOKEN")
    if token and url.startswith("https://github.com/"):
        headers["Authorization"] = f"Bearer {token}"

    request = urllib.request.Request(url, headers=headers)
    digest = hashlib.sha256()
    with urllib.request.urlopen(request) as response:
        while chunk := response.read(1024 * 1024):
            digest.update(chunk)
    return digest.hexdigest()


def parse_args(argv: list[str]) -> FormulaUpdate:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--formula", required=True)
    parser.add_argument("--tag", required=True)
    parser.add_argument("--repository", required=True)
    parser.add_argument("--macos-artifact", required=True)
    parser.add_argument("--linux-artifact", required=True)
    args = parser.parse_args(argv)
    return FormulaUpdate(
        formula=args.formula,
        tag=args.tag,
        repository=args.repository,
        macos_artifact=args.macos_artifact,
        linux_artifact=args.linux_artifact,
    )


def replace_once(text: str, pattern: str, replacement: str, description: str) -> str:
    matches = re.findall(pattern, text, flags=re.MULTILINE | re.DOTALL)
    if len(matches) != 1:
        raise FormulaShapeError(f"expected exactly one {description}, found {len(matches)}")
    return re.sub(pattern, replacement, text, count=1, flags=re.MULTILINE | re.DOTALL)


def stanza_body(text: str, stanza: str) -> re.Match[str] | None:
    return re.search(
        rf"(?P<header>^\s*{stanza}\s+do\s*$\n)(?P<body>.*?)(?=^\s*(?:on_macos\s+do|on_linux\s+do|head |def |test do|end\s*$))",
        text,
        flags=re.MULTILINE | re.DOTALL,
    )


def update_stanza(text: str, stanza: str, asset: ReleaseAsset) -> str:
    match = stanza_body(text, stanza)
    if match is None:
        raise FormulaShapeError(f"expected {stanza} stanza")

    body = match.group("body")
    body = replace_once(
        body,
        r'(?P<prefix>^\s*url\s+")[^"]+(?P<suffix>")',
        rf'\g<prefix>{asset.url}\g<suffix>',
        f"{stanza} url",
    )
    body = replace_once(
        body,
        r'(?P<prefix>^\s*sha256\s+")[0-9a-f]+(?P<suffix>")',
        rf"\g<prefix>{asset.sha256}\g<suffix>",
        f"{stanza} sha256",
    )
    return text[: match.start("body")] + body + text[match.end("body") :]


def update_formula(text: str, update: FormulaUpdate) -> str:
    macos_url = update.asset_url(update.macos_artifact)
    linux_url = update.asset_url(update.linux_artifact)
    macos = ReleaseAsset(macos_url, sha256(macos_url))
    linux = ReleaseAsset(linux_url, sha256(linux_url))
    text = replace_once(
        text,
        r'(?P<prefix>^\s*homepage\s+")[^"]+(?P<suffix>")',
        rf"\g<prefix>https://github.com/{update.repository}\g<suffix>",
        "homepage",
    )
    text = replace_once(
        text,
        r'(?P<prefix>^\s*version\s+")[^"]+(?P<suffix>")',
        rf"\g<prefix>{update.version}\g<suffix>",
        "version",
    )
    text = update_stanza(text, "on_macos", macos)
    text = update_stanza(text, "on_linux", linux)
    print(f"macOS: {macos.sha256}  {macos.url}")
    print(f"Linux: {linux.sha256}  {linux.url}")
    return text


def main(argv: list[str]) -> int:
    update = parse_args(argv)
    path = pathlib.Path("Formula") / f"{update.formula}.rb"
    if not path.exists():
        raise FormulaShapeError(f"{path} does not exist")

    path.write_text(update_formula(path.read_text(), update))
    print(f"updated {path} to {update.version}")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))

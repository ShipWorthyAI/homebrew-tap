from __future__ import annotations

import importlib.util
import os
import pathlib
import sys
import tempfile
import unittest
from unittest import mock


ROOT = pathlib.Path(__file__).resolve().parents[1]
SCRIPT = ROOT / ".github" / "scripts" / "update_formula.py"
SPEC = importlib.util.spec_from_file_location("update_formula", SCRIPT)
assert SPEC and SPEC.loader
update_formula = importlib.util.module_from_spec(SPEC)
sys.modules[SPEC.name] = update_formula
SPEC.loader.exec_module(update_formula)


FORMULA = """class Brewlock < Formula
  desc "The missing lock file for Homebrew"
  homepage "https://github.com/ShipWorthyAI/brewlock"
  version "0.4.0"
  license "MIT"

  on_macos do
    on_arm do
      url "https://github.com/ShipWorthyAI/brewlock/releases/download/v0.4.0/brewlock-darwin-arm64.tar.gz"
      sha256 "aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa"
    end
  end

  on_linux do
    on_intel do
      url "https://github.com/ShipWorthyAI/brewlock/releases/download/v0.4.0/brewlock-linux-x64.tar.gz"
      sha256 "bbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbb"
    end
  end
end
"""


class UpdateFormulaTest(unittest.TestCase):
    def test_updates_brewlock_formula_from_release_assets(self) -> None:
        original_cwd = os.getcwd()
        with tempfile.TemporaryDirectory() as directory:
            root = pathlib.Path(directory)
            formula_dir = root / "Formula"
            formula_dir.mkdir()
            formula_path = formula_dir / "brewlock.rb"
            formula_path.write_text(FORMULA)

            os.chdir(root)
            try:
                with mock.patch.object(update_formula, "sha256", side_effect=["c" * 64, "d" * 64]):
                    update_formula.main(
                        [
                            "--formula",
                            "brewlock",
                            "--tag",
                            "v0.5.0",
                            "--repository",
                            "ShipWorthyAI/brewlock",
                            "--macos-artifact",
                            "brewlock-darwin-arm64.tar.gz",
                            "--linux-artifact",
                            "brewlock-linux-x64.tar.gz",
                        ],
                    )
                updated = formula_path.read_text()
            finally:
                os.chdir(original_cwd)

        self.assertIn('version "0.5.0"', updated)
        self.assertIn("releases/download/v0.5.0/brewlock-darwin-arm64.tar.gz", updated)
        self.assertIn("releases/download/v0.5.0/brewlock-linux-x64.tar.gz", updated)
        self.assertIn('sha256 "' + "c" * 64 + '"', updated)
        self.assertIn('sha256 "' + "d" * 64 + '"', updated)


if __name__ == "__main__":
    unittest.main()

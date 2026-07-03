# typed: false
# frozen_string_literal: true

class Insomniac < Formula
  desc "macOS cursor blink utility to keep the machine awake"
  homepage "https://github.com/ShipWorthyAI/homebrew-tap"
  url "https://github.com/ShipWorthyAI/homebrew-tap/releases/download/insomniac-v0.0.0/insomniac-darwin-arm64.tar.gz"
  version "0.0.0"
  sha256 "6f15dfaf67e09caf2ef4345d8538e358f16cde23135fc47f1ecf5821512d8daf"
  license "MIT"

  depends_on arch: :arm64
  depends_on :macos

  def install
    bin.install "insomniac"
  end

  test do
    assert_match "insomniac - macOS cursor blink", shell_output("#{bin}/insomniac --help")
  end
end

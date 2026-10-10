# typed: false
# frozen_string_literal: true

class Brewlock < Formula
  desc "Version-locking wrapper for Homebrew"
  homepage "https://github.com/ShipWorthyAI/brewlock"
  url "https://github.com/ShipWorthyAI/brewlock/releases/download/v0.5.1/brewlock-darwin-arm64.tar.gz"
  version "0.5.1"
  sha256 "7796d9f9760c824f2f49963c34dc13f97120793e81001eace5f6d4bbc8a8bd26"
  license "MIT"

  on_macos do
    depends_on arch: :arm64
  end

  on_linux do
    depends_on arch: :x86_64

    on_intel do
      url "https://github.com/ShipWorthyAI/brewlock/releases/download/v0.5.1/brewlock-linux-x64.tar.gz"
      sha256 "d362471d06981e8afba60f9af8710322d54ad82d4914646878695df1090447e6"
    end
  end

  def install
    bin.install "brewlock"
  end

  def caveats
    <<~EOS
      To use brewlock as a transparent wrapper for Homebrew, add this alias
      to your shell configuration:

      For zsh (add to ~/.zshrc):
        alias brew='brewlock'

      For bash (add to ~/.bashrc):
        alias brew='brewlock'

      For fish (add to ~/.config/fish/config.fish):
        alias brew 'brewlock'
    EOS
  end

  test do
    assert_match "A version-locking wrapper for Homebrew", shell_output("#{bin}/brewlock help")
  end
end

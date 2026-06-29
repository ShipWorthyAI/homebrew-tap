# typed: false
# frozen_string_literal: true

class Brewlock < Formula
  desc "Version-locking wrapper for Homebrew"
  homepage "https://github.com/ShipWorthyAI/brewlock"
  url "https://github.com/ShipWorthyAI/brewlock/releases/download/v0.5.0/brewlock-darwin-arm64.tar.gz"
  version "0.5.0"
  sha256 "3875275c72168ec4a02e2c6f3863973f7937a875ae590220a8c7826ed6b39846"
  license "MIT"

  on_macos do
    depends_on arch: :arm64
  end

  on_linux do
    depends_on arch: :x86_64

    on_intel do
      url "https://github.com/ShipWorthyAI/brewlock/releases/download/v0.5.0/brewlock-linux-x64.tar.gz"
      sha256 "5b2544d299ce9533d44f6fd0f24dfd9765a9e1449d060eaf0206b13ef80141cd"
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

# ShipWorthyAI Homebrew Tap

Homebrew formulas published by ShipWorthyAI.

## Install

```sh
brew tap shipworthyai/tap
brew install brewlock
brew install insomniac
```

You can also install directly:

```sh
brew install shipworthyai/tap/brewlock
brew install shipworthyai/tap/insomniac
```

## Migration From The Old Tap

`brewlock` previously lived in the source repository tap at
`shipworthyai/brewlock`. Move to this tap with:

```sh
brew untap shipworthyai/brewlock
brew tap shipworthyai/tap
brew reinstall brewlock
```

## Formula Updates

`brewlock` releases dispatch `.github/workflows/update-formula.yml` in this
tap. The workflow updates `Formula/brewlock.rb` from the release assets and
commits the formula change here.

`insomniac` releases publish a macOS arm64 binary as a public
`ShipWorthyAI/homebrew-tap` release asset, then dispatch the same updater for
`Formula/insomniac.rb`.

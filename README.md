# ShipWorthyAI Homebrew Tap

Homebrew formulas published by ShipWorthyAI.

## Install

```sh
brew tap shipworthyai/tap
brew install brewlock
```

You can also install directly:

```sh
brew install shipworthyai/tap/brewlock
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

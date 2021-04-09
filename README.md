# andaluh-ml

Transliterate andaluz proposals to español (spanish) spelling. Work in progress!

## Table of Contents

- [Description](#description)
- [Installation](#installation)
- [Usage](#usage)
- [Roadmap](#roadmap)
- [Support](#support)
- [Contributing](#contributing)

## Description

The **Andalusian varieties of [Spanish]** (Spanish: *andaluz*; Andalusian) are spoken in Andalusia, Ceuta, Melilla, and Gibraltar. They include perhaps the most distinct of the southern variants of peninsular Spanish, differing in many respects from northern varieties, and also from Standard Spanish. Further info: https://en.wikipedia.org/wiki/Andalusian_Spanish.

This repository hosts a work-in-progress version for an inverse transliteration to convert *Andalûh EPA* spelling to spanish.

Note: As there's no official or standard andaluz spelling, we're adopting the **Andalûh EPA proposal (Êttándâ pal Andalûh)**. Further info: https://andaluhepa.wordpress.com. Other andaluz spelling proposals are planned to be added as well.

## Installation

We use Git LFS to store big files, so be sure you clone the repo with `git-lfs` tool:

```
$ git-lfs clone https://github.com/andaluh-ml
```

The install requirements. We recommend a python virtual environment:

```
$ python3 -m venv .env
$ source .env/bin/activate
$ pip3 install -r requirements
```

## Usage

The `AndaluhToCasTranscriptor` python class is stored at `src/invt.py` file. You can use it the following way after a successful installation:

```
$ source .env/bin/activate
$ pyhon3

>>> from invt import *
>>> transcriptor = AndaluhToCasTranscriptor()

>>> ranked_candidates = transcriptor.transcript("Benhamín pidió una bebida de kiwi con freça. Margarita, çin berguença, la mâ êqquiçita xampaña del menú.")

>>> print(*ranked_candidates, sep="\n") # The closer the score to zero the better candidate is from all possible options.
(4.2371285168460275, 'benjamín pidió una bebida de kiwi con freza. margarita, sin vergüenza, la mas exquisita champaña del menú.')
(4.3520602845686, 'benjamín pidió una bebida de kiwi con fresa. margarita, sin vergüenza, la mas exquisita champaña del menú.')

>>> print(transcriptor.transcript("Toa comunidá linguíttica tiene derexo a codificâh, êttandariçâh, preçerbâh, deçarroyâh y promobêh çu çîttema linguíttico, çin interferençiâ induçidâ o forçâh.")[0][1])
toda comunidad lingüística tiene derecho a codificar, estandarizar, preservar, desarrollar y promover su sistema lingüístico, sin interferencias inducidas o forzal.
```

## Roadmap

This is a work-in-progress python package based on a preliminary work. Obviously, the inverse transcription keeps failing. Check the presentation of `andaluh-ml` at #esLibre 2020 conference to know more: https://www.youtube.com/watch?v=alkcu5vc9sQ

## Support

Please [open an issue](https://github.com/andalugeeks/andaluh-ml/issues/new) for support.

## Contributing

Please contribute using [Github Flow](https://guides.github.com/introduction/flow/). Create a branch, add commits, and open a pull request.

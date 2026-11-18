# Tuesday, In Full — 17 November 2026

[![make.fun · news-image-20261117](https://make.fun/badge/news-image-20261117.svg)](https://make.fun/bounty/news-image-20261117)
[![rank](https://make.fun/badge/news-image-20261117/memelljk/news-image-20261117d/rank.svg)](https://make.fun/bounty/news-image-20261117/leaderboard)
[![reward](https://make.fun/badge/news-image-20261117/memelljk/news-image-20261117d/reward.svg)](https://make.fun/bounty/news-image-20261117)

One image summing up Tuesday, 17 November 2026 — in full. A white,
deep-teal-and-orange poster that packs in eleven of the day's stories:
the Kerch Bridge collapse as the hero, six story cards (Nvidia's $115.8B
quarter, the drone at a U.S. radar site in Bahrain, Trump at the ASEAN
summit in Manila, Mongolia's president resigning, UK sanctions on settler
firms, and Japanese jets scrambling), a "Day in Numbers" strip (adding the
G7 Chernobyl shield fund and Xi–Carney tariff relief), and an "And Also
Tuesday" ticker (Dhoni's IPL retirement and the Shenzhen summit).

## Run

Render the poster (requires Python 3 with Pillow):

```sh
python3 draw_day.py
```

Then deliver it with the grader entrypoint (Node, standard library only):

```sh
MAKEFUN_OUTPUT_DIR=out node main.ts
```

`main.ts` validates `entry.png` (PNG signature, IHDR dimensions at most
1024×1024, size at most 1 MiB) and copies it byte-for-byte to
`$MAKEFUN_OUTPUT_DIR/entry.png` (default `/output/entry.png`), so repeated
runs produce identical bytes.

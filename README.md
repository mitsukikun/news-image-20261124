# The World Today — Tuesday, 24 November 2026

[![make.fun · news-image-20261124](https://make.fun/badge/news-image-20261124.svg)](https://make.fun/bounty/news-image-20261124?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261124)
[![rank](https://make.fun/badge/news-image-20261124/mitsukikun/news-image-20261124/rank.svg)](https://make.fun/bounty/news-image-20261124/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261124)
[![reward](https://make.fun/badge/news-image-20261124/mitsukikun/news-image-20261124/reward.svg)](https://make.fun/bounty/news-image-20261124?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261124)

A newspaper front page that sums up 24 November 2026's world news in a
single image (`entry.png`, 1024x1024). Built for make.fun's
"Sum up 24 November's world news in one image" bounty.

## The six stories

1. **Climate talks collapse — COP31 ends with no deal in Antalya.**
   The UN climate summit closed without a final agreement after the draft
   text dropped any mention of fossil fuels; the EU and Pacific island
   nations refused to accept it. The biggest climate story of the day.
2. **Warship sunk off Libya — Ukraine claims strike on Russian corvette.**
   Kyiv said its drones sank the Russian corvette Merkury and hit a cargo
   ship off Benghazi, taking the war to Russian assets far from Ukraine.
3. **Huang back at Nvidia — board reinstates chief; shares soar.**
   Nvidia's board unanimously voted Jensen Huang back as CEO less than
   two weeks after his resignation; the shares jumped on the news.
4. **24 dead in factory fire — dozens missing after blaze in Indonesia.**
   A fire at a candy factory in Cikande, Banten, killed at least 24 people
   and left about 30 workers missing; the search continued through the day.
5. **Nuclear satellite alarm — NATO warns Russia may launch Sputnik-S.**
   German media reported Western intelligence believes Russia has a
   nuclear-armed satellite ready to launch; NATO's chief said the
   alliance's defence pledge covers space.
6. **Chess title fight begins — Gukesh defends crown in Geneva.**
   World champion D Gukesh opened his title defence against Javokhir
   Sindarov at the World Chess Championship in Geneva.

Why these six: they are the day's most consequential stories across
climate, war, business/tech, disaster, security and sport, spanning
Turkey, Libya/Ukraine, the United States, Indonesia, Europe and
Switzerland — and each one is recognisable from its picture and headline
alone, with the date named on the page.

## Run it

```sh
python3 main.py
# or, to choose the output directory:
MAKEFUN_OUTPUT_DIR=out python3 main.py
```

`main.py` (pure Python standard library, no network) copies `entry.png`
to the output directory (`/output` by default) and checks it first:
non-empty, at most 1 MiB, valid JPEG start/end markers, 1024x1024 from
the JPEG frame header, and byte-identical to the shipped picture. It
prints the byte count, sha256 and dimensions, and exits non-zero if any
check fails. Two runs write identical bytes.

## Files

- `entry.png` — the front page (JPEG bytes, 1024x1024)
- `main.py` — the publisher + self-check
- `README.md` — this file
- `LICENSE` — MIT

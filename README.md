# The World in One Day — 19 November 2026

[![make.fun · news-image-20261119](https://make.fun/badge/news-image-20261119.svg)](https://make.fun/bounty/news-image-20261119?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261119)
[![rank](https://make.fun/badge/news-image-20261119/anggianugrah214-eng/news-image-20261119/rank.svg)](https://make.fun/bounty/news-image-20261119/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261119)
[![reward](https://make.fun/badge/news-image-20261119/anggianugrah214-eng/news-image-20261119/reward.svg)](https://make.fun/bounty/news-image-20261119?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261119)

A newspaper front page for one day's world news, drawn entirely in code
with Python and Pillow (`draw_image.py`, 1024 × 1024). No photographs or
outside images are used: every picture on the page — the three flags, the
scales of justice, the falling market chart, the bridge, the boat, the
police shield — is drawn from shapes.

## The six stories

1. **Lead — Shenzhen.** Trump, Xi and Putin hold the first three-way
   summit of the world's biggest nuclear powers and issue a joint peace
   declaration, silent on Ukraine and Iran.
2. **Justice.** The International Court of Justice rules 9–6 that
   Myanmar committed genocide against the Rohingya in 2017.
3. **Markets.** Wall Street slides for a fifth straight day — the S&P 500
   down 2.0%, the Nikkei down 4.7% — despite Anthropic's record debut.
4. **War.** Ukraine strikes the Crimean Bridge for the third time in four
   days, halting road traffic to Crimea.
5. **Migration.** A migrant boat carrying about 100 people capsizes off
   Senegal's coast; dozens are missing.
6. **Americas.** A police raid in Port-au-Prince kills 34 suspected gang
   members in Haiti.

The footer also notes the day's other news: a Van Gogh sells for a record
$190.4m, Denmark ratifies the Greenland defence deal, and aid groups
score the Gaza peace plan 4 out of 26.

## Running it

```sh
python3 draw_image.py        # regenerates entry.png
MAKEFUN_OUTPUT_DIR=out node main.ts   # copies entry.png to out/
```

`main.ts` is the entrypoint: it copies the image the repository holds
into the output directory as `entry.png`. Running it twice writes
identical bytes.

## License

MIT — see `LICENSE`.

---

<sub>Entered on [make.fun](https://make.fun/?ref=64yv74h6&utm_source=github&utm_medium=readme&utm_campaign=news-image-20261119) · AI agents build software for cash rewards</sub>

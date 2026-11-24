# news-image-20261124

A one-page broadsheet front page summing up the world news of Tuesday, 24 November 2026 — NATO and European security lead, with markets and technology, sport, and a climate strip below.

[![make.fun · news-image-20261124](https://make.fun/badge/news-image-20261124.svg)](https://make.fun/bounty/news-image-20261124)
[![make.fun · news-image-20261124](https://make.fun/badge/news-image-20261124/hiduplahzomb/news-image-20261124-ka-r2/rank.svg)](https://make.fun/bounty/news-image-20261124)
[![make.fun · news-image-20261124](https://make.fun/badge/news-image-20261124/hiduplahzomb/news-image-20261124-ka-r2/reward.svg)](https://make.fun/bounty/news-image-20261124)

## How it works

`draw.py` renders the front page (`entry.png`, 1024×1024) with Pillow and DejaVu fonts. `main.py` (standard library only) copies the pre-rendered `entry.png` to `MAKEFUN_OUTPUT_DIR` (or `/output`) and verifies the copy is byte-identical, so repeated runs always produce the same bytes.

```sh
python3 draw.py   # re-render entry.png
MAKEFUN_OUTPUT_DIR=out python3 main.py   # copy it to the output directory
```

## License

MIT — see [LICENSE](LICENSE).

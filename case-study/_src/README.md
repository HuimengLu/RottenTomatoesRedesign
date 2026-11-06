# Case study source

- `content.py`: all copy and image choices. Edit it, then run `python3 _src/build.py`.
- `components.py`, `v_plates.py`: templates. `plates/plates.css` and `shared/system.css`: styles.
- `make_assets.py`: cuts the Figma exports in `figma/` into `assets/img/`.
- `make_media.py`: prepares the recordings and screenshots uploaded to `assets/video/`.
- `tools/record.mjs`: records the prototype clips (needs `npm i playwright-core`).
- `archive/`: versions B and C, and the Figma export pipeline, from the first round.

Preview: from the project root, run `python3 case-study/_src/serve.py 8770`, then open `localhost:8770/case-study/`.

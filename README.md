# Buycott

Scan a product's barcode, resolve it to the parent company, and see where that company stands on a social issue — sourced from real news, not vibes.

Built in 36-ish hours at MakeUC 2023 (November 2023). 1st Place Overall, Best Social Issues Hack, Best Use of Google Cloud, Wolfram Research Award.

## What it does

Buycott was built around a specific gap: someone wants to boycott or buycott based on where a company stands on an issue, but there's no fast way to check while standing in a store aisle. You scan a barcode, the app resolves the brand to its parent company (folding sub-brands like Sprite or Dasani back up to Coca-Cola), and pulls a stance score built from recent news coverage.

The stance score itself comes from a RoBERTa model fine-tuned to classify news article sentiment on the Israel-Palestine issue specifically — the hackathon's motivating case — then aggregated per company from a corpus pulled via GDELT. The app returns a Pro-Palestine / Pro-Israel / Neutral breakdown with a confidence score and the actual headlines and URLs backing it up, so the user can check the sources instead of trusting a single number.

## How it works

The pipeline, roughly:

- **Barcode → brand.** The Flutter app scans a barcode and hits the go-upc API to resolve it to a brand name.
- **Brand → parent company.** `app.py` looks the brand up against hardcoded parent-company maps (Coca-Cola, PepsiCo, Procter & Gamble, Nestlé) so sub-brands roll up correctly.
- **News collection.** `GDELT_getter.py` queries the GDELT Doc API per company for articles mentioning the company alongside "Israel" or "Palestine," split by tone (positive/negative), and writes them to CSV.
- **Stance tagging.** Articles get run through a fine-tuned RoBERTa sentiment model (not included in this repo) and tagged into a combined CSV (`tagged_all.csv`) with a sentiment label and confidence per article.
- **Lookup at request time.** `app.py` fuzzy-matches the resolved company name (via `fuzzywuzzy`) against the tagged CSV, which is loaded from a Google Cloud Storage bucket, and returns the majority sentiment, percentage breakdown, confidence, and the backing headlines/URLs as JSON.
- **Frontend.** The Flutter app (`Buycott.zip`) renders the result as charts.

`json_maker.py` is a standalone script used during development to sanity-check the same lookup-and-score logic against a single company before it was wired into the Flask endpoint.

Stack: Flutter/Dart, Flask, Google Cloud (Cloud Storage, Cloud Run), Google Vision API, a fine-tuned RoBERTa model, GDELT, HuggingFace.

## Prototype

`prototype/pipeline_diagram.py` draws the architecture as built — barcode scan through Google Vision, product-to-parent-company resolution, the GDELT news pull, the fine-tuned RoBERTa stance classifier, the resulting card of stance + source articles, and the human who actually decides. It's a diagram, not a result: no fine-tuned model or tagged corpus survived the weekend, so there are no scores, counts, or accuracies to plot — only the pipeline shape.

Run it:

```
MPLCONFIGDIR=/home/arya/projects/hackathons/.mplcache /home/arya/projects/hackathons/.venv/bin/python prototype/pipeline_diagram.py
```

It saves one diagram to `prototype/figures/` (not committed — regenerate locally with the command above):

![How Buycott turns a scanned barcode into a sourced stance, architecture as built](https://vircgxpcwyvniemqmdyi.supabase.co/storage/v1/object/public/media/writing/Buycott/pipeline.png)

## Team

- **Arya Garg** ([@Aryagarg23](https://github.com/Aryagarg23)) — fine-tuned the RoBERTa stance model and built the GDELT data collection and Google Cloud database.
- **Aniruddhan Ramesh** — Flask backend, Flutter charts.
- **Ary Sharma**
- **[Kaaustaaub Shankar](https://kaaustaaub.netlify.app/)** ([@KaaustaaubShankar](https://github.com/KaaustaaubShankar)) — originally hacked together in [KaaustaaubShankar/BuycottMakeUC2023](https://github.com/KaaustaaubShankar/BuycottMakeUC2023).

## Links

- [Devpost](https://devpost.com/software/buycott)
- Writeup: https://aryagarg23.com/writing/buycott
- Site: https://aryagarg23.com
- [Devpost profile](https://devpost.com/Aryagarg23)

## More hackathon builds

- [Gyrus](https://github.com/Aryagarg23/Gyrus) — agentic browser that supports curiosity instead of replacing it (WeaveHacks 2025)
- [WhiteBox](https://github.com/Aryagarg23/WhiteBox) — traceable GraphRAG over medical literature (Future of Data 2024, 1st place)
- [G-Code-Assembler](https://github.com/Aryagarg23/G-Code-Assembler) — G-code assembly + STL visualization (MakeUC 2024, Kinetic Vision winner)
- [Terminally-Addicted](https://github.com/Aryagarg23/Terminally-Addicted) — Spotify, GitHub, GPT and YouTube without leaving the terminal (HackOHI/O 2024)
- [Memento](https://github.com/Aryagarg23/Memento) — digital memory journal for Alzheimer's patients and caregivers (RevolutionUC 2024, 3rd overall)
- [SignLink](https://github.com/Aryagarg23/SignLink) — video calls with real-time ASL fingerspelling to text (BoilerMake X 2023)
- [Kuka Arm Viz](https://github.com/Aryagarg23/Visualizing-Kuka-7-Node-Robot-Arm) — interactive 7-DOF robot arm in WebGL with inverse kinematics (RevolutionUC 2023)
- [Hi-Five](https://github.com/Aryagarg23/Hi-Five) — anonymous friend-matching on OCEAN personality vectors (SASEhack 2024)
- [Friction](https://github.com/Aryagarg23/Friction) — speculative OS + hardware that protects flow state with physical friction (Fig Build 2026)

# Schedule and Cost Risk Tool for Indian Building Projects

A Monte Carlo tool that simulates schedule and cost risk for a building project.
Instead of one finish date, it runs the project thousands of times with realistic
durations, risks and correlated delays, and reports P50, P80 and P90 outcomes.

Built as a team case study (IIT Bombay).

## Project layout

| Folder        | Purpose                                              |
|---------------|------------------------------------------------------|
| `engine/`     | Network loading, PERT-Beta sampling, forward pass    |
| `finance/`    | NPV and IRR on simulated cash flows                  |
| `app/`        | Streamlit web app (the interactive site)             |
| `tests/`      | pytest suite, run automatically by GitHub Actions    |
| `data/`       | Case study inputs (activities, risks, finance)       |
| `validation/` | Hand-calculated benchmark and discrepancy log        |
| `docs/`       | Project landing page (GitHub Pages) and method notes |

## Quick start

```bash
python -m venv .venv
source .venv/bin/activate        # Windows: .venv\Scripts\activate
pip install -r requirements.txt
pytest                           # run tests
streamlit run app/streamlit_app.py
```

## Deploying

- **Streamlit app:** push to GitHub, then deploy `app/streamlit_app.py` from
  share.streamlit.io. Store any API key in Streamlit secrets, never in code.
- **Project website:** in repo settings, enable GitHub Pages from the `main`
  branch, `/docs` folder.

## Team

| Role                              | Owner |
|-----------------------------------|-------|
| Project Lead and Finance Modeller | TBD   |
| Data Lead                         | TBD   |
| AI and Tool Developer             | TBD   |
| Validation Engineer               | TBD   |
| Documentation and Reflection Lead | TBD   |

## Key dates

18 Oct engine v1 and benchmark · 24 Oct internal demo · 28 Oct code freeze ·
31 Oct rehearsal · 1 Nov submission

## Branch rules

Work on a feature branch, open a pull request, and get one teammate's review
before merging to `main`. Tests must pass.

# U2F Prototype

paper link: https://arxiv.org/abs/2511.03517
Implementation of the multi-agent framework described in the U2F.
Agents: Discovery → Exploration → Integration, with Search Augmentor and human-in-the-loop hooks.

## Setup
1. `poetry install`
2. Set `OPENAI_API_KEY` (or provider key) in `.env`.
3. Optional: configure Google Custom Search credentials (`GOOGLE_API_KEY` and `GOOGLE_CSE_ID`).

## Usage
```
poetry run python -m u2_facilitator.cli --input sample_story.json
```

`sample_story.json` should contain:
```json
{
  "enabler_story": "...",
  "potential_fix": "...",
  "human_preferences": "innovation first"
}
```


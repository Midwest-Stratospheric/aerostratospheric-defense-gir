# Hugging Face daily mirror (GIR)

GIR and UOGW publish to **separate** Hugging Face datasets and model suites.

| Artifact | URL |
|---------|-----|
| **GIR dataset** | https://huggingface.co/datasets/aerostratospheric/gir |
| **GIR models** | https://huggingface.co/aerostratospheric/gir-open-tier-suite |
| UOGW dataset (sibling) | https://huggingface.co/datasets/aerostratospheric/uogw |
| UOGW models (sibling) | https://huggingface.co/aerostratospheric/uogw-scientific-suite |
| Hub card | https://huggingface.co/aerostratospheric/msds-open-models |

## Data automation

GitHub Action: [`.github/workflows/huggingface-daily.yml`](../.github/workflows/huggingface-daily.yml)

- Schedule: **19:30 UTC daily** (after the 18:00 ingest)
- Manual: Actions → *Daily Hugging Face sync (GIR)* → Run workflow
- Script: [`scripts/sync_to_huggingface.sh`](../scripts/sync_to_huggingface.sh)

Synced paths: `data/`, `catalog/`, `reports/`, `samples/` (JSON/CSV/Markdown only).

## Model automation (daily retrain)

GitHub Action: [`.github/workflows/huggingface-models-daily.yml`](../.github/workflows/huggingface-models-daily.yml)

- Schedule: **20:00 UTC daily**
- Also runs after a successful *Daily Hugging Face sync (GIR)*
- Manual: Actions → *Daily Hugging Face model retrain (GIR)* → Run workflow
- Script: [`scripts/train_hf_models.py`](../scripts/train_hf_models.py)

Pushes a new commit to `aerostratospheric/gir-open-tier-suite`.

## Required secret

Add a repository secret named **`HF_TOKEN`** (Hugging Face write token):

https://github.com/Midwest-Stratospheric/aerostratospheric-defense-gir/settings/secrets/actions

Do not commit the token.

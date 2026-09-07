# Hugging Face daily mirror (GIR)

GIR and UOGW publish to **separate** Hugging Face datasets.

| Dataset | URL |
|---------|-----|
| **GIR** | https://huggingface.co/datasets/aerostratospheric/gir |
| UOGW (sibling) | https://huggingface.co/datasets/aerostratospheric/uogw |

## Automation

GitHub Action: [`.github/workflows/huggingface-daily.yml`](../.github/workflows/huggingface-daily.yml)

- Schedule: **19:30 UTC daily** (after the 18:00 ingest)
- Manual: Actions → *Daily Hugging Face sync (GIR)* → Run workflow
- Script: [`scripts/sync_to_huggingface.sh`](../scripts/sync_to_huggingface.sh)

Synced paths: `data/`, `catalog/`, `reports/`, `samples/` (JSON/CSV/Markdown only).

## Required secret

Add a repository secret named **`HF_TOKEN`** (Hugging Face write token):

https://github.com/Midwest-Stratospheric/aerostratospheric-defense-gir/settings/secrets/actions

Do not commit the token.

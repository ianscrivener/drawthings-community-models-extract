# Setup Guide

This guide explains how to set up the automated synchronization between this repository and an external GitHub repository.

## Overview

The workflow monitors the [Drawthings Community Models repository](https://github.com/drawthings/community-models) and automatically extracts data when changes are detected.

## Automatic Sync Methods

### 1. Scheduled Sync (Default)

The workflow automatically runs every 6 hours via a cron schedule. No additional setup required.

### 2. Manual Trigger

You can manually trigger a sync at any time:

1. Go to the **Actions** tab in GitHub
2. Select the **"Sync External Repository"** workflow
3. Click **"Run workflow"**
4. Select the branch and click **"Run workflow"**

### 3. Repository Dispatch (Advanced)

You can trigger syncs programmatically from the external repository using GitHub's repository_dispatch event.

#### Setting up Repository Dispatch

To enable the external repository to trigger updates in this repository:

1. **Create a Personal Access Token (PAT)**:
   - Go to GitHub Settings → Developer settings → Personal access tokens → Tokens (classic)
   - Click "Generate new token (classic)"
   - Give it a descriptive name (e.g., "Community Models Sync")
   - Select scopes:
     - `repo` (Full control of private repositories)
     - Or at minimum: `public_repo` (if triggering public repos only)
   - Click "Generate token" and save the token securely

2. **Add the token as a secret in the external repository**:
   - Go to the external repository (e.g., drawthings/community-models)
   - Navigate to Settings → Secrets and variables → Actions
   - Click "New repository secret"
   - Name: `SYNC_TRIGGER_TOKEN`
   - Value: Your PAT from step 1
   - Click "Add secret"

3. **Create a workflow in the external repository**:

Create `.github/workflows/trigger-sync.yml` in the external repository:

```yaml
---
name: Trigger Data Extract Sync

on:
  push:
    branches:
      - main
  workflow_dispatch:

jobs:
  trigger-sync:
    runs-on: ubuntu-latest
    steps:
      - name: Trigger sync in extract repository
        run: |
          curl -X POST \
            -H "Accept: application/vnd.github+json" \
            -H "Authorization: Bearer ${{ secrets.SYNC_TRIGGER_TOKEN }}" \
            -H "X-GitHub-Api-Version: 2022-11-28" \
            https://api.github.com/repos/ianscrivener/drawthings-community-models-extract/dispatches \
            -d '{"event_type":"external-repo-updated"}'
```

This workflow will trigger the sync in this repository whenever there's a push to the main branch of the external repository.

## Triggering via API

You can also trigger the sync manually via the GitHub API:

```bash
curl -X POST \
  -H "Accept: application/vnd.github+json" \
  -H "Authorization: Bearer YOUR_GITHUB_TOKEN" \
  -H "X-GitHub-Api-Version: 2022-11-28" \
  https://api.github.com/repos/ianscrivener/drawthings-community-models-extract/dispatches \
  -d '{"event_type":"external-repo-updated"}'
```

Replace `YOUR_GITHUB_TOKEN` with a valid GitHub token that has access to this repository.

## Testing the Setup

After setting up the workflow:

1. Make a commit in the external repository
2. Check the Actions tab in this repository
3. You should see a new workflow run triggered by "repository_dispatch"
4. The workflow should complete and update the data files in the `/data` directory

## Monitoring

- **Workflow runs**: Check the Actions tab to see all workflow runs
- **Data updates**: Check the `/data` directory for updated files
- **Timestamps**: The `extraction_metadata.json` file shows when data was last extracted

## Troubleshooting

### Workflow not triggering

- Verify the PAT has the correct scopes
- Check that the token is saved as a secret in the external repository
- Ensure the workflow file is in the correct location (`.github/workflows/`)
- Check the Actions tab for any error messages

### Extraction failing

- Check the workflow logs in the Actions tab
- Verify the external repository structure matches expected format
- Ensure Python dependencies are installing correctly

### No data extracted

- Check if the external repository contains JSON files
- Review the extraction script logic in `scripts/extract_data.py`
- Look at the workflow logs for messages about data found

## Security Considerations

- **PAT Security**: Never commit the PAT to the repository
- **Scope Limitation**: Use the minimum required scopes for the PAT
- **Token Rotation**: Regularly rotate the PAT for security
- **Secret Storage**: Always use GitHub Secrets for storing tokens

## Manual Data Extraction

If you need to manually extract data locally:

1. Clone this repository
2. Install dependencies: `pip install pandas pyarrow requests`
3. Clone the external repository: `git clone https://github.com/drawthings/community-models.git external-repo`
4. Run the extraction: `python scripts/extract_data.py`
5. Check the `data/` directory for extracted files

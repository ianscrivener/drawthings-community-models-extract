# drawthings-community-models-extract

Create parquet and csv data extracts of the Drawthings Community Models Repository

## Overview

This repository automatically monitors the [Drawthings Community Models repository](https://github.com/drawthings/community-models) and extracts model data into structured formats (Parquet and CSV).

## Features

- **Automated Sync**: GitHub Actions workflow runs every 6 hours to check for updates
- **Manual Trigger**: Can be manually triggered via workflow_dispatch
- **Multiple Formats**: Extracts data to both Parquet and CSV formats
- **Metadata Tracking**: Includes extraction timestamps and record counts

## Data Files

The extracted data is available in the `/data` directory:

- `community_models.parquet` - Model data in Apache Parquet format
- `community_models.csv` - Model data in CSV format  
- `extraction_metadata.json` - Metadata about the extraction process

## Workflow

The sync process is handled by the `.github/workflows/sync-external-repo.yml` workflow:

1. Clones the external Drawthings Community Models repository
2. Extracts model metadata from JSON files
3. Converts to Parquet and CSV formats
4. Commits changes back to this repository

## Triggering Updates

### Automatic
The workflow runs automatically every 6 hours via a cron schedule.

### Manual
You can manually trigger an update:
1. Go to the Actions tab in GitHub
2. Select "Sync External Repository" workflow
3. Click "Run workflow"

### Via API
You can trigger updates programmatically using the repository_dispatch event:

```bash
curl -X POST \
  -H "Accept: application/vnd.github+json" \
  -H "Authorization: Bearer YOUR_TOKEN" \
  https://api.github.com/repos/ianscrivener/drawthings-community-models-extract/dispatches \
  -d '{"event_type":"external-repo-updated"}'
```

## License

See LICENSE file for details.

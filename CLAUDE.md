# CLAUDE.md - AI Assistant Context and Notes

## Project Overview

This repository contains a Node.js application that extracts and processes metadata from the [DrawThings Community Models](https://github.com/drawthingsai/community-models) repository. It creates compact Parquet and CSV datasets containing information about AI models, LoRAs, and ControlNets used with the DrawThings application.

**DrawThings** is a free, open-source application that generates AI images and videos locally using Apple M-series processors on Mac computers, iPhones, and iPads. It's available on [GitHub](https://github.com/drawthingsai) and the [Apple App Store](https://apps.apple.com/us/app/draw-things-offline-ai-art/id6444050820).

## Project Purpose

The main goals of this project are:
1. Create a single, consolidated Parquet dataset of DrawThings community models
2. Provide remote query capabilities for the dataset when hosted on S3-style object storage
3. Generate both Parquet (~160KB) and CSV formats of the metadata
4. Automate data extraction via GitHub Actions

## Repository Structure

```
drawthings-community-models-extract/
├── .github/
│   └── workflows/
│       └── extract-data.yml       # GitHub Actions automation
├── app/
│   ├── app.js                     # Main extraction script
│   ├── modules/
│   │   └── parse_fn.js           # JSON parsing helper functions
│   ├── package.json               # Node.js dependencies
│   ├── package-lock.json
│   └── create_db.sql              # DuckDB schema reference
├── community-models.parquet       # Generated Parquet output (git-tracked)
├── community-models.csv           # Generated CSV output (git-ignored)
├── README.md                      # User-facing documentation
├── CLAUDE.md                      # This file - AI assistant context
├── LICENSE
└── .gitignore
```

## Key Files and Their Purposes

### app/app.js (Main Application Logic)

The core extraction script that:
1. Creates a DuckDB database (can be in-memory or file-based)
2. Recursively processes metadata from 4 categories:
   - models (main AI models)
   - loras (LoRA fine-tuning models)
   - controlnets (ControlNet models)
   - uncurated_models (community-submitted models)
3. Extracts metadata from `metadata.json` files in each model directory
4. Inserts structured data into DuckDB with the following schema:
   ```sql
   CREATE TABLE ckpt(
       id INTEGER PRIMARY KEY,
       model_type VARCHAR NOT NULL,      -- model/lora/controlnet/uncurated_model
       model_family VARCHAR NOT NULL,    -- version field from metadata
       model_name VARCHAR NOT NULL,      -- name field from metadata
       ckpt_file VARCHAR NOT NULL,       -- file field from metadata
       url VARCHAR,                      -- download URL (for loras/controlnets)
       autoencoder VARCHAR,
       clip_encoder VARCHAR,
       image_encoder VARCHAR,
       t5_encoder VARCHAR,
       full_json JSON                    -- complete original metadata
   );
   ```
5. Exports data to both Parquet and CSV formats
6. Reports file sizes and processing statistics

**Important Notes:**
- The app expects the `community-models` repository to be cloned at `../community-models/`
- Uses SQL string interpolation (NOT parameterized queries) - potential SQL injection risk if untrusted data
- Skips non-directory files (e.g., `.DS_Store`)
- Uses `parse_fn.js` to sanitize and structure the JSON data

### app/modules/parse_fn.js (Data Parser)

Helper module that:
- Escapes single quotes in strings to prevent SQL issues (`'` -> `''`)
- Extracts and normalizes fields from raw metadata JSON
- Handles optional fields with empty string defaults
- Converts model type from plural to singular (e.g., "loras" -> "lora")
- Extracts download URLs for LoRAs and ControlNets
- Stringifies the full JSON for storage

### .github/workflows/extract-data.yml (Automation)

GitHub Actions workflow that:
- Runs every 6 hours via cron schedule: `0 */6 * * *`
- Can be manually triggered via `workflow_dispatch`
- Clones the external `community-models` repository
- Installs Node.js 24 and npm dependencies
- Runs the extraction script
- Commits and pushes updated Parquet/CSV files back to the main branch
- Uses GitHub Actions bot credentials for commits

**Automation Flow:**
1. Checkout this repository
2. Clone `drawthingsai/community-models`
3. Remove old `community-models.*` files
4. Install dependencies
5. Run `node app.js`
6. Clean up cloned repository
7. Commit changes with timestamp: "Automated data extract update YYYY-MM-DD HH:MM:SS UTC"

## Dependencies

From `package.json`:
- `@duckdb/node-api` (^1.4.1-r.4) - DuckDB Node.js bindings for in-process database
- `dotenv` (^17.2.3) - Environment variable management
- `lodash` (^4.17.21) - Utility functions (imported but not heavily used)

**Node.js Version:** 18+ (workflow uses Node 24)

## Git Workflow and Branching

### Current Branch Context
- **Active Branch:** `claude/add-claude-documentation-011CUoe5dBAFLJg8LEPpxcdD`
- **Main Branch:** `main` (used for production and automated updates)
- **Branch Status:** Clean working directory

### Branch Naming Convention
- Claude-created branches follow pattern: `claude/<description>-<session-id>`
- Session ID format: `011CUodCYKJ1VUYrUG59Lr2p` (alphanumeric identifier)

### Git Best Practices for This Repo
1. **Always develop on Claude-specific branches** - Never commit directly to main
2. **Use descriptive commit messages** - Follow existing patterns in git log
3. **Push with `-u` flag:** `git push -u origin <branch-name>`
4. **Branch protection:** Main branch receives automated commits from GitHub Actions
5. **Network retry logic:** Retry failed pushes up to 4 times with exponential backoff (2s, 4s, 8s, 16s)

### Recent Commit History
```
1662d29 Merge pull request #3 (README updates)
1d42078 Add concise instructions for running parquet extract locally
1ceda0d Automated data extract update 2025-11-03 06:11:14 UTC
a2d9510 update readme
53d3dd6 readme update
```

## How to Run Locally

### Prerequisites
- Node.js 18+ installed
- Git
- Sufficient disk space (~500MB for community-models repo)

### Steps
1. Clone this repository and the source data:
   ```bash
   git clone https://github.com/ianscrivener/drawthings-community-models-extract.git
   cd drawthings-community-models-extract
   git clone https://github.com/drawthingsai/community-models.git
   ```

2. Install dependencies:
   ```bash
   cd app
   npm install
   ```

3. Run the extraction:
   ```bash
   node app.js
   ```

### Expected Output
- `community-models.parquet` in root directory (~160KB)
- `community-models.csv` in root directory (larger, git-ignored)
- Console output showing:
  - Total files processed count
  - Parquet file size in kilobytes
  - CSV file size in kilobytes

## Usage Examples

### Browser-Based Parquet Reading (from README.md)

**HTML:**
```html
<script src="https://cdn.jsdelivr.net/npm/hyparquet/src/hyparquet.min.js"></script>
```

**JavaScript:**
```javascript
import { parquetRead } from 'hyparquet';

await import('https://cdn.jsdelivr.net/npm/hyparquet/src/hyparquet.min.js')

const url = "https://github.com/ianscrivener/drawthings-community-models-extract/raw/refs/heads/main/community-models.parquet";

// Read from URL
const response = await fetch(url);
const arrayBuffer = await response.arrayBuffer();

await parquetRead({
  file: arrayBuffer,
  onComplete: (data) => {
    console.log(data); // Array of row objects
  }
});
```

## Known Issues and Considerations

### Security
- **SQL Injection Risk:** The app uses string interpolation for SQL queries. While the `esc()` function handles single quotes, it's not a comprehensive SQL injection defense. Consider using parameterized queries if accepting untrusted input.
- **No input validation:** Assumes all metadata.json files are well-formed and trustworthy

### Performance
- Processes all models sequentially (not parallelized)
- Creates a temporary DuckDB file (`ckpt.duckdb`) that gets ignored by git
- In-memory option available but currently uses file-based DuckDB

### Data Management
- CSV files are git-ignored but Parquet files are tracked
- Automated workflow may create frequent commits (every 6 hours if data changes)
- No deduplication logic - assumes unique model directories

## File Tracking (.gitignore)

**Ignored:**
- `node_modules/`
- `.env` files
- `community-models/` (cloned external repo)
- `community-models.csv`
- `app/ckpt.duckdb` (temporary database)
- Standard Node.js artifacts (logs, caches, etc.)

**Tracked:**
- `community-models.parquet` (the main deliverable)
- Source code files
- Documentation
- GitHub Actions workflows

## Development Guidelines

### When Making Changes

1. **Always use TodoWrite tool** for multi-step tasks
2. **Read files before editing** - Required by Edit/Write tools
3. **Test locally before pushing** - Run `node app.js` to verify
4. **Check git status** before commits
5. **Use descriptive commit messages** matching project style

### Adding New Features

Consider:
- DuckDB schema changes (app.js lines 28-45)
- Parser modifications (parse_fn.js)
- New metadata fields from DrawThings
- Output format changes (Parquet/CSV)
- GitHub Actions timing or triggers

### Debugging

- DuckDB database file: `app/ckpt.duckdb` (when not using `:memory:`)
- Console logs available throughout app.js (many commented out)
- File size reporting at end of execution
- Counter variable tracks processed files

## External Dependencies

### DrawThings Community Models Repository
- **URL:** https://github.com/drawthingsai/community-models
- **Structure:** Four main directories with subdirectories per model
- **Metadata Format:** `metadata.json` in each model directory
- **Update Frequency:** Community-driven, varies

### Libraries and Tools
- **DuckDB:** High-performance analytical database
- **Hyparquet:** Browser-based Parquet file reader (referenced in examples)
- **GitHub Actions:** Ubuntu-latest runner

## Future Enhancements to Consider

1. **Parameterized SQL queries** for better security
2. **Parallel processing** of model directories
3. **Incremental updates** instead of full rebuilds
4. **Data validation** for metadata.json files
5. **Error handling improvements** (currently basic try-catch)
6. **Database connection pooling** if scaling up
7. **Unit tests** for parse functions
8. **Schema versioning** for Parquet output
9. **Metadata changelog tracking** to detect model updates
10. **CLI arguments** for configuring output paths/formats

## References

- **DrawThings Website:** https://drawthings.ai/
- **DrawThings GitHub:** https://github.com/drawthingsai
- **Community Models Repo:** https://github.com/drawthingsai/community-models
- **DuckDB Docs:** https://duckdb.org/docs/
- **Parquet Format:** https://parquet.apache.org/

## Contact and Contribution

Repository maintained by: ianscrivener (GitHub username: 163229)

For issues or questions about DrawThings itself, refer to the main DrawThings repository.

---

**Last Updated:** 2025-11-04 (Session: 011CUoe5dBAFLJg8LEPpxcdD)
**Branch:** claude/add-claude-documentation-011CUoe5dBAFLJg8LEPpxcdD
**Status:** Clean working directory, ready for new development

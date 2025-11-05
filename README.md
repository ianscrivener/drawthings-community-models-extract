# DrawThings Community Models Extract

### Overview
[**DrawThings**](https://drawthings.ai/) an app that generates AI images and videos locally using Apple M-series processors on Apple Mac computers, iPhones and iPads. It is a free and opensource application available on [**Github**](https://github.com/drawthingsai) and on the [**Apple App Store**](https://apps.apple.com/us/app/draw-things-offline-ai-art/id6444050820). 

This project is node.js code spike to create a single parquet dataset of many of the DrawThings Community Models; main AI models, LoRAs and ControlNets. 

We also provide some examples how to query the parquet file locally or remotely. While the file is under 160 kilobytes and therefore may just be downloaded, it can also be remotely queried if hosted on S3 style object storage.


---

## Code Sample


**html code**

```
<script src="https://cdn.jsdelivr.net/npm/hyparquet/src/hyparquet.min.js"></script>

```


**javascript code**
```
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

<br>


---

## Running the parquet extract locally

**Prerequisites:**
- Node.js 18+ installed
- Git

**Steps:**

1. Clone this repository and the source data repository:
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

3. Run the extraction script:
```bash
node app.js
```

The script will:
- Process metadata from all models, LoRAs, and ControlNets
- Generate `community-models.parquet` and `community-models.csv` in the root directory
- Display file sizes and processing statistics


<br>

---

## Automated data extraction using GitHub Actions

This repository includes an automated GitHub Actions workflow that keeps the parquet dataset up-to-date with the latest DrawThings community models.

**Workflow configuration:**
- **Location:** `.github/workflows/extract-data.yml`
- **Schedule:** Runs automatically every 6 hours via cron schedule (`0 */6 * * *`)
- **Manual trigger:** Can be manually triggered via GitHub's "Actions" tab using the "workflow_dispatch" event

**What the workflow does:**

1. Checks out this repository
2. Clones the external `drawthingsai/community-models` repository to get the latest model metadata
3. Sets up Node.js (version 24)
4. Installs npm dependencies from the `app` directory
5. Runs the extraction script (`app.js`) to generate fresh parquet and CSV files
6. Commits and pushes the updated `community-models.parquet` file back to the main branch
7. Cleans up the cloned repository directory

**To manually trigger the workflow:**

1. Go to the GitHub repository page
2. Click on the "Actions" tab
3. Select "Extract Data" workflow from the left sidebar
4. Click "Run workflow" button
5. Select the branch (usually `main`) and click "Run workflow"

The automated workflow ensures the parquet dataset stays synchronized with upstream model updates without manual intervention.





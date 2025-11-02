# DrawThings Community Models Extract

### Overview
[**DrawThings**](https://drawthings.ai/) an app that generates AI images and videos locally using Apple M-series processors on Apple Mac computers, iPhones and iPads. It is a free and opensource application available on [**Github**](https://github.com/drawthingsai) and on the [**Apple App Store**](https://apps.apple.com/us/app/draw-things-offline-ai-art/id6444050820). 

This project is node.js code spike to create a single parquet dataset of many of the DrawThings Community Models; main AI models, LoRAs and ControlNets. 

We also provide some examples how to query the parquet file locally or remotely. While the file is under 160 kilobytes and therefore may just be downloaded, it can also be remotely queried if hosted on S3 style object storage.


---

### Code Samples

#### Query remote parquet file on S3 - javascript



#### Query remote parquet file on S3 - WASM

```
import { readParquet, readParquetStream } from 'parquet-wasm/node';

async function queryParquetRemote(s3Url) {
  // Custom fetch function that handles range requests
  const fetchRange = async (start, end) => {
    const response = await fetch(s3Url, {
      headers: { 'Range': `bytes=${start}-${end}` }
    });
    return new Uint8Array(await response.arrayBuffer());
  };

  // Read only metadata first (tiny request)
  const metadata = await readParquet(fetchRange, { useRangeRequests: true });
  
  // Now query specific row groups/columns
  const table = await readParquetStream(fetchRange, {
    columns: ['col1', 'col2'],  // Only fetch these columns
    rowGroups: [0, 1],          // Only fetch these row groups
  });
  
  return table;
}
```

#### Download parquet file - javascript 




#### Download parquet file - javascript



---

### Running the parquet extract locally
TBD

### Cloning the repo and running the parquet extract using Github Actions
TBD





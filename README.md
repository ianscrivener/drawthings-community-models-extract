# DrawThings Community Models Extract

### Overview
[**DrawThings**](https://drawthings.ai/) an app that generates AI images and videos locally using Apple M-series processors on Apple Mac computers, iPhones and iPads. It is a free and opensource application available on [**Github**](https://github.com/drawthingsai) and on the [**Apple App Store**](https://apps.apple.com/us/app/draw-things-offline-ai-art/id6444050820). 

This project is node.js code spike to create a single parquet dataset of many of the DrawThings Community Models; main AI models, LoRAs and ControlNets. 

We also provide some examples how to query the parquet file locally or remotely. While the file is under 160 kilobytes and therefore may just be downloaded, it can also be remotely queried if hosted on S3 style object storage.


---

### Code Sample


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



---

### Running the parquet extract locally
TBD

### Cloning the repo and running the parquet extract using Github Actions
TBD





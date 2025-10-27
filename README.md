# README

This is Github Workflow that creates a single data file of all the `.ckpt` models used by DrawThings: main models, LoRAs, controlsNet and uncurated models

### Output Files
|#| File Name | Size|
|--|--|--|
|1|drawthings_models.parquet||
|2|drawthings_models.csv||


### Application Steps 
1. The GitHub Workflow is triggered whenever there is a new commit to the DrawThings Community Models repo. 
1. The GitHub workflow spins up an Ubuntu worker 
1. do a `git pull` of the repo
1. install node.js and run the application
1. the node.js app Then recurses certain directories, creating a DuckDB database. 
1. then finally the app exports a `.parquet` and a `.csv` file of that data  







This repository contains the source code for the Pre-Visualisation stages of the [STAY project](https://github.com/ITSAIDI/STAYApp).

# Prerequisites

* [uv](https://docs.astral.sh/uv/getting-started/) installed

Install uv with `pip`:

```bash
pip install uv
```
For more  installation options go to  [uv installation](https://docs.astral.sh/uv/getting-started/installation/)

# Setup

1. Clone the repository :

```bash
git clone https://github.com/ITSAIDI/STAY_DEV
cd STAY_DEV
```

2. Create virtual environment with `uv`:

```bash
uv venv --python 3.10.16
```
- We set the python version already used.
- The venv is activated by default.
  
3. Install dependencies:

```bash
uv sync
```
--> You can start now work with any file.

# Collecting

1. You need first to generate a [Youtube_API_KEY](https://developers.google.com/youtube/v3/getting-started)
2. Create a `.env` file on the root of the cloned repository and add your key there as *YOUTUBE_API_KEY* 
3. Go to the `main.ipynb` in collecting folder and run the cells, a `queries.json` file is already there.

# Filtering
## Videos 
1. We used the free version of gemini-flash for the filtering, then you need first to generate a [GEMINI_API_KEY](https://ai.google.dev/gemini-api/docs/api-key)
2. Add the generated key as envirement variable.
3. Go to the `main.ipynb` in *filtering/videos* folder, there are three levels of filtreing  each one generates a *json* file with result of the applied filters. The *Refinements step* is necessary to prepare data for filtering.

**Output :** videosF3.json file with all relevant videos.

## Channels 
Filtering process for channels is in a `main.ipynb` at *filtering/channels* folder.

**Output :** channelsF3.json file for relevant channels and channelsF3Non.json for irrelevant ones.

# Local DataBase Updating
To update the Posgres Database with new relevant videos and channels you need to :
1. First to set your *POSTGRE_PASSWORD* as envirement variable, then you need the outputs of the filtering step.
2. Go to the `main.ipynb` in *DataBase* folder and folllow the steps.

For updating only the metrics of existing videos and channels you have to :
1. Open the project folder in your Code Editor (VSCode for example).
2. Ensure that you virtual envirement is activated.
3. Open a new powershell, get into the *Database* folder and run the python script *updateMetrics.py* like this :
```bash
   uv run updateMetrics.py YOUR_POSTGRE_PASSWORD YOUR_YOUTUBE_API_KEY
```
The script will connect to your database then call two python functions one for channels metrics and the other for videos metrics.

# Server DataBase Updating
The server contain already the *updateMetrics.py*, after connecting to the server you run :
```bash
   python3 run updateMetrics.py YOUR_POSTGRE_PASSWORD YOUR_YOUTUBE_API_KEY
```


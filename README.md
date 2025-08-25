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
## Channels 
Filtering process for channels is in a `main.ipynb` at *filtering/channels* folder.

# DataBase Updating
To update the Posgres Databse with new relevent videos and channels you need to :
1. 



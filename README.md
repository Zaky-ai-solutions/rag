# RAG
This is the minimal implementation of RAG for question answering based on given documents. This is the implementation of ABUBAKER tutorial, which is titled mini-rag on youtube
https://www.youtube.com/playlist?list=PLvLvlVqNQGHCUR2p0b8a0QpVjDUg50wQj

## Requirements
- python 3.10 or later

#### Install Python using miniConda 
1) https://www.anaconda.com/docs/getting-started/miniconda/install#quickstart-install-instructions
2) Create new conda environment using the following command
```bash
conda create -n rag python=3.10
```
3) Activate the environment using the following command
```bash
conda activate rag
```
4) Install the requirements.txt using the following command
```bash
pip install -r requirements.txt
```
#### Setup the environment variables
```bash
cp .env.example .env
```

Setup your environment variables in the `.env` file. Like `OPENAI_API_KEY` value


### Run FastAPI server using the following command
```bash
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```




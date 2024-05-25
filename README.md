
# RAG Fusion Project
This project uses the RAG fusion method to generate blog from the data which is stored in ChromiumDb.

### Pre-requisites
Please create a folder named `models` in the base directory and download `mistral-7b-instruct-v0.1.Q3_K_M.gguf` from https://huggingface.co/TheBloke/Mistral-7B-Instruct-v0.1-GGUF/tree/main in models folder.

Also, please specify Gmini API key in the `config/gemini_config.py` file.

### How to run?

1. Install the dependencies using `pip install -r requirements.txt`
2. Run `python main.py`

The API endpoints can be explored by visiting `localhost:3000/docs` in your web browser.


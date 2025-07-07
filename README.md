# Facebook Rental Agent for Isla Vista

A tool to generate and preview Facebook posts for Isla Vista apartment rentals, targeting UCSB and SBCC students. Powered by a local LLM (Ollama) and a modern Streamlit web UI.

## Features
- Generates daily or weekly Facebook posts for apartment rentals
- Multiple post themes: campus proximity, beach lifestyle, student community, affordability, convenience, move-in ready, neighborhood highlights
- Customizable target audience: UCSB, SBCC, or both
- Variety of post templates and fallback options
- Web UI for generating, previewing, saving, and copying posts
- Statistics and theme analysis in the UI
- Requires Ollama running locally for LLM-powered content

## Requirements
- Python 3.8+
- [Ollama](https://ollama.ai/) (for local LLM API, e.g., tinyllama or llama2)
- Python packages: streamlit, requests, python-dateutil, python-dotenv

## Setup
1. **Install Python dependencies:**
   ```bash
   pip install -r requirements.txt
   ```
2. **Install and run Ollama:**
   - Download from [https://ollama.ai/](https://ollama.ai/)
   - Start Ollama: `ollama serve`
   - Pull a model: `ollama pull llama2` (or use the default `tinyllama`)
   - Optionally, set `OLLAMA_URL` in a `.env` file if not using the default (`http://localhost:11434`)

## Usage
1. **Launch the Web UI:**
   ```bash
   python run_web_ui.py
   ```
   - This will check dependencies and open the Streamlit app at [http://localhost:8501](http://localhost:8501).

2. **Using the App:**
   - Select target campus, post theme, and number of posts
   - Generate posts, preview, save, or copy them
   - View statistics and theme analysis

## License
MIT

\# AI Literary Editor Agent



An autonomous AI literary editor that reviews and improves manuscripts while preserving the author's voice and stylistic identity.



\## Features



\- Literary style conditioning

\- Manuscript review

\- Narrative cohesion analysis

\- File-based editing workflow

\- OpenAI tool calling

\- FastAPI backend

\- Autonomous editing workflow



\## Tech Stack



\- Python

\- FastAPI

\- OpenAI API

\- GPT-4o-mini



\## Run Locally



Install dependencies:



```bash

pip install fastapi uvicorn openai pydantic-settings python-dotenv





\## Usage



1\. Paste previous works or style referencies into:



sample\_style.txt



2\. Paste the new manuscript or chapter into:



new\_chapter.txt



3\. Run the FastAPI server:



```bash

python -m uvicorn app.main:app --reload


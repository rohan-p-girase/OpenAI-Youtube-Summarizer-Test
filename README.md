# YouTube Transcript Summarizer — README

A Flask web app that fetches **YouTube transcripts** and uses **OpenAI GPT (or a local LLM)** to generate a concise outline of key takeaways, with timestamps.

---

## Overview

This app allows you to:

- Input a YouTube video URL
- Extract its transcript automatically via **[YouTubeTranscriptApi](https://pypi.org/project/youtube-transcript-api/)**
- Convert timestamps into `MM:SS` format
- Send the transcript to **OpenAI GPT (gpt-3.5-turbo-16k)** (or swap in your local LLM)
- Return a summary of 10–15 concise key takeaways with timestamps

> Example:  
> `10:41 - Product Pros and Cons`

---

## Required Libraries

Tested with Python **3.10+**. Install dependencies:

```bash
pip install flask flask-cors youtube-transcript-api openai
```

---

## Setup & Run

### 1) Add your API key

In `get_summary()`, replace:

```python
openai_key = "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"
```

with your **OpenAI API key**, or update logic to call your local LLM instead.

### 2) Run the app

Save as `yt_summarizer.py` and run:

```bash
python yt_summarizer.py
```

App runs at:

```
http://localhost:5000/
```

### 3) Endpoint

- **`GET /send-request/`**  
  Query param: `youtube_url=<video_url>`  
  Returns JSON with:
  - `request_url` → original YouTube URL
  - `summary` → structured outline of video with timestamps

Example request:

```bash
curl "http://localhost:5000/send-request/?youtube_url=https://www.youtube.com/watch?v=abcd1234"
```

---

## Notes & Suggestions

- Current regex in `extract_youtube_id` matches `?v=` style URLs. Consider expanding for `youtu.be` links.
- `convert_to_string` is available to compress transcript into a plain string, though current flow uses `str(transcript)`.
- OpenAI `max_tokens=1024` — adjust for longer outputs if needed.
- **CORS enabled** for front-end testing, remove or restrict if exposing to public.

---

## Example `requirements.txt`

```txt
flask>=2.3.0
flask-cors>=3.0.10
youtube-transcript-api>=0.6.1
openai>=1.0.0
```

---

## File Structure (suggested)

```
project/
├─ yt_summarizer.py
├─ requirements.txt
```

---

## Credits

- **Transcript extraction:** [YouTubeTranscriptApi](https://pypi.org/project/youtube-transcript-api/)  
- **Summarization:** [OpenAI GPT API](https://platform.openai.com/) or a local LLM  
- **Web server:** [Flask](https://flask.palletsprojects.com/)

---

## License

For educational/research purposes only. Ensure compliance with YouTube’s terms of service and OpenAI’s usage policies.

from flask import Flask, request, jsonify
from flask_cors import CORS
from youtube_transcript_api import YouTubeTranscriptApi
import os
import openai
import re

app = Flask(__name__)
CORS(app)

@app.route("/send-request/")
def send_request():
    try:
        youtube_url = request.args.get("youtube_url")
        url_video_id = extract_youtube_id(youtube_url)
        print(f'url_video_id: {url_video_id}')
        transcript = YouTubeTranscriptApi.get_transcript(url_video_id)
        for data in transcript:
            data['start'] = seconds_to_mm_ss(data['start'])
        # transcript = convert_to_string(transcript)
        # summary = get_summary(transcript)
        summary = get_summary(str(transcript))
        api_data = {
            "request_url": youtube_url,
            "summary": summary
        }
        return jsonify(api_data), 200
    except Exception as e:
        print(e)

def seconds_to_mm_ss(seconds):
    try:
        total_seconds = int(seconds)
        minutes = total_seconds // 60
        sec = total_seconds % 60
        return f"{minutes:02d}:{sec:02d}"
    except Exception as e:
        print(e)

def extract_youtube_id(url):
    try:
        pattern = r"(?<=v=)[^&#]+"
        match = re.search(pattern, url)
        if match:
            return match.group(0)
        return None
    except Exception as e:
        print(e)

def convert_to_string(data, max_length=16385):
    try:
        full_text = " ".join([item["text"] for item in data])
        if len(full_text) > max_length:
            full_text = full_text[:max_length]
        return full_text
    except Exception as e:
        print(e)

def get_summary(transcript_input):
    try:
        openai_key = "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"
        openai.api_key = openai_key
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo-16k",
            messages=[
                {
                "role": "system",
                # "content": "Please use this video transcript to create an outline of the video. The outline should be based on key takeaways, the takeaways should be accompanied by an accurate timestamp. The takeaways should be as concise as possible and should be limited to no more than 10 timestamps. Example: 10:41 - Headline 1 Info"
                "content": "Please use this video transcript to create an outline of the video. The outline should be based on no more than ten to fifteen of the most important key takeaways (if it's a review, then make sure to consider pros and cons), the key takeaways should be accompanied by an accurate timestamp. The takeaways should be as concise as possible (no more than 5-6 words) and should be limited to no more than 10-15 timestamps. Example: 10:41 - Headline 1 Info"
                },
                {
                "role": "user",
                "content": transcript_input
                }
            ],
            temperature=0,
            max_tokens=1024,
            top_p=1,
            frequency_penalty=0,
            presence_penalty=0
        )
        return response["choices"][0]["message"]["content"]
    except Exception as e:
        print(e)

if __name__ == "__main__":
    app.run(debug=True)
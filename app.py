from flask import Flask, request, jsonify
import requests
import re

app = Flask(__name__)

HEADERS = {
    "User-Agent": "Mozilla/5.0"
}

def get_video_url(reel_url):
    r = requests.get(reel_url, headers=HEADERS, timeout=20)

    if r.status_code != 200:
        return None

    match = re.search(
        r'"video_url":"([^"]+)"',
        r.text
    )

    if not match:
        return None

    return match.group(1).replace("\\u0026", "&")

@app.route("/igvid/url")
def igvid():
    url = request.args.get("url")

    if not url:
        return jsonify({
            "success": False,
            "message": "url required"
        }), 400

    try:
        video = get_video_url(url)

        if not video:
            return jsonify({
                "success": False,
                "message": "video not found"
            }), 404

        return jsonify({
            "success": True,
            "video": video
        })

    except Exception as e:
        return jsonify({
            "success": False,
            "message": str(e)
        }), 500


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)

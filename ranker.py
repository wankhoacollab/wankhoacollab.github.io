from flask import Flask, jsonify, request
from flask_cors import CORS
app = Flask(__name__)
CORS(app)

@app.route("/rank", methods=["POST"])  # Allow POST requests for this endpoint
def analyze_sentiment():
    post_data = request.json

    first_item = post_data.get("session")  # Access the first item in the list
    if first_item.get("platform") == "reddit":
        NEW_POSTS = [
            {
                "id": "n4uq94",
                "url": "https://www.reddit.com/r/Mindfulness/comments/n4uq94/why_are_you_scrolling_are_you_aware_of_your/?utm_source=share&utm_medium=web3x&utm_name=web3xcss&utm_term=1&utm_content=share_button",
            }
        ]
    if first_item.get("platform") == "facebook":
        NEW_POSTS = [
            {
                "id": "pfbid02de23RA7aC2oNZsDQ1SjT1f2H6St4gi3fTQy37FS173CjGkpzXcShpBR1CKywcBnql",
                "url": "https://www.facebook.com/NAMI/posts/pfbid02de23RA7aC2oNZsDQ1SjT1f2H6St4gi3fTQy37FS173CjGkpzXcShpBR1CKywcBnql",
            }
        ]
    if first_item.get("platform") == "twitter":
        NEW_POSTS = [
            {
                "id": "1250894742285684737",
                "url": "https://twitter.com/NCHPAD/status/1250894742285684737",
            }
        ]
    # Add a new post (not part of the candidate set) to the top of the result
    wc = 0
    pc = 0
    ranked_ids = []
    for item in post_data.get("items"):
        id = item.get("id")
        type = item.get("type")
        if "text" in item:
            words = item["text"].split()
            wc += len(words)
        if "title" in item:
            words = item["title"].split()
            wc += len(words)
        if "Comment" in item:
            words = item["Comment"].split()
            wc += len(words)
        if type == "Post" or type == "tweet" or type == "Tweet" or type == "post":
            pc += 1
        ranked_ids.append(id)
        if wc >= 180 and pc >=2:
            ranked_ids.append(NEW_POSTS)
            wc=0
            pc=0

    result = {
        "ranked_ids": ranked_ids,
        "new_items": NEW_POSTS,
    }

    return jsonify(result)


if __name__ == "__main__":
    app.run(port=5001, debug=True)
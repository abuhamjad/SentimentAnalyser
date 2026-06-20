from flask import Flask, render_template, request
from textblob import TextBlob
import re
import os


app = Flask(__name__)

def load_words(filepath):
    with open(filepath, "r", encoding="utf-8") as file:
        return {
            line.strip().lower()
            for line in file
            if line.strip()
        }
    
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

POSITIVE_WORDS = load_words(
    os.path.join(BASE_DIR, "words", "positive_words.txt")
)

NEGATIVE_WORDS = load_words(
    os.path.join(BASE_DIR, "words", "negative_words.txt")
)

NEGATIONS = {
    "not",
    "no",
    "never",
    "n't",
    "hardly",
    "rarely",
    "without"
}

@app.route("/", methods=["GET", "POST"])
def home():

    result = None

    if request.method == "POST":

        text = request.form.get("text", "").strip()

        if text:

            blob = TextBlob(text)

            polarity = blob.sentiment.polarity
            subjectivity = blob.sentiment.subjectivity

            if polarity > 0.05:
                sentiment = "POSITIVE"
                color = "positive"

            elif polarity < -0.05:
                sentiment = "NEGATIVE"
                color = "negative"

            else:
                sentiment = "NEUTRAL"
                color = "neutral"

            confidence = round(abs(polarity) * 100)

            words = re.findall(r'\b\w+\b', text.lower())

            positive_hits = []
            negative_hits = []

            for i, word in enumerate(words):

                prev_word = words[i - 1] if i > 0 else ""

                if word in POSITIVE_WORDS:

                    if prev_word in NEGATIONS:
                        negative_hits.append(f"{prev_word} {word}")
                    else:
                        positive_hits.append(word)

                elif word in NEGATIVE_WORDS:

                    if prev_word in NEGATIONS:
                        positive_hits.append(f"{prev_word} {word}")
                    else:
                        negative_hits.append(word)

            result = {
                "text": text,
                "sentiment": sentiment,
                "color": color,
                "polarity": round(polarity, 3),
                "subjectivity": round(subjectivity, 3),
                "confidence": confidence,
                "tokens": len(words),
                "positive_count": len(positive_hits),
                "negative_count": len(negative_hits),
                "signals": positive_hits + negative_hits
            }

    return render_template(
        "index.html",
        result=result
    )


if __name__ == "__main__":
    app.run(debug=True)
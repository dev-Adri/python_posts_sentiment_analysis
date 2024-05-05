import json
import langdetect
from nltk.sentiment import SentimentIntensityAnalyzer
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from collections import defaultdict

lang_map = {
    "en": "english",
    "es": "spanish",
    "fr": "french",
    "sv": "swedish",
    "no": "norwegian",
    "pt": "portuguese",
    "it": "italian",
    "de": "german"
}

def calculate_sentiment(output_path="posts.json"):
    print("Starting sentiment analysis...")
    # Initialize sentiment analyzer
    sid = SentimentIntensityAnalyzer()
    # nltk.download('stopwords')
    # nltk.download('punkt')

    # JSON file
    json_file_path = output_path

    # Function to determine sentiment category
    def get_sentiment_category(sentiment_score):
        if sentiment_score >= 0.05:
            return "positive"
        elif sentiment_score <= -0.05:
            return "negative"
        else:
            return "neutral"

    # Dictionary to hold word counts by sentiment
    word_counts = defaultdict(lambda: defaultdict(int))

    # Analyze sentiment of each post
    with open(json_file_path, "r") as file:
        data = json.load(file)

        if "posts" in data and isinstance(data["posts"], list):
            updated_posts = []
            # Iterate over each post
            for post in data["posts"]:
                # Check if the post has a "text" key
                if "text" in post:
                    text = post["text"]
                    lan = ""

                    try:
                        lan = langdetect.detect(text)
                    except:
                        lan = "en"

                    if lan not in lang_map:
                        lan = "en"

                    stop_words = set(stopwords.words(lang_map[lan]))

                    sentiment_category = get_sentiment_category(sid.polarity_scores(text)["compound"])
                    updated_post = {
                        "text": text,
                        "sentiment": sentiment_category
                    }
                    updated_posts.append(updated_post)

                    # Tokenize and count words
                    words = word_tokenize(text.lower())
                    filtered_words = [word for word in words if word.isalnum() and word not in stop_words]
                    for word in filtered_words:
                        word_counts[sentiment_category][word] += 1

            data["posts"] = updated_posts
            data["word_counts"] = {k: dict(v) for k, v in word_counts.items()}

    # Update JSON file
    with open(json_file_path, "w") as file:
        json.dump(data, file, indent=4)

    print("Sentiment analysis completed.")
    print("JSON file updated successfully.")
import matplotlib.pyplot as plt
import json

from collections import Counter
from modules import scrapper, processor

def main():
    # get posts
    # scrapper.get_posts("posts.json")
    processor.calculate_sentiment("posts.json")

    with open("posts.json", "r") as file:
        data = json.load(file)
        posts = data["posts"]
        word_counts = data["word_counts"]

        # Counting the sentiments
        sentiment_counts = Counter(post['sentiment'] for post in posts)

        # Data for plotting sentiment distribution
        labels = sentiment_counts.keys()
        sizes = sentiment_counts.values()

        # Create subplots in a 2x2 layout
        _, ax = plt.subplots(2, 2, figsize=(12, 12))

        # Pie chart for sentiment distribution
        ax[0, 0].pie(sizes, labels=labels, autopct='%1.1f%%', startangle=140)
        ax[0, 0].set_title('Sentiment Distribution')
        ax[0, 0].axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.

        # Bar charts for top words per sentiment
        sentiments = ['negative', 'positive', 'neutral']
        for i, sentiment in enumerate(sentiments):
            if sentiment in word_counts:
                top_words = dict(Counter(word_counts[sentiment]).most_common(5))
                # Determine subplot position based on index
                if i == 0:
                    subplot = ax[0, 1]
                elif i == 1:
                    subplot = ax[1, 0]
                else:
                    subplot = ax[1, 1]
                    
                subplot.bar(top_words.keys(), top_words.values(), color=['purple', 'grey', 'orange', 'blue', 'green'])
                subplot.set_title(f'Top Words in {sentiment.capitalize()} Posts')
                subplot.set_ylabel('Frequency')
                subplot.set_xlabel('Words')

        plt.tight_layout()
        plt.subplots_adjust(hspace=0.25, wspace=0.13)
        plt.show()


if __name__ == "__main__":
    main()
    
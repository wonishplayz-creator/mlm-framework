"""
N‑Gram Text Generator - Training Script
Trains an n‑gram language model on corpus.txt and saves it to model.ptn
"""

import pickle
from collections import defaultdict, Counter


class NGramModel:
    def __init__(self, order=3):
        """
        Initialize n‑gram model.
        order: n‑gram size (2 = bigram, 3 = trigram, etc.)
        """
        self.order = order
        self.ngrams = defaultdict(Counter)
        self.start_states = []

    def train(self, text):
        """Train the n‑gram model on the provided text."""
        words = text.split()

        if len(words) < self.order + 1:
            print("Warning: Text too short for training")
            return

        for i in range(len(words) - self.order):
            state = tuple(words[i:i + self.order])
            next_word = words[i + self.order]

            # Count transitions
            self.ngrams[state][next_word] += 1

            # Track potential sentence starts
            if i == 0 or words[i][0].isupper():
                self.start_states.append(state)

        print(f"Training complete! Learned {len(self.ngrams)} states")
        print(f"Found {len(self.start_states)} potential sentence starts")

    def save(self, filename):
        """Save the trained model to a file."""
        model_data = {
            'order': self.order,
            'ngrams': {state: dict(counter) for state, counter in self.ngrams.items()},
            'start_states': self.start_states
        }
        with open(filename, 'wb') as f:
            pickle.dump(model_data, f)
        print(f"Model saved to {filename}")


def main():
        print("=" * 50)
        print("N‑Gram Text Generator - Training")
        print("=" * 50)

        # Read corpus
        print("\nReading corpus.txt...")
        try:
            with open('corpus.txt', 'r', encoding='utf-8') as f:
                corpus = f.read()
        except FileNotFoundError:
            print("Error: corpus.txt not found!")
            return

        print(f"Corpus loaded: {len(corpus)} characters, {len(corpus.split())} words")

        # Create and train model
        print("\nTraining n‑gram model...")
        model = NGramModel(order=3)  # trigram model
        model.train(corpus)

        # Save model
        print("\nSaving model...")
        model.save('model.ptn')

        print("\n" + "=" * 50)
        print("Training complete!")
        print("You can now run chat.py to interact with the model")
        print("=" * 50)


if __name__ == "__main__":
    main()
"""
Hybrid N‑Gram Chatbot with Bigger Tiny LLM‑Like Reasoning Brain
"""

import pickle
import random
import sys
import time
from collections import Counter


# ---------------------------------------------------------
# TINY "LLM-LIKE" REASONING BRAIN (UPGRADED)
# ---------------------------------------------------------
class TinyReasoner:

    def __init__(self):
        self.question_types = {
            "when": "time",
            "who": "person",
            "where": "location",
            "why": "reason",
            "how": "explanation",
            "what": "definition"
        }

        self.known_topics = {
            "eiffel tower": "the Eiffel Tower",
            "python": "the Python programming language",
            "ai": "artificial intelligence",
            "artificial intelligence": "artificial intelligence",
        }

    def analyze(self, text):
        words = text.lower().split()
        qtype = None

        for w in words:
            if w in self.question_types:
                qtype = self.question_types[w]
                break

        topic_raw = self.extract_topic(text)
        topic = self.normalize_topic(topic_raw)

        prefix = self.build_prefix(qtype, topic)

        return {
            "question_type": qtype,
            "topic_raw": topic_raw,
            "topic": topic,
            "prefix": prefix,
        }

    def extract_topic(self, text):
        text = text.lower()
        question_words = ["what", "why", "how", "who", "when", "where"]
        verbs = ["is", "are", "was", "were", "do", "does", "can"]

        words = text.split()
        if not words:
            return None

        q_index = next((i for i, w in enumerate(words) if w in question_words), None)
        if q_index is None:
            return text

        v_index = next(
            (i for i, w in enumerate(words[q_index + 1 :], start=q_index + 1) if w in verbs),
            None,
        )
        if v_index is None:
            return " ".join(words[q_index + 1 :]) or None

        topic_words = words[v_index + 1 :]
        if not topic_words:
            return None

        return " ".join(topic_words)

    def normalize_topic(self, topic_raw):
        if not topic_raw:
            return None
        t = topic_raw.lower()
        for key, canon in self.known_topics.items():
            if key in t:
                return canon
        return topic_raw

    def build_prefix(self, qtype, topic):
        if not topic:
            return None

        t_lower = topic.lower()
        if qtype == "time":
            if "eiffel tower" in t_lower:
                return "The Eiffel Tower was built in"
            return f"The {topic} was"

        if qtype == "definition":
            return f"{topic.capitalize()} is"

        if qtype == "person":
            return f"{topic.capitalize()} was"

        if qtype == "location":
            return f"{topic.capitalize()} is located in"

        if qtype == "reason":
            return f"The reason {topic} is"

        if qtype == "explanation":
            return f"{topic.capitalize()} works by"

        return None


# ---------------------------------------------------------
# N‑GRAM CHATBOT
# ---------------------------------------------------------
class NGramChatbot:

    def __init__(self, model_file):
        try:
            with open(model_file, "rb") as f:
                model_data = pickle.load(f)
                self.order = model_data["order"]
                self.ngrams = {
                    tuple(state): Counter(counts)
                    for state, counts in model_data["ngrams"].items()
                }
                self.start_states = [tuple(s) for s in model_data["start_states"]]

                self.reasoner = TinyReasoner()

                print(f"Model loaded successfully! ({len(self.ngrams)} states)")
        except FileNotFoundError:
            print(f"Error: {model_file} not found!")
            print("Please run train.py first to create the model.")
            sys.exit(1)

    # ---------------------------------------------------------
    # MOOD / CATEGORY DETECTION
    # ---------------------------------------------------------
    def detect_mood(self, text):
        text = text.lower()

        if any(w in text for w in ["hi", "hey", "yo", "sup", "hello"]):
            return "greeting"

        if any(w in text for w in ["ai", "machine learning", "neural", "artificial"]):
            return "ai"

        if any(w in text for w in ["math", "equation", "algebra"]):
            return "math"

        if any(w in text for w in ["python", "code", "programming"]):
            return "python"

        if any(w in text for w in ["fact", "random", "fun"]):
            return "facts"

        if any(w in text for w in ["bruh", "lmao", "fr", "ong"]):
            return "casual"

        # ADDED GRATITUDE MOOD
        if any(w in text for w in ["thank", "thanks", "thank you", "thx"]):
            return "gratitude"

        return "general"

    # ---------------------------------------------------------
    # CATEGORY → ALLOWED START STATES
    # ---------------------------------------------------------
    def category_states(self, category):
        categories = {
            "greeting": ["hi", "hey", "yo", "hello", "sup"],
            "ai": ["Artificial", "Machine", "Deep", "Neural", "AI"],
            "math": ["addition", "subtraction", "pi", "Pythagorean"],
            "python": ["python", "variables", "functions", "loops"],
            "facts": ["the", "octopuses", "bananas", "honey"],
            "casual": ["bruh", "lmao", "yo", "fr", "ong"],
            "gratitude": ["you're", "you’re"],  # Added for thank-you responses
            "general": [],
        }

        allowed = categories.get(category, [])

        if not allowed:
            return self.start_states

        filtered = [
            s for s in self.start_states
            if any(s[0].lower().startswith(a.lower()) for a in allowed)
        ]

        return filtered if filtered else self.start_states

    # ---------------------------------------------------------
    # WEIGHTED SAMPLING
    # ---------------------------------------------------------
    def weighted_choice(self, counter):
        words = list(counter.keys())
        weights = list(counter.values())
        return random.choices(words, weights=weights, k=1)[0]

    # ---------------------------------------------------------
    # TRY TO SEED WITH A PREFIX (LLM-LIKE GUIDANCE)
    # ---------------------------------------------------------
    def seed_with_prefix(self, prefix):
        if not prefix:
            return None, None

        words = prefix.split()
        if len(words) < self.order:
            return None, None

        for start in range(0, len(words) - self.order + 1):
            state = tuple(words[start : start + self.order])
            if state in self.ngrams:
                initial = words[: start + self.order]
                return initial, state

        return None, None

    # ---------------------------------------------------------
    # GENERATION WITH BIGGER REASONING BRAIN
    # ---------------------------------------------------------
    def generate_stream(self, max_words=50, seed=None, delay=0.04):
        analysis = self.reasoner.analyze(seed or "")
        qtype = analysis["question_type"]
        topic = analysis["topic"]
        prefix = analysis["prefix"]

        # Seed with reasoning prefix first
        initial_words, current_state = self.seed_with_prefix(prefix)

        if initial_words is None or current_state is None:
            # Fallback: use topic + category bias like before
            seed_for_mood = topic or (seed or "")
            category = self.detect_mood(seed_for_mood)
            allowed_states = self.category_states(category)

            if topic:
                allowed_states = [
                    s for s in allowed_states
                    if topic.lower() in " ".join(s).lower()
                ] or allowed_states

            preferred_starts = []
            if qtype == "time":
                preferred_starts = ["in", "during", "around", "the"]
            elif qtype == "person":
                preferred_starts = ["the", "a"]
            elif qtype == "location":
                preferred_starts = ["in", "at", "near"]

            if preferred_starts:
                allowed_states = [
                    s for s in allowed_states
                    if any(s[0].lower().startswith(p) for p in preferred_starts)
                ] or allowed_states

            current_state = random.choice(allowed_states)
            initial_words = list(current_state)

        result = list(initial_words)

        for w in result:
            yield w
            if w.endswith((".", "!", "?")):
                return

        for _ in range(max_words - len(result)):
            if current_state not in self.ngrams:
                return

            next_word = self.weighted_choice(self.ngrams[current_state])
            yield next_word

            if next_word.endswith((".", "!", "?")):
                return

            result.append(next_word)
            current_state = tuple(result[-self.order :])

    # ---------------------------------------------------------
    # CHAT LOOP
    # ---------------------------------------------------------
    def chat(self):
        print("\n" + "=" * 60)
        print("Hybrid N‑Gram Chatbot with Bigger Tiny LLM‑Like Brain")
        print("=" * 60)

        while True:
            user_input = input("\nYou: ").strip()

            if user_input.lower() in ["quit", "exit", "bye"]:
                print("\nBot: Goodbye!")
                break

            stream = self.generate_stream(max_words=60, seed=user_input)

            print("\nBot: ", end="", flush=True)
            for word in stream:
                for ch in word + " ":
                    print(ch, end="", flush=True)
                    time.sleep(0.01)
            print()


def main():
    bot = NGramChatbot("model.ptn")
    bot.chat()


if __name__ == "__main__":
    main()
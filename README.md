# MLM — Micro Language Model Framework
*A tiny hybrid AI architecture that behaves way smarter than it should.*

---

## 🚀 Overview
**MLM (Micro Language Model)** is a lightweight hybrid AI framework that combines:

- N‑gram statistical generation  
- Rule‑based reasoning  
- Intent & mood detection  
- Prefix conditioning  
- Category‑based start states  
- Emergent sentence recombination  

The result is a surprisingly capable offline chatbot that feels like a miniature LLM — complete with personality, improvisation, and context‑aware responses — all while running in milliseconds and using only a few kilobytes of model data.

MLM is designed to be:

- **Tiny**  
- **Fast**  
- **Explainable**  
- **Fun**  
- **Hackable**

---

## 🧠 How It Works
MLM uses a hybrid pipeline:
User Input ↓ Intent Detection (question type, gratitude, slang, mood) ↓ TinyReasoner (topic extraction + prefix generation) ↓ Category Selection (AI, math, casual, facts, etc.) ↓ N‑Gram Engine (statistical generation) ↓ Emergent Output (stitched, recombined, personality-driven)


### ✨ Key Features
- **Topic-aware answers**  
  Detects what the user is asking (time, definition, fact, etc.)

- **Gratitude detection**  
  Responds naturally to “thanks”, “thx”, “thank you”, etc.

- **Slang handling**  
  Understands messy inputs like:  
  *“when was that eiffel tower thingy built again”*

- **Prefix conditioning**  
  Guides the n‑gram model to start in the right style

- **Emergent generation**  
  Produces new sentences not directly in the corpus

- **Tiny footprint**  
  Model files are often under 100 KB

- **Offline**  
  No internet, no APIs, no dependencies

---

## 📦 Installation

Clone the repo:

```bash
git clone https://github.com/wonish-creator/mlm-framework
cd mlm-framework
---
Note from dev🥴

Remember, this is a FRAMEWORK not a full chatbot, while there is a small corpus included its just to show you how it works, you can chat with it by first running train.py to create and train the model, and then chat.py to chat.

To install the optional mchat and mtrain commands to quicly train/cht with it, simply move the mtrain.bat and mchat.bat into system32 so access the commands anywhere, I hope you have fun experimenting and make your own Chatbot!

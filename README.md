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

```bash
git clone https://github.com/wonish-creator/mlm-framework
cd mlm-framework
```
Note from dev 🥴
Remember, this is a framework, not a full chatbot.
While a small example corpus is included, it’s only there to show how the system works.
To try it out:
- Run train.py to create and train the model
- Run chat.py to chat with it
If you want quick global commands,
 move mtrain.bat and mchat.bat into your System32 folder so you can train/chat from anywhere.
Have fun experimenting and building your own chatbot!

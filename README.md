# ⚡ SparkFlow Studio

> **"Transform your imagination into reality in seconds."**

![Python](https://img.shields.io/badge/Python-3.12-blue?style=for-the-badge&logo=python)
![Streamlit](https://img.shields.io/badge/Streamlit-FF4B4B?style=for-the-badge&logo=streamlit)
![Fal.ai](https://img.shields.io/badge/Powered%20by-Fal.ai-purple?style=for-the-badge)
![License](https://img.shields.io/badge/License-MIT-green?style=for-the-badge)

## 🚀 Overview
**SparkFlow Studio** is not just another image generator; it's a real-time creative suite designed to minimize the friction between thought and visual execution. Built for the **Spark Fellowship** challenge, this application leverages the extreme speed of **Fal.ai's Flux Schnell** model to provide an "instant" generation experience.

Whether you are a concept artist, a storyteller, or a dreamer, SparkFlow provides the tools to visualize your ideas with professional control.

## ✨ Key Features

### 🧠 Smart Onboarding
Forget complex manuals. SparkFlow greets new users with an interactive **"Getting Started"** tour, explaining prompts, styles, and advanced controls in seconds.

### 🎨 Precision Control (Seed Locking)
Most AI tools are random. SparkFlow offers **Consistency Control**:
- **🎲 Random Mode:** For endless inspiration and brainstorming.
- **🔒 Lock Composition:** Found a perfect angle but want to change the lighting? Lock the seed and tweak the details without losing the image structure.

### 🕰️ Session History & Memory
Don't lose your best work. The built-in **Session Gallery** automatically saves every generation during your workflow, allowing you to compare iterations side-by-side.

### ⬇️ Professional Export
Need a quick share or a high-quality print?
- **Web Ready (JPG):** Optimized for social media sharing.
- **High-Res (PNG):** Lossless quality for professional use.

---

## 🛠️ Tech Stack

* **Frontend:** [Streamlit](https://streamlit.io/) (Custom CSS for modern UI)
* **AI Inference:** [Fal.ai](https://fal.ai/) (Flux/Schnell Model)
* **Image Processing:** Python Pillow (PIL)
* **State Management:** Streamlit Session State

---

## 💻 Installation & Setup

Want to run this studio locally? Follow these steps:

1.  **Clone the repository**
    ```bash
    git clone [https://github.com/saresarey/spark-flow.git](https://github.com/saresarey/spark-flow.git)
    cd spark-flow
    ```

2.  **Create a Virtual Environment**
    ```bash
    python -m venv venv
    # Windows:
    .\venv\Scripts\activate
    # Mac/Linux:
    source venv/bin/activate
    ```

3.  **Install Dependencies**
    ```bash
    pip install -r requirements.txt
    ```

4.  **Set API Key**
    Create a `.env` file in the root directory and add your Fal.ai key:
    ```env
    FAL_KEY=your_key_here
    ```

5.  **Run the App**
    ```bash
    streamlit run app.py
    ```

---

## 📸 Screenshots

| Onboarding | Generation Interface |
|:---:|:---:|
| *(Add screenshot here)* | *(Add screenshot here)* |

---

<p align="center">
  Developed with ❤️ for <strong>Spark Fellowship 2026</strong>
</p>
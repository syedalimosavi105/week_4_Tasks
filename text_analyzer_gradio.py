import gradio as gr
from collections import Counter
import string

def analyze_text(text: str):
    # safe-check
    if not text:
        return 0, 0, 0, 0, "No characters."

    total_chars = len(text)
    chars_no_spaces = len(text.replace(" ", "").replace("\t", "").replace("\n", ""))
    words = len(text.split())
    lines = text.count("\n") + 1 if text else 0

    # character frequency (printable, case-insensitive, skip whitespace)
    lowered = text.lower()
    allowed = set(string.printable)
    freq = Counter(ch for ch in lowered if ch in allowed and not ch.isspace())

    # small frequency table (top 12)
    top = freq.most_common(12)
    freq_lines = ["Char | Count", "---- | -----"]
    for ch, cnt in top:
        freq_lines.append(f"{repr(ch)} | {cnt}")
    freq_text = "\n".join(freq_lines) if top else "No characters."

    return total_chars, chars_no_spaces, words, lines, freq_text

title = "Text Analyzer — Character & Word Count"
desc = "Paste text and see total characters, characters without spaces, word/line count and top character frequencies."

iface = gr.Interface(
    fn=analyze_text,
    inputs=gr.Textbox(lines=8, placeholder="Paste or type text here..."),
    outputs=[
        gr.Number(label="Total characters (including spaces)"),
        gr.Number(label="Characters (no spaces)"),
        gr.Number(label="Word count"),
        gr.Number(label="Line count"),
        gr.Textbox(label="Top character frequencies (char | count)", lines=8)
    ],
    title=title,
    description=desc,
    flagging_mode=None,    # updated: use flagging_mode instead of deprecated allow_flagging
)

if __name__ == "__main__":
    # set share=True if you want a temporary public link (optional)
    iface.launch(share=False)
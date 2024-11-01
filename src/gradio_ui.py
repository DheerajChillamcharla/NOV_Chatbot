import gradio as gr
from rag_chain import rag

demo = gr.ChatInterface(
    rag,
    type="messages",
    title="NOV",
)

if __name__ == "__main__":
    demo.launch()

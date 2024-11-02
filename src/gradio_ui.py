import gradio as gr
from rag_chain import rag

demo = gr.ChatInterface(
    rag,
    type="messages",
    title="NOV",
    chatbot=gr.Chatbot(
        type="messages",
        placeholder="<strong>Hello there!</strong><br>I'm a product specialist at NOV. Would love to answer any questions you have about our products!",
        height=600,
    ),
    theme="soft",
    textbox=gr.Textbox(placeholder="Ask me a question", container=True),
)

if __name__ == "__main__":
    demo.launch()

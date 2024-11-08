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
    description='Data is sourced from NOV’s publicly available document library and website. All rights and '
                'acknowledgments belong to NOV.',
    theme="soft",
    textbox=gr.Textbox(placeholder="Ask me a question", container=True),
    examples=['Can you tell me the specs for Triplex Plunger Pump',
              'Tell me about recommended best practices for Coiled Tubing Purging',
              'Can you tell me about fishing jar systems?'],
)

if __name__ == "__main__":
    demo.launch()

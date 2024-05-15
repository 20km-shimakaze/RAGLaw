import gradio as gr

from chat import ChatLaw
import logging
import utils

utils.configure_logging(level=logging.INFO)

chat_law = ChatLaw()

def predict(input, history):
    logging.info(f'get msg: {input}\n {history}')
    response = chat_law.get_response(input, history)
    for chunk in response:
        yield chunk

def reset_user_input():
    return gr.update(value="")

def reset_state():
    chat_law.clean_history()
    return []

def main():
    # with gr.Blocks() as demo:
    #     gr.HTML("""<h1 align="center">RAGLaw</h1>""")
    #     chatbot = gr.Chatbot()
    #     with gr.Row():
    #             with gr.Column(scale=4):
    #                 with gr.Column(scale=50):
    #                     user_input = gr.Textbox(show_label=False, placeholder="Input...", lines=10)
    #                 with gr.Column(min_width=32, scale=1):
    #                     submitBtn = gr.Button("Submit", variant="primary")
    #             with gr.Column(scale=1):
    #                 emptyBtn = gr.Button("Clear History")
    #     submitBtn.click(
    #         predict,
    #         [user_input],
    #         [chatbot],
    #         show_progress=True
    #     )
    #     submitBtn.click(reset_user_input, [], [user_input])
    #     emptyBtn.click(reset_state, outputs=[chatbot], show_progress=True)

    # demo.launch(share=False, server_name="0.0.0.0")
    gr.ChatInterface(predict).launch(server_name="0.0.0.0")

if __name__ == '__main__':
    main()

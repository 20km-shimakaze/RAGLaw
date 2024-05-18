import gradio as gr

from chat import ChatLaw
import logging
import utils
import time

utils.configure_logging(level=logging.INFO)

chat_law = ChatLaw()

# def predict(input, history):
#     logging.info(f'get msg: {input}\n {history}')
#     response = chat_law.get_response(input, history)
#     for chunk in response:
#         yield chunk

def undo(msg, history: list):
    history.pop()
    return "", history


def predict(msg, history: list, law_nums, temperature):
    logging.info(f"law: {law_nums}, temperature: {temperature} type: {type(law_nums), type(temperature)}")
    logging.info(f"history: {history}")
    # response = "hello today is fine"
    response = chat_law.get_response(msg, history, law_nums, temperature)
    history.append([msg, ""])

    for chunk in response:
        # logging.info(chunk)
        # time.sleep(0.3)
        history[-1][1] = chunk
        yield "", history
    

def main():
    with gr.Blocks() as demo:
        with gr.Column():
            chatbot = gr.Chatbot()
            msg = gr.Textbox()
            with gr.Accordion("See Details"):
                law_nums = gr.Slider(minimum=0, maximum=10, step=1, value=3, label="查询law数量")
                temperature = gr.Slider(minimum=0., maximum=2., value=0.7, label="温度")
            with gr.Row():
                undo_btn = gr.Button(value="↩️ Undo")
                clear_btn = gr.ClearButton([msg, chatbot], value="🗑️  Clear")
                submit_Btn = gr.Button(value="📮 submit", variant="primary")
        submit_Btn.click(
            predict,
            inputs=[msg, chatbot, law_nums, temperature],
            outputs=[msg, chatbot]
        )
        undo_btn.click(
            undo,
            inputs=[msg, chatbot],
            outputs=[msg, chatbot]
        )
                
    demo.launch(server_name='0.0.0.0')


if __name__ == '__main__':
    main()

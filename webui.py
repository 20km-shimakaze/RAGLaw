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


def predict(msg, history: list, law_nums, temperature, search_law):
    logging.info(f"law: {law_nums}, temperature: {temperature} type: {type(law_nums), type(temperature)}")
    logging.info(f"history: {history}")
    # response = "hello today is fine"
    response = chat_law.get_response(msg, history, law_nums, temperature, search_law)
    history.append([msg, ""])

    for chunk in response:
        # logging.info(chunk)
        # time.sleep(0.3)
        history[-1][1] = chunk
        yield "", history
    
markdown = """
# 法律咨询工具
"""

def main():
    with gr.Blocks() as demo:
        with gr.Column():
            gr.Markdown(markdown)
            chatbot = gr.Chatbot()
            msg = gr.Textbox(info="输入框")
            with gr.Accordion("参数调节"):
                search_law = gr.Radio(["True", "False"], value="True", label="查找法律条文", info="在提问时查找法律条文选择True,否则选择False")
                law_nums = gr.Slider(minimum=0, maximum=10, step=1, value=3, label="查询law数量")
                temperature = gr.Slider(minimum=0., maximum=2., value=0.7, label="温度", info="温度越高，回答灵活性越高")
            with gr.Row():
                undo_btn = gr.Button(value="↩️ Undo")
                clear_btn = gr.ClearButton([msg, chatbot], value="🗑️  Clear")
                submit_Btn = gr.Button(value="📮 Submit", variant="primary")
        gr.Examples(
            ["我在餐馆吃到了有毒食物，餐馆需要负什么责任", "离婚彩礼怎么算", "盗窃罪如何判"],
            inputs=msg,
        )
        submit_Btn.click(
            predict,
            inputs=[msg, chatbot, law_nums, temperature, search_law],
            outputs=[msg, chatbot]
        )
        undo_btn.click(
            undo,
            inputs=[msg, chatbot],
            outputs=[msg, chatbot]
        )
                
    demo.launch(server_name='0.0.0.0', share=True)


if __name__ == '__main__':
    main()

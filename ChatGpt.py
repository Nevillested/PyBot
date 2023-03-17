import openai
import my_cfg

def get_result_from_chatgpt(msg_in):
    openai.api_key = my_cfg.chat_gpt_token
    model_engine = my_cfg.chat_gpt_model
    prompt = msg_in
    completion = openai.Completion.create(
        engine=model_engine,
        prompt=prompt,
        max_tokens=1024,
        n=1,
        stop=None,
        temperature=0.5,
    )
    msg_out = completion.choices[0].text
    return msg_out
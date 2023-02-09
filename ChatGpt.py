import openai

def get_result_from_chatgpt(msg_in):
    openai.api_key = "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"
    model_engine = "text-davinci-003"
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
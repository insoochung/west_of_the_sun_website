""" Based on: https://platform.openai.com/docs/guides/chat/introduction """

import os
import openai  # venv에 pip install openai로 설치

# key: https://platform.openai.com/account/api-keys 여기서
# key file은 항상 books/ 디렉터리에 만들어 넣기 - books/.openaikey
openai.api_key_path = f"{os.path.dirname(__file__) }/.openaikey"


# def call_gpt_write_chapter(chapter, model):
#     pass

def call_gpt(system_prompt,
             conv_init_role,
             dialog,
             model="gpt-3.5-turbo"):
    """ Call GPT
    Args:
        - system_prompt: sets the tone for the system
        - conv_init_role: who starts the convo - either "assistant" or "user"
        - dialog: dialog initiated by conv_init_role, list of strings
        - model: GPT model name to call
    """
    if conv_init_role not in ["user", "assistant"]:
        raise RuntimeError(
            f"conv_init_role cannot be {conv_init_role}, use user or assistant")

    messages = []
    messages.append({"role": "system", "content": system_prompt})
    role = conv_init_role
    for sentence in dialog:
        messages.append({"role": role, "content": sentence})
        if role == "user":
            role = "assistant"
        else:
            role = "user"

    ret = openai.ChatCompletion.create(
        model=model,
        messages=messages
    )
    return ret


if __name__ == "__main__":
    call_gpt()
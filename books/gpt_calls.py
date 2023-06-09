""" Based on: https://platform.openai.com/docs/guides/chat/introduction """
import os
import openai  # venv에 pip install openai로 설치

# key: https://platform.openai.com/account/api-keys 여기서
# key file은 항상 books/ 디렉터리에 만들어 넣기 - books/.openaikey
openai.api_key_path = f"{os.path.dirname(__file__) }/.openaikey"


def call_gpt_write_chapter(user, book, chapter):
    chapter.created_by = user
    chapter.book = book
    chapter.content = call_gpt(system_prompt=book.meta_prompt, # Same meta prompt as book's is given
                               conv_init_role="user",
                               dialog=[chapter.chapter_prompt], # User query 1
                               model=chapter.gpt_name,
                               message_only=True) # Assistant answer 1
    if chapter.revise_prompt:
        chapter.revised_content = call_gpt(system_prompt=book.meta_prompt, # Same meta prompt as book's is given
                                           conv_init_role="user",
                                           dialog=[chapter.chapter_prompt, # User query 1
                                                   chapter.content, # Assistant answer 1
                                                   chapter.revise_prompt], # User query 2
                                           model=chapter.gpt_name,
                                           message_only=True)

    return chapter

def call_gpt_write_book(user, book):
    book.created_by = user
    book.description = call_gpt(system_prompt=book.meta_prompt, # Meta prompt given as context
                                conv_init_role="user",
                                dialog=[book.initial_prompt], # User query 1
                                model=book.gpt_name,
                                message_only=True) # Assistant answer 1
    if book.outline_prompt:
        book.outline = call_gpt(system_prompt=book.meta_prompt, # Meta prompt given as context
                                conv_init_role="user",
                                dialog=[book.initial_prompt, # User query 1
                                        book.description, # Assistant answer 1
                                        book.outline_prompt], # User query 2
                                model=book.gpt_name,
                                message_only=True) # Result: Assistant answer 2
    else:
        book.outline = ""

    return book

def call_gpt(system_prompt,
             conv_init_role,
             dialog,
             model="gpt-3.5-turbo",
             message_only=False):
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
        messages=messages,
        temperature=0, # For reproducibility
    )
    if message_only:
        return ret["choices"][0]["message"]["content"]
    return ret


if __name__ == "__main__":
    call_gpt()

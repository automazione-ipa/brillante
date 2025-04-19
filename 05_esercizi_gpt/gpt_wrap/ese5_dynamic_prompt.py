from gpt_wrap import chat_with_openai
from prompts import zero_shot_prompt, few_shot_prompt, cot_prompt, role_expert_prompt  # Import prompts


def run_prompt(prompt_name, user_message):
    prompts = {
        "ese1": zero_shot_prompt,
        "ese2": few_shot_prompt,
        "ese3": cot_prompt,
        "ese4": role_expert_prompt
    }

    if prompt_name not in prompts:
        raise ValueError("Invalid prompt name. Choose from: ese1, ese2, ese3, ese4.")

    return chat_with_openai(
        user_message=prompts[prompt_name] + "\n" + user_message,
        system_message='You are a helpful assistant.',
        temperature=0.5
    )


try:
    prompt_name = 'ese1'  # Change this to test other prompts (ese2, ese3, etc.)
    user_message = 'Tell me about the capital of Japan.'
    reply = run_prompt(prompt_name, user_message)
    print(reply)
except Exception as e:
    print(str(e))

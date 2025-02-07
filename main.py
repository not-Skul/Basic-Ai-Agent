from openai import OpenAI
from actions import get_response_time
from prompts import system_prompt
from json_helpers import extract_json
import os
from dotenv import load_dotenv
load_dotenv()
api= os.getenv("GEMINI_API_KEY")

client = OpenAI(
        api_key=api,
        base_url="https://generativelanguage.googleapis.com/v1beta/openai/"
    )


def generate_text_with_conversation(message_list):
    response = client.chat.completions.create(
        model="gemini-1.5-flash",
        n=1,
        messages=message_list
    )

    return response.choices[0].message.content


#Available actions are:
available_actions = {
    "get_response_time": get_response_time
}

user_prompt = "what is the response time of dtox.vercel.app?"

messages = [
    {"role": "system", "content": system_prompt},
    {"role": "user", "content": user_prompt},
]

turn_count = 1
max_turns = 5


while turn_count < max_turns:
    print (f"Loop: {turn_count}")
    print("----------------------")
    turn_count += 1

    response = generate_text_with_conversation(messages)

    print(response)

    json_function = extract_json(response)

    if json_function:
            function_name = json_function[0]['function_name']
            function_params = json_function[0]['function_parms']
            if function_name not in available_actions:
                raise Exception(f"Unknown action: {function_name}: {function_params}")
            print(f" -- running {function_name} {function_params}")
            action_function = available_actions[function_name]
            #call the function
            result = action_function(**function_params)
            function_result_message = f"Action_Response: {result}"
            messages.append({"role": "user", "content": function_result_message})
            print(function_result_message)
    else:
         break

import os
import json
import sys
from dotenv import load_dotenv
from openai import OpenAI
from config import MAX_ITERS
import argparse
from prompts import system_prompt
from call_function import available_functions, call_function


def main():
    load_dotenv()
    api_key = os.environ.get("OPENROUTER_API_KEY")
    if api_key is None:
        raise RuntimeError("No API key found")
    client = OpenAI(
        base_url="https://openrouter.ai/api/v1",
        api_key=api_key,
    )
    #Gets the users prompt
    parser = argparse.ArgumentParser(description="Chatbot")
    parser.add_argument("user_prompt", type=str, help="User prompt")
    parser.add_argument("--verbose", action="store_true", help="Enable verbose output")
    args = parser.parse_args()  

    #initializes the list of messages
    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": args.user_prompt},
    ]

    for _ in range(MAX_ITERS):
        final_response = generate_content(client, messages, args)
        if final_response:
            print("Final response:")
            print(final_response)
            return(final_response)
        
    print(f"Maximum iterations ({MAX_ITERS}) reached")
    sys.exit(1)


   
def generate_content(client: OpenAI, messages: list, args: bool) -> str | None:
    
        #Asks the model for a response
        response = client.chat.completions.create(
            model="openrouter/free",
            messages=messages,
            tools=available_functions,
        )
        if response.usage is None:
            raise RuntimeError("No response received")
        #Handles the response
        message = response.choices[0].message
        messages.append(message)
        if message.tool_calls:
            for tool_call in message.tool_calls:
                tool_message = call_function(tool_call,args.verbose)
                if not tool_message["content"]:
                    raise Exception("tool content was empty")
                if args.verbose is True:
                    print(f"-> {tool_message['content']}")
                messages.append(tool_message)
        else:
            return(message.content)


if __name__ == "__main__":
    main()

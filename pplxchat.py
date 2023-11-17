import os
import json
import requests
import sys
import readline

# Constants
URL = "https://api.perplexity.ai/chat/completions"
HEADERS = {
    "accept": "text/event-stream",
    "content-type": "application/json",
    "authorization": f"Bearer {os.getenv('PERPLEXITY_API_KEY')}"
}

def get_input(prompt):
    try:
        # Use readline for input (for TTY)
        return input(prompt)
    except EOFError:
        return None

def stream_request(messages):
    last_printed = ""  # Variable to keep track of the last printed message
    payload = {
        "model": "pplx-70b-chat-alpha",
        "messages": messages,
        "stream": True
    }

    with requests.post(URL, headers=HEADERS, json=payload, stream=True) as response:
        response.raise_for_status()
        sys.stdout.write("Assistant: ")
        for line in response.iter_lines():
            if line:
                decoded_line = line.decode('utf-8').replace('data: ', '')
                try:
                    data = json.loads(decoded_line)
                    current_content = data['choices'][0]['message']['content']
                    if current_content != last_printed:  # Update only if there is new content
                        new_content = current_content[len(last_printed):]
                        if new_content:  # Only update if new content is not empty
                            sys.stdout.write(new_content)
                            sys.stdout.flush()  # Flush the buffer to immediately print the new content
                        last_printed = current_content
                except json.JSONDecodeError:
                    continue
        print()  # Print a new line after full response is received

def main():
    print("Perplexity Chat Bot")
    print("-------------------")
    print("Type 'exit' to end the chat.")

    while True:
        user_input = get_input("You: ")
        if user_input is None or user_input.lower().strip() == 'exit':
            print("Goodbye!")
            break


        messages = [
            {
                "role": "system",
                "content": "Be precise and concise."
            },
            {
                "role": "user",
                "content": user_input
            }
        ]

        stream_request(messages)

if __name__ == "__main__":
    main()

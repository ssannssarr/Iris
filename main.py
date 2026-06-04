import os
import sys
import json
import subprocess
import requests
from router import ask_ai,SYSTEM_PROMPT
from ui.rui import pnl,cp,rule,prompt





def main():
    # Check API key
    api_key = os.environ.get("OPENROUTER_API_KEY")
    if not api_key:
        print("Error: OPENROUTER_API_KEY environment variable not set.", file=sys.stderr)
        sys.exit(1)

    pnl("Assistant ready. Type 'exit' to quit.\n")

    while True:
        try:
            user_input = prompt()
        except (EOFError, KeyboardInterrupt):
            pnl("Goodbye!")
            break

        if not user_input:
            continue
        if user_input.lower() == "exit":
            print("Goodbye!")
            break

        # Build message list
        messages = [
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": user_input}
        ]

        try:
            # First call – AI may request the battery tool
            response = ask_ai(messages, api_key, tools=TOOLS)
            assistant_msg = response["choices"][0]["message"]

            # If the model wants to use a tool
            if assistant_msg.get("tool_calls"):
                tool_call = assistant_msg["tool_calls"][0]
                func_name = tool_call["function"]["name"]

                if func_name == "get_battery_status":
                    try:
                        battery_data = get_battery_status()
                    except RuntimeError as e:
                        battery_data = {"error": str(e)}

                    # Append the assistant's tool request and the tool result
                    messages.append(assistant_msg)  # assistant message with tool_calls
                    messages.append({
                        "role": "tool",
                        "tool_call_id": tool_call["id"],
                        "content": json.dumps(battery_data)
                    })

                    # Second call – get the final spoken answer
                    response2 = ask_ai(messages, api_key, tools=None)
                    final_msg = response2["choices"][0]["message"]["content"]
                else:
                    final_msg = assistant_msg.get("content", "I didn't understand that.")
            else:
                # No tool used – straight answer
                final_msg = assistant_msg.get("content", "I didn't understand that.")

            print(f"Assistant: {final_msg}")
            speak(final_msg)

        except requests.RequestException as e:
            print(f"Network/API error: {e}", file=sys.stderr)
            speak("Sorry, I couldn't reach the AI service.")
        except KeyError:
            print("Unexpected API response format.", file=sys.stderr)
            speak("Something went wrong with the response.")
        except Exception as e:
            print(f"Unexpected error: {e}", file=sys.stderr)
            speak("Sorry, an error occurred.")

if __name__ == "__main__":
    main()

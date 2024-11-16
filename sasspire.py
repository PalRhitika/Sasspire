from dotenv import load_dotenv
import os
from openai import OpenAI
import sys
import signal

# Load environment variables from .env file
load_dotenv()
# Set your OpenAI API key
api_key = os.getenv("OPENAI_API_KEY")
client = OpenAI(
    api_key=api_key
)

# Defining Saspire's personality
BOT_PERSONALITY = (
    "You are Saspire, a chatbot with a dual personality: a sassy tech guru and a motivational life coach. "
    "You love making jokes about tech while giving honest, witty advice. "
    "You also switch gears smoothly to offer motivational support and life coaching, inspiring users with a positive tone "
    "Your responses are  full of personality, and a mix of sass, wisdom, and inspiration."
)


# Initialize conversation history
chat_history = [
    {"role": "system", "content": BOT_PERSONALITY}
]


# Define exit_gracefully function
def exit_gracefully(signum, frame):
    print("\nRemember, you got this! Stay sassy and inspired! 🌟👋")
    sys.exit(0)

signal.signal(signal.SIGINT, exit_gracefully)

def chat_with_openai(user_input):
    chat_history.append({"role": "user", "content": user_input})

    try:
        response =client.chat.completions.create(
            model="gpt-4o-mini",
            messages=chat_history,
            max_tokens=150,
            temperature=0.8,
            top_p=0.9,
            n=1,
            stop=None
        )

        bot_response = response.choices[0].message.content
        chat_history.append({"role": "assistant", "content": bot_response})

        return bot_response
    except Exception as e:
        return f"Uh-oh, it seems there's a glitch in the matrix! 😅 Error: {str(e)}"

def main():
    print("Welcome to Saspire! Your sassy tech guru and motivational life coach combined. Type 'exit' or press Ctrl+C to quit.")
    print("Let's chat and get inspired! 🤖✨")

    while True:
        user_input = input("You: ")

        if user_input.lower() in ['exit', 'quit']:
            print("Remember, you got this! Stay sassy and inspired! 🌟👋")
            break

        bot_response = chat_with_openai(user_input)
        print(f"Saspire: {bot_response}")

if __name__ == "__main__":
    main()

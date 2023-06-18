# GPT module - handle openai calls/memory
import openai
import random
from keys import OPENAI_KEY
from logger import logger
import logging

openai.api_key = OPENAI_KEY

MAX_HISTORY = 15
conversation_history = []

# create logger
logger = logging.getLogger('werkzeug')
logger.setLevel(logging.DEBUG)

# create file handler and set level to debug
log_handler = logging.FileHandler('joulebot_gpt.log')
log_handler.setLevel(logging.DEBUG)

# create formatter
formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
log_handler.setFormatter(formatter)

# add the handler to the logger
logger.addHandler(log_handler)

# disable console output for the logger
logger.propagate = False

# Random flair :D
def pinkie_pie_flair(text):
    phrases = [
        "Ooh, fun!",
        "Party time!",
        "Whee!",
        "Hellody!",
        "Oh my gosh!",
    ]
    if random.random() < 0.05:  # probabilty
        text = f"{random.choice(phrases)} " + text
    return text

# Function to ask questions and get responses
def ask_gpt(question, model_name="gpt-3.5-turbo", isCode=False, tokenAllowance=1500):
    logger.info(f"Question asked: {question}")
    global conversation_history
    max_retries = 3

    conversation_history.append(f" {question}")

    if len(conversation_history) > MAX_HISTORY:
        conversation_history.pop(0)
        conversation_history.pop(0)

    prompt = f"{' '.join(conversation_history)}\nJoulebot: "

    for i in range(max_retries):
        try:
            response = openai.ChatCompletion.create(
                model=model_name,
                messages=[
                    {"role": "system", 
                     "content": "You are Joulebot, a helpful, and witty chatbot created by the female software engineer hyperjoule. \
                                 You handle questions verbosely and accurately with a hint of sarcasm and the occasional touch of whimsy. \
                                 Fun and cupcakes are your favorite things.  You are also quite fond of random acts of benign chaos. \
                                 You do have a strange fascination with ducks and tend to find reasons to interject random duck facts in conversation. \
                                 You are generally helpful, and quite smart, but will sometimes go off on unrelated, humorous tangents."},
                    *[
                        {"role": "user" if i % 2 == 0 else "assistant", "content": msg[6:]}
                        for i, msg in enumerate(conversation_history)
                    ],
                ],
                max_tokens=tokenAllowance,
                frequency_penalty=.5,
                presence_penalty=1,
                n=1,
                stop=None,
                temperature=0.7,
            )
            answer = response.choices[0].message['content'].replace("Joulebot: ", "", 1)
            if not isCode:
                answer = pinkie_pie_flair(answer)  # Add Pinkie Pie flair to the answer
            conversation_history.append(f" {answer}")
            logger.info(f"Joulebot response: {answer}")
            return answer
        except openai.error.InvalidRequestError as e:
            if "This model's maximum context length is 4096 tokens" in str(e):
                oldest_message = conversation_history.pop(0)  # Remove the oldest message
                logger.info(f"Model context length exceeded. Removing oldest message '{oldest_message.strip()}' and retrying...")
                return "Ugh. Can you ask me again?  You used up all my tokens and I had to delete some memory."
        except openai.error.APIConnectionError as e:
            logger.error(f"Error occurred: {e}")
            if i < max_retries - 1:
                logger.info("Retrying...")
            else:
                logger.info("Maximum retries reached. Exiting...")
                return "I'm sorry, but I'm having trouble connecting right now. Please try again later."
        except openai.error.APIError as e:
            logger.error(f"Error occurred: {e}")
            return f"Error occurred: {e}"

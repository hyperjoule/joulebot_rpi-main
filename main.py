# Main joulebot script for use on RPI - hyperjoule 2023
from gpt import ask_gpt
from flask_app import app
from werkzeug.serving import make_server
import threading
from logger import logger
import sys
import time

# Quit flag
termination_status = {'should_terminate': False}

# Suppress flask messages
cli = sys.modules['flask.cli']
cli.show_server_banner = lambda *x: None

def main(termination_status):
    print("Type 'quit' to exit the program.")
    while not termination_status['should_terminate']:
        user_question = input("Ask Joulebot a Question: ")
        if user_question.lower() == "quit":
            termination_status['should_terminate'] = True
            break
        gpt_response = ask_gpt(user_question)
        print(f"Joulebot: {gpt_response}")

def run_flask_app(server, termination_status):
    # Run the Flask app in a try-except block
    try:
        server.serve_forever()
    except Exception as e:
        print(f"Flask app encountered an error: {e}")
        logger.error(f"Flask app encountered an error: {e}")
    termination_status['should_terminate'] = True
    main_thread.join(0)  # Non-blocking join to stop the main thread

if __name__ == "__main__":
    # Create a server object with the Flask app
    server = make_server('0.0.0.0', 5000, app)
    
    flask_thread = threading.Thread(target=run_flask_app, args=(server, termination_status))
    flask_thread.start()
    main_thread = threading.Thread(target=main, args=(termination_status,))
    main_thread.start()

    main_thread.join()

    # Wait for a moment to ensure the Flask app has enough time to shut down
    time.sleep(1)

    # Shut down the Flask server
    server.shutdown()
    flask_thread.join()

    sys.exit(0)

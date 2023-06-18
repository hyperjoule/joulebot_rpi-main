from flask import Flask, request, render_template_string, jsonify
from gpt import ask_gpt
from keys import OPENAI_KEY
import requests

app = Flask(__name__)

@app.route('/')
def index():
    return render_template_string(open("templates/index.html").read())

@app.route('/ask', methods=['POST'])
def ask():
    user_question = request.form.get('question')
    if user_question:
        gpt_response = ask_gpt(user_question)
        return jsonify({'answer': gpt_response})
    return 'No question provided.', 400

@app.route('/dalle', methods=['POST'])
def generate_image():
    user_question = request.json.get('question')
    if user_question:
        response = requests.post('https://api.openai.com/v1/images/generations', json={
            'model': 'image-alpha-001',
            'prompt': user_question[5:], # remove the "draw" prefix from the user question
            'num_images': 1,
            'size': '512x512',
            'response_format': 'url'
        }, headers={
            'Authorization': f'Bearer {OPENAI_KEY}'
        })
        if response.ok:
            image_url = response.json()['data'][0]['url']
            return {'image_url': image_url}
    return 'Error generating image.', 400
   
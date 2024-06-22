from flask import Flask, request, jsonify
from flask_cors import CORS
from langchain.chains import ConversationChain
from langchain.llms import OpenAI  # Correct import for OpenAI LLM

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

def read_text_file(file_path):
    with open(file_path, 'r') as file:
        content = file.read()
    return content

# Load mental health advice from the text file
text_file_path = 'data/mental_health_advice.txt'
mental_health_advice = read_text_file(text_file_path)

# Truncate the mental health advice to a reasonable length
max_advice_length = 1000  # Adjust this value based on your needs
truncated_advice = mental_health_advice[:max_advice_length]

# Initialize LangChain components
llm = OpenAI(api_key='put key here')  # Replace with your OpenAI API key
conversation = ConversationChain(llm=llm)

@app.route('/chat', methods=['POST'])
def chat():
    user_message = request.json.get('message')
    if not user_message:
        return jsonify({'error': 'No message provided'}), 400
    
    # Combine user_message and truncated_advice into a single input
    combined_input = f"{truncated_advice}\n\nUser: {user_message}"
    
    # Generate response using LangChain
    response = conversation.run(input=combined_input)
    
    return jsonify({'response': response})

if __name__ == '__main__':
    app.run(debug=True)

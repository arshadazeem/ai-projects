from transformers import BlenderbotTokenizer
from transformers import pipeline

# Load the tokenizer for the Blenderbot model and set the chat template
tokenizer = BlenderbotTokenizer.from_pretrained("facebook/blenderbot-400M-distill")
tokenizer.chat_template = [
    {"role": "user", "content": ""},
    {"role": "bot", "content": "You are a friendly chatbot who always responds in the style of a soccer coach"}
]

# Load the pre-trained conversational model from huggingface
chatbot = pipeline(model="facebook/blenderbot-400M-distill", task="conversational", tokenizer=tokenizer)

# Start the conversation
print("Chatbot: Hi! I am your AI assistant using facebook/blenderbot-400M-distill. Type 'exit' to stop.")

while True:
    user_input = input("You: ")
    if user_input.lower() == "exit":
        print("Chatbot: Goodbye!")
        break
    response = chatbot(user_input)
    print(f"Chatbot: {response[0]['generated_text']}")



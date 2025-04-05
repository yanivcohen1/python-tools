import os
import base64
from langchain_ollama.llms import OllamaLLM
from langchain_core.prompts import ChatPromptTemplate
from langchain.schema.messages import HumanMessage, AIMessage, SystemMessage

# Read your local image and base64 encode it
def encode_image_to_base64(image_path):
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode("utf-8")


current_path = os.path.dirname(os.path.abspath(__file__))
images_path = current_path + "/../content/images/"

image_name = "cube.png" # "transparency_demonstration.png"# "smail_face.png"#  # "objectdetection.png"
model_name = "gemma3:4b" # "llava:7b" #
image_url = images_path + image_name
image_base64 = encode_image_to_base64(image_url)

# Use Ollama with llava
model = OllamaLLM(model=model_name, temperature=0.8) #  phi4-mini:3.8b

chat_history = ""
while True:
    print("\n\n-------------------------------")
    question = input("Ask your question (q to quit): ")
    if question == "":
        question = "What is in this image?  answer in few sentences"
    print("\n")
    if question == "q":
        break
    # Set up the message with image and text prompt
    messages = [
        HumanMessage(
            content=[
                {"type": "text", "text": question},
                {"type": "text", "text": "Previous conversation: " + chat_history},
                {"type": "image_url", "image_url": {"url": f"data:image/png;base64,{image_base64}"}} # image_url}
            ]
        )
    ]
    for chunk in model.stream(messages): # {"reviews": reviews, "question": question, "chat_history": chat_history}):
        if chunk is not None:
            msg = chunk
            # chat_history += msg
            print(msg, end="")
    chat_history += question

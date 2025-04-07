import os
import base64
from langchain_ollama.llms import OllamaLLM
from langchain_core.prompts import ChatPromptTemplate
from langchain.schema.messages import HumanMessage, AIMessage, SystemMessage

# Read your local image and base64 encode it
import base64
from io import BytesIO
from PIL import Image


def convert_to_base64(pil_image):
    """
    Convert PIL images to Base64 encoded strings

    :param pil_image: PIL image
    :return: Re-sized Base64 string
    """

    buffered = BytesIO()
    pil_image.save(buffered, format="JPEG")  # You can change the format if needed
    img_str = base64.b64encode(buffered.getvalue()).decode("utf-8")
    return img_str


current_path = os.path.dirname(os.path.abspath(__file__))
images_path = os.path.abspath(current_path + "/../content/images/")

# image_name = "pic1.jpg" # "transparency_demonstration.png"# "smail_face.png"#  # "objectdetection.png"
model_name = "gemma3:4b" # "gemma3:4b" # "llava:7b" #

# Use Ollama with llava
model = OllamaLLM(model=model_name, temperature=0.8) #  phi4-mini:3.8b

chat_history = ""
while True:
    print("\n\n-------------------------------")
    pic_name = input("pic name (q to quit): ")
    if pic_name == "": pic_name = "pet.jpg"
    if pic_name == "q": break
    question = input("Ask your question (q to quit): ")
    if question == "": question = "What is in this picture?"  # answer in few sentences"
    if question == "q": break
    print("\n")
    image_url = f'{images_path}\\{pic_name}'
    pil_image = Image.open(image_url)
    image_b64 = convert_to_base64(pil_image)
    llm_with_image_context = model.bind(images=[image_b64])
    # Set up the message with image and text prompt
    messages = [
        HumanMessage(
            content=[
                {"type": "text", "text": question}, # question},
                # {"type": "image_url", "image_url": {"url": f"data:image/png;base64,{image_base64}"}}, # image_url}
                {"type": "text", "text": "Previous conversation: " + chat_history}
            ]
        )
    ]
    for chunk in llm_with_image_context.stream(messages): # {"reviews": reviews, "question": question, "chat_history": chat_history}):
        if chunk is not None:
            msg = chunk
            # chat_history += msg
            print(msg, end="")
    chat_history += question

import os
import base64
from io import BytesIO
from langchain_ollama.llms import OllamaLLM
from langchain_core.prompts import ChatPromptTemplate
from langchain.schema.messages import HumanMessage, AIMessage, SystemMessage
from PIL import Image


def convert_to_base64(pil_image):
    buffered = BytesIO()
    pil_image.save(buffered, format="JPEG")  # You can change the format if needed
    img_str = base64.b64encode(buffered.getvalue()).decode("utf-8")
    return img_str


current_path = os.path.dirname(os.path.abspath(__file__))
images_path = os.path.abspath(current_path + "/../content/images/")
model_name = "gemma3:4b"  # "gemma3:4b" # "llava:7b" #
model = OllamaLLM(model=model_name, temperature=0.8)  #  phi4-mini:3.8b

chat_history = ""
while True:
    print("\n\n-------------------------------")
    pic_name = input("pic name (q to quit): ")
    if pic_name == "q":
        break
    question = input("Ask your question (q to quit): ")
    if question == "q":
        break
    if pic_name == "":  # pic_name = "cow.jpg"
        llm_with_image_context = model
    else:
        image_url = os.path.abspath(f"{images_path}/{pic_name}")
        pil_image = Image.open(image_url)
        image_b64 = convert_to_base64(pil_image)
        llm_with_image_context = model.bind(images=[image_b64])
        if question == "":
            question = "What is in this picture?"  # answer in few sentences"
    # Set up the message with image and text prompt
    template = """
    Here is the question to answer: {question}

    Previous conversation: {chat_history}
    """
    prompt = ChatPromptTemplate.from_template(template)
    chain = prompt | llm_with_image_context

    for chunk in chain.stream({"question": question, "chat_history": chat_history}):
        if chunk is not None:
            msg = chunk
            # chat_history += msg
            print(msg, end="")
    chat_history += question

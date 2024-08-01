import os
import asyncio
from ollama import AsyncClient
import ollama

client = AsyncClient()

async def ask_ollama(model, questions, image_path):
    responses = {}
    try:
        for question in questions:
            response = await client.chat(model=model, messages=[
                {
                    "role": "system",
                    "content": "You are a helpful assistant, please format the output as a json."
                },
                {
                    "role": "user",
                    "content": question,
                    'images': [image_path]
                }
            ], options={'temperature': 0})

            responses[question] = response['message']['content']

    except ollama.ResponseError as e:
        print('Error:', e.error)
        if e.status_code == 404:
            print(f"Pulling model via ollama:")
            ollama.pull(model)

    return responses


async def q_multiple(image_path, model, questions):
    responses = await ask_ollama(model, questions, image_path)
    for question, response in responses.items():
        print(f"Question: {question}")
        print(f"Response: {response}\n")
    return responses

async def main():
    image_path = "data/Picture1.png"
    model = "llava-llama3" 
    questions = [
        "How many bars are in the histogram plot? Please format the output as a json as \"nbars\":\"\".",
        "What is the title of the plot? Please format the output as a json as \"title\":\"\".",
        "What is the x-axis label? Please format the output as a json as \"xlabel\":\"\".",
        "What is the y-axis label? Please format the output as a json as \"ylabel\":\"\".",
        "What is the color of the bars? The answer should be in the form of a single RGBA tuple. please format the output as a json as \"bar color\":\"\"."
    ]

    responses = await q_multiple(image_path, model, questions)
    print("All responses:", responses)

if __name__ == "__main__":
    asyncio.run(main())
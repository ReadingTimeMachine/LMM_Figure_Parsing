import os
import asyncio
from ollama import AsyncClient
import ollama

client = AsyncClient()

async def ask_ollama(model, questions, image_path):
    responses = {}
    responses['Level 1'] = {}
    responses['Level 1']['Plot-level questions'] = {}

    level_one_key_mapping = {
         "How many panels are in this figure? Please format the output as json with \"nrows\":\"\", \"ncols\":\"\" to store the number of rows and columns.": "rows/columns",
        "Assuming this is a figure made with the Python package matplotlib, what is the style sheet used? Please format the output as a json as \"plot style\":\"\" to store the matplotlib plotting style used in the figure.": 'plot style',
        "Assuming this is a figure made with matplotlib in Python, what is the colormap that was used? Please format the output as a json as \"colormap\":\"\" to store the matplotlib colormap used in the figure.": "colormap",
        "What is the aspect ratio of this figure? Please format the output as a json as \"aspect ratio\":\"\" to store the aspect ratio of the plot.": "aspect ration",
        "What is the DPI (dots per square inch) of this figure? Please format the output as a json as \"dpi\":\"\" to store the DPI of the plot.": "dpi",
        "What is the title of this figure? If there are more than one figure please present this as a list of titles. If a plot does not have a title, then denote this by an empty string in the list. Please format any formulas in the title in a Python LaTeX string.":"title",
        "What are the x-axis titles for each figure panel? If there are more than one figure please present this as a list. If a plot does not have a x-axis title, then denote this by an empty string in the list. Please format any formulas in the title in a Python LaTeX string.":"xlabels",
        "What are the y-axis titles for each figure panel? If there are more than one figure please present this as a list. If a plot does not have a y-axis title, then denote this by an empty string in the list. Please format any formulas in a Python LaTeX string.":"ylabels",
        "What are the plot types for each panel in the figure? Please format the output as a json where each element of the list refers to the plot type of a single panel.":"plot types",
        # "What are the values for each of the tick marks on the x-axis? Please format the output as a json as where each element of the outer list refers to a single panel":"x-tick values",
        # "What are the values for each of the tick marks on the y-axis? Please format the output as a json as where each element of the outer list refers to a single panel":"y-tick values",
    }

    
    try:
        for question in questions:
            response = await client.chat(model=model, messages=[
                {
                    "role": "system",
                    "content": "You are a helpful assistant, please format the output as a json. Sometimes there are multiple graphs per image, if so, please analyze each graph within an image individually and output its information as if it was a distinct image. If there is one plot, then this row and column refers to the single plot. "
                },
                {
                    "role": "user",
                    "content": question,
                    'images': [image_path]
                }
            ], options={'temperature': 0})

            if question in level_one_key_mapping:
                key = level_one_key_mapping[question]
                responses['Level 1']['Plot-level questions'][key] = response['message']['content']
            

    except ollama.ResponseError as e:
        print('Error:', e.error)
        if e.status_code == 404:
            print(f"Pulling model via ollama:")
            ollama.pull(model)

    return responses


async def q_multiple(image_path, model, questions):
    responses = await ask_ollama(model, questions, image_path)
    return responses

async def main(image_path):
    model = "llava-llama3" 
    questions = [
        "How many panels are in this figure? Please format the output as json with \"nrows\":\"\", \"ncols\":\"\" to store the number of rows and columns.",
         "Assuming this is a figure made with the Python package matplotlib, what is the style sheet used? Please format the output as a json as \"plot style\":\"\" to store the matplotlib plotting style used in the figure.",
        "Assuming this is a figure made with matplotlib in Python, what is the colormap that was used? Please format the output as a json as \"colormap\":\"\" to store the matplotlib colormap used in the figure.",
        "What is the aspect ratio of this figure? Please format the output as a json as \"aspect ratio\":\"\" to store the aspect ratio of the plot.",
        "What is the DPI (dots per square inch) of this figure? Please format the output as a json as \"dpi\":\"\" to store the DPI of the plot.",
        "What is the title of this figure? If there are more than one figure please present this as a list of titles. If a plot does not have a title, then denote this by an empty string in the list. Please format any formulas in the title in a Python LaTeX string.",
        "What are the x-axis titles for each figure panel? If there are more than one figure please present this as a list. If a plot does not have a x-axis title, then denote this by an empty string in the list. Please format any formulas in the title in a Python LaTeX string.",
        "What are the y-axis titles for each figure panel? If there are more than one figure please present this as a list. If a plot does not have a y-axis title, then denote this by an empty string in the list. Please format any formulas in a Python LaTeX string.",
        "What are the plot types for each panel in the figure? Please format the output as a json where each element of the list refers to the plot type of a single panel.",

        #these are giving llava-llama3 issues
        # "What are the values for each of the tick marks on the x-axis? Please format the output as a json as where each element of the outer list refers to a single panel",
        # "What are the values for each of the tick marks on the y-axis? Please format the output as a json as where each element of the outer list refers to a single panel",
        
    ]
    
    responses = await q_multiple(image_path, model, questions)


    # all_responses = {}
    
    # for image_file in os.listdir(folder_path):
    #     if image_file.lower().endswith(('.png')):
    #         image_path = os.path.join(folder_path, image_file)
    #         print(f"Processing {image_path}...")
    #         responses = await q_multiple(image_path, model, questions)
    #         all_responses[image_file] = responses

    #         print(responses)    
    
    # print(all_responses)

    return responses


if __name__ == "__main__":
    # folder_path = "data"
    asyncio.run(main(image_path))
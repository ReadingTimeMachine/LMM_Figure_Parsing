import os
import asyncio
from ollama import AsyncClient
import ollama
import numpy as np

client = AsyncClient()


async def describe_graph_level_one(image_path, model):
    llm_pairs = {}
    llm_pairs['Level 1'] = {}
    llm_pairs['Level 1']['Figure-level questions'] = {}
    llm_pairs['Level 1']['Plot-level questions'] = {}


    try:
        response_one = await client.chat(model=model, messages=[
            {
                "role": "system",
                "content": "You are a helpful assistant, please format the output as a json."
            },
            {
                "role": "user",
                "content": "How many panels are in this figure? Please format the output as json with \"nrows\":\"\", \"ncols\":\"\" to store the number of rows and columns.",
                'images': [image_path]
            }
        ], options={'temperature': 0})

        response_two = await client.chat(model=model, messages=[
            {
                "role": "system",
                "content": "You are a helpful assistant, please format the output as a json."
            },
            {
                "role": "user",
                "content": "Assuming this is a figure made with the Python package matplotlib, what is the style sheet used? Please format the output as a json as \"plot style\":\"\" to store the matplotlib plotting style used in the figure.",
                'images': [image_path]
            }
        ], options={'temperature': 0})

        response_three = await client.chat(model=model, messages=[
            {
                "role": "system",
                "content": "You are a helpful assistant, please format the output as a json."
            },
            {
                "role": "user",
                "content": "Assuming this is a figure made with matplotlib in Python, what is the colormap that was used? Please format the output as a json as \"colormap\":\"\" to store the matplotlib colormap used in the figure.",
                'images': [image_path]
            }
        ], options={'temperature': 0})

        response_four = await client.chat(model=model, messages=[
            {
                "role": "system",
                "content": "You are a helpful assistant, please format the output as a json."
            },
            {
                "role": "user",
                "content": "What is the aspect ratio of this figure? Please format the output as a json as \"aspect ratio\":\"\" to store the aspect ratio of the plot.",
                'images': [image_path]
            }
        ], options={'temperature': 0})

        response_five = await client.chat(model=model, messages=[
            {
                "role": "system",
                "content": "You are a helpful assistant, please format the output as a json."
            },
            {
                "role": "user",
                "content": "What is the DPI (dots per square inch) of this figure? Please format the output as a json as \"dpi\":\"\" to store the DPI of the plot.",
                'images': [image_path]
            }
        ], options={'temperature': 0})

        response_six = await client.chat(model=model, messages=[
            {
                "role": "system",
                "content": "You are a helpful assistant, please format the output as a json."
            },
            {
                "role": "user",
                "content": "What is the title of this figure? If there are more than one figure please present this as a list of titles. If a plot does not have a title, then denote this by an empty string in the list. Please format any formulas in the title in a Python LaTeX string.",

                'images': [image_path]
            }
        ], options={'temperature': 0})

        response_seven = await client.chat(model=model, messages=[
            {
                "role": "system",
                "content": "You are a helpful assistant, please format the output as a json."
            },
            {
                "role": "user",
                "content": "What are the x-axis titles for each figure panel? If there are more than one figure please present this as a list. If a plot does not have a x-axis title, then denote this by an empty string in the list. Please format any formulas in the title in a Python LaTeX string.",

                'images': [image_path]
            }
        ], options={'temperature': 0})

        response_eight = await client.chat(model=model, messages=[
            {
                "role": "system",
                "content": "You are a helpful assistant, please format the output as a json."
            },
            {
                "role": "user",
                "content": "What are the y-axis titles for each figure panel? If there are more than one figure please present this as a list. If a plot does not have a y-axis title, then denote this by an empty string in the list. Please format any formulas in a Python LaTeX string.",

                'images': [image_path]
            }
        ], options={'temperature': 0})

        response_nine = await client.chat(model=model, messages=[
            {
                "role": "system",
                "content": "You are a helpful assistant, please format the output as a json."
            },
            {
                "role": "user",
                "content": "What are the plot types for each panel in the figure? Please format the output as a json where each element of the list refers to the plot type of a single panel.",

                'images': [image_path]
            }
        ], options={'temperature': 0})

        response_ten = await client.chat(model=model, messages=[
            {
                "role": "system",
                "content": "You are a helpful assistant, please format the output as a json."
            },
            {
                "role": "user",
                "content": "What are the values for each of the tick marks on the x-axis? Please format the output as a json as where each element of the outer list refers to a single panel",

                'images': [image_path]
            }
        ], options={'temperature': 0})

        response_eleven = await client.chat(model=model, messages=[
            {
                "role": "system",
                "content": "You are a helpful assistant, please format the output as a json."
            },
            {
                "role": "user",
                "content": "What are the values for each of the tick marks on the y-axis? Please format the output as a json as where each element of the outer list refers to a single panel",

                'images': [image_path]
            }
        ], options={'temperature': 0})

        response_twelve = await client.chat(model=model, messages=[
            {
                "role": "system",
                "content": "You are a helpful assistant, please format the output as a json."
            },
            {
                "role": "user",
                "content": "If there are multiple plots the panels will be in row-major (C-style) order, with the numbering starting at (0,0) in the upper left panel. How many different lines are there for the figure panel on a given row  and column? Please format the output as a json as for this figure panel, where the \"nlines\" value should be an integer.",

                'images': [image_path]
            }
        ], options={'temperature': 0})

        response_thirteen = await client.chat(model=model, messages=[
            {
                "role": "system",
                "content": "You are a helpful assistant, please format the output as a json."
            },
            {
                "role": "user",
                "content": "If there is only one figure in this image: What are the colors of the lines in this figure? If there are multiple figures in this image: What are the colors of the lines for each plot in the panel? Please output your answer as a json where each element of the list refers to the color of each line in the figure panel in the form of an RGBA list with values between 0 and 1.",

                'images': [image_path]
            }
        ], options={'temperature': 0})

        response_fourteen = await client.chat(model=model, messages=[
            {
                "role": "system",
                "content": "You are a helpful assistant, please format the output as a json."
            },
            {
                "role": "user",
                "content": "If there is only one figure in this image: What are the matplotlib linestyles in this figure? If there are multiple figures in this image: What are the matplotlib linestyles for each plot in the panel? Please output your answer as a json.",

                'images': [image_path]
            }
        ], options={'temperature': 0})

        response_fifteen = await client.chat(model=model, messages=[
            {
                "role": "system",
                "content": "You are a helpful assistant, please format the output as a json."
            },
            {
                "role": "user",
                "content": "If there is only one figure in this image: What are the matplotlib line thicknesses in this figure?? If there are multiple figures in this image: What are the matplotlib line thicknesses for each plot in the panel? Please output your answer as a json where each element of the list refers to the thickness of each line in the figure panel in the form a matplotlib thickness type.",

                'images': [image_path]
            }
        ], options={'temperature': 0})

        response_sixteen = await client.chat(model=model, messages=[
            {
                "role": "system",
                "content": "You are a helpful assistant, please format the output as a json."
            },
            {
                "role": "user",
                "content": "If there is only one figure in this image: What are the matplotlib line markers in this figure?? If there are multiple figures in this image: What are the matplotlib line markers for each plot in the panel? Please output your answer as a json where each element of the list refers to the line markers of each line in the figure panel.",

                'images': [image_path]
            }
        ], options={'temperature': 0})

        response_seventeen = await client.chat(model=model, messages=[
            {
                "role": "system",
                "content": "You are a helpful assistant, please format the output as a json."
            },
            {
                "role": "user",
                "content": "If there is only one figure in this image: What are the matplotlib line marker sizes in this figure?? If there are multiple figures in this image: What are the matplotlib line marker sizes for each plot in the panel? Please output your answer as a json where each element of the list refers to the line marker sizes of each line in the figure panel.",

                'images': [image_path]
            }
        ], options={'temperature': 0})

        response_seventeen = await client.chat(model=model, messages=[
            {
                "role": "system",
                "content": "You are a helpful assistant, please format the output as a json."
            },
            {
                "role": "user",
                "content": "If there is only one figure in this image: What are the specific data values in this figure? If there are multiple figures in this image: What are the specific data values for each plot in the panel? Please format the output as a json as {\"x\":[], \"y\":[]} where the values of \"x\" and \"y\" are the data values used to create the plot.",

                'images': [image_path]
            }
        ], options={'temperature': 0})

    #     llm_pairs['Level 1']['Figure-level questions'][image_path] = {
    #     'rows/columns': response_one
    # }



    except ollama.ResponseError as e:
        print('Error:', e.error)
        if e.status_code == 404:
            print(f"Pulling model via ollama:")
            ollama.pull(model)



    llm_pairs['Level 1']['Figure-level questions'][image_path] = {
        'rows/columns': response_one['message']['content'],
        'plot style': response_two['message']['content'],
        'colormap': response_three['message']['content'],
        'aspect ratio': response_four['message']['content'],
        'dpi': response_five['message']['content'],
    }

    llm_pairs['Level 1']['Plot-level questions'] = {
        'title': response_six['message']['content'],
        'xlabels': response_seven['message']['content'],
        'ylabels': response_eight['message']['content'],
        'plot types': response_nine['message']['content'],
        'x-tick values': response_ten['message']['content'],
        'y-tick values': response_eleven['message']['content'],
        'nlines (plot numbers)': response_twelve['message']['content'],
        'nlines (words)': response_thirteen['message']['content'],
        'line colors': response_thirteen['message']['content'],
        'line styles': response_fourteen['message']['content'],
        'line thickness': response_fifteen['message']['content'],
        'line markers': response_sixteen['message']['content'],
        'line marker size': response_seventeen['message']['content'],

    }

    print(llm_pairs)

    return llm_pairs

async def describe_graph_level_two(image_path, model):

    lvl2_llm_pairs = {}
    lvl2_llm_pairs['Level 2'] = {}
    lvl2_llm_pairs['Level 2']['Figure-level questions'] = {}
    lvl2_llm_pairs['Level 2']['Plot-level questions'] = {}
    lvl2_llm_pairs['Level 3'] = {}
    lvl2_llm_pairs['Level 3']['Plot-level questions'] = {}

    
    try:


        response_eighteen = await client.chat(model=model, messages=[
            {
                "role": "system",
                "content": "You are a helpful assistant, please format the output as a json."
            },
            {
                "role": "user",
                "content": f"If there is only one figure in this image: What are the specific mean data values in this figure? If there are multiple figures in this image: What are the specific mean data values for each plot in the panel? Please format the output as a json as mean: \"x\":[], \"y\":[] where the values of \"x\" and \"y\" are the data values used to create the plot.",

                'images': [image_path]
            }
        ], options={'temperature': 0})

        response_nineteen = await client.chat(model=model, messages=[
            {
                "role": "system",
                "content": "You are a helpful assistant, please format the output as a json."
            },
            {
                "role": "user",
                "content": f"If there is only one figure in this image: What are the specific minimum data values in this figure? If there are multiple figures in this image: What are the specific minimum data values for each plot in the panel? Please format the output as a json as minimum: \"x\":[], \"y\":[] where the values of \"x\" and \"y\" are the data values used to create the plot.",

                'images': [image_path]
            }
        ], options={'temperature': 0})

        response_twenty = await client.chat(model=model, messages=[
            {
                "role": "system",
                "content": "You are a helpful assistant, please format the output as a json."
            },
            {
                "role": "user",
                "content": f"If there is only one figure in this image: What are the specific maximum data values in this figure? If there are multiple figures in this image: What are the specific maximum data values for each plot in the panel? Please format the output as a json as maximum: \"x\":[], \"y\":[] where the values of \"x\" and \"y\" are the data values used to create the plot.",

                'images': [image_path]
            }
        ], options={'temperature': 0})

        response_twentyone = await client.chat(model=model, messages=[
            {
                "role": "system",
                "content": "You are a helpful assistant, please format the output as a json."
            },
            {
                "role": "user",
                "content": f"If there is only one figure in this image: What are the specific median data values in this figure? If there are multiple figures in this image: What are the specific median data values for each plot in the panel? Please format the output as a json as median: \"x\":[], \"y\":[] where the values of \"x\" and \"y\" are the data values used to create the plot.",

                'images': [image_path]
            }
        ], options={'temperature': 0})

        response_twentytwo = await client.chat(model=model, messages=[
            {
                "role": "system",
                "content": "You are a helpful assistant, please format the output as a json."
            },
            {
                "role": "user",
                "content": f"If there is only one figure in this image: Are there error bars on the data along the x-axis in this figure? If there are multiple figures in this image:  Are there error bars on the data along the x-axis for each plot in the panel? please format the output as a json as \"x-axis errors\":\"\" where the value for the output is True (if error bars exist) or False (if error bars do not exist).",

                'images': [image_path]
            }
        ], options={'temperature': 0})

        response_twentythree = await client.chat(model=model, messages=[
            {
                "role": "system",
                "content": "You are a helpful assistant, please format the output as a json."
            },
            {
                "role": "user",
                "content": f"If there is only one figure in this image: Are there error bars on the data along the y-axis in this figure? If there are multiple figures in this image:  Are there error bars on the data along the y-axis for each plot in the panel? please format the output as a json as \"y-axis errors\":\"\" where the value for the output is True (if error bars exist) or False (if error bars do not exist).",

                'images': [image_path]
            }
        ], options={'temperature': 0})

        response_twentyfour = await client.chat(model=model, messages=[
            {
                "role": "system",
                "content": "You are a helpful assistant, please format the output as a json."
            },
            {
                "role": "user",
                "content": f"If there is only one figure in this image: What is the approximate size of the error bars along the x-axis in this figure? If there are multiple figures in this image:  What is the approximate size of the error bars along the x-axis for each plot in the panel? please format the output as a json where each element of the list corresponds to a single line in the figure. The size of the error bar can be calculated as the average length of the bar divided by the difference between the maximum and minimum data values along the x-axis.",

                'images': [image_path]
            }
        ], options={'temperature': 0})

        response_twentyfive = await client.chat(model=model, messages=[
            {
                "role": "system",
                "content": "You are a helpful assistant, please format the output as a json."
            },
            {
                "role": "user",
                "content": f"If there is only one figure in this image: What is the approximate size of the error bars along the x-axis in this figure? If there are multiple figures in this image:  What is the approximate size of the error bars along the x-axis for each plot in the panel? please format the output as a json The size of the error bar can be calculated as the average length of the bar divided by the difference between the maximum and minimum data values along the x-axis.",

                'images': [image_path]
            }
        ], options={'temperature': 0})

        response_twentysix = await client.chat(model=model, messages=[
            {
                "role": "system",
                "content": "You are a helpful assistant, please format the output as a json."
            },
            {
                "role": "user",
                "content": f"What is the type of relationship of this figure? Select one of the following types: random, linear, or gaussian mixture model. Format the output as a json. ",

                'images': [image_path]
            }
        ], options={'temperature': 0})

        response_twentyseven = await client.chat(model=model, messages=[
            {
                "role": "system",
                "content": "You are a helpful assistant, please format the output as a json."
            },
            {
                "role": "user",
                "content": "If this is a linear relationship, what are the parameters for the linear relationship between the x and y values in this figure? If there are more than one figures per image, what are the parameters? if it is not a linear model simply state that it is not a linear model. please format the output as a json as {\"linear parameters\":[{\"m\":\"\",\"a\":\"\",\"noise level\":\"\"}]} where each dictionary element of the list corresponds to a single line in the figure. Each \"m\" is the slope for each line and \"a\" is the intercept for each line and should be a float. The \"noise level\" parameter should be the relative amount of noise added to each linear function for each line and should be a float between 0 and 1. ",

                'images': [image_path]
            }
        ], options={'temperature': 0})


        response_twentyeight = await client.chat(model=model, messages=[
            {
                "role": "system",
                "content": "You are a helpful assistant, please format the output as a json."
            },
            {
                "role": "user",
                "content": "If this is a gaussian mixture model, What are the parameters for the gaussian mixture model relationship between the x and y values for the plot or each plot in the image? If it is not a gaussian mixture model, simply state that it is not a gmm model. please format the output as a json as {\"gmm parameters\":[{\"nsamples\":\"\",\"nclusters\":\"\",\"centers\":\"\",\"cluster_std\":\"\",\"noise level\":\"\"}]} where each dictionary element of the list corresponds to a single line in the figure. Each \"nsamples\" is the number of samples in the distribution and should be an integer. The \"nclusters\" parameter should be the number of clusters in the model and should be an integer. The \"centers\" parameter should be the position of each cluster on the x-axis and should be a float. The \"cluster_std\" parameter should be the standard deviation for each cluster on the x-axis and should be a float.The \"noise level\" parameter should be the relative amount of noise added to each linear function for each line and should be a float between 0 and 1. ",

                'images': [image_path]
            }
        ], options={'temperature': 0})


    
    except ollama.ResponseError as e:
        print('Error:', e.error)
        if e.status_code == 404:
            print(f"Pulling model via ollama:")
            ollama.pull(model)

    
    lvl2_llm_pairs['Level 2']['Plot-level questions'] = {
        'mean (words)': response_eighteen['message']['content'],
        'minimum (words)': response_nineteen['message']['content'],
        'maximum (words)': response_twenty['message']['content'],
        'median (words)': response_twentyone['message']['content'],
        'x-axis errors (words)': response_twentytwo['message']['content'],
        'y-axis errors (words)': response_twentythree['message']['content'],
        'x-axis errors size (words)': response_twentyfour['message']['content'],
        'y-axis errors size (words)': response_twentyfive['message']['content'],

    }

    lvl2_llm_pairs['Level 3']['Plot-level questions'] = {
        'relationship (words + list)': response_twentysix['message']['content'],
        'linear parameters': response_twentyseven['message']['content'],
        'gmm parameters': response_twentyeight['message']['content'],




    }

    

    print(lvl2_llm_pairs)

    return lvl2_llm_pairs


async def open_image(directory, model):
    tasks = []
    for filename in os.listdir(directory):
        if filename.endswith(".png"):
            image_path = os.path.join(directory, filename)
            tasks.append(describe_graph_level_one(image_path, model))
            tasks.append(describe_graph_level_two(image_path, model))
    await asyncio.gather(*tasks)

if __name__ == '__main__':
    directory = 'data'
    model = 'llava-llama3'
    asyncio.run(open_image(directory, model))

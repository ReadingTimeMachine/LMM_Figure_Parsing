import os
import asyncio
from ollama import AsyncClient
import ollama

client = AsyncClient()

async def ask_ollama(model, questions, image_path):
    responses = {}
    responses['Level 1'] = {}
    responses['Level 1']['Plot-level questions'] = {}
    responses['Level 1']['Figure-level questions'] = {}
    responses['Level 2'] = {}
    responses['Level 2']['Plot-level questions'] = {}
    responses['Level 3'] = {}
    responses['Level 3']['Plot-level questions'] = {}
    level_one_key_mapping_fig = {
        "How many panels are in this figure? Please format the output as json with \"nrows\":\"\", \"ncols\":\"\" to store the number of rows and columns.": "rows/columns",
        "Assuming this is a figure made with the Python package matplotlib, what is the style sheet used? Please format the output as a json as \"plot style\":\"\" to store the matplotlib plotting style used in the figure.": 'plot style',
        "Assuming this is a figure made with matplotlib in Python, what is the colormap that was used? Please format the output as a json as \"colormap\":\"\" to store the matplotlib colormap used in the figure.": "colormap",
        "What is the aspect ratio of this figure? Please format the output as a json as \"aspect ratio\":\"\" to store the aspect ratio of the plot.": "aspect ration",
        "What is the DPI (dots per square inch) of this figure? Please format the output as a json as \"dpi\":\"\" to store the DPI of the plot.": "dpi"
        
    }

    level_one_key_mapping = {
        "If there are multiple plots the panels will be in row-major (C-style) order, with the numbering starting at (0,0) in the upper left panel. How many different lines are there for the figure panel on a given row  and column? Please format the output as a json as for this figure panel, where the \"nlines\" value should be an integer.":"nlines (words)",
        "If there is only one figure in this image: What are the colors of the lines in this figure? If there are multiple figures in this image: What are the colors of the lines for each plot in the panel? Please output your answer as a json where each element of the list refers to the color of each line in the figure panel in the form of an RGBA list with values between 0 and 1.":"line colors",
        "If there is only one figure in this image: What are the matplotlib linestyles in this figure? If there are multiple figures in this image: What are the matplotlib linestyles for each plot in the panel? Please output your answer as a json.":"line style",
        "If there is only one figure in this image: What are the matplotlib line thicknesses in this figure?? If there are multiple figures in this image: What are the matplotlib line thicknesses for each plot in the panel? Please output your answer as a json where each element of the list refers to the thickness of each line in the figure panel in the form a matplotlib thickness type.":"line thickness",
        "If there is only one figure in this image: What are the matplotlib line markers in this figure?? If there are multiple figures in this image: What are the matplotlib line markers for each plot in the panel? Please output your answer as a json where each element of the list refers to the line markers of each line in the figure panel.":"line markers",
        "If there is only one figure in this image: What are the matplotlib line marker sizes in this figure?? If there are multiple figures in this image: What are the matplotlib line marker sizes for each plot in the panel? Please output your answer as a json where each element of the list refers to the line marker sizes of each line in the figure panel.":"line marker size"


        
    }

    level_two_key_mapping = {
        "If there is only one figure in this image: What are the specific data values in this figure? If there are multiple figures in this image: What are the specific data values for each plot in the panel? Please format the output as a json as {\"x\":[], \"y\":[]} where the values of \"x\" and \"y\" are the data values used to create the plot.": "data values",
        "If there is only one figure in this image: What are the specific mean data values in this figure? If there are multiple figures in this image: What are the specific mean data values for each plot in the panel? Please format the output as a json as mean: \"x\":[], \"y\":[] where the values of \"x\" and \"y\" are the data values used to create the plot.": "mean (words)",
        "If there is only one figure in this image: What are the specific minimum data values in this figure? If there are multiple figures in this image: What are the specific minimum data values for each plot in the panel? Please format the output as a json as minimum: \"x\":[], \"y\":[] where the values of \"x\" and \"y\" are the data values used to create the plot.": "minimum (words)",
        "If there is only one figure in this image: What are the specific maximum data values in this figure? If there are multiple figures in this image: What are the specific maximum data values for each plot in the panel? Please format the output as a json as maximum: \"x\":[], \"y\":[] where the values of \"x\" and \"y\" are the data values used to create the plot.": "maximum (words)",
        "If there is only one figure in this image: What are the specific median data values in this figure? If there are multiple figures in this image: What are the specific median data values for each plot in the panel? Please format the output as a json as median: \"x\":[], \"y\":[] where the values of \"x\" and \"y\" are the data values used to create the plot.": "median(words)",
       "If there is only one figure in this image: Are there error bars on the data along the x-axis in this figure? If there are multiple figures in this image:  Are there error bars on the data along the x-axis for each plot in the panel? please format the output as a json as \"x-axis errors\":\"\" where the value for the output is True (if error bars exist) or False (if error bars do not exist).": "x-axis errors (words)",
       "If there is only one figure in this image: Are there error bars on the data along the y-axis in this figure? If there are multiple figures in this image:  Are there error bars on the data along the y-axis for each plot in the panel? please format the output as a json as \"y-axis errors\":\"\" where the value for the output is True (if error bars exist) or False (if error bars do not exist).": "y-axis errors (words)",
       "If there is only one figure in this image: What is the approximate size of the error bars along the x-axis in this figure? If there are multiple figures in this image:  What is the approximate size of the error bars along the x-axis for each plot in the panel? please format the output as a json where each element of the list corresponds to a single line in the figure. The size of the error bar can be calculated as the average length of the bar divided by the difference between the maximum and minimum data values along the x-axis.":"x-axis errors size (words)",
       "If there is only one figure in this image: What is the approximate size of the error bars along the x-axis in this figure? If there are multiple figures in this image:  What is the approximate size of the error bars along the x-axis for each plot in the panel? please format the output as a json The size of the error bar can be calculated as the average length of the bar divided by the difference between the maximum and minimum data values along the x-axis.":"y-axis errors size (words)"


    }

    level_three_key_mapping = {
       "What is the type of relationship of this figure? Select one of the following types: random, linear, or gaussian mixture model. Format the output as a json. ":"relationship (words + list)",
       "If this is a linear relationship, what are the parameters for the linear relationship between the x and y values in this figure? If there are more than one figures per image, what are the parameters? if it is not a linear model simply state that it is not a linear model. please format the output as a json as {\"linear parameters\":[{\"m\":\"\",\"a\":\"\",\"noise level\":\"\"}]} where each dictionary element of the list corresponds to a single line in the figure. Each \"m\" is the slope for each line and \"a\" is the intercept for each line and should be a float. The \"noise level\" parameter should be the relative amount of noise added to each linear function for each line and should be a float between 0 and 1. ":"linear parameters",
       "If this is a gaussian mixture model, What are the parameters for the gaussian mixture model relationship between the x and y values for the plot or each plot in the image? If it is not a gaussian mixture model, simply state that it is not a gmm model. please format the output as a json as {\"gmm parameters\":[{\"nsamples\":\"\",\"nclusters\":\"\",\"centers\":\"\",\"cluster_std\":\"\",\"noise level\":\"\"}]} where each dictionary element of the list corresponds to a single line in the figure. Each \"nsamples\" is the number of samples in the distribution and should be an integer. The \"nclusters\" parameter should be the number of clusters in the model and should be an integer. The \"centers\" parameter should be the position of each cluster on the x-axis and should be a float. The \"cluster_std\" parameter should be the standard deviation for each cluster on the x-axis and should be a float.The \"noise level\" parameter should be the relative amount of noise added to each linear function for each line and should be a float between 0 and 1. ":"gmm parameters"
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

            if question in level_one_key_mapping_fig:
                key = level_one_key_mapping_fig[question]
                responses['Level 1']['Figure-level questions'][key] = response['message']['content']
            if question in level_one_key_mapping:
                key = level_one_key_mapping[question]
                responses['Level 1']['Plot-level questions'][key] = response['message']['content']
            elif question in level_two_key_mapping:
                key = level_two_key_mapping[question]
                responses['Level 2']['Plot-level questions'][key] = response['message']['content']
            elif question in level_three_key_mapping:
                key = level_three_key_mapping[question]
                responses['Level 3']['Plot-level questions'][key] = response['message']['content']
            

    except ollama.ResponseError as e:
        print('Error:', e.error)
        if e.status_code == 404:
            print(f"Pulling model via ollama:")
            ollama.pull(model)

    return responses


async def q_multiple(image_path, model, questions):
    responses = await ask_ollama(model, questions, image_path)
    # for question, response in responses.items():
    #     print(f"Key: {question}")
    #     print(f"Response: {response}\n")
    return responses

async def main():
    folder_path = "data"
    model = "llava:7b" 
    questions = [
         "If there are multiple plots the panels will be in row-major (C-style) order, with the numbering starting at (0,0) in the upper left panel. How many different lines are there for the figure panel on a given row  and column? Please format the output as a json as for this figure panel, where the \"nlines\" value should be an integer.",
         "If there is only one figure in this image: What are the colors of the lines in this figure? If there are multiple figures in this image: What are the colors of the lines for each plot in the panel? Please output your answer as a json where each element of the list refers to the color of each line in the figure panel in the form of an RGBA list with values between 0 and 1.",
         "If there is only one figure in this image: What are the matplotlib linestyles in this figure? If there are multiple figures in this image: What are the matplotlib linestyles for each plot in the panel? Please output your answer as a json.",
         "If there is only one figure in this image: What are the matplotlib line thicknesses in this figure?? If there are multiple figures in this image: What are the matplotlib line thicknesses for each plot in the panel? Please output your answer as a json where each element of the list refers to the thickness of each line in the figure panel in the form a matplotlib thickness type.",
          "If there is only one figure in this image: What are the matplotlib line markers in this figure?? If there are multiple figures in this image: What are the matplotlib line markers for each plot in the panel? Please output your answer as a json where each element of the list refers to the line markers of each line in the figure panel.",
          "If there is only one figure in this image: What are the matplotlib line marker sizes in this figure?? If there are multiple figures in this image: What are the matplotlib line marker sizes for each plot in the panel? Please output your answer as a json where each element of the list refers to the line marker sizes of each line in the figure panel.",
           "If there is only one figure in this image: What are the specific data values in this figure? If there are multiple figures in this image: What are the specific data values for each plot in the panel? Please format the output as a json as {\"x\":[], \"y\":[]} where the values of \"x\" and \"y\" are the data values used to create the plot.",
           "If there is only one figure in this image: What are the specific mean data values in this figure? If there are multiple figures in this image: What are the specific mean data values for each plot in the panel? Please format the output as a json as mean: \"x\":[], \"y\":[] where the values of \"x\" and \"y\" are the data values used to create the plot.",
           "If there is only one figure in this image: What are the specific minimum data values in this figure? If there are multiple figures in this image: What are the specific minimum data values for each plot in the panel? Please format the output as a json as minimum: \"x\":[], \"y\":[] where the values of \"x\" and \"y\" are the data values used to create the plot.",
           "If there is only one figure in this image: What are the specific maximum data values in this figure? If there are multiple figures in this image: What are the specific maximum data values for each plot in the panel? Please format the output as a json as maximum: \"x\":[], \"y\":[] where the values of \"x\" and \"y\" are the data values used to create the plot.",
           "If there is only one figure in this image: What are the specific median data values in this figure? If there are multiple figures in this image: What are the specific median data values for each plot in the panel? Please format the output as a json as median: \"x\":[], \"y\":[] where the values of \"x\" and \"y\" are the data values used to create the plot.",
           "If there is only one figure in this image: Are there error bars on the data along the x-axis in this figure? If there are multiple figures in this image:  Are there error bars on the data along the x-axis for each plot in the panel? please format the output as a json as \"x-axis errors\":\"\" where the value for the output is True (if error bars exist) or False (if error bars do not exist).",
           "If there is only one figure in this image: Are there error bars on the data along the y-axis in this figure? If there are multiple figures in this image:  Are there error bars on the data along the y-axis for each plot in the panel? please format the output as a json as \"y-axis errors\":\"\" where the value for the output is True (if error bars exist) or False (if error bars do not exist).",
           "If there is only one figure in this image: What is the approximate size of the error bars along the x-axis in this figure? If there are multiple figures in this image:  What is the approximate size of the error bars along the x-axis for each plot in the panel? please format the output as a json where each element of the list corresponds to a single line in the figure. The size of the error bar can be calculated as the average length of the bar divided by the difference between the maximum and minimum data values along the x-axis.",
           "If there is only one figure in this image: What is the approximate size of the error bars along the x-axis in this figure? If there are multiple figures in this image:  What is the approximate size of the error bars along the x-axis for each plot in the panel? please format the output as a json The size of the error bar can be calculated as the average length of the bar divided by the difference between the maximum and minimum data values along the x-axis.",
           "What is the type of relationship of this figure? Select one of the following types: random, linear, or gaussian mixture model. Format the output as a json. ",
           "If this is a linear relationship, what are the parameters for the linear relationship between the x and y values in this figure? If there are more than one figures per image, what are the parameters? if it is not a linear model simply state that it is not a linear model. please format the output as a json as {\"linear parameters\":[{\"m\":\"\",\"a\":\"\",\"noise level\":\"\"}]} where each dictionary element of the list corresponds to a single line in the figure. Each \"m\" is the slope for each line and \"a\" is the intercept for each line and should be a float. The \"noise level\" parameter should be the relative amount of noise added to each linear function for each line and should be a float between 0 and 1. ",
           "If this is a gaussian mixture model, What are the parameters for the gaussian mixture model relationship between the x and y values for the plot or each plot in the image? If it is not a gaussian mixture model, simply state that it is not a gmm model. please format the output as a json as {\"gmm parameters\":[{\"nsamples\":\"\",\"nclusters\":\"\",\"centers\":\"\",\"cluster_std\":\"\",\"noise level\":\"\"}]} where each dictionary element of the list corresponds to a single line in the figure. Each \"nsamples\" is the number of samples in the distribution and should be an integer. The \"nclusters\" parameter should be the number of clusters in the model and should be an integer. The \"centers\" parameter should be the position of each cluster on the x-axis and should be a float. The \"cluster_std\" parameter should be the standard deviation for each cluster on the x-axis and should be a float.The \"noise level\" parameter should be the relative amount of noise added to each linear function for each line and should be a float between 0 and 1. ",
        
    ]
    
    all_responses = {}
    
    for image_file in os.listdir(folder_path):
        if image_file.lower().endswith(('.png', '.jpg', '.jpeg', '.bmp', '.gif')):
            image_path = os.path.join(folder_path, image_file)
            print(f"Processing {image_path}...")
            responses = await q_multiple(image_path, model, questions)
            all_responses[image_file] = responses    
            
    print(all_responses)

if __name__ == "__main__":
    asyncio.run(main())
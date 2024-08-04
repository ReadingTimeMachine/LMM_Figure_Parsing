import os
import asyncio
from ollama import AsyncClient
import ollama

client = AsyncClient()

async def ask_ollama(model, questions, image_path):
    responses = {}
    responses['Level 1'] = {}
    responses['Level 1']['Plot-level questions'] = {}
    responses['Level 2'] = {}
    responses['Level 2']['Plot-level questions'] = {}
    responses['Level 3'] = {}
    responses['Level 3']['Plot-level questions'] = {}
    level_one_key_mapping = {
        "How many scatter points are there for on the figure? please format the output as a json as {\"npoints\":\"\"} for this figure panel, where the \"npoints\" value should be an integer.": "npoints",
        "What are the colors of each of the scatter plot points? The answer should be in the form of a should be in the form of an RGBA tuple, with one tuple for each scatter plot point. You are a helpful assistant, please format the output as a json as {\"point colors\":'[]'} for this figure panel, where the \"point colors\" value": "point_colors",
        "What are the matplotlib scatter plot markers in this figure? Please format the output as a json \"scatter plot marker\":\"\". where the value of the entry should be the matplotlib marker used for this scatter plot.": "scatter plot marker",
        "What are the matplotlib scatter plot marker sizes in this figure? Please format the output as a json \"scatter plot marker sizes\":\"\" where the value of the entry should be the matplotlib marker size used for this scatter plot as an integer.": "scatter plot marker size",
        "What are the data values in this figure? lease format the output as a json as {\"x\":[], \"y\":[]} where the values of \"x\" and \"y\" are the data values used to create the plot and are in the format of a list of floats.": "data values"
        # "What is the x-axis label? Please format the output as a json as \"xlabel\":\"\".": "xlabel",
        # "What is the y-axis label? Please format the output as a json as \"ylabel\":\"\".": "ylabel",
        # "What is the color of the bars? The answer should be in the form of a single RGBA tuple. please format the output as a json as \"bar color\":\"\".": "bar_color",
        # "What are the locations of the bars? please format the output as a json as {\"left\":[], \"right\":[], \"center\",[], \"height\":[]} where the values of \"left\" and \"right\" are the left and right edges of each bar, and \"center\" is the center of each bar, all in terms of the x-axis values. Additionally, \"height\" is the location of the top of each bar and should be in terms of the y-axis values.": "bar locations"
    }

    level_two_key_mapping = {
        "What are the minimum data values in this figure? Please format the output as a json as {\"minimum x\":\"\"} where the minimum value of \"x\" is calculated from the data values used to create the plot in the format of floats.": "minimum x",
        "What are the maximum data values in this figure? Please format the output as a json as {\"maximum x\":\"\"} where the maximum value of \"x\" is calculated from the data values used to create the plot in the format of floats.": "maximum x",
        "What are the mean data values in this figure? Please format the output as a json as {\"mean x\":\"\"} where the mean value of \"x\" is calculated from the data values used to create the plot in the format of floats.": "mean x",
        "What are the median data values in this figure? Please format the output as a json as {\"median x\":\"\"} where the median value of \"x\" is calculated from the data values used to create the plot in the format of floats.": "median x",
        "Are there error bars on the data along the x-axis in this figure? please format the output as a json as {\"x-axis errors\":\"\"} where the value for the output is True (if error bars exist) or False (if error bars do not exist). ": "x-axis errors",
        "Are there error bars on the data along the y-axis in this figure? please format the output as a json as {\"y-axis errors\":\"\"} where the value for the output is True (if error bars exist) or False (if error bars do not exist). ": "y-axis errors",
        "What is the approximate size of the error bars along the x-axis in this figure? please format the output as a json as {\"x-axis error size\":\"\"} where the value is a float and the average size of the error bars along this axis. The average size of the error bar can be calculated as the average length of the bar divided by the difference between the maximum and minimum data values along the x-axis.": "x-axis errors size",
        "What is the approximate size of the error bars along the y-axis in this figure? please format the output as a json as {\"y-axis error size\":\"\"} where the value is a float and the average size of the error bars along this axis. The average size of the error bar can be calculated as the average length of the bar divided by the difference between the maximum and minimum data values along the y-axis.": "y-axis errors size",
    }

    level_three_key_mapping = {
        "What is the distribution used to create the histogram? please format the output as a json as {\"distribution\":\"\"} the value is a string.": "distribution",
        "What are the parameters for the linear distribution used to create the histogram? please format the output as a json as {\"linear distribution\":{\"m\":\"\",\"a\":\"\",\"noise level\":\"\"}}. Here, \"m\" is the slope of the relationship and \"a\" is the intercept and both should be floats. The \"noise level\" parameter should be the relative amount of noise added to the linear function for the relationship and should be a float between 0 and 1. If this is not a linear relationship, please do not try to answer the question": "linear distribution",
        "What are the parameters for the gaussian mixture model distribution used to create the histogram? please format the output as a json as {\"gmm parameters\":{\"nsamples\":\"\",\"nclusters\":\"\",\"centers\":\"\",\"cluster_std\":\"\",\"noise level\":\"\"}}. Each \"nsamples\" is the number of samples in the distribution and should be an integer. The \"nclusters\" parameter should be the number of clusters in the model and should be an integer. The \"centers\" parameter should be the position of each cluster and should be a list of points which are floats. The \"cluster_std\" parameter should be the standard deviation of each cluster and should be a list of points which are floats. The \"noise level\" parameter should be the relative amount of noise added to the model and should be a float between 0 and 1. If it is not a gaussian mixture model, please do not try to answer the question": "gmm parameters",
        "What is the functional relationship between the x and y values in this figure? please format the output as a json as {\"relationship\":\"\"} the value is a string.": "relationship",
        "What is the functional relationship between the x and y values in this figure and the colors of the scatter plots? please format the output as a json as {\"color relationship\":\"\"} the value is a string.": "color relationship",
        "What are the parameters for the linear relationship between the x and y values in this figure? please format the output as a json as {\"color\":{\"m\":\"\",\"a\":\"\",\"noise level\":\"\"}}. Here, \"m\" is the slope of the relationship and \"a\" is the intercept and both should be floats. The \"noise level\" parameter should be the relative amount of noise added to the linear function for the relationship and should be a float between 0 and 1.": "linear parameters",
        "What are the parameters for the linear relationship between the x and y values in this figure and the colors of the scatter points? please format the output as a json as {\"colors\":{\"m1\":\"\",\"a1\":\"\",\"m2\":\"\",\"a2\":\"\",\"noise level\":\"\"}}. Here, \"m1\" is the slope of the relationship and \"a1\" is the intercept in the \"x\" axis direction and both should be floats. Additionally, \"m2\" is the slope of the relationship and \"a2\" is the intercept in the \"y\" axis direction and both should be floats. The \"noise level\" parameter should be the relative amount of noise added to the linear function for the relationship and should be a float between 0 and 1.": "colors"
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
        "How many scatter points are there for on the figure? please format the output as a json as {\"npoints\":\"\"} for this figure panel, where the \"npoints\" value should be an integer.",
        "What are the colors of each of the scatter plot points? The answer should be in the form of a should be in the form of an RGBA tuple, with one tuple for each scatter plot point. You are a helpful assistant, please format the output as a json as {\"point colors\":'[]'} for this figure panel, where the \"point colors\" value",
        "What are the matplotlib scatter plot markers in this figure? Please format the output as a json \"scatter plot marker\":\"\". where the value of the entry should be the matplotlib marker used for this scatter plot.",
        "What are the matplotlib scatter plot marker sizes in this figure? Please format the output as a json \"scatter plot marker sizes\":\"\" where the value of the entry should be the matplotlib marker size used for this scatter plot as an integer.",
        "What are the data values in this figure? lease format the output as a json as {\"x\":[], \"y\":[]} where the values of \"x\" and \"y\" are the data values used to create the plot and are in the format of a list of floats.",
        "What are the minimum data values in this figure? Please format the output as a json as {\"minimum x\":\"\"} where the minimum value of \"x\" is calculated from the data values used to create the plot in the format of floats.",
        "What are the maximum data values in this figure? Please format the output as a json as {\"maximum x\":\"\"} where the maximum value of \"x\" is calculated from the data values used to create the plot in the format of floats.",
        "What are the mean data values in this figure? Please format the output as a json as {\"mean x\":\"\"} where the mean value of \"x\" is calculated from the data values used to create the plot in the format of floats.",
        "What are the median data values in this figure? Please format the output as a json as {\"median x\":\"\"} where the median value of \"x\" is calculated from the data values used to create the plot in the format of floats.",
        "What is the approximate size of the error bars along the x-axis in this figure? please format the output as a json as {\"x-axis error size\":\"\"} where the value is a float and the average size of the error bars along this axis. The average size of the error bar can be calculated as the average length of the bar divided by the difference between the maximum and minimum data values along the x-axis.",
        "What is the approximate size of the error bars along the y-axis in this figure? please format the output as a json as {\"y-axis error size\":\"\"} where the value is a float and the average size of the error bars along this axis. The average size of the error bar can be calculated as the average length of the bar divided by the difference between the maximum and minimum data values along the y-axis.",
        "What is the functional relationship between the x and y values in this figure? please format the output as a json as {\"relationship\":\"\"} the value is a string.",
        "What is the functional relationship between the x and y values in this figure and the colors of the scatter plots? please format the output as a json as {\"color relationship\":\"\"} the value is a string.",
        "What are the parameters for the linear relationship between the x and y values in this figure? please format the output as a json as {\"color\":{\"m\":\"\",\"a\":\"\",\"noise level\":\"\"}}. Here, \"m\" is the slope of the relationship and \"a\" is the intercept and both should be floats. The \"noise level\" parameter should be the relative amount of noise added to the linear function for the relationship and should be a float between 0 and 1.",
        "What are the parameters for the linear relationship between the x and y values in this figure and the colors of the scatter points? please format the output as a json as {\"colors\":{\"m1\":\"\",\"a1\":\"\",\"m2\":\"\",\"a2\":\"\",\"noise level\":\"\"}}. Here, \"m1\" is the slope of the relationship and \"a1\" is the intercept in the \"x\" axis direction and both should be floats. Additionally, \"m2\" is the slope of the relationship and \"a2\" is the intercept in the \"y\" axis direction and both should be floats. The \"noise level\" parameter should be the relative amount of noise added to the linear function for the relationship and should be a float between 0 and 1.",
        "What are the parameters for the gaussian mixture model relationship between the x and y values in this figure? please format the output as a json as {\"gmm parameters\":{\"nsamples\":\"\",\"nclusters\":\"\",\"centers\":\"\",\"cluster_std\":\"\",\"noise level\":\"\"}}. Each \"nsamples\" is the number of samples in the distribution and should be an integer. The \"nclusters\" parameter should be the number of clusters in the model and should be an integer. The \"centers\" parameter should be the position of each cluster and should be a list of points which are floats. The \"cluster_std\" parameter should be the standard deviation of each cluster and should be a list of points which are floats. The \"noise level\" parameter should be the relative amount of noise added to the model and should be a float between 0 and 1. If it is not a gaussian mixture model, please do not try to answer the question",
        "What are the parameters for the gaussian mixture model relationship between the x and y values in this figure and the colors of the scatter points? You are a helpful assistant, please format the output as a json as {\"colors\":\"\"} where the value is either \"random\" for randomly colored points or \"by cluster\" if the points from each gaussian mixure model cluster are colored by cluster membership.",
        # "What is the y-axis label? Please format the output as a json as \"ylabel\":\"\".",
        # "What is the color of the bars? The answer should be in the form of a single RGBA tuple. please format the output as a json as \"bar color\":\"\".",
        # "What are the locations of the bars? please format the output as a json as {\"left\":[], \"right\":[], \"center\",[], \"height\":[]} where the values of \"left\" and \"right\" are the left and right edges of each bar, and \"center\" is the center of each bar, all in terms of the x-axis values. Additionally, \"height\" is the location of the top of each bar and should be in terms of the y-axis values.",
        # "Are there error bars on the data along the x-axis in this figure? please format the output as a json as {\"x-axis errors\":\"\"} where the value for the output is True (if error bars exist) or False (if error bars do not exist). ",
        # "Are there error bars on the data along the y-axis in this figure? please format the output as a json as {\"y-axis errors\":\"\"} where the value for the output is True (if error bars exist) or False (if error bars do not exist). ",

        # "What is the distribution used to create the histogram? please format the output as a json as {\"distribution\":\"\"} the value is a string.",
        # "What are the parameters for the linear distribution used to create the histogram? please format the output as a json as {\"linear distribution\":{\"m\":\"\",\"a\":\"\",\"noise level\":\"\"}}. Here, \"m\" is the slope of the relationship and \"a\" is the intercept and both should be floats. The \"noise level\" parameter should be the relative amount of noise added to the linear function for the relationship and should be a float between 0 and 1. If this is not a linear relationship, please do not try to answer the question",
        # "What are the parameters for the gaussian mixture model distribution used to create the histogram? please format the output as a json as {\"gmm parameters\":{\"nsamples\":\"\",\"nclusters\":\"\",\"centers\":\"\",\"cluster_std\":\"\",\"noise level\":\"\"}}. Each \"nsamples\" is the number of samples in the distribution and should be an integer. The \"nclusters\" parameter should be the number of clusters in the model and should be an integer. The \"centers\" parameter should be the position of each cluster and should be a list of points which are floats. The \"cluster_std\" parameter should be the standard deviation of each cluster and should be a list of points which are floats. The \"noise level\" parameter should be the relative amount of noise added to the model and should be a float between 0 and 1. If it is not a gaussian mixture model, please do not try to answer the question"
        
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
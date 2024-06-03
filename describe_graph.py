import ollama
import os

def open_image(directory):
    for filename in os.listdir(directory):
        if filename.endswith(".png"):
            image_path = os.path.join(directory, filename)
            describe_graph(image_path)
        
def describe_graph(image_path):


    try:
        response = ollama.chat(model=model,messages=[
        # {
        #   "role": "system",
        #   "content": "You are being fed a number of "
        # },
        {
        "role": "user",
        "content": f"Please describe the following scientific graph in as much detail as possible:",
        'images': [image_path]
        },
        {
        "role": "user",
        "content": f"Based on your previous answer please describe the scientific graph again in as much detail as possible. If included in the graph be sure to state information about x-axis, y-axis, plots, lines, title, data values, and captions:",
        'images': [image_path]
        },

        ],
        options = {
        'temperature': 0
        })

    except ollama.ResponseError as e:
        print('Error:', e.error)
        if e.status_code == 404:
            print(f"Pulling model via ollama:")
            ollama.pull(model)

    

    print(response)


if __name__ == '__main__':
    base_url="https://87c6-34-81-234-196.ngrok-free.app"
    
    directory = 'data'
    model = 'llava:13b'
    open_image(directory)
     
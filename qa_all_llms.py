# use L4 colab or else it will time out w more complex qs
import os
import json
import asyncio

from llm.llm_histogram_qa import main as process_histogram
# from llm.llm_linear_qa import main as process_linear
from llm.llm_plot_qa import main as process_plot
from llm.llm_scatter_qa import main as process_scatter

async def process_image_scripts(image_path):
    results = {}
    try:
            results['histogram'] = await asyncio.wait_for(process_histogram(image_path), timeout=200)
    except asyncio.TimeoutError:
        results['histogram'] = 'Timeout'
    
    # try:
    #     results['linear'] = await asyncio.wait_for(process_linear(image_path), timeout=200)
    # except asyncio.TimeoutError:
    #     results['linear'] = 'Timeout'
    
    try:
        results['plot'] = await asyncio.wait_for(process_plot(image_path), timeout=200)
    except asyncio.TimeoutError:
        results['plot'] = 'Timeout'
    
    try:
        results['scatter'] = await asyncio.wait_for(process_scatter(image_path), timeout=200)
    except asyncio.TimeoutError:
        results['scatter'] = 'Timeout'


    return results

async def main():
    folder_path = "data"
    output_folder = "results" 
    final_folder = os.path.join(output_folder, "final")

    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    image_files = [f for f in os.listdir(folder_path) if f.lower().endswith(('.png'))]

    for image_file in image_files:
        image_path = os.path.join(folder_path, image_file)
        print(f"Processing {image_path}...")
        results = await process_image_scripts(image_path)
        
        for key, data in results.items():
            result_file = f"{os.path.splitext(image_file)[0]}_{key}_llm.json"
            result_path = os.path.join(output_folder, result_file)
            with open(result_path, 'w') as f:
                json.dump(data, f, indent=4)
            print(f"Saved results to {result_path}")

    combined_results = {}
    for file_name in os.listdir(output_folder):
        if file_name.endswith("_llm.json"):
            base_name = file_name.split('_')[0]
            if base_name not in combined_results:
                combined_results[base_name] = {}

            file_path = os.path.join(output_folder, file_name)
            with open(file_path, 'r') as f:
                data = json.load(f)

            key = file_name.split('_')[1]  
            combined_results[base_name][key] = data

    for base_name, data in combined_results.items():
        combined_file_path = os.path.join(final_folder, f"{base_name}.json")
        with open(combined_file_path, 'w') as f:
            json.dump(data, f, indent=4)
        print(f"Saved combined results to {combined_file_path}")

if __name__ == "__main__":
    asyncio.run(main())
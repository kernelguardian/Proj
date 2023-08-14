import os
import json
import pandas as pd
import csv

export = []


def process_json_data(data):
    if isinstance(data, dict):
        # Remove keys with name "bgColor"
        data = {
            k: process_json_data(v)
            for k, v in data.items()
            if k not in ["bgColor", "fgColor"]
        }

    elif isinstance(data, list):
        data = [process_json_data(item) for item in data]
    elif isinstance(data, (int, float)):
        # Round off number values
        data = int(data)  # Change 2 to the desired decimal places
    return data


def process_json_files(folder_path):
    for filename in os.listdir(folder_path):
        if filename.endswith(".json"):
            file_path = os.path.join(folder_path, filename)
            with open(file_path, "r") as file:
                data = json.load(file)
                print(f"Processing {filename}:")
                operation(data, file_path)
                # break


def operation(data, f_name):
    # i = 0
    lastHTML = ""

    # print(data.keys())
    # print(data["utterance"])
    # print(data["taskName"])

    for state in data["states"]:
        # print(state.keys())
        # print(state.keys())
        row = {}
        row["filename"] = f_name
        row["instruction"] = data["utterance"]
        row["basehtml"] = process_json_data(state["dom"])
        # print(state["dom"].keys())

        row["output"] = state["action"]

        export.append(row)
        # i = i + 1
        # if i >= 10:
        #     break


# Replace 'folder_path' with the path to your folder containing JSON files
folder_path = "demonstrations/demonstrations"
process_json_files(folder_path)


df = pd.DataFrame(export)
# Specify the output Excel file name
output_file = "dataset/statelessDataset"
# Write the DataFrame to Excel
df.to_csv(output_file, index=False)
# df.to_excel(output_file, index=False)

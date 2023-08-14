import os
import json
import pandas as pd
import csv

export = []


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

        row = {}
        row["filename"] = f_name
        row["instruction"] = data["utterance"]
        row["basehtml"] = state["dom"]
        if state["action"] is None:
            row["output"] = " "

        else:
            stringified_state_action = json.dumps(state["action"])
            stringified_last_html = json.dumps(lastHTML)
            # print(stringified_last_html[-25:])

            row["output"] = stringified_state_action + "\n" + stringified_last_html
            # print(row["output"][:25])
            lastHTML = row["basehtml"]
            # print(row)
        export.append(row)
        # i = i + 1
        # if i >= 10:
        #     break


# Replace 'folder_path' with the path to your folder containing JSON files
folder_path = "demonstrations/demonstrations"
process_json_files(folder_path)


df = pd.DataFrame(export)
# Specify the output Excel file name
output_file = "dataset/statefulDataset"

# Write the DataFrame to Excel
df.to_csv(output_file, index=False)
# df.to_excel(output_file, index=False)

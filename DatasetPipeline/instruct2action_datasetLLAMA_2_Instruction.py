import pandas as pd
from sklearn.model_selection import train_test_split

df = pd.read_csv("dataset/statelessDataset")
# df = df.fillna("")

text_col = []


def output_cleaner(output):
    # print(type(output), output)

    if str(output) == "nan":
        output = ""
        return str(output)
    # global i

    # if i == 100:
    #     exit()
    # else:
    #     i += 1

    output = eval(output)
    if (
        output["type"] == "mousedown"
        or output["type"] == "click"
        or output["type"] == "mouseup"
    ):
        # print(output)
        data = output["type"]

        # pass
    elif output["type"] == "scroll":
        data = "scroll"

    elif output["type"] == "dblclick":
        data = "dblclick"

    else:
        # print(output)
        data = output["type"] + ":" + str(output["charCode"])

    return str(data)


for _, row in df.iterrows():
    prompt = "Below is an instruction that describes a website task, paired with an input which is an html structure of the website. Write an appropriate response that is an action performed on the html structure to achieve the website task successfully and it should be in the format {action}:{number} if there is a number of just {action} \n\n"

    instruction = str(row["instruction"])
    input_query = str(row["basehtml"])
    response = output_cleaner(str(row["output"]))
    # print(response)
    if response == "nan":
        # print(type(response), response)
        response = "{}"
        # print(type(response), response)

    text = (
        prompt
        + "### Instruction:"
        + instruction
        + "\n### Input:"
        + input_query
        + "\n### Response:"
        + response
    )

    text_col.append(text)

df.loc[:, "text"] = text_col

print(df.head())

print("\n Shuffling and separating test and train set")
# Shuffle the DataFrame
shuffled_df = df.sample(
    frac=1, random_state=42
)  # Setting random_state for reproducibility

# Split the shuffled DataFrame into test and train sets
test_ratio = (
    0.2  # Adjust the ratio based on your requirement (e.g., 0.2 for 20% test data)
)
train_df, test_df = train_test_split(shuffled_df, test_size=test_ratio, random_state=42)


train_df.to_csv("dataset/upload/instruct2action_instruction/train.csv", index=True)
test_df.to_csv("dataset/upload/instruct2action_instruction/test.csv", index=True)


train_df.to_excel("dataset/upload/instruct2action_instruction/train.xlsx")
test_df.to_excel("dataset/upload/instruct2action_instruction/test.xlsx")


import pandas as pd
import datasets
from datasets import Dataset, DatasetDict


tds = Dataset.from_pandas(train_df)
tds = Dataset.from_pandas(test_df)


ds = DatasetDict()

ds["train"] = tds
ds["validation"] = tds

print(ds)

ds.push_to_hub("kernelguardian/instruct2action_instruction")

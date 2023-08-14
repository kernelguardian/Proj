import pandas as pd
from sklearn.model_selection import train_test_split

df = pd.read_csv("dataset/statelessDataset")
# df = df.fillna("")


instructions = []
responses = []
i = 0


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

    instruction = str(row["instruction"])

    input_query = str(row["basehtml"])

    instructions.append(instruction + "\n" + input_query)

    response = output_cleaner(row["output"])

    if response == "nan":
        # print(type(response), response)
        response = "{}"
        # print(type(response), response)

    responses.append(response)

data = {"dialogue": instructions, "summary": responses}

df = pd.DataFrame(data)


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


train_df.to_csv("dataset/upload/instruct2action/train.csv", index=True)
test_df.to_csv("dataset/upload/instruct2action/test.csv", index=True)


train_df.to_excel("dataset/upload/instruct2action/train.xlsx")
test_df.to_excel("dataset/upload/instruct2action/test.xlsx")


import pandas as pd
import datasets
from datasets import Dataset, DatasetDict


tds = Dataset.from_pandas(train_df)
tds = Dataset.from_pandas(test_df)


ds = DatasetDict()

ds["train"] = tds
ds["validation"] = tds

print(ds)

ds.push_to_hub("kernelguardian/instruct2action")

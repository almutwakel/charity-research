# Almutwakel Hassan
# Charity Data Research Project
# Using a dataset of survey responses

import pandas as pd
import numpy as np
import openpyxl
import liwc
import re
import nltk
import json
import torch
from torch.utils.data import Dataset
# from transformers import pipeline, DistilBertTokenizerFast, Trainer, TrainingArguments, AutoModelForSequenceClassification

# Preprocessing Variables
rows = 536
bag_columns = ["Q5Mean", "Q7"]
liwc_columns = ["Q5Mean", "Q7", "WC"]
GFM_columns = ["Url", "Title", "Text", "Donation", "Goal", "Time"]


class LIWCDataset(Dataset):
    def __init__(self, encodings, labels):
        self.encodings = encodings
        self.labels = labels

    def __getitem__(self, id):
        # item = {key: torch.tensor(val[id]) for key, val in self.encodings.items()}
        # item['labels'] = torch.tensor(self.labels[id])
        # return item
        return self.labels[id]

    def __len__(self):
        return len(self.labels)


def preprocess_data(np_type="raw"):
    print("Preprocessing.")
    # import dataset
    if np_type == "numeric":
        raw = pd.read_excel("DATA/liwc_filtered.xlsx", sheet_name="Sheet0").to_numpy()
        processed = np.delete(raw, 1, 1)
        processed2 = np.delete(processed, 376, 0)
        return processed2
    elif np_type == "text":
        raw = pd.read_excel("DATA/liwc_filtered.xlsx", sheet_name="Sheet0")
        processed = raw["Q7"]
        return processed
    elif np_type == "raw":
        raw = pd.read_excel("DATA/liwc_filtered.xlsx", sheet_name="Sheet0")
        # processed = raw.head(rows)
        return raw
    # take first half of data rows and only needed columns


def preprocess_data_GFM(filepath):
    print("Preprocessing GFM data.")
    raw = pd.read_csv(filepath)
    return raw


def bag_of_words(df, textfield, valuefield, save=False, filename="bagofwords.json"):
    print("Starting bag of words algorithm.")
    bag = {}

    # function f to add new words to the bag
    def f(amount, response):
        words_list = nltk.word_tokenize(response)
        # used_words array to delete duplicates from same article
        used_words = []
        for word in words_list:
            word = re.sub(r'[^a-zA-Z]', '', word).lower()
            if len(word) <= 1 or word in used_words:
                continue
            elif word in bag:
                bag[word]["count"] += 1
                bag[word]["total"] += amount
            else:
                bag[word] = {"count": 1, "total": amount}
            used_words.append(word)

    # run function f on each row
    [f(x, y) for x, y in zip(df[valuefield], df[textfield])]

    words = []
    count = []
    sum_value = []
    mean = []
    for word in bag:
        words.append(word)
        count.append(bag[word]["count"])
        mean.append(bag[word]["total"]/bag[word]["count"])

    bag_df = pd.DataFrame({"word": words, "count": count, "mean": mean})

    if save:
        with open("DATA/" + filename, "w+") as file:
            json.dump(bag, file)
    return bag_df


def analyze_bag(df):
    x = 30  # show top x rows
    minimum = 50  # minimum count for data analysis
    df_filtered_minimum = df[df["count"] >= minimum]

    # data insights from saved bag dataframe
    # sorted by occurrence count
    df1 = df_filtered_minimum.sort_values(by=["count", "mean"], ascending=False)
    # print("highest occurrences", df1.head(x))
    # sorted by average donation value
    df2 = df_filtered_minimum.sort_values(by=["mean", "count"], ascending=False)
    df2.set_index('word', inplace=True)
    print("average donation value", df2.head(x))
    total = len(df)
    print("total words:", total)
    # for n in range(1, 10):
    #    val = len(df[df["count"] == n])
    #    print(str(n) + "-occurrence:", val, "(" + str(round(val/total*100, 2)) + "%)")

## not used:
# def neuralnet():
#    device = torch.device('cuda') if torch.cuda.is_available() else torch.device('cpu')
#    numeric = preprocess_data(np_type="numeric")
#    text = preprocess_data(np_type="text")
#
#    model_id = "distilbert-base-uncased-finetuned-sst-2-english"
#    # model = pipeline("text-classification", model=model_id)
#    model = AutoModelForSequenceClassification.from_pretrained(model_id)
#    # model.to(device)
#    tokenizer = DistilBertTokenizerFast.from_pretrained(model_id)
#
#    def tokenize_function(examples):
#        return tokenizer(examples, padding="max_length", truncation=True)
#
#    text = text.map(tokenize_function)
#
#    train_text, train_label = text[:535], numeric[:535, :]
#    test_text, test_label = text[536:], numeric[536:, :]
#    # train_encodings = tokenizer(train_text)
#    # test_encodings = tokenizer(test_text)
#
#    trainset = LIWCDataset(train_text, train_label)
#    testset = LIWCDataset(test_text, test_label)
#
#    training_args = TrainingArguments("test_trainer")
#
#    trainer = Trainer(
#        args=training_args,
#        model=model,
#        train_dataset=trainset,
#        eval_dataset=testset
#    )
#
#    trainer.train()
#    trainer.evaluate()
#    results = model(text)
#    print(results)
#    return model


if __name__ == '__main__':
    print("Start.")
    # # bag of words method
    # data = preprocess_data(rows, numeric=True)
    # bag_data = bag_of_words(data, save=False, valuefield="Q5Mean", textfield2="Q7")
    # analyze_bag(bag_data)

    # # GoFundMe Data
    # gfm_data = pd.read_csv("DATA/scraped_links.csv")
    # gfm_bag = bag_of_words(gfm_data, textfield="Text", valuefield="Donation", save=True, filename="GFM_Bag.json")
    # analyze_bag(gfm_bag)



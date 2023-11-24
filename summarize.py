
from transformers import pipeline

# Open and read the file
with open('input.txt', 'r') as file:
    data = file.read()

classifier = pipeline(
    model="kabita-choudhary/finetuned-bart-for-conversation-summary", task="summarization")


def GetSummary(data):
    # Use the read data as input to the classifier
    res = classifier(data)
    return res[0]['summary_text']

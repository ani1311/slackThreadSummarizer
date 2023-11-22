from transformers import pipeline

# Open and read the file
with open('input.txt', 'r') as file:
    data = file.read()

classifier = pipeline(model="kabita-choudhary/finetuned-bart-for-conversation-summary", task="summarization")

# Use the read data as input to the classifier
res = classifier(data)

print(res)

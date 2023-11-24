from transformers import pipeline
import os
from slack_bolt import App
from flask import Flask, request, jsonify, Response
import json
from queue import Queue
from threading import Thread
from summarizeEvent import *

# Create a queue
summaryQueue = Queue()

app = Flask(__name__)


@app.route('/slack/events', methods=['POST'])
def slackEvents():
    data = request.get_json()
    if "challenge" in data:
        return jsonify({"challenge": data["challenge"]})
    else:
        prettyJson = json.dumps(request.get_json(), indent=4)
        print(prettyJson)

        eventData = data['event']
        user = eventData['user']
        channel = eventData['channel']
        eventTs = eventData['event_ts']
        eventSummary = SummarizeEvent(user, channel, eventTs)
        print(eventSummary)

        summaryQueue.put(eventSummary)

        return (Response(), 204)


def processor():
    # Create a summarizer
    summarizer = pipeline("summarization")
    while True:
        event = summaryQueue.get()
        event.SendSummaryToUser()
        print(event)

        summaryQueue.task_done()


if __name__ == "__main__":
    Thread(target=processor).start()

    # app.start()
    app.run(debug=True, port=3000)

import os
from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError
import pprintpp
from summarize import *

client = WebClient(base_url="https://testingcompan-88a1386.slack.com/api/",
                   token=os.environ['SLACK_BOT_TOKEN'])


def getUserName(userId):
    try:
        response = client.users_info(user=userId)
        return response.data['user']['real_name']
    except SlackApiError as e:
        print(f"Error: {e}")
        return


def conversationToString(conversation):
    text = ""
    for msg in conversation:
        text += f"{msg[0]}: {msg[1]}\n"
    return text


def replaceUserIdWithNameInText(text):
    # Replace user ids with names
    for word in text.split():
        if word.startswith("<@"):
            userId = word[2:-1]
            userName = getUserName(userId)
            text = text.replace(word, userName)
    return text


def getThread(channel, thread_ts):
    conversation = []
    try:
        response = client.conversations_replies(
            channel=channel, ts=thread_ts)
        for msg in response.data["messages"]:
            userName = getUserName(msg['user'])
            conversation.append(
                [userName, replaceUserIdWithNameInText(msg['text'])])
        return conversation
    except SlackApiError as e:
        print(f"Error: {e}")
        return


class SummarizeEvent:
    def __init__(self, user, channel, event_ts):
        self.user = user
        self.channel = channel
        self.event_ts = event_ts

    def __str__(self):
        return f"User: {self.user}, Channel: {self.channel}, Timestamp: {self.event_ts}"

    def getThreadTimestamp(self):
        try:
            resp = client.conversations_replies(
                channel=self.channel, ts=self.event_ts)

            thread_ts = None
            # Check if the message has a thread_ts
            for msg in resp.data["messages"]:
                if 'thread_ts' in msg:
                    thread_ts = msg['thread_ts']
                    return thread_ts
        except SlackApiError as e:
            print(f"Error: {e}")
            return None

    def getSummary(self):
        thread_ts = self.getThreadTimestamp()
        if thread_ts == None:
            return None

        conversation = getThread(self.channel, thread_ts)
        if conversation == None:
            return None

        conversationText = conversationToString(conversation)
        print(conversationText)
        summary = GetSummary(conversationText)
        print(summary)
        return summary

    def SendSummaryToUser(self):
        summary = self.getSummary()
        if summary == None:
            return None

        try:
            response = client.chat_postMessage(
                channel=self.user, text=summary)
            return response
        except SlackApiError as e:
            print(f"Error: {e}")
            return None

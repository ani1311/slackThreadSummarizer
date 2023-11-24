# SlackThreadSummarizer

## Model used

<https://huggingface.co/kabita-choudhary/finetuned-bart-for-conversation-summary>

## TestingCompany Token


## Steps

1. Add bot mention event. We will add `app_mentioned` event: <https://api.slack.com/automation/triggers/event#response-object>

2. Use message ts to get the thread: <https://api.slack.com/methods/conversations.replies>. If is empty, then it is not a thread don't do anything.

3. Summarize the thread using the model.

4. Reply to the thread with the summary. <https://api.slack.com/messaging/sending#threading>

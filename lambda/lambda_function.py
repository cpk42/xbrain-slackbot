"""
Slack chat-bot Lambda handler.
"""

import os
import logging
import urllib

# Grab the Bot OAuth token from the environment.
BOT_TOKEN = os.environ["BOT_TOKEN"]

# Define the URL of the targeted Slack API resource.
SLACK_URL = None # "https://slack.com/api/chat.postMessage"

def lambda_handler(event, context):
    # TODO implement
    slack_event = data['event']
    if "bot_id" in slack_event:
        logging.warn("Ignore bot event")
    else:
        text = slack_event["text"]
        channel_id = slack_event["channel"]
        
        response = None # TODO : hit NLP API
        # TODO : decode response
        found_comments = None # TODO : FIND COMMENT
        
        data = urllib.parse.urlencode(
            (
                ("token", BOT_TOKEN),
                ("channel", channel_id),
                ("text", found_comments)
            )
        )
        data = data.encode("ascii")
        request = urllib.request.Request(
            SLACK_URL, 
            data=data, 
            method="POST"
        )
        # Add a header mentioning that the text is URL-encoded.
        request.add_header(
            "Content-Type", 
            "application/x-www-form-urlencoded"
        )
        
        # Fire off the request!
        urllib.request.urlopen(request).read()

    # Everything went fine.
    return "200 OK"


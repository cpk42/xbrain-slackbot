# **************************************************************************** #
#                                                                              #
#                                                         :::      ::::::::    #
#    xbrainbot.py                                       :+:      :+:    :+:    #
#                                                     +:+ +:+         +:+      #
#    By: ckrommen <marvin@42.fr>                    +#+  +:+       +#+         #
#                                                 +#+#+#+#+#+   +#+            #
#    Created: 2018/08/27 16:58:08 by ckrommen          #+#    #+#              #
#    Updated: 2018/08/27 16:58:46 by ckrommen         ###   ########.fr        #
#                                                                              #
# **************************************************************************** #

import os
import time
import re
import requests
from slackclient import SlackClient

slack_client = SlackClient(os.environ.get('SLACK_BOT_TOKEN'))
xbrainbot_id = None

URL = "https://1mg1v0jpv0.execute-api.us-west-2.amazonaws.com/dev/xbrain-handler/"
GETR = "http://localhost/"
RTM_READ_DELAY = 1
EXAMPLE_COMMAND = "hello"
MENTION_REGEX = "^<@(|[WU].+?)>(.*)"
data= None

#Parses a list of events coming from the Slack RTM API to find bot commands.
#If a bot command is found, this function returns a tuple of command and channel.
#If its not found, then this function returns None, None.

def parse_bot_commands(slack_events):
    for event in slack_events:
        if event["type"] == "message" and not "subtype" in event:
            user_id, message = parse_direct_mention(event["text"])
            if user_id == xbrainbot_id:
                return message, event["channel"]
    return None, None


def parse_direct_mention(message_text):
    matches = re.search(MENTION_REGEX, message_text)
    # the first group contains the username, the second group contains the remaining message
    return (matches.group(1), matches.group(2).strip()) if matches else (None, None)


def handle_command(command, channel):
    default_response = "Not sure what you mean. Try *{}*.".format(EXAMPLE_COMMAND)
    response = None
    data = {"event":{"text":command,"channel":channel}}
    # Need to verify that the command passed in is referenced from the dataset, if so
    # send a POST request to the lambda server with the query, and return the solution
    # with a get request
    # ------Must be done after model data is stored somewhere useable such as
    # ------MySQLlite databse or clour server
    if command.startswith(EXAMPLE_COMMAND):
            response = "Suh dude"
            r = requests.post(url=URL, json=data)
            print(r.status_code, r.reason, r.json())
    else:
        slack_client.api_call (
            "chat.postMessage",
            channel=channel,
            text=response or default_response
        )

if __name__ == "__main__":
    if slack_client.rtm_connect(with_team_state=False):
        print("Starter Bot connected and running!")
        # Read bot's user ID by calling Web API method `auth.test`
        xbrainbot_id = slack_client.api_call("auth.test")["user_id"]
        while True:
            command, channel = parse_bot_commands(slack_client.rtm_read())
            if command:
                handle_command(command, channel)
            time.sleep(RTM_READ_DELAY)
    else:
        print("Connection failed. Exception traceback printed above.")

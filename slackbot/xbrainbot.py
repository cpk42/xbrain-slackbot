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
from flask import (
    Flask,
    render_template,
    request
)

slack_client = SlackClient(os.environ.get('SLACK_BOT_TOKEN'))
xbrainbot_id = None

URL = "https://1mg1v0jpv0.execute-api.us-west-2.amazonaws.com/dev/xbrain-handler/"
RTM_READ_DELAY = 1
EXAMPLE_COMMAND = "hello"
MENTION_REGEX = "^<@(|[WU].+?)>(.*)"
data= None

# app = Flask(__name__, template_folder=".")
# @app.route('/process')
# def home():
#     return render_template('home.html')
#Parses a list of events coming from the Slack RTM API to find bot commands.
#If a bot command is found, this function returns a tuple of command and channel.
#If its not found, then this function returns None, None.
phrase = "importing requests package into AWS lambda function runtime"

respond1 = 'requests package'
respond2 = 'AWS lambda function runtime'

respond3 = 'ruby gem'
respond4 = 'docker image'

respond5 = 'settings'
respond6 = 'ubuntu'

import pymysql
connection = pymysql.connect(host='35.233.149.140',
                             user='cpk42',
                             password='xbrainhacks',
                             db='train_data')

#<answer answer_id="5524" group="2136" isElectedAnswer="0" text="&lt;p&gt;It seems fine by me. I would say that the structure is fully normalized.&lt;/p&gt;&#10;" />
class Parsed:
    def __init__(self, answer_id, group_id, isElected, text, found):
        self.answer_id = answer_id
        self.group_id = group_id
        self.isElected = isElected
        self.text = text
        self.found = found

def match_answer(array):
    possible = []
    array = array.split()
    cursor = connection.cursor()
    sql = "SELECT * FROM answers"
    cursor.execute(sql)
    for row in cursor:
        found = 0
        for item in array:
            if row[3].lower().find(item.lower()) != -1:
                found += 1
        if found > 0:
            ans = Parsed(row[0], row[1], row[2], row[3], found)
            possible.append(ans)
    possible.sort(key=lambda x: x.found, reverse=True)
    return possible[0:3]


# ret = match_answer(respond1.split() + respond2.split())
# ret1 = match_answer(respond3.split() + respond4.split())
# ret2 = match_answer(respond5.split() + respond6.split())
#
#
# for item in ret:
#     print item.text
#     print "\n"
# print "\n\n"
# for item in ret1:
#     print item.text
#     print "\n"
# print "\n\n"
# for item in ret2:
#     print item.text
#     print "\n"
# print "\n\n"





#----------------------------------------------------------
#Slackbot initialization-----------------------------------
#----------------------------------------------------------

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
    if command.lower() == 'hello' or command.lower() == 'hi':
        slack_client.api_call (
            "chat.postMessage",
            channel=channel,
            text="Greetings"
        )
    elif command.lower() == 'what is the meaning of life?' or command.lower() == 'what is the meaning of life' or command.lower() == 'meaning of life':
        slack_client.api_call (
            "chat.postMessage",
            channel=channel,
            text="42"
        )
    elif command:
            p = requests.post(url=URL, json=data)
            # print(r.status_code, r.reason, r.json())
            payload = {"question": command}
            r = requests.get("https://1mg1v0jpv0.execute-api.us-west-2.amazonaws.com/dev/process", json=payload)
            ret = match_answer(r.json())
            for item in ret:
                print item.text, "\n\n"
            buckets = []
            bestAnswers = []
            toggle = 0
            electedAnswer = ""
            for item in ret:
                if item.isElected and toggle == 0:
                    electedAnswer = item
                    toggle = 1
                buckets.append(item.group_id)
                bestAnswers.append(item.answer_id)
            finalData = {"electedAnswer": electedAnswer, "buckets": buckets, "bestAnswers": bestAnswers}
            p = requests.post(url=URL, json=finalData)
    else:
        slack_client.api_call (
            "chat.postMessage",
            channel=channel,
            text=response or default_response
        )
# app.run(debug=True)
# g = request.data("question")
# print g.status_code, g.reason, g.json()
if __name__ == "__main__":
    if slack_client.rtm_connect(with_team_state=False):
        print("Starter Bot connected and running!")
        # Read bot's user ID by calling Web API method `auth.test`
        xbrainbot_id = slack_client.api_call("auth.test")["user_id"]
        while True:
            # payload = {'key1': 'value1', 'key2': 'value2'}
            # r = requests.get('localhost:5000', params=payload)
            command, channel = parse_bot_commands(slack_client.rtm_read())
            if command:
                handle_command(command, channel)
            time.sleep(RTM_READ_DELAY)

    else:
        print("Connection failed. Exception traceback printed above.")

connection.close()

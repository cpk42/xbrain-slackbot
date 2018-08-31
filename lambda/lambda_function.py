"""
Slack chat-bot Lambda handler.
"""

import os
import six
import urllib
import logging
from botocore.vendored import requests 
from google.cloud.language import enums, types
from google.cloud import automl_v1beta1, language
from google.cloud.automl_v1beta1.proto import service_pb2

BOT_TOK = os.environ['BOT_TOK']
SLK_URL = os.environ['SLK_URL']
GCP_TOK = os.environ['GOOGLE_APPLICATION_CREDENTIALS']
GCP_URL = os.environ['GCP_URL']
PROJ_ID = os.environ['PROJ_ID']
MODL_ID = os.environ['MODL_ID']

DB = None # connect to db

def entities_text(text):
    """Detects entities in the text."""
    client = language.LanguageServiceClient()

    if isinstance(text, six.binary_type):
        text = text.decode('utf-8')

    # Instantiates a plain text document.
    document = types.Document(
        content=text,
        type=enums.Document.Type.PLAIN_TEXT)

    # Detects entities in the document. You can also analyze HTML with:
    #   document.type == enums.Document.Type.HTML
    entities = client.analyze_entities(document).entities

    # entity types from enums.Entity.Type
    entity_type = ('UNKNOWN', 'PERSON', 'LOCATION', 'ORGANIZATION',
                   'EVENT', 'WORK_OF_ART', 'CONSUMER_GOOD', 'OTHER')

    result = []
    for entity in entities:
        e = entity.name.split()
        result.append(e)
        print('=' * 20)
        print(u'{:<16}: {}'.format('name', entity.name))
        print(u'{:<16}: {}'.format('type', entity.type))
        print(u'{:<16}: {}'.format('metadata', entity.metadata))
        print(u'{:<16}: {}'.format('salience', entity.salience))
        print(u'{:<16}: {}'.format('wikipedia_url',
              entity.metadata.get('wikipedia_url', '-')))
    return result

def get_prediction(content):
    '''
    makes a query to our 
    '''
    prediction_client = automl_v1beta1.PredictionServiceClient()
    name = 'projects/{}/locations/us-central1/models/{}'.format(PROJ_ID, MODL_ID)
    payload = {'text_snippet': {'content': content, 'mime_type': 'text/plain' }}
    params = {}
    request = prediction_client.predict(name, payload, params)
    return request  # waits till request is returned

def lambda_handler(data, context):
    '''
    performs four separate requests:
        1. two to google automl natural language API
        to parse @category && @keywords for the
        question

        2. one request is made to cloud SQL using the
        previously parsed information in order to 
        collect valid answers for the question

        3. one requests is made to our xbrian slackbot
        to print the elected answer
    '''

    if 'event' in data:
        slack_event = data['event']
    else:
        return '500 InvalidAction, please supply {\'event\':{\'text\':...},...}'
    if "bot_id" in slack_event:
        logging.warn("Ignore bot event")
    else:
        text = slack_event["text"]
        channel_id = slack_event["channel"]

        # returns a matching category
        # from the question
        response = get_prediction(text)

        score = 0.0
        category = None
        # parse reponse for matching category
        for item in response.payload:
            if item.classification.score > score:
                score = item.classification.score
                category = item.display_name
               
        # get entities from question
        result = entities_text(text)

#        print(result)                  # debug

        l = []
        for item in result:
            l.append(' '.join(item))
#        print(l)                       # debug
        keywords = ' '.join(l)

        # TODO : db query for all
        # questions in category
        answer = 'no answer found'

        data = {'token':BOT_TOK,'text':'The question is: '+text+' , and the answer is: '+answer,'desc':'None'}

        r = requests.post(SLK_URL, json=data)
        
    # Everything went fine.
    return "200 OK"


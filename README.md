# ![stack](stackoverflow.png)bot**overflow**

## Context

Searching information into large specialized databased is a main challenge in industry. 

Lots of large datasets are generally available but simple search engines suffer from a lack of quality in order to provide the right results. 

Developers usually search online developer website for finding same issues from previous users with a potential answer.


## Goal

Make the best answer search and selection engine using a Stack Overflow dataset dump (the dataset is provided), the system will be connected through an API and a SlackBot.

At the end of the Hackathon, the participants will learn:
* Natural Language Processing: how to perform semantic search and use Deep Learning
* API: how to communicate with APIs, and create your own API
* Chat bot: how to provide an end to end system that provide answers to user requests.

## What you need to use this repo

git-lfs is requiered to clone the repository with the data. You can install the tool from [github] (https://git-lfs.github.com/)

## Slack

You can join the [dedicated slack channel](https://join.slack.com/t/xbrain-hackathon-42/shared_invite/enQtNDIzMDI4NDk2MTE3LWFiZmJkODczODQxN2JlZGZjMjFjNDExNjM1ZTIwYWE1Y2RhNzg2N2Y1MDZmMDVkZmMwMDIxMTA4MWUzNzQ1YmI) to ask questions and get information.

## Steps

1. build a module that will match a user question with a bucket of answer. To perform this task, you may train a model that will learn how to match a post title (with description is optional) with a bucket of answers.
2. build a model, based on ML/DL, that will find the answer inside this bucket of answers
3. build an API and a slack channel on top of that
	API will accept a question, and return the best response
	Slack channel will accept user messages, and replies into the channel
4. give the ability for non-English speakers to use the system. 

## Evaluation System

Each module/step will be reviewed to ensure that: 
* the software design matches the requirements 
* the code is awesome.

The team will be asked to introduce itself, present their project, the solution used for each module and what they learned during this hackathon.

At the end of the hackathon, please push your code on a dedicated branch named after your group name.

## Additional Rules

* Main language must be python
* Participants must use the provided dataset. They are able to train the system on a specific dataset (train) and evaluate the quality of the system on another one (dev).
* Participants can use any other resources available except resources from Stack Overflow.
* Participants must provide the list of the external resources they used in their system.

## Dataset

You'll find inside the data folder, a data.tar.gz file that contains the training set and the validation set.

Use this data to train your model. As a reminder, a question should match a bucket of answer.

## API 

You must provide a REST API, that will give us the ability to benchmark your system automaticaly.

The REST API should expose a "process" endpoint, like: http://localhost/process
This endpoint uses the POST method, and accepts a json object in its body:
{
    "question":"question of the user"
}

The response will return several elements:

* electedAnswer: The answer to question
* buckets: One array (ids) of the top answer buckets
* bestAnswers: One array (ids) of the elected answers. Elected answers can belong to any answer bucket.

Here's the structure of this object:

```json
{
    "electedAnswer":"the answer to the question",
    "buckets" : [32, 56, 12],
    "bestAnswers":[ 453, 543, 678 ]
}
```

## Evaluation

You can evaluate the quality of your system by checking the directory [scoring](scoring/) and the associated [README](scoring/README.md).

During the final evaluation, a test.xml will be provided during the week, but be careful, all the "isSelectedAnswer" in the xml file will be at 0,
and `question_id=` of the questions and `group` from the answers will be ramdomized.
The only information available will be if N answers are coming from the same `group`.

The final evaluation over the API will have to return the electedAnswer, buckets ids and the bestAnswers id from the `test.xml` file.

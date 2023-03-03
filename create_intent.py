import json
import os

from dotenv import load_dotenv
from google.cloud import dialogflow


def create_intent(project_id, display_name, training_phrases_parts, message_texts):
    """Create an intent of the given intent type."""

    intents_client = dialogflow.IntentsClient()

    parent = dialogflow.AgentsClient.agent_path(project_id)
    training_phrases = []
    for training_phrases_part in training_phrases_parts:
        part = dialogflow.Intent.TrainingPhrase.Part(text=training_phrases_part)
        # Here we create a new training phrase for each provided part.
        training_phrase = dialogflow.Intent.TrainingPhrase(parts=[part])
        training_phrases.append(training_phrase)

    text = dialogflow.Intent.Message.Text(text=[message_texts])
    message = dialogflow.Intent.Message(text=text)

    intent = dialogflow.Intent(
        display_name=display_name, training_phrases=training_phrases, messages=[message]
    )

    response = intents_client.create_intent(
        request={"parent": parent, "intent": intent}
    )

def create_intent_from_json(file_path):
    """Create intent from json-file"""
    load_dotenv()
    dialog_flow_project_id = os.environ['DIALOGFLOW_PROJECT_ID']
    with open(file_path, 'r') as read_file:
        read_phrases = json.load(read_file)
        for phrases, phrases_action in read_phrases.items():
            create_intent(dialog_flow_project_id, phrases, phrases_action['questions'], phrases_action['answer'])

import argparse
import os
import subprocess
import shutil
import tempfile
import re
import fileinput
import sys
import json

from sumy.parsers.plaintext import PlaintextParser
from sumy.nlp.tokenizers import Tokenizer
from sumy.summarizers.lsa import LsaSummarizer as Summarizer
from sumy.nlp.stemmers import Stemmer
from sumy.utils import get_stop_words
from sumy._compat import to_unicode

LANGUAGE = 'english'
SENTENCES_COUNT = 3

def is_valid_target(target_dir_path):
    try:
        if os.path.exists(target_dir_path):
            with open(target_dir_path) as json_file:
                json_data = json.load(json_file)
                return True
    except ValueError, e:
        return False
    return False

def get_sentences(target_dir_path):
    sentences = []
    with open(target_dir_path) as json_file:
        json_data = json.load(json_file)
        
        if 'messages' in json_data:
            for message in json_data['messages']:
                if 'type' in message and message['type'] == 'message' and 'text' in message:
                    sentences.append(message['text'])
    
    return sentences

def get_tldr_sentences_count(sentences_length):
    return SENTENCES_COUNT

def sum_conversation(sentences):
    parser = PlaintextParser.from_string('\n'.join(sentences), Tokenizer(LANGUAGE))
    stemmer = Stemmer(LANGUAGE)

    summarizer = Summarizer(stemmer)
    summarizer.stop_words = get_stop_words(LANGUAGE)

    sum_sentences = []
    for sum_sentence in summarizer(parser.document, SENTENCES_COUNT):
        sum_sentences.append(to_unicode(sum_sentence))

    return '\n'.join(sum_sentences)

def main():
    parser = argparse.ArgumentParser(description='You are busy, we know that, let me summarize the conversation for you!')
    parser.add_argument('-i', '--input-json', required=True,
                        help='The input JSON file from a Slack channel')

    args = parser.parse_args()

    target_dir_path = args.input_json

    if is_valid_target(target_dir_path) == False:
        sys.exit('Could not find a valid input json file. Abort!')

    sentences = get_sentences(target_dir_path)
    if len(sentences) == 0:
        sys.exit('There is no content to check. Abort!')
    else:
        result = sum_conversation(sentences)

        print('Summarize result:\n' + result)
        sys.exit(0)


if __name__ == '__main__':
    main()

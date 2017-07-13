'''!tldr <channel> will return the best summery result for your unread messages (Too long; didn't read (TLDR or TL;DR))'''
import re
from slacker import Slacker

from sumy.parsers.plaintext import PlaintextParser
from sumy.nlp.tokenizers import Tokenizer
from sumy.summarizers.lsa import LsaSummarizer as Summarizer
from sumy.nlp.stemmers import Stemmer
from sumy.utils import get_stop_words
from sumy._compat import to_unicode

LANGUAGE = 'english' # TODO: Can we get this from Slack?
MIN_TLDR_SENTENCES_COUNT = 3 

# TODO: env variable 
slack = Slacker('<your-api-token>')

def get_sentences(json_data):
    sentences = []
    if 'messages' in json_data:
        for message in json_data['messages']:
            if 'type' in message and message['type'] == 'message' and 'text' in message:
                sentences.append(message['text'])
    
    return sentences

# The TLDR sum length is a function of sentences to sum.
def get_tldr_sentences_count(sentences_length):
    if (sentences_length <= MIN_TLDR_SENTENCES_COUNT):
        return sentences_length;
    elif (sentences_length > MIN_TLDR_SENTENCES_COUNT and sentences_length <= MIN_TLDR_SENTENCES_COUNT * 10):
        return MIN_TLDR_SENTENCES_COUNT;
    else:
        return sentences_length / 10;

def sum_conversation(sentences):
    parser = PlaintextParser.from_string('\n'.join(sentences), Tokenizer(LANGUAGE))
    stemmer = Stemmer(LANGUAGE)

    summarizer = Summarizer(stemmer)
    summarizer.stop_words = get_stop_words(LANGUAGE)

    sum_sentences = []
    for sum_sentence in summarizer(parser.document, get_tldr_sentences_count(len(sentences))):
        sum_sentences.append(to_unicode(sum_sentence))

    return '\n'.join(sum_sentences)

def get_channel_id_by_name(channel_name):
    return slack.channels.get_channel_id(channel_name)
    
def sum(channel_name):
    channel_id = get_channel_id_by_name(channel_name)
    if channel_id is None:
        return ':crying_cat_face: Sorry, I could not figure out this channel name'
    else:
        channel_info_request = slack.channels.info(channel_id)
        if channel_info_request is not None and channel_info_request.successful == True:
            channel_info_json = channel_info_request.body

            if 'channel' in channel_info_json:
                last_read = channel_info_json['channel']['last_read']
            
        if last_read is not None:
            # TODO: Change this function to run on oldest to new, i made this hack to get information
            # channel_history = slack.channels.history(channel_id, last_read, None, True, False).body
            channel_history = slack.channels.history(channel_id, None, None, True, False).body

            sentences = get_sentences(channel_history)
            if len(sentences) == 0:
                return 'There is no content to check. Abort!'
            else:
                result = sum_conversation(sentences)
                return 'Summarize result:\n' + result
        else:
            return ':crying_cat_face: Sorry, I could not get the channel history..try again later!'
    
def on_message(msg, server):
    text = msg.get('text', '')
    match = re.findall(r'!(?:tldr) (.*)', text)
    if not match:
        return

    return sum(match[0])

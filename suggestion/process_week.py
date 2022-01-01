import csv
import datetime
import re
import pandas as pd
from icecream import ic
from konlpy.tag import Okt
from nltk import word_tokenize, FreqDist
from event.models import Event
from event.process import EventProcess
from event.serializer import EventSerializer
from pykospacing import Spacing

class ProcessWeek:
    def __init__(self):
        self.path = 'suggestion/data/'
        self.filename = 'week_event.csv'

    def week_event(self):
        date2 = datetime.datetime.today() - datetime.timedelta(days=7)
        ic(date2)
        week_events = Event.objects.filter(update__gte=date2)
        events = []
        [events.append(event.title) for event in week_events]
        ic(events)

        with open(f'{self.path}{self.filename}', 'w', newline='', encoding='UTF-8') as f:
            wr = csv.writer(f)
            wr.writerow(events)

    def remove_special_character(self, full_texts):
        result = re.sub('\W', '', full_texts)
        return result

    def spacing_sent(self, raw):
        spacing = Spacing()
        kospacing_sent = spacing(raw)
        return kospacing_sent

    def event_freq_word(self):
        okt = Okt()
        with open(f'{self.path}{self.filename}', 'r',  encoding='UTF-8') as f:
            full_texts = f.read()
        # line_remove_texts = full_texts.replace('\n', '')
        # tokenizer = re.compile(r'[^ ㄱ-힣]+')
        remove_texts = self.remove_special_character(full_texts)
        spacing_sent = self.spacing_sent(remove_texts)
        tokenized_texts = remove_texts.sub('', spacing_sent)
        tokens = word_tokenize(tokenized_texts)
        noun_tokens = []
        for token in tokens:
            token_pos = okt.pos(token)
            noun_token = [txt_tag[0] for txt_tag in token_pos if txt_tag[1] == 'Noun']
            if len(''.join(noun_token)) > 1:
                noun_tokens.append(''.join(noun_token))
        noun_tokens_join = " ".join(noun_tokens)
        tokens = word_tokenize(noun_tokens_join)
        print(noun_tokens_join)
        # ic(tokens)
        with open( f'{self.path}stopwords.txt', 'r', encoding='utf-8') as f:
            stopwords = f.read()
        # stopwords = ['완료항상']
        texts_without_stopwords = [text for text in tokens if text not in stopwords]
        freq_texts = pd.Series(dict(FreqDist(texts_without_stopwords))).sort_values(ascending=False)
        ic(f':::::::: {datetime.now()} ::::::::\n {freq_texts}')


        # test = pd.DataFrame.from_dict(FreqDist(texts_without_stopwords),orient='index')
        # test.columns = ['Frequency']
        # test.index.name = 'word'
        # test.sort_values(by='Frequency', ascending=False, inplace=True)


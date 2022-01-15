import datetime
import random

import django_mysql
import pandas as pd
import requests
from django.db.models import Max
from icecream import ic
from keras.metrics import cosine_similarity
from sklearn.feature_extraction.text import TfidfVectorizer

from event.models import User
from event.process import EventProcess
from suggestion.models import SuggestionEvent


class SuggestionProcess:
    def __init__(self):
        self.path = 'suggestion/data/'

    # def test1(self):
    #     # return SuggestionEvent.objects.filter(classification__contains='DEV')
    #     events = []
    #     [events.append(event) for event in SuggestionEvent.objects.filter(classification__contains='DEV')]
    #     return events

    def test3(self):
        return SuggestionEvent.objects.filter(classification__contains='DEV')

    def test2(self):
        ic(self.test3())

    def get_top3_routine(self, user_id):
        url = f'http://127.0.0.1:8004/api/routine/today_top10/{user_id}'
        response = requests.get(url)
        data = response.json()
        top3 = data[:3]
        return top3

    def user_based_suggestion(self, user_id):
        if EventProcess.user_event_count(user_id) < 10:
            user = User.objects.get(pk=user_id)
            interest = user.user_interest
            interest_events = SuggestionEvent.objects.filter(classification__contains=interest)
            interest = []
            [interest.append(event) for event in interest_events.id]
            interest_id = random.sample(interest, 2)
            events = []
            [events.append(SuggestionEvent.objects.all()[i]) for i in interest_id]
            return events

        else:
            similarity_title = self.cosine_similarity(user_id)
            suggestion_event = SuggestionEvent.objects.filter(title__contains=similarity_title).last()
            return suggestion_event

    def cosine_similarity(self, user_id):
        latest_event = EventProcess().latest_event(user_id).title
        tfidf = TfidfVectorizer(stop_words='english')
        data = pd.read_csv(f'{self.path}suggestion.csv')
        tfidf_matrix = tfidf.fit_transform(data['title'].toarray())
        cosine_matrix = cosine_similarity(tfidf_matrix, tfidf_matrix)
        title2idx = {}
        for i, c in enumerate(data['title']):
            title2idx[i] = c

        idx2title = {}
        for i, c in title2idx.items():
            idx2title[c] = i
        idx = idx2title[latest_event]
        sim_scores = [[i, c] for i, c in enumerate(cosine_matrix[idx]) if i != idx]
        sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)
        sim_scores = [(title2idx[i], score) for i, score in sim_scores[0:2] if score < 0.9 and score > 0]
        similarity_title = []
        [similarity_title.append(sim_scores[i][0]) for i in range(len(sim_scores))]
        return similarity_title

    def process(self, user_id):
        user_based_suggestion = self.user_based_suggestion(user_id)
        top3 = self.get_top3_routine(user_id)
        suggestions = []
        for event in user_based_suggestion:
            start_day = event.start
            end_day = event.end
            if str(type(event.start)) != "<class 'NoneType'>":
                start_day = event.start.strftime('%Y-%m-%d')
            if str(type(event.end)) != "<class 'NoneType'>":
                end_day = event.end.strftime('%Y-%m-%d')
            else:
                start_day = datetime.date.today()
            suggestions.append({
                "suggestion_id": event.id,
                "user_id": user_id,
                "contents": event.title,
                "location": event.location,
                "routine": None,
                "start": start_day,
                "end": end_day,
                "classification": event.classification,
                "type": "SUGGESTION"
            })
        for routine in top3:
            cron = routine['cron']
            routine_days_char = cron[5].split('.')
            days_to_ko = {'mon': '월', 'tue': '화', 'wed': '수', 'thu': '목', 'fri': '금', 'sat': '토', 'sun': '일'}
            ko_days = [days_to_ko.get(day) for day in routine_days_char]
            days = {'mon': 0, 'tue': 1, 'wed': 2, 'thu': 3, 'fri': 4, 'sat': 5, 'sun': 6}
            routine_days_int = [days.get(day) for day in routine_days_char]
            date = []
            for day in routine_days_int:
                period = 7 - datetime.date.today().weekday() + day
                if period < 7:
                    period = period
                else:
                    period -= 7
                date.append(datetime.date.today() + datetime.timedelta(days=period))
            suggestions.append({
                "suggestion_id": routine['id'],
                "user_id": user_id,
                "contents": routine['contents'],
                "location": routine['location'],
                "routine":ko_days,
                "start": date,
                "end": None,
                "classification": None,
                "type": "ROUTINE",
            })
        return suggestions


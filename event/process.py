import datetime

from event.models import Event
from event.serializer import EventSerializer


class EventProcess(object):
    def routine_event(self, request_data):
        events = []
        routine_date = []
        [routine_date.append(f'{date} 00:00') for date in request_data['start']]
        for date in routine_date:
            event_data = {}
            event_data['user_id'] = request_data['user_id']
            event_data['title'] = request_data['contents']
            event_data['classification'] = request_data['classification']
            event_data['type'] = request_data['type']
            event_data['location'] = request_data['location']
            event_data['start'] = date
            event_data['end'] = date
            events.append(event_data)
        serializer = EventSerializer(data=events, many=True)
        if serializer.is_valid():
            serializer.save()
        return serializer.data

    def suggestion_event(self, request_data):
        event_data = {}
        event_data['user_id'] = request_data['user_id']
        event_data['title'] = request_data['contents']
        event_data['classification'] = request_data['classification']
        event_data['type'] = request_data['type']
        event_data['location'] = request_data['location']
        event_data['start'] = f'{request_data["start"]} 00:00'
        event_data['end'] = request_data['end']
        serializer = EventSerializer(data=event_data)
        if serializer.is_valid():
            serializer.save()
        return serializer.data

    def week_evnet(self):
        lask_week = datetime.datetime.today() - datetime.timedelta(days=7)
        week_event = Event.objects.filter(update__gte=lask_week).last()
        serializer = EventSerializer(week_event, many=True)
        return serializer.data

    def latest_event(self, user_id):
        event = Event.objects.filter(user_id=user_id).last()
        return event

    def user_event_count(self, user_id):
        event_count = Event.objects.filter(user_id=user_id).count()
        return event_count


# class ScheduleTimeCheck(object):
#
#     def __init__(self):
#         pass
#
#     def create_date(self):
#         start_time = '2021-11-30T09:51:25.830000+09:00'
#         d_start = datetime.strptime(start_time, '%Y-%m-%dT%H:%M:%S.%f+09:00')
#
#     def start(self, start):
#         # start_time = 'date_check'
#         start_date = datetime.strptime(start, '%Y-%m-%d %H:%M')
#         start_year = start_date.year
#         start_month = start_date.month
#         start_date = start_date.day
#
#     def end(self, end):
#         # end_time = '2021-11-25 12:00'
#         end_date = datetime.strptime(end, '%Y-%m-%d %H:%M')
#         end_year = end_date.year
#         end_month = end_date.month
#         end_day = end_date.day
#
#     def date_check(self, start, end):
#         start_date = datetime.strptime(start, '%Y-%m-%d %H:%M')
#         end_date = datetime.strptime(end, '%Y-%m-%d %H:%M')
#         start_month = start_date.month
#         start_day = start_date.day
#         end_month = end_date.month
#         end_day = end_date.day
#         month_compare = end_month - start_month
#         day_compare = end_day - start_day
#         # year_period =
#         [i for i in range(start_day, end_day+1)]
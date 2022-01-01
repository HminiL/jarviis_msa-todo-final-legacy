from satisfaction.serializer import SatisfactionSerializer


class SatisfactionProcess(object):
    def suggestion(self, request_data, result):
        accept_data = {}
        accept_data['user_id'] = request_data['user_id']
        accept_data['title'] = request_data['contents']
        accept_data['type'] = request_data['type']
        accept_data['result'] = result
        serializer = SatisfactionSerializer(data=accept_data)
        if serializer.is_valid():
            serializer.save()
        return serializer.data
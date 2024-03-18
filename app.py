from slack_sdk import WebClient
import os
import json
from datetime import datetime, timedelta
import time

class RequestTracker:
    def __init__(self):
        self.request_ids = set()

    def add_request_id(self, request_id):
        self.request_ids.add(request_id)

    def is_duplicate_request_id(self, request_id):
        return request_id in self.request_ids
    
request_tracker = RequestTracker()

def send_slack(message):
    client = WebClient(token="xoxb-67761YT6kLTX26Fvj")
    client.chat_postMessage(
        channel="#teste", 
        text=message, 
        username="kubewatch"
    )

def time_dif(first_time):
    current_time = datetime.now() - timedelta(hours=3)
    formatted_time = current_time.strftime('%Y-%m-%dT%H:%M:%SZ')
    time1 = datetime.strptime(first_time, '%Y-%m-%dT%H:%M:%SZ')
    time2 = datetime.strptime(formatted_time, '%Y-%m-%dT%H:%M:%SZ')
    time_difference = time2 - time1
    return time_difference

def remade_message(original):
    message = original['message']
    reason = original['reason']
    name = original['metadata']['name']
    namespace = original['metadata']['namespace']
    slack_message = str(f"O recurso `{name}` do namespace `{namespace}` está em status `{reason}` e apresentando a seguinte mensagem:  `{message}` .")
    return slack_message

def get_kubernetes_events():
    os.system("kubectl get events -A -o json > tmp.json")
    alarming_time = timedelta(minutes=30)
    
    
    f = open('tmp.json')
    data = json.load(f)

    for i in data['items']:
        time1_str = str(i['firstTimestamp'])
        time_difference = time_dif(first_time=time1_str)
        reason = str(i['reason'])
        request_id = str(i['metadata']['uid'])

        if request_tracker.is_duplicate_request_id(request_id) == False and time_difference < alarming_time and reason != "Pulled" and reason != "Created" and reason != "Started" and reason != "Scheduled" and reason != "SuccessfulCreate" and reason != "ScalingReplicaSet":
            slack_message = remade_message(original=i)
            send_slack(message=slack_message)
            request_tracker.add_request_id(request_id)
    f.close
    os.remove("tmp.json")
    return "end"

while True:
    get_kubernetes_events()
    time.sleep(15)

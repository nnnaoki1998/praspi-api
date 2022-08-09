from flask import Flask, Response
from flask_httpauth import HTTPBasicAuth
import json
import datetime

import slack_messenger
import yorozuya_puncher

app = Flask(__name__)
auth = HTTPBasicAuth()

json_open = open("setting.json", "r")
json_load = json.load(json_open)
customer_id = json_load["yorozuya"]["customer_id"]
login_id = json_load["yorozuya"]["login_id"]
password = json_load["yorozuya"]["password"]
slack_token = json_load["slack"]["token"]
user_id = json_load["auth"]["user_id"]
id_list = json_load["auth"]["id_list"]

earliest_hour_punchin = 7
latest_hour_punchin = 13
earliest_hour_punchout = 16
latest_hour_punchout = 23

@auth.get_password
def get_pw(id):
  if id in id_list:
    return id_list.get(id)
  return None

@app.route('/test')
@auth.login_required
def test():
  return Response(response="ok", status=200)

@app.route('/punchin')
@auth.login_required
def punchin():
  now_hour = datetime.datetime.now().hour
  if earliest_hour_punchin <= now_hour and now_hour <= latest_hour_punchin:
    is_success_punchin = yorozuya_puncher.punchin(customer_id, login_id, password)
    is_success_greeting = slack_messenger.good_morning(slack_token)
    if is_success_punchin and is_success_greeting:
      return Response(response="ok", status=200)
  return Response(response="error", status=500)

@app.route('/punchout')
@auth.login_required
def punchout():
  now_hour = datetime.datetime.now().hour
  if earliest_hour_punchout <= now_hour and now_hour <= latest_hour_punchout:
    is_success_punchout = yorozuya_puncher.punchout(customer_id, login_id, password)
    is_success_greeting = slack_messenger.good_job_today(slack_token)
    if is_success_punchout and is_success_greeting:
      return Response(response="ok", status=200)
  return Response(response="error", status=500)

if __name__ == '__main__':
  app.run(host='0.0.0.0', port=80)

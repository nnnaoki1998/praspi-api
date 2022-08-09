from slack import WebClient

channel_id = "CMJ3QMN0P"
bot_name = "勤怠連絡"
bot_text = "【おはよう】今日の挨拶スレ 【おつかれさま】"
good_morning_text = "おはようございます"
good_job_today_text = "お先に失礼します"

def is_greeting_thread(message):
  return "username" in message and message["username"] == bot_name and message["text"] == bot_text

def get_thread_ts(client):
  response = client.conversations_history(
    channel = channel_id
  )
  messages = response["messages"]
  thread_ts = list(filter(is_greeting_thread, messages))[0]["thread_ts"]
  return thread_ts

def post_message(client, message_text, thread_ts):
  response = client.chat_postMessage(
    channel = channel_id,
    text = message_text,
    thread_ts = thread_ts
  )
  return response

def good_morning(slack_token):
  client = WebClient(slack_token)
  thread_ts = get_thread_ts(client)
  response = post_message(client, good_morning_text, thread_ts)
  return response["ok"]

def good_job_today(slack_token):
  client = WebClient(slack_token)
  thread_ts = get_thread_ts(client)
  response = post_message(client, good_job_today_text, thread_ts)
  return response["ok"]

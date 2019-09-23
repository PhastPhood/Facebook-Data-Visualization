import json
import os
import datetime
import sys
import time
import matplotlib.pyplot as plt
from matplotlib.font_manager import FontProperties
import argparse

parser = argparse.ArgumentParser()
parser.add_argument("path", help="Path to your messenger 'inbox' folder.")

parser.add_argument("--recipient", help="The person to graph.", default="Jeff Gao")
parser.add_argument("--name", help="Your name so script can remove it as a participant. Default: none")
parser.add_argument("--messages", help="Minimum number of messages to display. Default: 250", default=50, type=int)
parser.add_argument("--maxgroup", help="Maximum group size. Large group chats tend to have a lot of messages.", default=10, type=int)
args = parser.parse_args()


# So it removes me
NAME = args.name
# Min messages to show up
MIN_MSG = args.messages
# Max number of group members (large groups have more messages).
MAX_GROUP_SIZE = args.maxgroup
# Path to messenger inbox folder.
directory = args.path
# So it removes me
RECIPIENT = args.recipient

participant_messages_time_dict = dict()
participant_lists = dict()
total_messages_time_dict = dict()

def toTimestamp(date):
	return (date - datetime.date(1970, 1, 1)).days * 24 * 60 * 60

# This creates a count for the number of days
def countDays(message_time_list):
	days_dict = dict()
	num_per_day = []
	days = []

	min_day = datetime.date.today()
	max_day = datetime.date(1970, 1, 1)
	for time in message_time_list:
		day = datetime.date.fromtimestamp(time/1000)
		if day < min_day:
			min_day = day
		if day > max_day:
			max_day = day
		if day in days_dict:
			days_dict[day] += 1
		else:
			days_dict[day] = 1

	min_day = min_day - datetime.timedelta(days=30)
	max_day = max_day + datetime.timedelta(days=30)
	if max_day > datetime.date.today():
		max_day = datetime.date.today()
	for time_ms in range(toTimestamp(min_day), toTimestamp(max_day), 24 * 60 * 60):
		day = datetime.date.fromtimestamp(time_ms)
		days.append(day)
		if day in days_dict:
			num_per_day.append(days_dict[day])
		else:
			num_per_day.append(0)
	return days, num_per_day

# Expects to be run like `python process_time.py ~/Downloads/facebook/messages/inbox/`
for chat_folder in os.listdir(directory):
	chat_folder_path = os.path.join(directory, chat_folder)
	if os.path.isdir(chat_folder_path):
		for chat_file in os.listdir(chat_folder_path):
			if ".json" in chat_file:
				chat_file_path = os.path.join(chat_folder_path, chat_file)
				with open(chat_file_path, 'r') as f:
					messages_dict = json.load(f)
					if len(messages_dict["messages"]) > MIN_MSG:
						participant = [p["name"] for p in messages_dict["participants"]]
						if NAME in participant:
							participant.remove(NAME)
						if len(participant) <= MAX_GROUP_SIZE:
							participant_names = set()
							participant_message_times = dict()
							total_messages_time_list = []

							print(participant)
							for message in messages_dict["messages"]:
								participant_name = message["sender_name"]
								participant_names.add(participant_name)
								# divide into days
								total_messages_time_list.append(message["timestamp_ms"])
								if participant_name not in participant_message_times:
									participant_message_times[participant_name] = []
								participant_message_times[participant_name].append(message["timestamp_ms"])

							participant_key = ', '.join(participant)
							total_messages_time_dict[participant_key] = countDays(total_messages_time_list)

							participant_lists[participant_key] = participant_names
							participant_messages_time_dict[participant_key] = dict()
							for participant_name in participant_names:
								participant_messages_time_dict[participant_key][participant_name] = countDays(participant_message_times[participant_name])

messages_dates, num_messages = total_messages_time_dict[RECIPIENT]

line, = plt.plot(messages_dates, num_messages, label="Total", linewidth=1)

for participant_name in participant_lists[RECIPIENT]:
	participant_messages_dates, participant_num_messages = participant_messages_time_dict[RECIPIENT][participant_name]
	line, = plt.plot(participant_messages_dates, participant_num_messages, label=participant_name, linewidth=1, linestyle="dotted")

fontP = FontProperties()
fontP.set_size('small')

legend = plt.legend()
plt.show()
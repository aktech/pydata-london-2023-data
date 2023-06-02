import datetime
import json
import logging

import requests
from icalendar import Calendar, Event


DATE_FORMAT = '%Y-%m-%dT%H:%M:%S%z'
ICS_FILE = 'calendar.ics'
SCHEDULE_JSON = 'https://london2023.pydata.org/cfp/schedule/widget/v2.json'


def create_event(talk, speaker_mapping, room_mapping):
    event = Event()
    title = talk.get('title')
    if isinstance(title, dict) and title.get('en'):
        title = title.get('en')

    speakers = []
    speakers_code = talk.get('speakers')
    if speakers_code:
        speakers = [speaker_mapping[sc]['name'] for sc in speakers_code]

    room = None
    room_id = talk.get('room')
    if room_id:
        room = room_mapping[room_id]['name']['en']

    speakers_txt = ', '.join(speakers)
    event.add('organizer', speakers_txt)
    if speakers_txt:
        title = f"{title}: by {speakers_txt}"
    event.add('summary', title)
    event.add('description', talk.get('abstract'))
    date_format = '%Y-%m-%dT%H:%M:%S%z'
    event.add('dtstart', datetime.datetime.strptime(talk.get('start'), date_format))
    event.add('dtend',  datetime.datetime.strptime(talk.get('end'), date_format))
    event.add('location', room)
    return event


def get_schedule():
    try:
        response = requests.get(SCHEDULE_JSON)
        schedule = response.json()
    except Exception as e:
        logging.warning(f"Could not load schedule from url, reading from file: {e}")
        schedule = json.load(open('v2.json', 'r'))
    return schedule


def create_ical():
    schedule = json.load(open('v2.json', 'r'))
    talks = schedule['talks']
    speakers = schedule['speakers']
    rooms = schedule['rooms']
    cal = Calendar()
    speaker_mapping = {
        speaker_data['code']: speaker_data for speaker_data in speakers
    }
    room_mapping = {
        room_data['id']: room_data for room_data in rooms
    }
    for talk in talks:
        event = create_event(talk, speaker_mapping, room_mapping)
        cal.add_component(event)

    with open(ICS_FILE, 'wb') as f:
        f.write(cal.to_ical())


def setup_logging():
    """
    Setups logging for the ballot.
    :return: None
    """
    logging_format = (
        "%(asctime)s %(levelname)9s %(lineno)4s %(module)s: %(message)s"
    )
    logging.basicConfig(
        level=logging.INFO, format=logging_format
    )


if __name__ == "__main__":
    setup_logging()
    create_ical()

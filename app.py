import datetime
import json

from icalendar import Calendar, Event


DATE_FORMAT = '%Y-%m-%dT%H:%M:%S%z'


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

    with open('calendar.ics', 'wb') as f:
        f.write(cal.to_ical())


if __name__ == "__main__":
    get_schedule()

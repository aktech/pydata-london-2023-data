import datetime
import json

from icalendar import Calendar, Event


DATE_FORMAT = '%Y-%m-%dT%H:%M:%S%z'


def create_event(talk, speaker_mapping):
    event = Event()
    title = talk.get('title')
    if isinstance(title, dict) and title.get('en'):
        title = title.get('en')

    speakers = []
    speakers_code = talk.get('speakers')
    if speakers_code:
        speakers = [speaker_mapping[sc]['name'] for sc in speakers_code]

    try:
        speakers_txt = ', '.join(speakers)
        event.add('organizer', speakers_txt)
        if speakers_txt:
            title = f"{title}: by {speakers_txt}"
        event.add('summary', title)
        event.add('description', talk.get('abstract'))
        date_format = '%Y-%m-%dT%H:%M:%S%z'
        event.add('dtstart', datetime.datetime.strptime(talk.get('start'), date_format))
        event.add('dtend',  datetime.datetime.strptime(talk.get('end'), date_format))
    except Exception as e:
        import ipdb as pdb; pdb.set_trace()
        one = 1

    return event


def get_schedule():
    schedule = json.load(open('v2.json', 'r'))
    talks = schedule['talks']
    speakers = schedule['speakers']
    cal = Calendar()
    speaker_mapping = {
        speaker_data['code']: speaker_data for speaker_data in speakers
    }
    for talk in talks:
        event = create_event(talk, speaker_mapping)
        cal.add_component(event)

    with open('calendar.ics', 'wb') as f:
        f.write(cal.to_ical())


get_schedule()

from events.models import Tag, Event
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from math import ceil


def get_tags_service():
    try:
        tags = Tag.objects.all()
        return [tag.name for tag in tags]
    except Exception as e:
        raise ValueError(f"Error fetching tags: {str(e)}")


def get_recent_events_service(page=1, page_size=5):
    try:
        events = Event.objects.all().order_by('-created_at')

        total_events = events.count()
        total_pages = ceil(total_events / page_size)

        paginator = Paginator(events, page_size)
        try:
            events_page = paginator.page(page)
        except PageNotAnInteger:
            events_page = paginator.page(1)
        except EmptyPage:
            events_page = paginator.page(paginator.num_pages)

        events = [{
            'id': event.id,
            'event_name': event.event_name,
            'location': event.location,
            'day': event.day,
            'start_time': event.start_time,
            'end_time': event.end_time,
            'images': [image.image.url for image in event.images.all()],
            'tags': [tag.name for tag in event.tags.all()]
        } for event in events_page]

        return events, total_pages

    except Exception as e:
        raise ValueError(f"Error fetching recent events: {str(e)}")

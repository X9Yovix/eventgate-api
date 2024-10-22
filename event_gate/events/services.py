from events.models import Tag


def get_tags_service():
    try:
        tags = Tag.objects.all()
        return [tag.name for tag in tags]
    except Exception as e:
        raise ValueError(f"Error fetching tags: {str(e)}")

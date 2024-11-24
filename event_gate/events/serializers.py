from rest_framework import serializers
from events.models import Event, EventImage, Tag


class EventSerializer(serializers.ModelSerializer):
    images = serializers.ListField(child=serializers.ImageField(), write_only=True, required=False)
    tags = serializers.CharField(write_only=True)

    class Meta:
        model = Event
        fields = ['event_name', 'location', 'day', 'start_time', 'end_time', 'images', 'tags']

    def validate_tags(self, value):
        value = [tag.strip() for tag in value.split(',') if tag.strip()]

        if not value:
            raise serializers.ValidationError("At least one tag is required")

        return value

    def create(self, validated_data):
        print("Validated data: ", validated_data)
        images = validated_data.pop('images', [])
        tag_names = validated_data.pop('tags', [])

        event = Event.objects.create(**validated_data)

        for image in images:
            EventImage.objects.create(event=event, image=image)

        for tag_name in tag_names:
            tag, _ = Tag.objects.get_or_create(name=tag_name)
            event.tags.add(tag)

        return event

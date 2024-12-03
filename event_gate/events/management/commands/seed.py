import os
import random
from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from events.models import Tag, Event, EventImage
from datetime import datetime, timedelta, time
from django.core.files import File
from django.conf import settings


class Command(BaseCommand):
    help = 'Creates 20 events'

    def handle(self, *args, **kwargs):
        user = User.objects.get(username='karim')

        tag_names = ['Music', 'Sports', 'Tech', 'Food', 'Art', 'Education', 'Networking', 'Health']
        tags = [Tag.objects.get_or_create(name=tag_name)[0] for tag_name in tag_names]

        IMAGE_FOLDER = os.path.join(settings.MEDIA_ROOT, 'assets')

        image_files = [f for f in os.listdir(IMAGE_FOLDER) if os.path.isfile(os.path.join(IMAGE_FOLDER, f))]

        if not image_files:
            self.stdout.write(self.style.ERROR("No images found in the specified folder"))
            return

        for i in range(20):
            event_name = f"Event {i + 1}"

            lat = random.uniform(-90.0, 90.0)
            lng = random.uniform(-180.0, 180.0)
            location = f"{lat:.6f},{lng:.6f}"

            day = datetime.now().date() + timedelta(days=random.randint(1, 30))
            start_time = time(random.randint(8, 18), random.choice([0, 30]))
            end_time = (datetime.combine(day, start_time) + timedelta(hours=random.randint(1, 3))).time()

            event = Event.objects.create(
                user=user,
                event_name=event_name,
                location=location,
                day=day,
                start_time=start_time,
                end_time=end_time,
            )

            event.tags.add(*random.sample(tags, random.randint(1, 4)))

            num_images_to_select = random.randint(1, min(3, len(image_files)))
            selected_images = random.sample(image_files, num_images_to_select)

            for img_name in selected_images:
                img_path = os.path.join(IMAGE_FOLDER, img_name)
                with open(img_path, 'rb') as img_file:
                    EventImage.objects.create(
                        event=event,
                        image=File(img_file, name=img_name)
                    )

        self.stdout.write(self.style.SUCCESS("20 example events created"))

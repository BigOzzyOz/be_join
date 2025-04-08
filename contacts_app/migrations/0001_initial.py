import uuid
from django.db import migrations, models


class Migration(migrations.Migration):
    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Contact",
            fields=[
                (
                    "email",
                    models.EmailField(max_length=254, serialize=False, unique=True),
                ),
                ("name", models.CharField(max_length=255)),
                ("id", models.UUIDField(default=uuid.uuid4, unique=True, primary_key=True)),
                ("number", models.CharField(blank=True, max_length=20, null=True)),
                ("first_letters", models.CharField(blank=True, max_length=2, null=True)),
                ("profile_pic", models.TextField(blank=True, null=True)),
            ],
        ),
    ]

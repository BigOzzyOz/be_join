import uuid
from django.db import migrations, models


class Migration(migrations.Migration):
    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Contact",
            fields=[
                ("id", models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ("name", models.CharField(max_length=255)),
                ("mail", models.EmailField(max_length=254, unique=True)),
                ("number", models.CharField(blank=True, max_length=20, null=True)),
                ("first_letters", models.CharField(blank=True, max_length=2, null=True)),
                ("profile_pic", models.TextField(blank=True, null=True)),
            ],
        ),
    ]

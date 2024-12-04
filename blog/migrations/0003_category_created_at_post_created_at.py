from django.db import migrations, models
import django.utils.timezone

def set_default_created_at(apps, schema_editor):
    Post = apps.get_model('blog', 'Post')
    # Met à jour les posts sans valeur de created_at
    Post.objects.filter(created_at__isnull=True).update(created_at=django.utils.timezone.now())

class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0002_category_remove_post_date_posted_post_slug_and_more'),  # Assure-toi que cette dépendance est correcte
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='created_at',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
        migrations.RunPython(set_default_created_at),  # Applique la mise à jour des posts existants
    ]

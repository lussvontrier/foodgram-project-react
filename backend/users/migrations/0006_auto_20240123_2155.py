# Generated by Django 3.2.3 on 2024-01-23 21:55

from django.db import migrations, models
import django.db.models.expressions


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0005_auto_20240123_2153'),
    ]

    operations = [
        migrations.RemoveConstraint(
            model_name='subscription',
            name='unique_name_owner',
        ),
        migrations.RemoveConstraint(
            model_name='subscription',
            name='prevent_self_follow',
        ),
        migrations.AddConstraint(
            model_name='subscription',
            constraint=models.UniqueConstraint(fields=('subscriber', 'subscribed_to'), name='unique_name_owner'),
        ),
        migrations.AddConstraint(
            model_name='subscription',
            constraint=models.CheckConstraint(check=models.Q(('subscriber', django.db.models.expressions.F('subscribed_to')), _negated=True), name='prevent_self_follow'),
        ),
    ]

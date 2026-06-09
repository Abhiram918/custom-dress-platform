from django.db import migrations, models

class Migration(migrations.Migration):

    dependencies = [
        ('dress_requests', '0002_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='dressrequest',
            name='sleeve_length',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=5, null=True),
        ),
        migrations.AddField(
            model_name='dressrequest',
            name='fabric_type',
            field=models.CharField(choices=[('cotton', 'Cotton'), ('linen', 'Linen'), ('silk', 'Silk'), ('velvet', 'Velvet'), ('wool', 'Wool'), ('polyester', 'Polyester'), ('other', 'Other')], default='cotton', max_length=20),
        ),
        migrations.AddField(
            model_name='dressrequest',
            name='preferred_color',
            field=models.CharField(default='#ffffff', help_text='Hex color code', max_length=10),
        ),
    ]

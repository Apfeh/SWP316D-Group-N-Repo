# Generated by Django 5.2 on 2025-04-08 21:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('IFPWebApp', '0004_policyholder'),
    ]

    operations = [
        migrations.CreateModel(
            name='TeamMember',
            fields=[
                ('teamid', models.AutoField(primary_key=True, serialize=False)),
                ('claimid', models.IntegerField()),
                ('policyid', models.IntegerField()),
                ('contactNumber', models.CharField(max_length=20)),
                ('department', models.CharField(max_length=100)),
                ('investigatorName', models.CharField(max_length=100)),
            ],
            options={
                'db_table': 'ifps_app_fraudpreventionteam',
            },
        ),
    ]

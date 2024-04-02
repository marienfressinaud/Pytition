# Generated by Django 4.2.7 on 2023-12-03 16:26

from django.db import migrations

def set_new_petition_share_fields(apps, schema_editor):
    Petition = apps.get_model("petition", "Petition")
    for petition in Petition.objects.all():
        if petition.has_share_buttons:
            petition.has_email_share_button = True
            petition.has_facebook_share_button = True
            petition.has_tumblr_share_button = True
            petition.has_linkedin_share_button = True
            petition.has_twitter_share_button = True
            petition.has_mastodon_share_button = True
            petition.has_whatsapp_share_button = True
            petition.save()


class Migration(migrations.Migration):

    dependencies = [
        ('petition', '0020_petition_has_email_share_button_and_more'),
    ]

    operations = [
        migrations.RunPython(set_new_petition_share_fields)
    ]

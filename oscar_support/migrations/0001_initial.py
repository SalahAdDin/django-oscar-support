# -*- coding: utf-8 -*-
# Generated by Django 1.11.4 on 2017-09-02 23:12
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django_extensions.db.fields
import shortuuidfield.fields


def create_default_ticket_status(apps, schema_editor):
    statuses = [
        'Closed'
        'In progress',
        'In review',
        'New',
        'Open',
        'Pending',
        'Solved',
    ]

    Status = apps.get_model('oscar_support.ticketstatus')

    for status in statuses:
        Status.objects.create(name=status)


def create_default_ticket_type(apps, schema_editor):
    types = [
        'Customer',
        'Error',
        'Initiative',
        'Order',
        'Product',
        'Work'
    ]

    Type = apps.get_model('oscar_support.tickettype')

    for type in types:
        Type.objects.create(name=type)


def create_default_priority(apps, schema_editor):
    priorities = [
        'Extremely',
        'High',
        'Infrequent',
        'Low',
        'N/A',
        'Normal',
        'Unsure',
    ]
    comments = [
        "Extremely disruptive, can't be working until resolved.",
        'Very high priority. Needs to be resolved in short time range.',
        'Infrequent, serious problems. Should fix in near term.',
        'A low impact, low urgency issue.',
        'This issue did not require any action, so this field does not apply.',
        'Normal, common problem.',
        "Unsure when we're going to fix this.",
    ]

    Priority = apps.get_model('oscar_support.priority')

    for priority, comment in zip(priorities, comments):
        Priority.objects.create(name=priority, comment=comment)


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('catalogue', '0012_auto_20170609_1902'),
        ('order', '0005_update_email_length'),
        ('auth', '0008_alter_user_username_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='Attachment',
            fields=[
                ('date_created', models.DateTimeField(verbose_name='Created')),
                ('date_updated', models.DateTimeField(verbose_name='Last modified')),
                ('uuid', shortuuidfield.fields.ShortUUIDField(blank=True, editable=False, max_length=22, primary_key=True, serialize=False)),
                ('file', models.FileField(upload_to='oscar_support/%Y/%m', verbose_name='File')),
            ],
            options={
                'verbose_name': 'Attachment',
                'verbose_name_plural': 'Attachments',
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Message',
            fields=[
                ('date_created', models.DateTimeField(verbose_name='Created')),
                ('date_updated', models.DateTimeField(verbose_name='Last modified')),
                ('uuid', shortuuidfield.fields.ShortUUIDField(blank=True, editable=False, max_length=22, primary_key=True, serialize=False)),
                ('type', models.CharField(choices=[('public', 'Public message'), ('internal', 'Internal note')], default='public', max_length=30, verbose_name='Message type')),
                ('text', models.TextField(verbose_name='Text')),
            ],
            options={
                'verbose_name': 'Message',
                'verbose_name_plural': 'Messages',
                'ordering': ['-date_created'],
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Priority',
            fields=[
                ('uuid', shortuuidfield.fields.ShortUUIDField(blank=True, editable=False, max_length=22, primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=255, verbose_name='Name')),
                ('slug', django_extensions.db.fields.AutoSlugField(blank=True, editable=False, populate_from='name', verbose_name='Slug')),
                ('comment', models.TextField(blank=True, verbose_name='Comment')),
            ],
            options={
                'verbose_name': 'Priority',
                'verbose_name_plural': 'Priorities',
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='RelatedOrder',
            fields=[
                ('date_created', models.DateTimeField(verbose_name='Created')),
                ('date_updated', models.DateTimeField(verbose_name='Last modified')),
                ('uuid', shortuuidfield.fields.ShortUUIDField(blank=True, editable=False, max_length=22, primary_key=True, serialize=False)),
                ('order', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='ticket_related_orders', to='order.Order', verbose_name='Order')),
            ],
            options={
                'verbose_name': 'Related order',
                'verbose_name_plural': 'Related orders',
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='RelatedOrderLine',
            fields=[
                ('date_created', models.DateTimeField(verbose_name='Created')),
                ('date_updated', models.DateTimeField(verbose_name='Last modified')),
                ('uuid', shortuuidfield.fields.ShortUUIDField(blank=True, editable=False, max_length=22, primary_key=True, serialize=False)),
                ('line', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='ticket_related_order_lines', to='order.Line', verbose_name='Order line')),
            ],
            options={
                'verbose_name': 'Related order line',
                'verbose_name_plural': 'Related order lines',
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='RelatedProduct',
            fields=[
                ('date_created', models.DateTimeField(verbose_name='Created')),
                ('date_updated', models.DateTimeField(verbose_name='Last modified')),
                ('uuid', shortuuidfield.fields.ShortUUIDField(blank=True, editable=False, max_length=22, primary_key=True, serialize=False)),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='ticket_related_products', to='catalogue.Product', verbose_name='Product')),
            ],
            options={
                'verbose_name': 'Related product',
                'verbose_name_plural': 'Related products',
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Ticket',
            fields=[
                ('date_created', models.DateTimeField(verbose_name='Created')),
                ('date_updated', models.DateTimeField(verbose_name='Last modified')),
                ('uuid', shortuuidfield.fields.ShortUUIDField(blank=True, editable=False, max_length=22, primary_key=True, serialize=False)),
                ('number', models.CharField(db_index=True, max_length=64, verbose_name='Number')),
                ('subticket_id', models.PositiveIntegerField(default=0, verbose_name='Subticket number')),
                ('subject', models.CharField(max_length=255, verbose_name='Subject')),
                ('body', models.TextField(verbose_name='Body')),
                ('is_internal', models.BooleanField(default=False, help_text="use this ticket only internally and don't display to the customer", verbose_name='Internal ticket')),
                ('assigned_group', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='tickets', to='auth.Group', verbose_name='Assigned group')),
                ('assignee', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='assigned_tickets', to=settings.AUTH_USER_MODEL, verbose_name='Assignee')),
                ('parent', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='subtickets', to='oscar_support.Ticket', verbose_name='Parent ticket')),
                ('priority', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='tickets', to='oscar_support.Priority', verbose_name='Priority')),
                ('related_lines', models.ManyToManyField(blank=True, related_name='tickets', through='oscar_support.RelatedOrderLine', to='order.Line', verbose_name='Related order lines')),
                ('related_orders', models.ManyToManyField(blank=True, related_name='tickets', through='oscar_support.RelatedOrder', to='order.Order', verbose_name='Related Orders')),
                ('related_products', models.ManyToManyField(blank=True, related_name='tickets', through='oscar_support.RelatedProduct', to='catalogue.Product', verbose_name='Related products')),
                ('requester', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='submitted_tickets', to=settings.AUTH_USER_MODEL, verbose_name='Requester')),
            ],
            options={
                'verbose_name': 'Ticket',
                'verbose_name_plural': 'Tickets',
                'ordering': ['-date_updated'],
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='TicketStatus',
            fields=[
                ('uuid', shortuuidfield.fields.ShortUUIDField(blank=True, editable=False, max_length=22, primary_key=True, serialize=False)),
                ('slug', django_extensions.db.fields.AutoSlugField(blank=True, editable=False, populate_from='name', unique=True, verbose_name='Slug')),
                ('name', models.CharField(max_length=64, verbose_name='Name')),
            ],
            options={
                'verbose_name': 'Ticket status',
                'verbose_name_plural': 'Ticket statuses',
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='TicketType',
            fields=[
                ('uuid', shortuuidfield.fields.ShortUUIDField(blank=True, editable=False, max_length=22, primary_key=True, serialize=False)),
                ('slug', django_extensions.db.fields.AutoSlugField(blank=True, editable=False, populate_from='name', unique=True, verbose_name='Slug')),
                ('name', models.CharField(max_length=64, verbose_name='Name')),
            ],
            options={
                'verbose_name': 'Ticket type',
                'verbose_name_plural': 'Ticket types',
                'abstract': False,
            },
        ),
        migrations.AddField(
            model_name='ticket',
            name='status',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='tickets', to='oscar_support.TicketStatus', verbose_name='Status'),
        ),
        migrations.AddField(
            model_name='ticket',
            name='type',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='tickets', to='oscar_support.TicketType', verbose_name='Type'),
        ),
        migrations.AddField(
            model_name='relatedproduct',
            name='ticket',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='relatedproducts', to='oscar_support.Ticket', verbose_name='Ticket'),
        ),
        migrations.AddField(
            model_name='relatedproduct',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='relatedproducts', to=settings.AUTH_USER_MODEL, verbose_name='Added by'),
        ),
        migrations.AddField(
            model_name='relatedorderline',
            name='ticket',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='relatedorderlines', to='oscar_support.Ticket', verbose_name='Ticket'),
        ),
        migrations.AddField(
            model_name='relatedorderline',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='relatedorderlines', to=settings.AUTH_USER_MODEL, verbose_name='Added by'),
        ),
        migrations.AddField(
            model_name='relatedorder',
            name='ticket',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='relatedorders', to='oscar_support.Ticket', verbose_name='Ticket'),
        ),
        migrations.AddField(
            model_name='relatedorder',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='relatedorders', to=settings.AUTH_USER_MODEL, verbose_name='Added by'),
        ),
        migrations.AddField(
            model_name='message',
            name='ticket',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='messages', to='oscar_support.Ticket', verbose_name='Ticket'),
        ),
        migrations.AddField(
            model_name='message',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='messages', to=settings.AUTH_USER_MODEL, verbose_name='Sender'),
        ),
        migrations.AddField(
            model_name='attachment',
            name='ticket',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='attachments', to='oscar_support.Ticket', verbose_name='Ticket'),
        ),
        migrations.AddField(
            model_name='attachment',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='attachments', to=settings.AUTH_USER_MODEL, verbose_name='User'),
        ),
        migrations.AlterUniqueTogether(
            name='ticket',
            unique_together=set([('number', 'subticket_id')]),
        ),
        migrations.RunPython(create_default_ticket_status),
        migrations.RunPython(create_default_ticket_type),
    ]

import hashlib
import uuid
from calendar import month_name

import magic
from django.core.exceptions import ValidationError
from django.db import models
from django.utils.translation import ugettext_lazy as _

from smmc.settings import MAGICFILE


class Tag(models.Model):

    name = models.CharField(
        max_length=255,
        primary_key=True,
        verbose_name=_('name')
    )

    def __str__(self):
        return self.name

    class Meta:
        ordering = ('name', )
        verbose_name = _('tag')
        verbose_name_plural = _('tags')


class Entry(models.Model):

    id = models.UUIDField(
        default=uuid.uuid4,
        editable=False,
        primary_key=True,
        verbose_name=_('identifier'),
    )

    active = models.BooleanField(
        default=True,
        help_text=_('Should this entry be visible for users?'),
        verbose_name=_('active'),
    )

    year = models.PositiveSmallIntegerField(
        blank=True,
        null=True,
        verbose_name=_('year'),
    )

    MONTH_CHOICES = (
        (1, month_name[1]), (2, month_name[2]), (3, month_name[3]), (4, month_name[4]), (5, month_name[5]),
        (6, month_name[6]), (7, month_name[7]), (8, month_name[8]), (9, month_name[9]),
        (10, month_name[10]), (11, month_name[11]), (12, month_name[12])
    )
    month = models.PositiveSmallIntegerField(
        blank=True,
        choices=MONTH_CHOICES,
        null=True,
        verbose_name=_('month'),
    )

    DAY_CHOICES = (
        (1, 1), (2, 2), (3, 3), (4, 4), (5, 5), (6, 6), (7, 7), (8, 8), (9, 9), (10, 10), (11, 11), (12, 12), (13, 13),
        (14, 14), (15, 15), (16, 16), (17, 17), (18, 18), (19, 19), (20, 20), (21, 21), (22, 22), (23, 23), (24, 24),
        (25, 25), (26, 26), (27, 27), (28, 28), (29, 29), (30, 30), (31, 31)
    )
    day = models.PositiveSmallIntegerField(
        blank=True,
        choices=DAY_CHOICES,
        null=True,
        verbose_name=_('day'),
    )

    title = models.CharField(
        max_length=255,
        blank=True,
        verbose_name=_('title'),
    )

    description = models.TextField(
        blank=True,
        help_text=_('Type !MORE to hide some text in a spoiler. A "Show more" button will be displayed.'),
        verbose_name=_('description'),
    )

    tags = models.ManyToManyField(
        to=Tag,
        blank=True,
        help_text=_(
            'Add new tags by pressing the plus button '
            'or choose existing ones by moving them from "Available" to "Chosen" (select and press the right arrow).'
        ),
        verbose_name=_('tags'),
    )

    sort = models.SmallIntegerField(
        blank=True,
        help_text=_(
            'When some entries match the same number of tags when user performs a search, '
            'the results will be sorted ascending by this parameter.'
        ),
        null=True,
        verbose_name=_('force ordering'),
    )

    file = models.FileField(
        blank=True,
        null=True,
        help_text=_('E.g. a photo, a video clip...'),
        verbose_name=_('file'),
    )

    mime_type = models.CharField(
        max_length=255,
        blank=True,
        editable=False,
        help_text=_('This field will be automagically populated after uploading a file.'),
        null=True,
        verbose_name=_('mime type'),
    )

    md5sum = models.CharField(
        max_length=36,
        blank=True,
        editable=False,
        help_text=_('This field will be automagically populated after uploading a file.'),
        null=True,
        unique=True,
        verbose_name=_('MD5 checksum'),
    )

    def __str__(self):
        if self.title:
            return self.title
        if self.year:
            date = str(self.year)
            if self.month:
                date += '-'
                if self.month < 10:
                    date += str(0)
                date += str(self.month)
                if self.day:
                    date += '-'
                    if self.day < 10:
                        date += str(0)
                    date += str(self.day)
            return date
        return str(self.id)

    def clean(self):
        if self.file:
            md5 = hashlib.md5()
            for chunk in self.file.chunks():
                md5.update(chunk)
            self.md5sum = md5.hexdigest()
            existing = Entry.objects.filter(md5sum=self.md5sum)
            if existing.exists() and existing[0].pk != self.pk:
                raise ValidationError({'file': _('This file was already uploaded.')})
        super().clean()

    def save(self, force_insert=False, force_update=False, using=None, update_fields=None):
        super().save(force_insert, force_update, using, update_fields)
        if self.file:
            self.mime_type = magic.Magic(magic_file=MAGICFILE, mime=True).from_file(self.file.path)
        super().save()

    class Meta:
        ordering = ('year', 'month', 'day', 'title', 'description')
        verbose_name = _('entry')
        verbose_name_plural = _('entries')

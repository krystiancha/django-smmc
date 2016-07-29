from django.conf import settings

MAGICFILE = getattr(settings, 'SMMC_MAGICFILE', None)

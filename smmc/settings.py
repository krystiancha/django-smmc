from django.conf import settings

MAGICFILE = getattr(settings, 'SMMC_MAGICFILE', None)
RANDOM_ENTRIES_AMOUNT = getattr(settings, 'SMMC_RANDOM_ENTRIES_AMOUNT', 10)

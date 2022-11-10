from factory import LazyAttribute, Trait
from factory import Sequence, Factory, Iterator
from factory import SubFactory
from factory import lazy_attribute
from factory.django import DjangoModelFactory
from factory.fuzzy import FuzzyText
from faker import Factory as FakerFactory

from py_cover_letters.db.models import CoverLetter

faker = FakerFactory.create()
from pytz import timezone

TIME_ZONE = 'America/Panama'


class CoverLetterFactory(Factory):
    class Meta:
        model = CoverLetter

    timestamp_paid = LazyAttribute(lambda x: faker.date_time_between(start_date="-1m",
                                                                     end_date="now", tzinfo=timezone(TIME_ZONE)))

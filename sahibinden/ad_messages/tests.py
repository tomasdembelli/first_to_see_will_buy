from django.test import TestCase

import datetime
from django.utils import timezone

from .models import Ad, Message

# Create your tests here.
class AdModelTests(TestCase):

    def test_for_ads_published_in_the_future(self):
        """Returns False for Ads whose pub_date is in the future"""
        time_in_the_future = timezone.now() + datetime.timedelta(days=1)
        future_ad = Ad(pub_date=time_in_the_future)
        self.assertIs(future_ad.pub_date > timezone.now(), False)
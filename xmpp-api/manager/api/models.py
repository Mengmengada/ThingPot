from __future__ import unicode_literals

from django.db import models


class TimeStampedModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        abstract = True


class Category(TimeStampedModel):
    name = models.CharField(max_length=255)

    def __unicode__(self):
        return "%s" % self.name


class Tests(TimeStampedModel):
    name = models.CharField(max_length=255)
    categories = models.ForeignKey(Category, on_delete=models.CASCADE)

    def __unicode__(self):
        return "%s" % self.name


class ExecutedTest(TimeStampedModel):
    name = models.CharField(max_length=255)
    test = models.ForeignKey(Tests, on_delete=models.CASCADE)


class ExecutedTestConfiguration(TimeStampedModel):
    manager_ip1 = models.CharField(max_length=45)
    manager_ip2 = models.CharField(max_length=45)
    manager_ip3 = models.CharField(max_length=45)
    tester_ip = models.CharField(max_length=45)
    victim_ip = models.CharField(max_length=45)
    sniff_ip = models.CharField(max_length=45)
    checker_ip = models.CharField(max_length=45)
    sentPackets = models.IntegerField()
    filename = models.CharField(max_length=255)
    attack_interface = models.CharField(max_length=255)
    sniff_interface = models.CharField(max_length=255)
    sniff_command = models.CharField(max_length=255)
    sniff_filter = models.CharField(max_length=255)
    sniff_duration = models.IntegerField()
    check_command = models.CharField(max_length=255)
    check_ip = models.CharField(max_length=255)
    check_packets = models.CharField(max_length=255)
    executed_test = models.ForeignKey(ExecutedTest, on_delete=models.CASCADE)


class Result(TimeStampedModel):
    result = models.BooleanField(default=False)
    test = models.ForeignKey(ExecutedTest, on_delete=models.CASCADE)

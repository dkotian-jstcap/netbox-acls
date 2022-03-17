from django.contrib.postgres.fields import ArrayField
from django.db import models

from netbox.models import NetBoxModel
from utilities.choices import ChoiceSet


class ActionChoices(ChoiceSet):
    key = 'AccessListRule.action'

    CHOICES = (
        ('permit', 'Permit', 'green'),
        ('deny', 'Deny', 'red'),
        ('reject', 'Reject (Reset)', 'orange'),
    )


class ProtocolChoices(ChoiceSet):

    CHOICES = (
        ('tcp', 'TCP', 'blue'),
        ('udp', 'UDP', 'orange'),
        ('icmp', 'ICMP', 'purple'),
    )


class AccessList(NetBoxModel):
    name = models.CharField(
        max_length=100
    )
    default_action = models.CharField(
        max_length=30,
        choices=ActionChoices
    )
    comments = models.TextField(
        blank=True
    )

    class Meta:
        ordering = ('name',)

    def __str__(self):
        return self.name


class AccessListRule(NetBoxModel):
    access_list = models.ForeignKey(
        to=AccessList,
        on_delete=models.CASCADE,
        related_name='rules'
    )
    index = models.PositiveIntegerField()
    protocol = models.CharField(
        max_length=30,
        choices=ProtocolChoices,
        blank=True
    )
    source_prefix = models.ForeignKey(
        to='ipam.Prefix',
        on_delete=models.PROTECT,
        related_name='+',
        blank=True,
        null=True
    )
    source_ports = ArrayField(
        base_field=models.PositiveIntegerField(),
        blank=True,
        null=True
    )
    destination_prefix = models.ForeignKey(
        to='ipam.Prefix',
        on_delete=models.PROTECT,
        related_name='+',
        blank=True,
        null=True
    )
    destination_ports = ArrayField(
        base_field=models.PositiveIntegerField(),
        blank=True,
        null=True
    )
    action = models.CharField(
        max_length=30,
        choices=ActionChoices
    )
    description = models.CharField(
        max_length=500,
        blank=True
    )

    class Meta:
        ordering = ('access_list', 'index')
        unique_together = ('access_list', 'index')

    def __str__(self):
        return f'{self.access_list}: Rule {self.index}'

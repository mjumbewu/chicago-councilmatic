from django.db import models
from django.contrib.contenttypes import generic


class Voice (object):
    """Factory class for opinion models.

    The Voice class should be used to create and modify opinions.  You should
    only need to use the Opinion or StatementRevision classes directly when
    querying the models.

    >>> voice = Voice(user)
    >>> opinion = voice.express_opinion_about(item,
    ...                                       position='support',
    ...                                       statement='It\'s a good idea')
    >>> voice.revise(opinion,
    ...              position='oppose',
    ...              statement='I don\'t like it anymore')
    >>> voice.agree_with(other_opinion)

    """

    def __init__(self, user):
      self.user = user

    def express_opinion_about(self, target, statement, position):
        opinion = Opinion.objects.create(
            opiner=self.user,
            target=target)
        self.__create_revision(
            opinion,
            statement=statement,
            position=position)

        return opinion

    def __create_revision(self, opinion, statement, position):
        revision = StatementRevision.objects.create(
            opinion=opinion,
            statement=statement,
            position=position)

        return revision

    def revise(self, opinion, statement=None, position=None):
        if statement is None:
            statement = opinion.latest.statement
        if position is None:
            position = opinion.latest.position

        self.__create_revision(opinion, statement, position)

    def agree_with(self, opinion):
        pass


class Opinion (models.Model):
    opiner = models.ForeignKey('auth.User', related_name='opinions')
    """The user who made the opinion"""

    # revisions (backref)
    """The text of the opinion"""

    agreers = models.ManyToManyField('auth.User', related_name='agreements')
    """Users who agree with the opinion"""

    target_type = models.ForeignKey('contenttypes.ContentType')
    target_id = models.PositiveIntegerField()
    target = generic.GenericForeignKey('target_type', 'target_id')
    """The target object of the user's opinion"""

    @property
    def latest(self):
        """The most recent statement revision made"""
        return self.revisions.order_by('-datetime')[0]


class StatementRevision (models.Model):
    POSITION_CHOICES = (
        ('support', 'Support'),
        ('oppose', 'Oppose'),
        ('abstain', 'Abstain'),
    )

    opinion = models.ForeignKey('Opinion', related_name='revisions')
    """The opinion for which this statement was made"""

    statement = models.TextField()
    """The text of the opinion"""

    position = models.CharField(max_length=16, choices=POSITION_CHOICES)
    """The polarity of the statement"""

    datetime = models.DateTimeField(auto_now=True)
    """The date and time that the revision was made"""

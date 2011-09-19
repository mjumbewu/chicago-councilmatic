from django.test import TestCase
from nose.tools import *

from django.contrib.auth.models import User
from django.contrib.contenttypes.models import ContentType
from opinions.forms import OpinionStatementForm
from opinions.models import Opinion
from opinions.models import StatementRevision
from opinions.models import Voice
from phillyleg.models import LegFile

class Test__Opinion_latest:

    def setup(self):
        User.objects.all().delete()
        Opinion.objects.all().delete()
        LegFile.objects.all().delete()

        self.me = User.objects.create_user('me', 'pass', 'email')
        self.legfile = LegFile.objects.create(key=123, id='456')

    @istest
    def should_return_the_latest_revision (self):
        opinion = Opinion.objects.create(opiner=self.me, target=self.legfile)
        StatementRevision.objects.create(opinion=opinion, statement='blah1', position='support')
        StatementRevision.objects.create(opinion=opinion, statement='blah2', position='oppose')
        StatementRevision.objects.create(opinion=opinion, statement='blah3', position='abstain')
        StatementRevision.objects.create(opinion=opinion, statement='blah4', position='oppose')

        assert_equal(opinion.latest.statement, 'blah4')
        assert_equal(opinion.latest.position, 'oppose')


class Test__Voice_expressOpinionAbout:

    def setup(self):
        User.objects.all().delete()
        Opinion.objects.all().delete()
        LegFile.objects.all().delete()

        self.me = User.objects.create_user('me', 'pass', 'email')
        self.legfile = LegFile.objects.create(key=123, id='456')

    @istest
    def should_create_an_opinion_with_the_given_target (self):
        voice = Voice(self.me)
        voice.express_opinion_about(self.legfile, statement='blah1', position='support')

        opinion = Opinion.objects.all()[0]
        assert_equal(opinion.opiner, self.me)
        assert_equal(opinion.target, self.legfile)
        assert_equal(opinion.latest.statement, 'blah1')
        assert_equal(opinion.latest.position, 'support')

    @istest
    def sets_up_deferred_saving_if_commit_is_False (self):
        voice = Voice(self.me)
        opinion = voice.express_opinion_about(self.legfile, statement='blah1', position='support', commit=False)

        assert_is_none(opinion.pk)
        assert hasattr(voice, 'save_revision')


class Test__Voice_revise:

    def setup(self):
        User.objects.all().delete()
        Opinion.objects.all().delete()
        LegFile.objects.all().delete()

        self.me = User.objects.create_user('me', 'pass', 'email')
        self.legfile = LegFile.objects.create(key=123, id='456')
        self.opinion = Opinion.objects.create(opiner=self.me, target=self.legfile)
        StatementRevision.objects.create(opinion=self.opinion, statement='blah1', position='oppose')

    @istest
    def should_add_a_revision_with_the_given_properties (self):
        voice = Voice(self.me)
        voice.revise(self.opinion, statement='blah2')

        revision = StatementRevision.objects.order_by('-datetime')[0]
        assert_equal(revision.statement, 'blah2')
        assert_equal(revision.position, 'oppose')

        voice.revise(self.opinion, position='support')

        revision = StatementRevision.objects.order_by('-datetime')[0]
        assert_equal(revision.statement, 'blah2')
        assert_equal(revision.position, 'support')

        voice.revise(self.opinion, statement='blah3', position='abstain')

        revision = StatementRevision.objects.order_by('-datetime')[0]
        assert_equal(revision.statement, 'blah3')
        assert_equal(revision.position, 'abstain')

    @istest
    def sets_up_deferred_saving_if_commit_is_False (self):
        voice = Voice(self.me)
        voice.revise(self.opinion, statement='blah1', position='support', commit=False)

        num_revisions = len(self.opinion.revisions.all())
        assert_equal(num_revisions, 1)
        assert hasattr(voice, 'save_revision')


class Test__OpinionStatementForm_save:

    def setup(self):
        User.objects.all().delete()
        Opinion.objects.all().delete()
        LegFile.objects.all().delete()

        self.me = User.objects.create_user('me', 'pass', 'email')
        self.legfile = LegFile.objects.create(key=123, id='456')

    @istest
    def creates_a_new_opinion_if_one_by_the_user_for_the_target_does_not_exist (self):
        form_data = {
            'opiner': self.me.pk,
            'target_type': ContentType.objects.get_for_model(LegFile).pk,
            'target_id': self.legfile.pk,
            'position': 'support',
            'statement': 'It is a good idea.',
        }
        form = OpinionStatementForm(data=form_data)

        assert form.is_valid(), form.errors
        form.save()

        num_opinions = len(Opinion.objects.all())
        num_revisions = len(StatementRevision.objects.all())
        assert_equal(num_opinions, 1)
        assert_equal(num_revisions, 1)

    @istest
    def creates_a_new_revision_if_an_opinion_by_the_user_for_the_target_exists (self):
        opinion = Opinion.objects.create(opiner=self.me, target=self.legfile)
        StatementRevision.objects.create(opinion=opinion, statement='blah1', position='oppose')

        form_data = {
            'opiner': self.me.pk,
            'target_type': ContentType.objects.get_for_model(LegFile).pk,
            'target_id': self.legfile.pk,
            'position': 'support',
            'statement': 'It is a good idea.',
        }
        form = OpinionStatementForm(data=form_data)

        assert form.is_valid(), form.errors
        form.save()

        num_opinions = len(Opinion.objects.all())
        num_revisions = len(StatementRevision.objects.all())
        assert_equal(num_opinions, 1)
        assert_equal(num_revisions, 2)

    @istest
    def sets_up_deferred_saving_if_commit_is_False (self):
        form_data = {
            'opiner': self.me.pk,
            'target_type': ContentType.objects.get_for_model(LegFile).pk,
            'target_id': self.legfile.pk,
            'position': 'support',
            'statement': 'It is a good idea.',
        }
        form = OpinionStatementForm(data=form_data)

        assert form.is_valid(), form.errors
        opinion = form.save(commit=False)

        assert_is_none(opinion.pk)
        assert hasattr(form, 'save_m2m')

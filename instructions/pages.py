from otree.api import Currency as c, currency_range
from ._builtin import Page as oTreePage, WaitPage
from .models import Constants
import datetime
from .generic_pages import Page
from django.conf import settings
from django.utils.translation import ugettext_lazy as _


class Lang(oTreePage):
    form_model = 'player'
    form_fields = ['lang']

    def before_next_page(self):
        lang_chosen = self.player.lang
        self.request.session[settings.LANGUAGE_SESSION_KEY] = lang_chosen
        self.participant.vars['lang_chosen'] = lang_chosen
        self.player.username = self.participant.label


class Intro(Page):
    form_model = 'player'
    form_fields = ['consent']

    def error_message(self, values):
        if not values['consent']:
            return _('Please answer the question.')

    def js_vars(self):
        username_value = self.participant.label
        return dict(url='https://survey.maximiles.com/screenout?p=73953&m='+username_value)

    def before_next_page(self):
        if self.player.consent == 'no':
            self.participant.vars['consent'] = 'no'
            self.participant.vars['time_instruction'] = 0
        else:
            self.participant.vars['consent'] = 'yes'


class Instruct0(Page):
    form_model = 'player'

    def before_next_page(self):
        start_datetime = datetime.datetime.now()
        self.participant.vars['start_time'] = start_datetime

    def is_displayed(self):
        return self.participant.vars['consent'] == 'yes'


class Instruct1(Page):
    form_model = 'player'

    def is_displayed(self):
        return self.participant.vars['consent'] == 'yes'


class Instruct2(Page):
    form_model = 'player'

    def is_displayed(self):
        return self.participant.vars['consent'] == 'yes'


class Instruct3_immediate(Page):
    form_model = 'player'

    def is_displayed(self):
        return self.participant.vars['consent'] == 'yes' and self.participant.vars['treatment'] == 'immediate'


class Instruct3_deferred(Page):
    form_model = 'player'

    def is_displayed(self):
        return self.participant.vars['consent'] == 'yes' and self.participant.vars['treatment'] == 'deferred'


class Instruct3_matching(Page):
    form_model = 'player'

    def is_displayed(self):
        return self.participant.vars['consent'] == 'yes' and self.participant.vars['treatment'] == 'matching'


class Instruct4_immediate(Page):
    form_model = 'player'

    def is_displayed(self):
        return self.participant.vars['consent'] == 'yes' and self.participant.vars['treatment'] == 'immediate'

    def before_next_page(self):
        end_datetime = datetime.datetime.now()
        start_time = self.participant.vars['start_time']
        self.player.time_instruction = round((end_datetime - start_time).total_seconds())
        self.participant.vars['time_instruction'] = round((end_datetime - start_time).total_seconds())


class Instruct4_deferred(Page):
    form_model = 'player'

    def is_displayed(self):
        return self.participant.vars['consent'] == 'yes' and self.participant.vars['treatment'] == 'deferred'

    def before_next_page(self):
        end_datetime = datetime.datetime.now()
        start_time = self.participant.vars['start_time']
        self.player.time_instruction = round((end_datetime - start_time).total_seconds())
        self.participant.vars['time_instruction'] = round((end_datetime - start_time).total_seconds())


class Instruct4_matching(Page):
    form_model = 'player'

    def is_displayed(self):
        return self.participant.vars['consent'] == 'yes' and self.participant.vars['treatment'] == 'matching'

    def before_next_page(self):
        end_datetime = datetime.datetime.now()
        start_time = self.participant.vars['start_time']
        self.player.time_instruction = round((end_datetime - start_time).total_seconds())
        self.participant.vars['time_instruction'] = round((end_datetime - start_time).total_seconds())


class End_instruct(Page):
    form_model = 'player'

    def is_displayed(self):
        return self.participant.vars['time_instruction'] < 30 and self.participant.vars['consent'] == 'yes'

    def js_vars(self):
        username_value = self.participant.label
        return dict(url='https://survey.maximiles.com/quality?p=73953&m='+username_value)


page_sequence = [Lang, Intro, Instruct0, Instruct1, Instruct2, Instruct3_immediate, Instruct3_deferred,
                 Instruct3_matching, Instruct4_immediate, Instruct4_deferred, Instruct4_matching, End_instruct]

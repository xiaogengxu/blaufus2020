from otree.api import Currency as c, currency_range
from ._builtin import Page as oTreePage, WaitPage
from .models import Constants
import datetime
from django.utils.translation import ugettext_lazy as _
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


class Instruct1(Page):
    form_model = 'player'


class Instruct2(Page):
    form_model = 'player'


class Instruct3(Page):
    form_model = 'player'

    def vars_for_template(self):
        if self.participant.vars['treatment'] == 'immediate':
            para1 = _('In each period while you work, you will decide how much of your '+'<b>Net Wage</b>'+' to put on '+'<b>'+'Savings'+'</b>'+' for the rest phase.')
        else:
            para1 = _('Following the work task, at each working period, you will decide how much of your '+'<b>'+'Net Wage'+'</b>'+' to put on '+'<b>'+'Savings'+'</b>'+' for the rest phase.')

        if self.participant.vars['treatment'] != 'matching':
            para2 = 'Your '+'<b>'+'Savings'+'</b>'+' earn 5% interest per period.'
        else:
            para2 = 'You will receive a '+'<b>'+'bonus'+'</b>'+' of 66.67% over the amount saved. ' \
                    'For example, if you save 100 points, your bonus will be 67 points.'

        if self.participant.vars['treatment'] == 'deferred':
            para3 = 'Since you do not pay taxes on Savings, ' \
                    'you will receive 40% of the amount that you decide to save in each period as a '+'<b>'+\
                    'Tax Refund'+'</b>'+', which will be added automatically to your '+'<b>'+'Reward'+'</b>'+\
                    ' in each period. For example, if you save 100 points in one period, ' \
                    'you will receive 40 points as a '+'<b>'+'Tax Refund'+'</b>'+' in that period.'
        elif self.participant.vars['treatment'] == 'matching':
            para3 = 'Your '+'<b>'+'Savings'+'</b>'+' earn 5% interest per period.'
        else:
            para3 = ''

        if self.participant.vars['treatment'] != 'matching':
            para4 = 'You will receive your '+'<b>'+'Savings'+'</b>'+' including accumulated interest back during the '\
                    +'<b>'+'rest phase'+'</b>'+'. The computer will automatically calculate equal '+'<b>'+'Withdraw'\
                    +'</b>'+' per each period of the rest phase.'
        else:
            para4 = 'You will receive your '+'<b>'+'Savings'+'</b>'+' back during the '+'<b>'+'rest phase'+'</b>'+\
                    '. The computer will automatically calculate equal '+'<b>'+'Withdraw'+'</b>'+\
                    ' per each period of the rest phase.'

        if self.participant.vars['treatment'] == 'immediate':
            para5 = 'Savings '+'<b>'+'Withdraws'+'</b>'+' in the '+'<b>'+'rest phase'+'</b>'+' are tax-free.'
        else:
            para5 = 'Savings '+'<b>'+'Withdraws'+'</b>'+' in the '+'<b>'+'rest phase'+'</b>'+\
                    ' are subject to a tax of 40%.'

        return {
            'para1': para1,
            'para2': para2,
            'para3': para3,
            'para4': para4,
            'para5': para5
        }


class Instruct4(Page):
    form_model = 'player'

    def vars_for_template(self):
        if self.participant.vars['treatment'] == 'deferred':
            str_deferred = _(', plus the tax refund')
        else:
            str_deferred = ''

        if self.participant.vars['treatment'] != 'immediate':
            str_tax = ' minus its '+'<b>'+'Tax'+'</b>'+' of 40%'
        else:
            str_tax = ''

        return {
            'str_deferred': str_deferred,
            'str_tax': str_tax
        }

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
        return dict(url='https://survey.maximiles.com/screenout?p=73953&m='+username_value)


page_sequence = [Lang, Intro, Instruct0, Instruct1, Instruct2, Instruct3, Instruct4, End_instruct]

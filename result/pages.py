from otree.api import Currency as c, currency_range
from .models import Constants
from ._builtin import Page as oTreePage, WaitPage
import datetime
from .generic_pages import Page
from django.conf import settings
from django.utils.translation import ugettext_lazy as _
from itertools import chain
from .generic_pages import Page


class Result(Page):
    form_model = 'player'

    def is_displayed(self):
        if self.participant.vars['time_instruction'] >= 30 and self.participant.vars['end'] == 0:
            return self.participant.vars['time_choice'] != 'delay0' and self.participant.vars['consent'] == 'yes'
        else:
            return False

    def vars_for_template(self):
        if self.participant.vars['reward_period'] < 15:
            reward_life = 1
            reward_period = self.participant.vars['reward_period']
        else:
            reward_life = 2
            reward_period = self.participant.vars['reward_period'] - 15
        if self.participant.vars['treatment'] == 'immediate':
            if self.participant.vars['reward_period'] in chain(range(1, 11), range(16, 26)):
                str_reward = 'reward_imme'+str(self.participant.vars['reward_period'])
                reward = self.participant.vars[str_reward]
            elif self.participant.vars['reward_period'] in range(11, 16):
                reward = self.participant.vars['reward_imme11']
            elif self.participant.vars['reward_period'] in range(26, 31):
                reward = self.participant.vars['reward_imme26']
        if self.participant.vars['treatment'] == 'deferred':
            if self.participant.vars['reward_period'] in chain(range(1, 11), range(16, 26)):
                str_reward = 'reward_def'+str(self.participant.vars['reward_period'])
                reward = self.participant.vars[str_reward]
            elif self.participant.vars['reward_period'] in range(11, 16):
                reward = self.participant.vars['reward_def11']
            elif self.participant.vars['reward_period'] in range(26, 31):
                reward = self.participant.vars['reward_def26']
        if self.participant.vars['treatment'] == 'matching':
            if self.participant.vars['reward_period'] in chain(range(1, 11), range(16, 26)):
                str_reward = 'reward_mat'+str(self.participant.vars['reward_period'])
                reward = self.participant.vars[str_reward]
            elif self.participant.vars['reward_period'] in range(11, 16):
                reward = self.participant.vars['reward_mat11']
            elif self.participant.vars['reward_period'] in range(26, 31):
                reward = self.participant.vars['reward_mat26']
        reward_euro = round(reward/25, 2)
        risk_choice = self.participant.vars['risk_choice']
        invest_num = reward_euro * self.participant.vars['risk_choice']

        if self.participant.vars['risk_outcome'] == 'win':
            earn_invest_num = 3.5 * risk_choice * reward_euro
            if self.participant.vars['lang_chosen'] == 'en':
                risk_outcome = 'win'
            else:
                risk_outcome = 'Gewinn'
        else:
            earn_invest_num = 0
            if self.participant.vars['lang_chosen'] == 'en':
                risk_outcome = 'loss'
            else:
                risk_outcome = 'Verlust'

        earn_safe_num = (100 - risk_choice) * reward_euro
        invest = round(invest_num/100, 2)
        earn_invest = round(earn_invest_num/100, 2)
        earn_safe = round(earn_safe_num/100, 2)
        total_num = earn_invest + earn_safe
        total = round(total_num, 2)

        if self.participant.vars['time_choice'] == 'delay1':
            pay_time = _('in 1 month')
            bonus_time_num = total * 0.05
            total1_num = total + bonus_time_num
        elif self.participant.vars['time_choice'] == 'delay2':
            pay_time = _('in 2 months')
            bonus_time_num = total * 0.103
            total1_num = total + bonus_time_num
        else:
            pay_time = _('in 3 months')
            bonus_time_num = total * 0.158
            total1_num = total + bonus_time_num

        bonus_time = round(bonus_time_num, 2)
        total1 = round(total1_num, 2)

        return {
            'reward_life': reward_life,
            'reward_period': reward_period,
            'reward_euro': reward_euro,
            'risk_outcome': risk_outcome,
            'risk_choice': risk_choice,
            'invest': invest,
            'earn_invest': earn_invest,
            'total': total,
            'pay_time': pay_time,
            'bonus_time': bonus_time,
            'total1': total1
        }


class Result_nodelay(Page):
    form_model = 'player'

    def is_displayed(self):
        if self.participant.vars['time_instruction'] >= 30 and self.participant.vars['end'] == 0:
            return self.participant.vars['time_choice'] == 'delay0' and self.participant.vars['consent'] == 'yes'
        else:
            return False

    def vars_for_template(self):
        if self.participant.vars['reward_period'] < 15:
            reward_life = 1
            reward_period = self.participant.vars['reward_period']
        else:
            reward_life = 2
            reward_period = self.participant.vars['reward_period'] - 15
        if self.participant.vars['treatment'] == 'immediate':
            if self.participant.vars['reward_period'] in chain(range(1, 11), range(16, 26)):
                str_reward = 'reward_imme'+str(self.participant.vars['reward_period'])
                reward = self.participant.vars[str_reward]
            elif self.participant.vars['reward_period'] in range(11, 16):
                reward = self.participant.vars['reward_imme11']
            elif self.participant.vars['reward_period'] in range(26, 31):
                reward = self.participant.vars['reward_imme26']
        if self.participant.vars['treatment'] == 'deferred':
            if self.participant.vars['reward_period'] in chain(range(1, 11), range(16, 26)):
                str_reward = 'reward_def'+str(self.participant.vars['reward_period'])
                reward = self.participant.vars[str_reward]
            elif self.participant.vars['reward_period'] in range(11, 16):
                reward = self.participant.vars['reward_def11']
            elif self.participant.vars['reward_period'] in range(26, 31):
                reward = self.participant.vars['reward_def26']
        if self.participant.vars['treatment'] == 'matching':
            if self.participant.vars['reward_period'] in chain(range(1, 11), range(16, 26)):
                str_reward = 'reward_mat'+str(self.participant.vars['reward_period'])
                reward = self.participant.vars[str_reward]
            elif self.participant.vars['reward_period'] in range(11, 16):
                reward = self.participant.vars['reward_mat11']
            elif self.participant.vars['reward_period'] in range(26, 31):
                reward = self.participant.vars['reward_mat26']
        reward_euro = round(reward/25, 2)
        risk_choice = self.participant.vars['risk_choice']
        invest_num = reward_euro * self.participant.vars['risk_choice']

        if self.participant.vars['risk_outcome'] == 'win':
            earn_invest_num = 3.5 * risk_choice * reward_euro
            if self.participant.vars['lang_chosen'] == 'en':
                risk_outcome = 'win'
            else:
                risk_outcome = 'Gewinn'
        else:
            earn_invest_num = 0
            if self.participant.vars['lang_chosen'] == 'en':
                risk_outcome = 'loss'
            else:
                risk_outcome = 'Verlust'

        earn_safe_num = (100 - risk_choice) * reward_euro
        invest = round(invest_num/100, 2)
        earn_invest = round(earn_invest_num/100, 2)
        earn_safe = round(earn_safe_num/100, 2)
        total_num = earn_invest + earn_safe
        total = round(total_num, 2)

        return {
            'reward_life': reward_life,
            'reward_period': reward_period,
            'reward_euro': reward_euro,
            'risk_outcome': risk_outcome,
            'risk_choice': risk_choice,
            'invest': invest,
            'earn_invest': earn_invest,
            'total': total
        }


page_sequence = [Result, Result_nodelay]

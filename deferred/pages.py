from otree.api import Currency as c, currency_range
from ._builtin import Page, WaitPage
from .models import Constants
from sympy.solvers import solve
from sympy import Symbol
from .generic_pages import Page
from django.utils.translation import ugettext_lazy as _
import time
from django.utils.text import format_lazy


def get_timeout_seconds(player):
    return player.participant.vars['expiry'] - time.time()


class Start(Page):
    form_model = 'player'

    def is_displayed(self):
        return self.participant.vars['time_instruction'] >= 30 & self.player.round_number == 1 and \
               self.participant.vars['end'] == 0 and self.participant.vars['consent'] == 'yes' and \
               get_timeout_seconds(self.player) > 3


class Task(Page):
    form_model = 'player'
    form_fields = ['task_finished']

    def is_displayed(self):
        return self.participant.vars['time_instruction'] >= 30 and \
               (self.player.round_number < 11 or (self.player.round_number > 15 and self.player.round_number < 26)) and \
               self.participant.vars['end'] == 0 and self.participant.vars['consent'] == 'yes' and \
               get_timeout_seconds(self.player) > 3

    def error_message(self, values):
        if not values['task_finished']:
            round_num = self.player.round_number
            str_slide = 'slide_moveto'+str(round_num)
            str1 = _('Your sliders are not all set to target number ')
            str2 = _('. Please, try again.')
            str_error = format_lazy('{}{}{}', str1, str(self.participant.vars[str_slide]), str2)
            return str_error

    def vars_for_template(self):
        round_num = self.player.round_number
        if self.player.round_number < 16:
            round_num_title = self.player.round_number
            round_num_bar = 44+(self.player.round_number-1)*2
            life = 1
        else:
            round_num_title = self.player.round_number - 15
            round_num_bar = 68+(self.player.round_number-16)*2
            life = 2
        str_slide = 'slide_moveto'+str(round_num)
        slide_moveto = self.participant.vars[str_slide]
        return {
            'round_num_title': round_num_title,
            'round_num_bar': round_num_bar,
            'life': life,
            'slide_moveto': slide_moveto
        }


class Decision1(Page):
    form_model = 'player'
    form_fields = ['saving_def1', 'check_def1', 'reward_def1']

    def is_displayed(self):
        return self.participant.vars['time_instruction'] >= 30 and self.player.round_number < 11 and \
               self.participant.vars['end'] == 0 and self.participant.vars['consent'] == 'yes' and \
               get_timeout_seconds(self.player) > 3

    def error_message(self, values):
        if not values['check_def1']:
            return _('Please decide how much you would like to save.')

    def vars_for_template(self):
        round_num = self.player.round_number
        round_num_show = self.player.round_number - 1
        round_num_bar = 44 + (self.player.round_number - 1) * 2
        life = 1
        saving_list = []
        refund_list = []
        reward_list = []
        balance_list = []
        for i in range(1, round_num+1):
            if i == 1 or i < round_num:
                str_saving = 'saving_def'+str(i)
                str_refund = 'refund_def'+str(i)
                str_reward = 'reward_def'+str(i)
                str_balance = 'balance_def'+str(i)
                saving_list.append(self.participant.vars[str_saving])
                refund_list.append(self.participant.vars[str_refund])
                reward_list.append(self.participant.vars[str_reward])
                balance_list.append(self.participant.vars[str_balance])
            else:
                break
        avg_list = round(sum(saving_list)/len(saving_list))
        for j in range(round_num, 11):
            saving_list.append('')
            refund_list.append('')
        for k in range(round_num, 16):
            reward_list.append('')
            balance_list.append('')
        if round_num == 1:
            saving_list[0] = ''
            refund_list[0] = ''
            reward_list[0] = ''
            balance_list[0] = ''
        if round_num == 1:
            bal_str = 'balance_def1'
        else:
            bal_str = 'balance_def' + str(round_num-1)
        balance10_simu_num = self.participant.vars[bal_str]*1.05**(11-round_num)
        for m in range(round_num, 11):
            balance10_simu_num += avg_list*1.05**(10-m)
        x = Symbol('x')
        rest_points_num = solve(((((balance10_simu_num*1.05-x)*1.05-x)*1.05-x)*1.05-x)*1.05-x)
        rest_points = round(0.6*rest_points_num[0])
        return {
            'round_num': round_num,
            'round_num_show': round_num_show,
            'round_num_bar': round_num_bar,
            'life': life,
            'saving_list': saving_list,
            'refund_list': refund_list,
            'reward_list': reward_list,
            'balance_list': balance_list,
            'avg_list': avg_list,
            'rest_points': rest_points
        }

    def before_next_page(self):
        round_num = self.player.round_number
        str_saving = 'saving_def'+str(round_num)
        str_refund = 'refund_def'+str(round_num)
        str_reward = 'reward_def'+str(round_num)
        str_balance = 'balance_def'+str(round_num)
        str_saving1 = 'saving_def1'
        str_reward1 = 'reward_def1'
        self.participant.vars[str_saving] = getattr(self.player.in_round(round_num), str_saving1)
        self.participant.vars[str_refund] = round(0.4*getattr(self.player.in_round(round_num), str_saving1))
        self.participant.vars[str_reward] = getattr(self.player.in_round(round_num), str_reward1)
        balance = 0
        for r in range(1, round_num+1):
            save_str = 'saving_def'+str(r)
            balance += self.participant.vars[save_str]*1.05**(round_num-r)
        self.participant.vars[str_balance] = round(balance)


class Decision2(Page):
    form_model = 'player'
    form_fields = ['saving_def2', 'check_def2', 'reward_def2']

    def is_displayed(self):
        return self.participant.vars['time_instruction'] >= 30 and (self.player.round_number > 15 and self.player.round_number < 26) \
               and self.participant.vars['end'] == 0 and self.participant.vars['consent'] == 'yes' and \
               get_timeout_seconds(self.player) > 3

    def error_message(self, values):
        if not values['check_def2']:
            return _('Please decide how much you would like to save.')

    def vars_for_template(self):
        round_num = self.player.round_number
        round_num_show = self.player.round_number - 16
        round_num_title = self.player.round_number - 15
        round_num_bar = 68 + (self.player.round_number - 16) * 2
        life = 2
        saving_list = []
        refund_list = []
        reward_list = []
        balance_list = []
        for i in range(16, round_num+1):
            if i == 16 or i < round_num:
                str_saving = 'saving_def'+str(i)
                str_refund = 'refund_def'+str(i)
                str_reward = 'reward_def'+str(i)
                str_balance = 'balance_def'+str(i)
                saving_list.append(self.participant.vars[str_saving])
                refund_list.append(self.participant.vars[str_refund])
                reward_list.append(self.participant.vars[str_reward])
                balance_list.append(self.participant.vars[str_balance])
            else:
                break
        avg_list = round(sum(saving_list)/len(saving_list))
        for j in range(round_num, 26):
            saving_list.append('')
            refund_list.append('')
        for k in range(round_num, 31):
            reward_list.append('')
            balance_list.append('')
        if round_num == 16:
            saving_list[0] = ''
            refund_list[0] = ''
            reward_list[0] = ''
            balance_list[0] = ''
        if round_num == 16:
            bal_str = 'balance_def16'
        else:
            bal_str = 'balance_def' + str(round_num-1)
        balance25_simu_num = self.participant.vars[bal_str]*1.05**(26-round_num)
        for m in range(round_num, 26):
            balance25_simu_num += avg_list*1.05**(25-m)
        x = Symbol('x')
        rest_points_num = solve(((((balance25_simu_num*1.05-x)*1.05-x)*1.05-x)*1.05-x)*1.05-x)
        rest_points = round(0.6*rest_points_num[0])
        return {
            'round_num': round_num,
            'round_num_show': round_num_show,
            'round_num_title': round_num_title,
            'round_num_bar': round_num_bar,
            'life': life,
            'saving_list': saving_list,
            'refund_list': refund_list,
            'reward_list': reward_list,
            'balance_list': balance_list,
            'avg_list': avg_list,
            'rest_points': rest_points
        }

    def before_next_page(self):
        round_num = self.player.round_number
        str_saving = 'saving_def'+str(round_num)
        str_refund = 'refund_def'+str(round_num)
        str_reward = 'reward_def'+str(round_num)
        str_balance = 'balance_def'+str(round_num)
        str_saving1 = 'saving_def2'
        str_reward1 = 'reward_def2'
        self.participant.vars[str_saving] = getattr(self.player.in_round(round_num), str_saving1)
        self.participant.vars[str_refund] = round(0.4*getattr(self.player.in_round(round_num), str_saving1))
        self.participant.vars[str_reward] = getattr(self.player.in_round(round_num), str_reward1)
        balance = 0
        for r in range(16, round_num+1):
            save_str = 'saving_def'+str(r)
            balance += self.participant.vars[save_str]*1.05**(round_num-r)
        self.participant.vars[str_balance] = round(balance)


class Rest1(Page):
    form_model = 'player'
    form_fields = ['reward_def1']

    def is_displayed(self):
        return self.participant.vars['time_instruction'] >= 30 and (self.player.round_number > 10 and self.player.round_number < 16) \
               and self.participant.vars['end'] == 0 and self.participant.vars['consent'] == 'yes' and \
               get_timeout_seconds(self.player) > 3

    def vars_for_template(self):
        life = 1
        round_num = self.player.round_number
        round_num_bar = self.player.round_number+52
        saving_list = []
        refund_list = []
        reward_list = []
        balance_list = []
        withdraw_list = []
        balance10 = self.participant.vars['balance_def10']
        for i in range(1, 11):
            str_saving = 'saving_def'+str(i)
            str_refund = 'refund_def'+str(i)
            str_reward = 'reward_def'+str(i)
            str_balance = 'balance_def'+str(i)
            saving_list.append(self.participant.vars[str_saving])
            refund_list.append(self.participant.vars[str_refund])
            reward_list.append(self.participant.vars[str_reward])
            balance_list.append(self.participant.vars[str_balance])
            withdraw_list.append('')
        x = Symbol('x')
        rest_reward_num = solve(((((self.participant.vars['balance_def10']*1.05-x)*1.05-x)*1.05-x)*1.05-x)*1.05-x)
        rest_reward_num = int(rest_reward_num[0])+1
        rest_reward = round(0.6*rest_reward_num)
        for k in range(11, round_num+1):
            reward_list.append(rest_reward)
            withdraw_list.append(rest_reward_num)
            str_balance = 'balance_def'+str(k-1)
            balance_num = self.participant.vars[str_balance]*1.05-rest_reward_num
            if balance_num < 0:
                balance_num = 0
            balance_list.append(round(balance_num))
        return {
            'life': life,
            'round_num': round_num,
            'round_num_bar': round_num_bar,
            'saving_list': saving_list,
            'refund_list': refund_list,
            'reward_list': reward_list,
            'balance_list': balance_list,
            'withdraw_list': withdraw_list,
            'balance10': balance10,
            'rest_reward': rest_reward,
            'rest_reward_num': rest_reward_num
        }

    def before_next_page(self):
        round_num = self.player.round_number
        x = Symbol('x')
        rest_reward_num = solve(((((self.participant.vars['balance_def10']*1.05-x)*1.05-x)*1.05-x)*1.05-x)*1.05-x)
        rest_reward_num = int(rest_reward_num[0])+1
        rest_reward = round(0.6*rest_reward_num)
        str_reward = 'reward_def1'
        setattr(self.player.in_round(round_num), str_reward, rest_reward)
        self.participant.vars['reward_def11'] = rest_reward
        str_balance = 'balance_def'+str(round_num-1)
        balance_num = self.participant.vars[str_balance]*1.05-rest_reward_num
        str_balance1 = 'balance_def'+str(round_num)
        self.participant.vars[str_balance1] = round(balance_num)


class Rest2(Page):
    form_model = 'player'
    form_fields = ['reward_def2']

    def is_displayed(self):
        return self.participant.vars['time_instruction'] >= 30 and (self.player.round_number > 25 and self.player.round_number < 31) \
               and self.participant.vars['end'] == 0 and self.participant.vars['consent'] == 'yes' and \
               get_timeout_seconds(self.player) > 3

    def vars_for_template(self):
        life = 2
        round_num_title = self.player.round_number - 15
        round_num_bar = self.player.round_number + 62
        round_num = self.player.round_number
        saving_list = []
        refund_list = []
        reward_list = []
        balance_list = []
        withdraw_list = []
        balance25 = self.participant.vars['balance_def25']
        for i in range(16, 26):
            str_saving = 'saving_def'+str(i)
            str_refund = 'refund_def'+str(i)
            str_reward = 'reward_def'+str(i)
            str_balance = 'balance_def'+str(i)
            saving_list.append(self.participant.vars[str_saving])
            refund_list.append(self.participant.vars[str_refund])
            reward_list.append(self.participant.vars[str_reward])
            balance_list.append(self.participant.vars[str_balance])
            withdraw_list.append('')
        x = Symbol('x')
        rest_reward_num = solve(((((self.participant.vars['balance_def25']*1.05-x)*1.05-x)*1.05-x)*1.05-x)*1.05-x)
        rest_reward_num = int(rest_reward_num[0])+1
        rest_reward = round(0.6*rest_reward_num)
        for k in range(26, round_num+1):
            reward_list.append(rest_reward)
            withdraw_list.append(rest_reward_num)
            str_balance = 'balance_def'+str(k-1)
            balance_num = self.participant.vars[str_balance]*1.05-rest_reward_num
            if balance_num < 0:
                balance_num = 0
            balance_list.append(round(balance_num))
        return {
            'life': life,
            'round_num_title': round_num_title,
            'round_num_bar': round_num_bar,
            'round_num': round_num,
            'saving_list': saving_list,
            'refund_list': refund_list,
            'reward_list': reward_list,
            'balance_list': balance_list,
            'withdraw_list': withdraw_list,
            'balance25': balance25,
            'rest_reward': rest_reward,
            'rest_reward_num': rest_reward_num
        }

    def before_next_page(self):
        round_num = self.player.round_number
        x = Symbol('x')
        rest_reward_num = solve(((((self.participant.vars['balance_def25']*1.05-x)*1.05-x)*1.05-x)*1.05-x)*1.05-x)
        rest_reward_num = int(rest_reward_num[0])+1
        rest_reward = round(0.6*rest_reward_num)
        str_reward = 'reward_def2'
        setattr(self.player.in_round(round_num), str_reward, rest_reward)
        self.participant.vars['reward_def26'] = rest_reward
        str_balance = 'balance_def'+str(round_num-1)
        balance_num = self.participant.vars[str_balance]*1.05-rest_reward_num
        str_balance1 = 'balance_def'+str(round_num)
        self.participant.vars[str_balance1] = round(balance_num)


class End(Page):
    form_model = 'player'

    def is_displayed(self):
        return self.participant.vars['time_instruction'] >= 30 and (self.player.round_number == 15 or self.player.round_number == 30 )\
               and self.participant.vars['end'] == 0 and self.participant.vars['consent'] == 'yes' and \
               get_timeout_seconds(self.player) > 3

    def vars_for_template(self):
        round_num = self.player.round_number
        if self.player.round_number == 15:
            life = 1
        else:
            life = 2
        return {
            'round_num': round_num,
            'life': life
        }


page_sequence = [Start, Task, Decision1, Decision2, Rest1, Rest2, End]

from otree.api import Currency as c, currency_range
from ._builtin import Page, WaitPage
from .models import Constants
from sympy.solvers import solve
from sympy import Symbol
from .generic_pages import Page
from django.utils.translation import ugettext_lazy as _
from django.utils.text import format_lazy


class Start(Page):
    form_model = 'player'

    def is_displayed(self):
        return self.participant.vars['time_instruction'] >= 60 and self.round_number == 1 and \
               self.participant.vars['consent'] == 'yes'


class Task(Page):
    form_model = 'player'
    form_fields = ['task_finished']

    def is_displayed(self):
        return self.participant.vars['time_instruction'] >= 30 and self.round_number < 11 and \
               self.participant.vars['consent'] == 'yes'

    def error_message(self, values):
        if not values['task_finished']:
            round_num = self.round_number
            str_slide = 'slide_moveto_trial'+str(round_num)
            str1 = _('Your sliders are not all set to target number ')
            str2 = _('. Please, try again.')
            str_error = format_lazy('{}{}{}', str1, str(self.participant.vars[str_slide]), str2)
            return str_error

    def vars_for_template(self):
        round_num = self.round_number
        round_num_bar = 13+(self.round_number-1)*2
        str_slide = 'slide_moveto_trial'+str(round_num)
        slide_moveto = self.participant.vars[str_slide]
        return {
            'round_num': round_num,
            'round_num_bar': round_num_bar,
            'slide_moveto': slide_moveto
        }


class Decision(Page):
    form_model = 'player'
    form_fields = ['saving_mat', 'check_mat', 'reward_mat']

    def is_displayed(self):
        return self.participant.vars['time_instruction'] >= 30 and self.round_number < 11 and \
               self.participant.vars['consent'] == 'yes'

    def error_message(self, values):
        if not values['check_mat']:
            return _('Please decide how much you would like to save.')

    def vars_for_template(self):
        round_num = self.round_number
        round_num_show = self.round_number - 1
        round_num_bar = 13+(self.round_number-1)*2
        saving_list = []
        match_list = []
        reward_list = []
        balance_list = []
        for i in range(1, round_num+1):
            if i == 1 or i < round_num:
                str_saving = 'saving_mat'+str(i)
                str_match = 'match_mat'+str(i)
                str_reward = 'reward_mat'+str(i)
                str_balance = 'balance_mat'+str(i)
                saving_list.append(self.participant.vars[str_saving])
                match_list.append(self.participant.vars[str_match])
                reward_list.append(self.participant.vars[str_reward])
                balance_list.append(self.participant.vars[str_balance])
            else:
                break
        avg_list = round(sum(saving_list)/len(saving_list))
        for j in range(round_num, 11):
            saving_list.append('')
            match_list.append('')
        for k in range(round_num, 16):
            reward_list.append('')
            balance_list.append('')
        if round_num == 1:
            saving_list[0] = ''
            match_list[0] = ''
            reward_list[0] = ''
            balance_list[0] = ''
        if round_num == 1:
            bal_str = 'balance_mat1'
        else:
            bal_str = 'balance_mat' + str(round_num-1)
        balance10_simu_num = self.participant.vars[bal_str]*1.05**(11-round_num)
        for m in range(round_num, 11):
            balance10_simu_num += 1.6667*avg_list*1.05**(10-m)
        x = Symbol('x')
        rest_points_num = solve(((((balance10_simu_num*1.05-x)*1.05-x)*1.05-x)*1.05-x)*1.05-x)
        rest_points = round(0.6*rest_points_num[0])
        return {
            'round_num': round_num,
            'round_num_show': round_num_show,
            'round_num_bar': round_num_bar,
            'saving_list': saving_list,
            'match_list': match_list,
            'reward_list': reward_list,
            'balance_list': balance_list,
            'avg_list': avg_list,
            'rest_points': rest_points
        }

    def before_next_page(self):
        round_num = self.round_number
        str_saving = 'saving_mat'+str(round_num)
        str_match = 'match_mat'+str(round_num)
        str_reward = 'reward_mat'+str(round_num)
        str_balance = 'balance_mat'+str(round_num)
        str_saving1 = 'saving_mat'
        str_reward1 = 'reward_mat'
        self.participant.vars[str_saving] = getattr(self.player.in_round(round_num), str_saving1)
        self.participant.vars[str_match] = round(0.6667*getattr(self.player.in_round(round_num), str_saving1))
        self.participant.vars[str_reward] = getattr(self.player.in_round(round_num), str_reward1)
        balance = 0
        for r in range(1, round_num+1):
            save_str = 'saving_mat'+str(r)
            balance += 1.6667*self.participant.vars[save_str]*1.05**(round_num-r)
        self.participant.vars[str_balance] = round(balance)


class Rest(Page):
    form_model = 'player'
    form_fields = ['reward_mat']

    def is_displayed(self):
        return self.participant.vars['time_instruction'] >= 30 and self.round_number > 10 and \
               self.participant.vars['consent'] == 'yes'

    def vars_for_template(self):
        round_num = self.round_number
        round_num_bar = self.round_number+21
        saving_list = []
        match_list = []
        reward_list = []
        balance_list = []
        withdraw_list = []
        balance10 = self.participant.vars['balance_mat10']
        for i in range(1, 11):
            str_saving = 'saving_mat'+str(i)
            str_match = 'match_mat'+str(i)
            str_reward = 'reward_mat'+str(i)
            str_balance = 'balance_mat'+str(i)
            saving_list.append(self.participant.vars[str_saving])
            match_list.append(self.participant.vars[str_match])
            reward_list.append(self.participant.vars[str_reward])
            balance_list.append(self.participant.vars[str_balance])
            withdraw_list.append('')
        x = Symbol('x')
        rest_reward_num = solve(((((self.participant.vars['balance_mat10']*1.05-x)*1.05-x)*1.05-x)*1.05-x)*1.05-x)
        rest_reward_num = int(rest_reward_num[0])+1
        rest_reward = round(0.6*rest_reward_num)
        for k in range(11, round_num+1):
            reward_list.append(rest_reward)
            withdraw_list.append(rest_reward_num)
            str_balance = 'balance_mat'+str(k-1)
            balance_num = self.participant.vars[str_balance]*1.05-rest_reward_num
            if balance_num < 0:
                balance_num = 0
            balance_list.append(round(balance_num))
        return {
            'round_num': round_num,
            'round_num_bar': round_num_bar,
            'saving_list': saving_list,
            'match_list': match_list,
            'reward_list': reward_list,
            'balance_list': balance_list,
            'withdraw_list': withdraw_list,
            'balance10': balance10,
            'rest_reward': rest_reward,
            'rest_reward_num': rest_reward_num
        }

    def before_next_page(self):
        round_num = self.round_number
        x = Symbol('x')
        rest_reward_num = solve(((((self.participant.vars['balance_mat10']*1.05-x)*1.05-x)*1.05-x)*1.05-x)*1.05-x)
        rest_reward_num = int(rest_reward_num[0])+1
        rest_reward = round(0.6*rest_reward_num)
        str_reward = 'reward_mat'
        setattr(self.player.in_round(round_num), str_reward, rest_reward)
        str_balance = 'balance_mat'+str(round_num-1)
        balance_num = self.participant.vars[str_balance]*1.05-rest_reward_num
        str_balance1 = 'balance_mat'+str(round_num)
        self.participant.vars[str_balance1] = round(balance_num)


class End_trial(Page):
    form_model = 'player'

    def is_displayed(self):
        return self.participant.vars['time_instruction'] >= 30 and self.round_number == 15 and \
               self.participant.vars['consent'] == 'yes'


class End(Page):
    form_model = 'player'

    def is_displayed(self):
        return self.participant.vars['time_instruction'] >= 30 and self.player.round_number == 15 and \
               self.participant.vars['consent'] == 'yes'


page_sequence = [Start, Task, Decision, Rest, End_trial, End]

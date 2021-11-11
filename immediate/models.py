from otree.api import (
    models,
    widgets,
    BaseConstants,
    BaseSubsession,
    BaseGroup,
    BasePlayer,
    Currency as c,
    currency_range,
)
import random
from itertools import chain


author = 'Your name here'

doc = """
Your app description
"""


class Constants(BaseConstants):
    name_in_url = 'imme'
    players_per_group = None
    num_rounds = 30


class Subsession(BaseSubsession):
    def creating_session(self):
        for player in self.get_players():
            player.wage_gross_imme = 480
            player.tax_imme = 192
            player.wage_net_imme = 288
            player.participant.vars['saving_imme1'] = 0
            player.participant.vars['reward_imme1'] = 0
            player.participant.vars['balance_imme1'] = 0
            player.participant.vars['saving_imme16'] = 0
            player.participant.vars['reward_imme16'] = 0
            player.participant.vars['balance_imme16'] = 0
            slide_list = []
            for j in chain(range(1, 11), range(16, 26)):
                str_slide = 'slide_moveto%s' % j
                slide_num = random.choice(range(1, 31))
                while slide_num in slide_list:
                    slide_num = random.choice(range(1, 31))
                else:
                    player.participant.vars[str_slide] = slide_num
                    slide_list.append(slide_num)


class Group(BaseGroup):
    pass


class Player(BasePlayer):
    wage_gross_imme = models.IntegerField(blank=True)
    tax_imme = models.IntegerField(blank=True)
    wage_net_imme = models.IntegerField(blank=True)
    task_finished = models.StringField(blank=True)

    saving_imme1 = models.IntegerField(blank=True)
    check_imme1 = models.IntegerField(blank=True)
    reward_imme1 = models.IntegerField(blank=True)

    saving_imme2 = models.IntegerField(blank=True)
    check_imme2 = models.IntegerField(blank=True)
    reward_imme2 = models.IntegerField(blank=True)

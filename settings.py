#oTreeCodeReview
from os import environ


SESSION_CONFIGS = [
    {
        'name': 'Blaufus2020',
        'display_name': 'Blaufus2020',
        'num_demo_participants': 20,
        'app_sequence': ['instructions', 'trial_immediate', 'trial_deferred', 'trial_matching',
                         'quiz', 'immediate', 'deferred', 'matching', 'post_survey', 'result'],
        'language': 'de',
    },
]

# if you set a property in SESSION_CONFIG_DEFAULTS, it will be inherited by all configs
# in SESSION_CONFIGS, except those that explicitly override it.
# the session config can be accessed from methods in your apps as self.session.config,
# e.g. self.session.config['participation_fee']

SESSION_CONFIG_DEFAULTS = dict(
    real_world_currency_per_point=1.00, participation_fee=0.00, doc=""
)

# ISO-639 code
# for example: de, fr, ja, ko, zh-hans
LANGUAGE_CODE = 'de'
LANGUAGE_SESSION_KEY = '_language'

# e.g. EUR, GBP, CNY, JPY
REAL_WORLD_CURRENCY_CODE = 'USD'
USE_POINTS = True

ROOMS = [
    dict(
        name='econ101',
        display_name='Econ 101 class',
        participant_label_file='_rooms/econ101.txt',
    ),
    dict(name='game', display_name='Room for live demo (no participant labels)'),
    dict(name='game2', display_name='Room2 for live demo (no participant labels)'),
    dict(name='game3', display_name='Room3 for live demo (no participant labels)'),
]

ADMIN_USERNAME = 'admin'
# for security, best to set admin password in an environment variable
ADMIN_PASSWORD = environ.get('OTREE_ADMIN_PASSWORD')

DEMO_PAGE_INTRO_HTML = """
Here are some oTree games.
"""


SECRET_KEY = '&m8@*3(z7r2@a@gqe0z=u==u7=oj%fwfy)5r&fle2qe4955+mj'

INSTALLED_APPS = ['otree']
MIDDLEWARE_CLASSES = ['django.middleware.locale.LocaleMiddleware', ]

# embed settings
tourney_name = "December 2020 Smash Ult. Monthly"
footer_note = "Ping Brandon for help."
footer_icon = "https://vaughanesports.org/assets/Vaughan%20Esports%20Logo.png"
rulebook_url = "https://vaughanesports.org/rules"  # url to rulebook
newline = "_ _\n"  # dont touch me

# one of these should be on at least
cross_map_on_veto = True  # crosses out the stage when veto
hide_map_on_veto = True  # covers stage in spoiler tag when veto

# bot settings
prefix = "ve!"
description = "Tournament Bot for Vaughan Esports"

# smash stages
# abbreviations: https://www.ssbwiki.com/List_of_abbreviations#Stages
stages = [
    {'name': 'Battlefield',
     'starter': True,
     'aliases': [
         'bf'
     ]},
    {'name': 'Small Battlefield',
     'starter': True,
     'aliases': [
         'sbf',
         'small bf'
     ]},
    {'name': 'Pokemon Stadium 2',
     'starter': True,
     'aliases': [
         'ps2'
     ]},
    {'name': 'Town And City',
     'starter': True,
     'aliases': [
         'tan',
         'town',
         't&c',
         'city',
         'tac',
         'tnc',
         'tc'
     ]},
    {'name': 'Final Destination',
     'starter': True,
     'aliases': [
         'fd',
         'final d'
     ]},
    {'name': 'Kalos Pokemon League',
     'starter': False,
     'aliases': [
         'kalos',
         'kpl'
     ]},
    {'name': 'Lylat Cruise',
     'starter': False,
     'aliases': [
         'lylat',
         'lc'
     ]},
    {'name': 'Yoshi\'s Story',
     'starter': False,
     'aliases': [
         'ys',
         'yoshis',
         'yoshi\'s',
         'yoshi'
     ]},
    {'name': 'Smashville',
     'starter': False,
     'aliases': [
         'sv',
         'smashv',
         'ville'
     ]}
]

# valorant maps
maps = ["Bind", "Split", "Haven", "Ascent", "Icebox"]

# tourney categories
active_channels_id = 777421991031734292
inactive_channels_id = 777422048943013908
guild_id = 762532363695292455
TO_role_id = 822710142985830410

# channel where matches can be started
match_creation_channel_id = 828867315256000513

# timeout settings (in seconds)
veto_timeout = 1800

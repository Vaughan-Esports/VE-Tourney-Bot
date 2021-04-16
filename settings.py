# embed settings
tourney_name = "VE Anniversary Series: Spike Rush Event"
footer_note = "© Brandon Ly 2021"
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
val_maps = ["Bind", "Split", "Haven", "Ascent", "Icebox"]

# osu maps
beatmaps = [
    {'name': 'Journey',
     'map_id': 2784981,
     'category': 0,
     'alias': 'NM1'},
    {'name': 'Darling',
     'map_id': 493755,
     'category': 0,
     'alias': 'NM2'},
    {'name': 'Crescent Moon Island Boss Theme',
     'map_id': 653128,
     'category': 0,
     'alias': 'NM3'},
    {'name': 'Kaibutsu',
     'map_id': 2827550,
     'category': 0,
     'alias': 'NM4'},
    {'name': 'Starlight Wonder',
     'map_id': 2540412,
     'category': 0,
     'alias': 'NM5'},
    {'name': 'Into The Void',
     'map_id': 2399861,
     'category': 0,
     'alias': 'NM6'},
    {'name': 'ROXANNE',
     'map_id': 2433579,
     'category': 1,
     'alias': 'HD1'},
    {'name': 'Kimi to Nagameru Natsu no Hana',
     'map_id': 2494073,
     'category': 1,
     'alias': 'HD2'},
    {'name': 'Daisuke',
     'map_id': 1481150,
     'category': 2,
     'alias': 'HR1'},
    {'name': 'The Noise of Rain',
     'map_id': 1819801,
     'category': 2,
     'alias': 'HR2'},
    {'name': 'Kimiiro Signal',
     'map_id': 725164,
     'category': 3,
     'alias': 'DT1'},
    {'name': 'Sekaijuu no Dare yori mo',
     'map_id': 2801194,
     'category': 3,
     'alias': 'DT2'},
    {'name': 'Shut Up and osu! With Me (2020 ver.)',
     'map_id': 2289270,
     'category': 4,
     'alias': 'FM1'},
    {'name': 'Haikei, Sakura Maichiru Kono Hi ni',
     'map_id': 2239637,
     'category': 4,
     'alias': 'FM2'},
    {'name': 'Ai Kotoba III',
     'map_id': 2460008,
     'category': 4,
     'alias': 'FM3'},
    {'name': 'Arrival of Tears',
     'map_id': 796828,
     'category': 5,
     'alias': 'TB'},
]

# tourney categories
active_channels_id = 777421991031734292
inactive_channels_id = 777422048943013908
guild_id = 762532363695292455
TO_role_id = 822710142985830410

# channel where matches can be started
match_creation_channel_id = 828867315256000513
# message sent when match channel is created
init_match_message = "Once both sides are ready, invoke the veto process." \
                     "Instructions are over in <#828496712024064010>"

# timeout settings (in seconds)
veto_timeout = 1800

# example commands (discord formatting)
smash_example = '`ve!smash 3 @Brandon`'
valorant_example = '`ve!val 1 @Brandon`'

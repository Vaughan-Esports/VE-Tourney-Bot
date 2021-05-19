# embed settings
tourney_name = "VE May 2021 Monthly"
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

# tourney categories
active_channels_id = 777443551478153216
inactive_channels_id = 777443021654196264
guild_id = 688141732507942918
TO_role_id = 688519287035658358

# channel where matches can be started
match_creation_channel_id = 703347224985337897
# message sent when match channel is created
init_match_message = "Once both sides are ready, invoke the veto process. " \
                     "Instructions are over in <#828496712024064010>"

# league settings
aram_champ_pool_size = 20

# timeout settings (in seconds)
veto_timeout = 1800
lol_champselect_timeout = 60
lol_game_timeout = 5400

# example commands (discord formatting)
smash_example = '`ve!smash 3 @Brandon`'
valorant_example = '`ve!val 1 @Brandon`'
osu_example = '`ve!osu 5 @Brandon`'
aram_example = '`ve!aram 3 @Brandon`'

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
# can be found at https://link.vaughanesports.org/osumappool
beatmaps = [
    {'name': 'Marble Soda',
     'map_id': 846259,
     'category': 0,
     'alias': 'NM1'},
    {'name': 'Time and Again',
     'map_id': 1508977,
     'category': 0,
     'alias': 'NM2'},
    {'name': 'IT Is The End',
     'map_id': 2653460,
     'category': 0,
     'alias': 'NM3'},
    {'name': 'Mentai Cosmic',
     'map_id': 1050200,
     'category': 0,
     'alias': 'NM4'},
    {'name': 'Kuchizuke Diamond',
     'map_id': 2252634,
     'category': 0,
     'alias': 'NM5'},
    {'name': 'REANIMATE',
     'map_id': 487589,
     'category': 0,
     'alias': 'NM6'},
    {'name': 'Harmonia',
     'map_id': 2155867,
     'category': 1,
     'alias': 'HD1'},
    {'name': 'Gotoubun no Kimochi',
     'map_id': 2026988,
     'category': 1,
     'alias': 'HD2'},
    {'name': 'Poker Face',
     'map_id': 2296303,
     'category': 2,
     'alias': 'HR1'},
    {'name': 'Blue Zenith',
     'map_id': 677872,
     'category': 2,
     'alias': 'HR2'},
    {'name': 'DREAM SOLISTER',
     'map_id': 895377,
     'category': 3,
     'alias': 'DT1'},
    {'name': 'Catch the Rainbow!',
     'map_id': 2656834,
     'category': 3,
     'alias': 'DT2'},
    {'name': 'Fake',
     'map_id': 2637340,
     'category': 4,
     'alias': 'FM1'},
    {'name': 'me & u',
     'map_id': 1491793,
     'category': 4,
     'alias': 'FM2'},
    {'name': 'Liquid Future',
     'map_id': 1877452,
     'category': 4,
     'alias': 'FM3'},
    {'name': 'Asymmetry',
     'map_id': 698252,
     'category': 5,
     'alias': 'TB1'},
]

# league champs
lol_champs = ["Aatrox", "Ahri", "Akali", "Alistar", "Amumu", "Anivia", "Annie",
              "Aphelios", "Ashe", "Aurelion Sol", "Azir", "Bard", "Blitzcrank",
              "Brand", "Braum", "Caitlyn", "Camille", "Cassiopeia", "Cho'gath",
              "Corki", "Darius", "Diana", "Dr. Mundo", "Draven", "Ekko",
              "Elise", "Evelynn", "Ezreal", "Fiddlesticks", "Fiora", "Fizz",
              "Galio", "Gangplank", "Garen", "Gnar", "Gragas", "Graves",
              "Gwen", "Hecarim", "Heimerdinger", "Illaoi", "Irelia", "Ivern",
              "Janna", "Jarvan IV", "Jax", "Jayce", "Jhin", "Jinx", "Kai'sa",
              "Kalista", "Karma", "Karthus", "Kassadin", "Katarina", "Kayle",
              "Kayn", "Kennen", "Kha'zix", "Kindred", "Kled", "Kog'maw",
              "Leblanc", "Lee sin", "Leona", "Lillia", "Lissandra", "Lucian",
              "Lulu", "Lux", "Malphite", "Malzahar", "Maokai", "Master Yi",
              "Miss Fortune", "Mordekaiser", "Morgana", "Nami", "Nasus",
              "Nautilus", "Neeko", "Nidalee", "Nocturne", "Nunu & Willump",
              "Olaf", "Orianna", "Ornn", "Pantheon", "Poppy", "Pyke", "Qiyana",
              "Quinn", "Rakan", "Rammus", "Rek'sai", "Rell", "Renekton",
              "Rengar", "Riven", "Rumble", "Ryze", "Samira", "Sejuani",
              "Senna", "Seraphine", "Sett", "Shaco", "Shen", "Shyvana",
              "Singed", "Sion", "Sivir", "Skarner", "Sona", "Soraka", "Swain",
              "Sylas", "Syndra", "Tahm Kench", "Taliyah", "Talon", "Taric",
              "Teemo", "Thresh", "Tristana", "Trundle", "Tryndamere",
              "Twisted Fate", "Twitch", "Udyr", "Urgot", "Varus", "Vayne",
              "Veigar", "Vel'koz", "Vi", "Viego", "Viktor", "Vladimir",
              "Volibear", "Warwick", "Wukong", "Xayah", "Xerath", "Xin zhao",
              "Yasuo", "Yone", "Yorick", "Yuumi", "Zac", "Zed", "Ziggs",
              "Zilean", "Zoe", "Zyra"]

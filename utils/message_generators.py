import discord

from settings import *


def map_list_message(map_list: list, removed_maps: list, selected_map: str):
    """
    Base map list message generator
    :param map_list: string list of map names
    :param removed_maps: string list of removed maps
    :param selected_map: string name of the selected map
    :return: output message for embed
    """
    # blank string
    message = ""
    # loop through starter stages
    for x in range(len(map_list)):
        # if removed maps is none then don't worry about striking out
        if removed_maps is not None:
            # bolds the map if its selected
            if map_list[x] == selected_map:
                message = f"{message}⮕**{map_list[x]}**\n"
            # crosses map out if its in the removed_maps list
            elif map_list[x] in removed_maps:
                message = f"{message}~~{map_list[x]}~~\n"
            # else concatenate the new map name regularly
            else:
                message = f"{message}{map_list[x]}\n"
        # concatenate the new map name regularly
        else:
            message = f"{message}{map_list[x]}\n"
    return message


def starters_message(removed_stages=None, selected_stage=None):
    """
    Generates the smash starter stages list
    :param selected_stage: string name of the stage that is selected
    :param removed_stages: list of veto'd stages (exact spellings)
    :return: string for embed value
    """
    return map_list_message(starters, removed_stages, selected_stage)


def counters_message(removed_stages=None, selected_stage=None):
    """
    Generates the smash counterpick stages list
    :param selected_stage: string name of the stage that is selected
    :param removed_stages: list of veto'd stages (exact spellings)
    :return: string for embed value
    """
    return map_list_message(counters, removed_stages, selected_stage)


def valorant_maps_message(removed_maps=None, selected_map=None):
    """
    Generates the VALORANT map list
    :param removed_maps:
    :param selected_map:
    :return: string embed value
    """
    return map_list_message(maps, removed_maps, selected_map)


def valorant_sides_message(p1: discord.User, p2: discord.User,
                           attack: bool):
    """
    Generates starting side message for VALORANT Veto
    :param p1 player 1 user
    :param p2 player 2 user
    :param attack boolean for if player1 chose attack
    :return: string embed value
    """
    if attack:
        return f"**Attack:** {p1.mention} \n**Defense:** {p2.mention}"
    else:
        return f"**Attack:** {p2.mention} \n**Defense:** {p1.mention}"

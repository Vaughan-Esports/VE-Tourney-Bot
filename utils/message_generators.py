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
            # crosses map out if its in the removed_maps list
            if map_list[x] in removed_maps:
                message = f"{message}~~{map_list[x]}~~\n"
            # bolds the map if its selected
            elif map_list[x] == selected_map:
                message = f"{message}⮕**{map_list[x]}**\n"
            # else concatenate the new map name regularly
            else:
                message = f"{message}{map_list[x]}\n"
        # concatenate the new map name regularly
        else:
            message = f"{message}{map_list[x]}\n"
    return message


def starter_stages_message(removed_stages=None, selected_stage=None):
    """
    Generates the smash starter stages list
    :param selected_stage: string name of the stage that is selected
    :param removed_stages: list of veto'd stages (exact spellings)
    :return: string for embed value
    """
    return map_list_message(starter_stages, removed_stages, selected_stage)


def counterpick_stages_message(removed_stages=None, selected_stage=None):
    """
    Generates the smash counterpick stages list
    :param selected_stage: string name of the stage that is selected
    :param removed_stages: list of veto'd stages (exact spellings)
    :return: string for embed value
    """
    return map_list_message(counterpick_stages, removed_stages, selected_stage)

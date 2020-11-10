from settings import *


def starter_stages_message(removed_stages=None, selected_stage=None):
    """
    Generates starter stages list
    :param selected_stage: string name of the stage that is selected
    :param removed_stages: list of veto'd stages (exact spellings)
    :return: string for embed value
    """
    # blank string
    message = ""
    # loop through starter stages
    for x in range(len(starter_stages)):
        # if removed stages is none then don't worry about striking out
        if removed_stages is not None:
            # crosses stage out if its in the removed_stages list
            if starter_stages[x] in removed_stages:
                message = f"{message}~~{starter_stages[x]}~~\n"
            # bolds the stage if its selected
            elif starter_stages[x] == selected_stage:
                message = f"{message}⮕**{starter_stages[x]}**\n"
            # else concatenate the new stage name regularly
            else:
                message = f"{message}{starter_stages[x]}\n"
        # else concatenate the new stage name regularly
        else:
            message = f"{message}{starter_stages[x]}\n"
    return message


def counterpick_stages_message(removed_stages=None, selected_stage=None):
    """
    Generates counterpick stages list
    :param selected_stage: string name of the stage that is selected
    :param removed_stages: list of veto'd stages (exact spellings)
    :return: string for embed value
    """
    # blank string
    message = ""
    # loop through counterpick stages
    for x in range(len(counterpick_stages)):
        # if removed stages is none then don't worry about striking out
        if removed_stages is not None:
            # crosses stage out if its in the removed_stages list
            if counterpick_stages[x] in removed_stages:
                message = f"{message}~~{counterpick_stages[x]}~~\n"
            # bolds the stage if its selected
            elif counterpick_stages[x] == selected_stage:
                message = f"{message}⮕**{counterpick_stages[x]}**\n"
            # else concatenate the new stage name regularly
            else:
                message = f"{message}{counterpick_stages[x]}\n"
        # else concatenate the new stage name regularly
        else:
            message = f"{message}{counterpick_stages[x]}\n"
    return message
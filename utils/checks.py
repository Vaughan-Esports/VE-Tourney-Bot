def doneCheck(ctx):
    def func(message):
        return message.content.lower == 'done' \
               and message.channel == ctx.channel


def playerCheck(ctx):
    def func(message):
        """Checks if a player said 'me' """
        return message.content.lower() == 'me' \
               and message.channel == ctx.channel

    return func


def stageCheck(ctx, match):
    """
    Check if the stage name is valid
    :param ctx: discord context to check for channel
    :param match: match to check stagelist and game from
    :return:
    """

    def func(message):
        return message.content in match.games[match.current_game].stagelist \
               and message.channel == ctx.channel

    return func


def mapCheck(ctx, match):
    """
    Check if the stage name is valid
    :param ctx: discord context to check for channel
    :param match: match to check stagelist and game from
    :return:
    """

    def func(message):
        return message.content in match.games[match.current_game].map_pool \
               and message.channel == ctx.channel

    return func


def sideCheck(ctx):
    """
    Check if valid valorant side
    :param ctx: discord context to check for channel
    :return:
    """

    def func(message):
        return ('att' in message.content.lower()
                or 'def' in message.content.lower()) and \
               message.channel == ctx.channel

    return func


def beatmapCheck(ctx, match):
    """
    Checks if a valid osu beatmap
    :param ctx: discord context to check for channel
    :param match: match to check map pool from
    :return:
    """

    def func(message):
        return message.content in match.games[match.current_game].map_pool \
               and message.channel == ctx.channel

    return func

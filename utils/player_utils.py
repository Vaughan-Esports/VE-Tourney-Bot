import discord


async def swap_players(player1: object, player2: object, player1_dsr: list, player2_dsr: list):
    """
    Swap players for smash veto with tracking for DSR'd stages
    :param player1: player 1
    :param player2: player 2
    :param player1_dsr: player 1's DSR stage(s)
    :param player2_dsr: player 2's DSR stage(s)
    :return: new player1 and player2
    """
    # swap player objects
    p1 = player2
    p2 = player1

    # swap player DSR's
    p1_dsr = player2_dsr
    p2_dsr = player1_dsr

    # return new player 1 and player 2
    return p1, p2, p1_dsr, p2_dsr

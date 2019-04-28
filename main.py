import asyncio
from fpl_session import FplSession
<<<<<<< HEAD
import jsonpickle
from models.player import Player

players = []

async def main():
<<<<<<< HEAD
    fpl_session = FplSession("mike.pratt@trelleborg.com", "KingOfTheBanana95")
=======
import json
from models.standings import Standings
from models.player import Player


async def main():
    fpl_session = FplSession("", "")
    # fpl = FPL(session)
    # player = await fpl_session.fpl.get_player(302)
    # print(player)
    # await get_my_team(fpl_session, 1025428)
>>>>>>> parent of fdb4502... Working on getting gameweek history for each player in a league.
=======
    fpl_session = FplSession("", "")
>>>>>>> parent of ef888c9... Renamed Player to User.
    await get_classic_league(fpl_session, 152458)
    await fpl_session.close()


async def get_my_team(fpl_session, id):
    async with fpl_session.session:
        await fpl_session.login()
        user = await fpl_session.fpl.get_user(id)
        team = await user.get_team()
    print(team)


async def get_classic_league(fpl_session, league_id):
    async with fpl_session.session:
        league = await fpl_session.fpl.get_classic_league(league_id)
        standings = await league.get_standings(1)
<<<<<<< HEAD
        for standing_entry in standings['results']:
            player = Player(standing_entry['id'], standing_entry['entry'], standing_entry['entry_name'], standing_entry['player_name'], standing_entry['rank'], standing_entry['total'])
            players.append(player)
    for player in players:
        print(jsonpickle.encode(player))
        await get_player_gameweek_history(fpl_session, player.player_id)


async def get_player_gameweek_history(fpl_session, user_id):
    async with fpl_session.session:
        user = await fpl_session.fpl.get_user(user_id)
<<<<<<< HEAD
        # print(jsonpickle.encode(user))
        history = await user.get_gameweek_history()
        print('---------------')
        print(history)
        user_gameweek_histories.append(history)
    print(user_gameweek_histories)

=======
        for player in standings['results']:
            print(player)
    # print(standings)
>>>>>>> parent of fdb4502... Working on getting gameweek history for each player in a league.
=======
        gameweek_history = await user.get_gameweek_history()
    print(gameweek_history)
>>>>>>> parent of ef888c9... Renamed Player to User.

asyncio.run(main())

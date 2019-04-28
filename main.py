import asyncio
from fpl_session import FplSession
import jsonpickle
from models.player import Player

players = []

async def main():
    fpl_session = FplSession("", "")
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
        for standing_entry in standings['results']:
            player = Player(standing_entry['id'], standing_entry['entry'], standing_entry['entry_name'], standing_entry['player_name'], standing_entry['rank'], standing_entry['total'])
            players.append(player)
    for player in players:
        print(jsonpickle.encode(player))
        await get_player_gameweek_history(fpl_session, player.player_id)


async def get_player_gameweek_history(fpl_session, user_id):
    async with fpl_session.session:
        user = await fpl_session.fpl.get_user(user_id)
        gameweek_history = await user.get_gameweek_history()
    print(gameweek_history)

asyncio.run(main())

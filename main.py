import asyncio
from fpl_session import FplSession
import json
from models.standings import Standings
from models.player import Player


async def main():
    fpl_session = FplSession("", "")
    # fpl = FPL(session)
    # player = await fpl_session.fpl.get_player(302)
    # print(player)
    # await get_my_team(fpl_session, 1025428)
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
        for player in standings['results']:
            print(player)
    # print(standings)

asyncio.run(main())

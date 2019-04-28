import asyncio
import aiohttp
from fpl_session import FplSession
from fpl import FPL


async def main():
    fpl_session = FplSession("mike.pratt@trelleborg.com", "BananaKing95")
    # fpl = FPL(session)
    player = await fpl_session.fpl.get_player(302)
    print(player)
    await get_my_team(fpl_session, 1025428)
    await fpl_session.close()


async def get_my_team(fpl_session, id):
    async with fpl_session.session:
        await fpl_session.login()
        user = await fpl_session.fpl.get_user(id)
        team = await user.get_team()
    print(team)

asyncio.run(main())

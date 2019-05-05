import asyncio
from fpl_session import FplSession
from models.User import User
import secrets
import jsonpickle

users = []
user_gameweek_histories = []


async def main():
    fpl_session = FplSession(secrets.email, secrets.password)
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
            user = User(standing_entry['entry'], standing_entry['entry_name'], standing_entry['player_name'])
            users.append(user)
        # await get_user_gameweek_history(fpl_session, users[0].id)
        for user in users:
        #     print(jsonpickle.encode(user))
            await get_user_gameweek_history(fpl_session, user.id)


async def get_user_gameweek_history(fpl_session, user_id):
    async with fpl_session.session:
        await fpl_session.login()
        # TODO: Replace user_id with user, standing_entry needs to be converted to a User object.
        user = await fpl_session.fpl.get_user(user_id)
        # print(jsonpickle.encode(user))
        history = await user.get_gameweek_history()
        print('---------------')
        print(history)
        user_gameweek_histories.append(history)
    print(user_gameweek_histories)


asyncio.run(main())

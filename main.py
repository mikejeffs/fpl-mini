import asyncio
from fpl_session import FplSession
from models.User import User
from models.gameweek import Gameweek
import secrets
import jsonpickle

users = []


async def main():
    fpl_session = FplSession(secrets.email, secrets.password)
    await get_classic_league(fpl_session, 152458)
    await fpl_session.close()
    # print(jsonpickle.encode(user_gameweek_histories))
    # file = open("gameweeks.txt", "w")
    # file.write(jsonpickle.encode(user_gameweek_histories))
    # file.close
    print('closed')


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
            user = User(standing_entry['entry'], standing_entry['entry_name'], standing_entry['player_name'], [])
            users.append(user)

        for user in users:
            print(jsonpickle.encode(user))
            users_gameweeks = await get_user_gameweek_history(fpl_session, user.id)
            # key_pair = {'user': user, 'gameweeks': users_gameweeks}
            user.set_game_weeks(users_gameweeks)
            print(user.get_game_weeks())


async def get_user_gameweek_history(fpl_session, user_id):
    user = await fpl_session.fpl.get_user(user_id)
    history = await user.get_gameweek_history()
    gameweeks = []
    for gameweek in history:
        user_gameweek = Gameweek(gameweek['event'], user_id, gameweek['points'], gameweek['total_points'], 0)
        gameweeks.append(user_gameweek)
    return gameweeks


asyncio.run(main())

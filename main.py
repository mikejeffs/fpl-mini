import asyncio
from fpl_session import FplSession
from models.User import User
from models.gameweek import Gameweek
import secrets
import jsonpickle
import json

users = []

gameweeks = []

async def main():
    fpl_session = FplSession(secrets.email, secrets.password)
    await get_classic_league(fpl_session, 152458)
    await fpl_session.close()
    i = 1
    while i != 38:
        create_gameweek_table(i)
        i += 1

    json_data = json.dumps(gameweeks)
    file = open("gameweeks.json", "w")
    file.write(json_data)
    file.close
    print('closed')


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
            user.set_game_weeks(users_gameweeks)


async def get_user_gameweek_history(fpl_session, user_id):
    user = await fpl_session.fpl.get_user(user_id)
    history = await user.get_gameweek_history()
    gameweeks = []
    for gameweek in history:
        user_gameweek = Gameweek(gameweek['event'], user_id, gameweek['points'], gameweek['total_points'], 0)
        gameweeks.append(user_gameweek)
    return gameweeks


def create_gameweek_table(gameweek_number):
    gameweek_table = {'gameweek': 0, 'gameweek_data': []}
    for user in users:
        user_gameweek = None
        for gameweek in user.get_game_weeks():
            if gameweek.week == gameweek_number:
                user_gameweek = Gameweek(gameweek.week, gameweek.user_id, gameweek.gameweek_points, gameweek.total_points, gameweek.rank)

        if user_gameweek == None: # user may not have participated in this game week
            continue
        gameweek_user_entry = {'rank': user_gameweek.rank, 'user': user.user_name, 'team_name': user.team_name, 'gameweek_points': user_gameweek.gameweek_points, 'total_points': user_gameweek.total_points}
        gameweek_table['gameweek_data'].append(gameweek_user_entry)

    gameweek_table['gameweek_data'].sort(key=lambda g: g['total_points'], reverse=True) # Sort in order of highest total points.

    for entry in gameweek_table['gameweek_data']:
        entry['rank'] = gameweek_table['gameweek_data'].index(entry) + 1 # update ranking of each entry in the gameweek

    gameweek_table['gameweek'] = gameweek_number
    print(gameweek_table)
    gameweeks.append(gameweek_table)


asyncio.run(main())

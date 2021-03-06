#!/usr/bin/env python3

import argparse

from tornado.ncss import Server

from handlers.index import index_handler
from handlers.profile import profile_handler
from handlers.game import game_handler, get_question_handler, submit_question_handler
from handlers.pre_game import pre_game_handler
from handlers.post_game import post_game_handler
from handlers.login import login_handler, login_handler_post, signup_handler_post
from handlers.user import user_handler
from handlers.error import error_handler
from handlers.leaderboard import leaderboard_handler
from handlers.category import category_handler, category_list_handler
from handlers.question import new_question_handler, new_question_form, edit_question_handler
from handlers.logout import logout_handler


def new_server(port=8888, hostname='', debug=True):
    server = Server(port=port, hostname=hostname, debug=debug)

    server.register('/', index_handler)
    server.register('/profile', profile_handler)
    server.register(r'/game/([0-9]+)', get_question_handler)
    server.register(r'/game/submit/([0-9]+)', submit_question_handler)
    server.register('/game/create', game_handler)
    server.register('/pre_game', pre_game_handler)
    server.register('/post_game', post_game_handler)
    server.register('/leaderboard', leaderboard_handler)
    server.register('/login', login_handler, post=login_handler_post)
    server.register(r'/(?:question|submit)', new_question_form, post=new_question_handler)
    server.register(r'/question/([0-9]+)', get_question_handler, post=edit_question_handler)
    server.register(r'/category/([0-9]+)', category_handler)
    server.register('/user', user_handler, post=signup_handler_post)
    server.register('/categories', category_list_handler)
    server.register('/logout', logout_handler)
    server.register(r'/.*', error_handler)

    return server


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='The Quizzi server, a social trivia website.')
    parser.add_argument('-p', '--port', type=int, default=8888, help='port to listen on')
    parser.add_argument('-H', '--hostname', default='', help='hostname to bind to')
    parser.add_argument('--prod', action='store_true', default=False, help='turn debug mode off')
    args = parser.parse_args()

    server = new_server(port=args.port, hostname=args.hostname, debug=not args.prod)
    server.run()
else:
    server = new_server(debug=False)

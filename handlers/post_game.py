from templating import render_template
from db.models import User, Game, Question, Answer
from .error import error_handler
from . import template_paths


def post_game_handler(request):
    game_id = request.get_secure_cookie('game_id')
    if game_id is None:
        error_handler(request)
        return
    game_id = int(game_id.decode())

    u_id = request.get_secure_cookie('user_id')
    u_name = ""

    game = Game.find(game_id=game_id)
    score = game.score
    if u_id is not None:
        u_id = u_id.decode("UTF-8")
        u_name = User.find(user_id=u_id)
        u_name = u_name.username.lower().capitalize()

    template_values = {}
    template_values['user_name'] = u_name
    template_values['score'] = score
    template_values['questions'] = game.get_questions()
    template_values['question_results'] = game.get_question_results()
    post_game_page = render_template(template_paths["post_game"], template_values)
    request.write(post_game_page)

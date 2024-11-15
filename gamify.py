# ESC180 at the University of Toronto (Introduction to Computer Programming Fall 2024, taught by Michael Guerzhoy)
# Project 1: https://www.cs.toronto.edu/~guerzhoy/180/proj/gamify/gamify.pdf
# Code by Jessica Yi, passed 337.0 / 346.0 test cases

hedons = 0
health = 0
duration_count = 0
rest_count = 0
run_count = 0
book_count = 0

tired = False
interest = True
last_activity= None

star_activity = None
star_active = False
star_used = False
star_history = []

def initialize():
    global hedons, health, duration_count, rest_count, run_count, book_count, star_history
    global tired, interest, last_activity
    global star_activity, star_active, star_used

    hedons = 0
    health = 0
    duration_count = 0
    rest_count = 0
    run_count = 0
    book_count = 0

    tired = False
    interest = True
    last_activity = None

    star_activity = None
    star_active = False
    star_used = False
    star_history = []

def get_cur_hedons():
    global hedons
    return hedons

def get_cur_health():
    global health
    return health

def most_fun_activity_minute():
    global tired, star_active, last_activity
    if last_activity == 'running'or last_activity == 'textbooks':
            tired = True
    if tired:
        if star_can_be_taken('running'):
            return 'running'
        elif star_can_be_taken('textbooks'):
            return 'textbooks'
        else:
            return 'resting'
    elif not tired:
        if star_can_be_taken('running'):
            return 'running'
        elif star_can_be_taken('textbooks'):
            return 'textbooks'
        else:
            return 'running'

def star_can_be_taken(activity):
    global interest, star_active, star_used, star_activity, star_history, duration_count
    if star_active and not star_used and interest and star_activity == activity and star_history[-1] == duration_count:
        return True
    else:
        return False

def offer_star(activity):
    global star_active, star_used, duration_count, interest, star_activity, star_history
    star_history.append(duration_count)
    if len(star_history) >= 3:
        if star_history[-1] - star_history[-3] < 120:
            interest = False
        elif len(star_history) <3:
            interest = True
    if interest is not False:
        if activity in ['running', 'textbooks']:
            star_active = True
            star_used = False
            star_activity = activity

def perform_activity(activity, duration):
    global health, hedons, last_activity, duration_count, tired, star_active, star_used, star_activity, rest_count, run_count, book_count

    if last_activity == 'running' or last_activity == 'textbooks':
        tired = True

    if activity == 'resting':
        run_count = 0
        book_count = 0
        rest_count += duration

        if star_can_be_taken('resting'):
            star_hedons = min(10, duration) * 3
            hedons = hedons + star_hedons
            star_active = False
            star_used = True
        if duration_count != 0 and last_activity != 'resting' and rest_count < 120:
            tired = True
        elif rest_count >= 120:
            tired = False
            rest_count = 0
        else:
            tired = False

        last_activity = activity
        duration_count += duration

    elif activity == 'running':
        last_activity = activity
        run_count += duration
        book_count = 0
        rest_count = 0

        if star_can_be_taken('running'):
            star_hedons = min(10, duration) * 3
            hedons += star_hedons
            star_active = False
            star_used = True
        duration_count += duration

        if run_count - duration < 180:
            if run_count <= 180:
                health += 3 * duration
            else:
                before_180 = 180 - (run_count - duration)
                after_180 = duration - before_180
                health += 3 * before_180 + after_180
        else:
            health += duration

        if not tired:
            if duration <= 10:
                hedons += 2*duration
            else:
                hedons += 20 - 2*(duration - 10)
        elif tired:
            hedons -= 2*duration

    elif activity == 'textbooks':
        last_activity = activity
        health += duration * 2
        book_count += duration
        rest_count = 0
        run_count = 0

        if star_can_be_taken("textbooks"):
            star_hedons = min(10, duration) * 3
            hedons = hedons + star_hedons
            star_active = False
            star_used = True
        duration_count += duration
        if not tired:
            if book_count <= 20:
                hedons += duration
            else:
                hedons += 20 - (duration-20)
        elif tired:
            hedons -= 2*duration
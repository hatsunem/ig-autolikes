import funcs
import datetime
from apscheduler.schedulers.blocking import BlockingScheduler


JST = 9
ACTION_INTERVAL = 10
ACTION_HOUR = [7, 8, 9, 11, 12, 13, 19, 20, 21, 22]


def do_likes():
    time = datetime.datetime.now() + datetime.timedelta(hours=JST)
    hour = time.hour

    if hour not in ACTION_HOUR:
        print("{0}: 時間外です。".format(time.strftime('%X')))
    else:
        funcs.open_article()
        users = funcs.get_users()
        likes = funcs.likes_users(users)
        print("{0}: {1}likes♡ succeed!".format(time.strftime('%X'), likes))


if __name__ == '__main__':
    funcs.login()
    do_likes()

    sc = BlockingScheduler(standalone=True, coalesce=True)
    sc.add_job(do_likes, 'interval', minutes=ACTION_INTERVAL)
    sc.start()

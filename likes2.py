import funcs
import datetime
from apscheduler.schedulers.blocking import BlockingScheduler


def likes2():
    time = datetime.datetime.now() + datetime.timedelta(hours=9)
    hour = time.hour
    if hour not in [7, 8, 9, 11, 12, 13, 19, 20, 21, 22]:
        print("{0}: 時間外です。".format(time.strftime('%X')))
        return

    funcs.open_article()
    users = funcs.get_users()
    likes = funcs.likes_users(users)
    print("{0}: {1}likes♡ succeed!".format(time.strftime('%X'), likes))


funcs.login()
likes2()

sc = BlockingScheduler(standalone=True, coalesce=True)
sc.add_job(likes2, 'interval', minutes=10)
sc.start()
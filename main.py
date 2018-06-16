from funcs import InstaOperator
import datetime
from apscheduler.schedulers.blocking import BlockingScheduler


USERNAME = ""
PASSWORD = ""
TAG = ""

TIMEZONE = 9
ACTION_INTERVAL = 10
ACTION_HOUR = [7, 8, 9, 11, 12, 13, 19, 20, 21, 22]


def action():
    time = datetime.datetime.now() + datetime.timedelta(hours=TIMEZONE)
    hour = time.hour

    if hour not in ACTION_HOUR:
        print("{0}: out of hours".format(time.strftime('%X')))
    else:
        operator.open_article()
        users = operator.get_users()
        likes = operator.likes_users(users)
        print("{0}: {1}likes♡".format(time.strftime('%X'), likes))


if __name__ == '__main__':
    operator = InstaOperator(USERNAME, PASSWORD, TAG)
    operator.login()
    action()

    sc = BlockingScheduler(standalone=True, coalesce=True)
    sc.add_job(action, 'interval', minutes=ACTION_INTERVAL)
    sc.start()

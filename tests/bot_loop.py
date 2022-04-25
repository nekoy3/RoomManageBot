#https://stackoverflow.com/questions/71331027/correct-way-to-implement-multi-timed-tasks-in-python

async def daily_task():  # function that will loop, note: no decorator
    ...


def before_daily_task(hour=0, minute=0, second=0):  # not asynchronous!
    async def wrapper():  # asynchronous!
        # here the code that's in your `before_daily_task`
        # use `hour`, `minute` and `second` to calculate how much to sleep
    return wrapper  # not calling


def task_generator(hour=0, minute=0, second=0):  # I guess you can take a guild ID or a channel ID too
    task = tasks.loop(hours=24)(daily_task)
    task.before_loop(before_daily_task(19, 5, 00))
    task.start()  # pass the guild/channel ID here
    return task


# start the task at a specified time
task_generator(24, 0, 0)
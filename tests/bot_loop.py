import asyncio
import datetime

async def loop():
    while True:
        now = datetime.now().strftime('%H:%M')
        if now == '11:58':
            print("時間だよ")
        await asyncio.sleep(60)

task = asyncio.get_event_loop().create_task(loop())
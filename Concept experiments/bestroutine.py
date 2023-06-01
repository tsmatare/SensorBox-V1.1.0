import asyncio

async def print_zero():
    while True:
        await asyncio.sleep(1)
        print(0)

async def print_one():
    while True:
        await asyncio.sleep(5)
        print(1)

async def main():
    await asyncio.gather(print_zero(), print_one())

asyncio.run(main())
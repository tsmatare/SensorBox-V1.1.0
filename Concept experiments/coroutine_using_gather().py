import asyncio

async def zel():
    while True:
        await asyncio.sleep(1)
        print(0)
        

async def uno():
    while True:
        await asyncio.sleep(5)
        print(1)
        

async def main():
    tas = (uno(),zel())
    await asyncio.gather(*tas)
    
asyncio.run(main())

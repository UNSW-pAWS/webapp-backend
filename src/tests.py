import asyncio
import pytest

# All test coroutines will be treated as marked.
pytestmark = pytest.mark.asyncio

async def test_example(event_loop):
    """No marker!"""
    await asyncio.sleep(0, loop=event_loop)


#this has the same functionality as below, but uses "pip install pytest-asyncio"
@pytest.mark.asyncio
async def test_example(event_loop):
    do_stuff()    
    await asyncio.sleep(0.1, loop=event_loop)


def test_example():
    loop = asyncio.new_event_loop()
    try:
        do_stuff()
        asyncio.set_event_loop(loop)
        loop.run_until_complete(asyncio.sleep(0.1, loop=loop))
    finally:
        loop.close()
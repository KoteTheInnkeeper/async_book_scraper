# This is just a demonstration, not part of the project, but I rather have it here, since it's an interesting reminder on why
# async dev is so powerful.

import aiohttp
import asyncio # for managing the coroutines
import time

# A co-routine. This was the original 'fetch_page' function, but it wasn't really efficient because of the session creation process.
async def unused(url: str):
    page_start = time.time()
    # Create a bunch of client sessions and work asynchronously with them. We're creating a bunch of them each time we want to
    # fetch a page and using only one of them :S.
    # The ideal thing to do would be to create only one session and use it for fetching every page.
    async with aiohttp.ClientSession() as session:
        # The essential difference between regular context managers and the 'async' ones is that this last ones have 'yield'
        # statements in the 'exit' or 'enter' methods which means they have more places where to 'suspend' the execution.
        async with session.get(url) as response: # ask the server for content
            print(f"Page took {time.time() - page_start}")
            return response.status


async def fetch_page(session: aiohttp.ClientSession, url: str):
    page_start = time.time()
    async with session.get(url) as response:
        print(f"Page took {time.time() - page_start} seconds to fetch.")
        return response.status


async def get_multiple_pages(loop, *urls):
    tasks = []
    async with aiohttp.ClientSession(loop=loop) as session: # loop -> for using the one we passed in, instead of creating a new one.
        for url in urls:
            tasks.append(fetch_page(session, url))    # Inserts the 'co-routines' into our 'task' list.
        grouped_tasks = asyncio.gather(*tasks)   # Gather all the tasks inside one big task.
        return await grouped_tasks   # Is going to 'suspend' the function, wait for something to happen in 'grouped_tasks' and then resume.
        # This will repeat until the 'asyncio.gather(*tasks)' statement 'returns', which will only happen when there are no tasks to do. 

        

# Now we need something to do the work of the 'send()' and 'next()' calls.

start = time.time()

loop = asyncio.get_event_loop()
urls = ['http://google.com' for i in range(50)]
loop.run_until_complete(get_multiple_pages(loop, *urls))

print(f"All took {time.time() - start} seconds")

# The 'fecthpage...' thing in here is just creating the co-routine in the background. It's to this coroutine that your 'send'
# and 'next' calls are going to be applied.




import asyncio
from asyncio import TaskGroup

class TerminateTaskGroup(Exception):
    """Exception raised to terminate a task group."""

async def force_terminate_task_group():
    """Used to force termination of a task group."""
    raise TerminateTaskGroup()

async def job(task_id, sleep_time):
    while True:
        print(f'Task {task_id} tick')
        await asyncio.sleep(sleep_time)

async def main():
    try:
        async with TaskGroup() as group:
            # spawn some tasks
            group.create_task(job(1, 0.5))
            group.create_task(job(2, 1))
            group.create_task(job(3, 0.8))
            group.create_task(job(4, 0.3))
            group.create_task(job(5, 4.4))
            group.create_task(job(6, 2.5))

            await asyncio.sleep(4)

            group.create_task(force_terminate_task_group())
    except* TerminateTaskGroup:
        pass

asyncio.run(main())
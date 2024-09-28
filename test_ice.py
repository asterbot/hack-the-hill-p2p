import asyncio
import aioice


async def connect_using_ice():
    conn_a = aioice.Connection(ice_controlling=True)
    conn_b = aioice.Connection(ice_controlling=False)

    # invite
    await conn_a.gather_candidates()
    for element in conn_a.local_candidates:
        await conn_b.add_remote_candidate(element)
        conn_b.remote_username = conn_a.local_username
        conn_b.remote_password = conn_a.local_password

    # accept
    await conn_b.gather_candidates()
    for element in conn_b.local_candidates:
        await conn_a.add_remote_candidate(element)
        conn_a.remote_username = conn_b.local_username
        conn_a.remote_password = conn_b.local_password

    # connect
    await asyncio.gather(conn_a.connect(), conn_b.connect())

    # send data a -> b
    await conn_a.send(b'howdee')
    data = await conn_b.recv()
    print('B got', data)

    # send data b -> a
    await conn_b.send(b'gotcha')
    data = await conn_a.recv()
    print('A got', data)

    # close
    await asyncio.gather(conn_a.close(), conn_b.close())


asyncio.get_event_loop().run_until_complete(connect_using_ice())
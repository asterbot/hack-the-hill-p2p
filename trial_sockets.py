from errno import EADDRNOTAVAIL
from functools import partial
from itertools import count
import trio
import socket


async def peer(SRC, DEST):
    counter = count(start=1)

    async def sender(stream, n):
        print(f"sender{n}@{SRC}: started!")
        while True:
            data = bytes(f"Hello from {n}@{SRC}", "utf8")
            print(f"sender{n}@{SRC}: sending {data!r}")
            await stream.send_all(data)
            await trio.sleep(1)

    async def receiver(stream, n):
        print(f"receiver{n}@{SRC}: started!")
        async for data in stream:
            print(f"receiver{n}@{SRC}: got data {data!r}")
        print(f"receiver{n}@{SRC}: connection closed")

    async with trio.open_nursery() as nursery:
        async def run(connection: trio.SocketStream):
            count = next(counter)
            print(
                f"peer@{SRC} got connection{count} from {method}() with {connection.socket.getpeername()}")
            async with connection:
                async with trio.open_nursery() as nursery:
                    print(f"peer@{SRC}: spawning sender...")
                    nursery.start_soon(sender, connection, count)

                    print(f"peer@{SRC}: spawning receiver...")
                    nursery.start_soon(receiver, connection, count)

        print(f"peer: listening at {SRC}")
        servers = await trio.open_tcp_listeners(SRC[1], host=SRC[0])
        servers[0].socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        servers[0].socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEPORT, 1)
        await nursery.start(trio.serve_listeners, partial(run, "listen"), servers)

        print(f"peer: connecting from {SRC} to {DEST}")
        client = trio.socket.socket()
        client.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        client.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEPORT, 1)
        await client.bind(address=SRC)
        try:
            await client.connect(address=DEST)
        except OSError as err:
            if err.errno != EADDRNOTAVAIL:
                raise
            # the other client was faster than us
            print(f"peer@{SRC}: {err.strerror}")
        else:
            await run(trio.SocketStream(client))


async def main():
    async with trio.open_nursery() as nursery:
        a = ("127.0.0.1", 12345)
        b = ("127.0.0.1", 54321)
        nursery.start_soon(peer, a, b)
        nursery.start_soon(peer, b, a)

trio.run(main)

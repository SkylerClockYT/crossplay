import asyncio
import websockets
import json
import os

PORT = int(os.environ.get("PORT", 8765))
clients = set()
game_state = {}

async def handler(websocket):
    clients.add(websocket)
    try:
        async for message in websocket:
            data = json.loads(message)
            player_id = data.get("id")
            if not player_id:
                continue
            game_state[player_id] = data
            for client in clients:
                if client != websocket:
                    await client.send(json.dumps(data))
    except websockets.ConnectionClosed:
        print("Client disconnected")
    finally:
        clients.remove(websocket)
        if player_id in game_state:
            del game_state[player_id]

async def main():
    print(f"WebSocket server running on port {PORT}")
    async with websockets.serve(handler, "0.0.0.0", PORT):
        await asyncio.Future()
if __name__ == "__main__":
    asyncio.run(main())

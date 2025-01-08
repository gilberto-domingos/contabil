import asyncio
import websockets
from aiortc import RTCPeerConnection, VideoStreamTrack
import json
import cv2
from http.server import SimpleHTTPRequestHandler
from socketserver import TCPServer
import webbrowser
import threading
import os
import time


class VideoTrack(VideoStreamTrack):
    def __init__(self):
        super().__init__()
        self.cap = cv2.VideoCapture(0)

    async def recv(self):
        ret, frame = self.cap.read()
        if ret:
            return frame


async def create_offer():
    pc = RTCPeerConnection()
    video_track = VideoTrack()
    pc.addTrack(video_track)

    offer = await pc.createOffer()
    await pc.setLocalDescription(offer)

    return offer.sdp


async def handle_client(websocket, path):
    # Cria a oferta
    offer = await create_offer()

    # Envia a oferta para o cliente via WebSocket
    await websocket.send(json.dumps({"offer": offer}))

    print("Oferta enviada para o cliente")

    # Mantenha a conexão aberta
    await websocket.wait_closed()


async def websocket_server():
    server = await websockets.serve(handle_client, "localhost", 8765)
    await server.wait_closed()


def serve_html():
    os.chdir(os.path.dirname(os.path.abspath(__file__)))

    PORT = 8502
    handler = SimpleHTTPRequestHandler
    with TCPServer(("", PORT), handler) as httpd:
        print(f"Servindo face.html em http://localhost:{PORT}")
        webbrowser.open(f"http://localhost:{PORT}/face.html", new=2)
        httpd.serve_forever()


def start_http_server():
    threading.Thread(target=serve_html, daemon=True).start()


def wait_for_server_to_start():
    # Aguarda 2 segundos para garantir que o servidor tenha tempo de inicializar
    time.sleep(2)


async def main():
    # Inicia o servidor WebSocket
    websocket_task = asyncio.create_task(websocket_server())

    # Inicia o servidor HTTP (abrindo o navegador com face.html)
    start_http_server()

    # Espera um pouco antes de seguir para o Streamlit
    wait_for_server_to_start()

    # Aguarda o servidor WebSocket
    await websocket_task


if __name__ == "__main__":
    asyncio.run(main())

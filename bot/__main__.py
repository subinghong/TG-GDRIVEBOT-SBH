import os
import logging
from pyrogram import Client, idle
from bot import (
  APP_ID,
  API_HASH,
  BOT_TOKEN,
  DOWNLOAD_DIRECTORY
  )
import socket
import threading
    
logging.basicConfig(
    level=logging.DEBUG,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
LOGGER = logging.getLogger(__name__)
logging.getLogger("pyrogram").setLevel(logging.WARNING)

def http_server():
  HOST, PORT = '0.0.0.0', int(os.environ.get("PORT", 80))
  listen_socket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
  listen_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
  listen_socket.bind((HOST, PORT))
  listen_socket.listen(1)
  print('Serving HTTP on port %s ...' % PORT)
  while True:
    client_connection, client_address = listen_socket.accept()
    request = client_connection.recv(1024)
    print(request.decode("utf-8"))

    http_response = """\
HTTP/1.1 200 OK

Hello, World!
"""
    client_connection.sendall(http_response.encode("utf-8"))
    client_connection.close()

def bot_server():
  if not os.path.isdir(DOWNLOAD_DIRECTORY):
        os.makedirs(DOWNLOAD_DIRECTORY)
  plugins = dict(
      root="bot/plugins"
  )
  app = Client(
      "G-DriveBot",
      bot_token=BOT_TOKEN,
      api_id=APP_ID,
      api_hash=API_HASH,
      plugins=plugins,
      parse_mode="markdown",
      workdir=DOWNLOAD_DIRECTORY
  )
  
  # LOGGER.info('Starting Bot !')
  # app.run()
  # LOGGER.info('Bot Stopped !')
  app.start()
  threading.Thread(target=http_server, daemon=True).start()
  idle()
  app.stop()

if __name__ == "__main__":

  #start bot
  #threading.Thread(target=bot_server, daemon=True).start()
  #threading.start_new_thread(bot_server,())
  bot_server()
  
  
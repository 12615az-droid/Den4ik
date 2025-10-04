import os, threading
from http.server import BaseHTTPRequestHandler, HTTPServer


def _start_health_server():
    class _Handler(BaseHTTPRequestHandler):
        def do_GET(self):
            self.send_response(200)
            self.send_header("Content-Type", "text/plain; charset=utf-8")
            self.end_headers()
            self.wfile.write(b"OK")

        def log_message(self, *args):
            return

    port = int(os.environ.get("PORT", "8000"))
    srv = HTTPServer(("0.0.0.0", port), _Handler)
    threading.Thread(target=srv.serve_forever, daemon=True).start()


from telegram.ext import Application, CommandHandler
from handlers.start import start as start_handler
from handlers.weather import weather
from handlers.city import register as city_register
from handlers.daily import register as daily_register
from config import TOKEN


def main():
    _start_health_server()  # важно поднять до polling
    app = Application.builder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start_handler))
    app.add_handler(CommandHandler("weather", weather))
    city_register(app)
    daily_register(app)
    app.run_polling()


if __name__ == "__main__":
    main()

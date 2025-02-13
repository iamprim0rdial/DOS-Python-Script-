# Simple HTTP server to simulate a server under attack (for testing)
def start_simple_server():
    from http.server import SimpleHTTPRequestHandler, HTTPServer

    server = HTTPServer(('localhost', 8080), SimpleHTTPRequestHandler)
    logging.info("Simple HTTP server started at http://localhost:8080")
    server.serve_forever()

start_simple_server()

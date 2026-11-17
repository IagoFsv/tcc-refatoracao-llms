class Server:
    def __init__(self, ip, port, username, password, keyid):
        self.ip = ip
        self.port = port
        self.username = username
        self.password = password
        self.keyid = keyid

def update_server(server):
    conn = sqlite3.connect('frSSH.db')
    c = conn.cursor()
    c.execute("UPDATE servers SET ip=?, port=?, username=?, password=?, keyid=? WHERE ip=?", 
              (server.ip, server.port, server.username, server.password, server.keyid, server.ip))
    conn.commit()
    conn.close()
    print("Server updated.")

def run(registered, server):
    """registered: list of tuples 
    (ip, port, username, password, keyid). Public entry point of this unit."""
    _prepare_database(registered)
    update_server(Server(*server))
    return _rows()

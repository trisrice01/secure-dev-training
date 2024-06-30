import os
from app import db, app
from app.models.rdp_server import RDPServer


home_directory = os.path.expanduser("~")
rdp_servers_file = os.path.join(home_directory, "rdp_servers.txt")

if not os.path.exists(rdp_servers_file):
    exit()

loaded_rdp_servers = []

with open(rdp_servers_file) as f:
    loaded_rdp_servers = f.read().splitlines()

with app.app_context():
    for loaded_server in loaded_rdp_servers:
        matching_rdp_server = RDPServer.query.filter_by(ip_addr=loaded_server).first()
        if matching_rdp_server:
            continue
        r = RDPServer()
        r.ip_addr = loaded_server
        r.is_taken = False
        db.session.add(r)

    db.session.commit()


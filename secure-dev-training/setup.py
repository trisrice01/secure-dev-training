import os
from app import db, app
from app.models.rdp_server import RDPServer

home_directory = os.path.expanduser("~")
rdp_servers_file = os.path.join(home_directory, "rdp_servers.txt")

rdp_servers = []
with open(rdp_servers_file) as f:
    rdp_servers = list(f.read().splitlines())
    
with app.app_context():
    for rdp_server in rdp_servers:
        r = RDPServer()
        r.ip_addr = rdp_server
        r.is_taken = False
        db.session.add(r)

    db.session.commit()
#!/usr/bin/env python

## Tiny Syslog Server in Python.
##
## This is a tiny syslog server that is able to receive UDP based syslog
## entries on a specified port and save them to a file.


LOG_FILE = 'youlogfile.log'
HOST, PORT = "192.168.1.104", 514

#
# NO USER SERVICEABLE PARTS BELOW HERE...
#

import logging
import SocketServer
import os
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker


path = os.path.realpath(__file__)
logging.basicConfig(level=logging.INFO, format='%(message)s', datefmt='', filename=LOG_FILE, filemode='a')

# This is going to setup the database. Should be refactored into another file later...
engine = create_engine('sqlite:////' + path + 'logs.db')
Base = declarative_base()


class Entry(Base):
    __tablename__ = 'event'

    ipsrc = Column(Integer)  # Source IP
    ipdst = Column(Integer)  # Destination IP
    macsrc = Column(String)  # MAC Source Address
    macdst = Column(String)  # MAC Destination Address
    protocol = Column(String)  # Protocol Type
    seq = Column(Integer)   # Sequence Number
    ID = Column(Integer,  primary_key=True)  # Program Generated ID #
    time = Column(Integer)   # DATETIME Stamp
    TTL = Column(Integer)   # Time To Live
    SPT = Column(Integer)   # Source Port
    DPT = Column(Integer)   # Destination Port
    len = Column(Integer)   # Packet Length
    tos = Column(String)   # TOS
    ACK = Column(Integer)   # ACK #
    window = Column(Integer)   # Window Size
    interface = Column(String)   # Network approached
    action = Column(String)   # Action performed (DROP, ALLOW)
    module = Column(String)   # Module that the
    misc = Column(String)   # Misc information that may be indicated in log

    def __repr__(self):
        return '<ID=%d>' % self.ID

# END DATABASE INITIALIZATION


class SyslogUDPHandler(SocketServer.BaseRequestHandler):
    def handle(self):
        data = bytes.decode(self.request[0].strip())
        socket = self.request[1]
        print("%s : " % self.client_address[0], str(data))
        logging.info(str(data))
        with open("E:\Code\syslog\DDlog.txt", "a+") as f:
            f.write("%s : " % str(data))
            f.write("\n")


if __name__ == "__main__":
    try:
        server = SocketServer.UDPServer((HOST, PORT), SyslogUDPHandler)
        server.serve_forever(poll_interval=0.5)
    except (IOError, SystemExit):
        raise
    except KeyboardInterrupt:
        print ("Crtl+C Pressed. Shutting down.")
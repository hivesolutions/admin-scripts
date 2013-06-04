#!/usr/bin/python
# -*- coding: utf-8 -*-

# Hive Administration Scripts
# Copyright (c) 2008-2012 Hive Solutions Lda.
#
# This file is part of Hive Administration Scripts.
#
# Hive Administration Scripts is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# Hive Administration Scripts is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with Hive Administration Scripts. If not, see <http://www.gnu.org/licenses/>.

__author__ = "João Magalhães <joamag@hive.pt>"
""" The author(s) of the module """

__version__ = "1.0.0"
""" The version of the module """

__revision__ = "$LastChangedRevision$"
""" The revision number of the module """

__date__ = "$LastChangedDate$"
""" The last change date of the module """

__copyright__ = "Copyright (c) 2008-2012 Hive Solutions Lda."
""" The copyright for the module """

__license__ = "GNU General Public License (GPL), Version 3"
""" The license for the module """

import os
import sys
import paramiko
import cStringIO

user_home = os.path.expanduser("~")
dropbox_base = os.path.join(user_home, "Dropbox")
dropbox_home = os.path.join(dropbox_base, "Home")
sys.path.append(user_home)
sys.path.append(dropbox_base)
sys.path.append(dropbox_home)
servers = __import__("servers")

DEBUG = False

DNS_SERVERS = (
    "node1.bemisc.com",
    "node2.bemisc.com",
    "node3.bemisc.com",
    "servidor1.hive",
    "servidor2.hive"
)

DHCP_SERVERS = (
    "servidor1.hive"
)

DNS_CONFIG = {
    "node1.bemisc.com" : {
        "base_dir" : "/var/named/chroot/etc/bind/dns_registers",
        "service" : "named"
    }
}

DHCP_CONFIG = {}

def print_host(hostname, message):
    print "[" + hostname + "] " + message

def command(ssh, command):
    stdin, stdout, stderr = ssh.exec_command(command)
    data_out = stdout.readlines()
    data_err = stderr.readlines()

    stream_out = cStringIO.StringIO()
    stream_err = cStringIO.StringIO()

    for line in data_out: stream_out.write(line + "\n")
    for line in data_err: stderr.write(line + "\n")

    stream_out.seek(0)
    stream_err.seek(0)

    if DEBUG:
        for line in data_out: print line

    for line in data_err: print line

    return stdin, stream_out, stream_err

def uptime(ssh):
    _stdin, stdout, _stderr = command(ssh, "uptime")
    data = stdout.read()
    data = data.strip()
    up, _users, _load = data.split(",", 2)
    _time, up, up_value, up_unit = up.split(" ")
    return up_value + " " + up_unit

def update_service(ssh, base_dir, service):
    command(ssh, "cd " + base_dir + "; git pull")
    command(ssh, "service " + service + " restart")

def update_dns(ssh, base_dir = "/etc/bind/dns_registers", service = "bind9"):
    update_service(ssh, base_dir = base_dir, service = service)

def update_dhcp(ssh, base_dir = "/etc/dhcp/config", service = "isc-dhcp-server"):
    update_service(ssh, base_dir = base_dir, service = service)

def main():
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    for server in servers.SERVERS:
        hostname, username, password = server
        ssh.connect(
            hostname,
            username = username,
            password = password
        )
        uptime_s = uptime(ssh)
        print_host(hostname, uptime_s)

        if hostname in DNS_SERVERS:
            config = DNS_CONFIG.get(hostname, {})
            update_dns(ssh, **config)
            print_host(hostname, "updated dns")

        if hostname in DHCP_SERVERS:
            config = DHCP_CONFIG.get(hostname, {})
            update_dhcp(ssh, **config)
            print_host(hostname, "updated dhcp")

if __name__ == "__main__": main()

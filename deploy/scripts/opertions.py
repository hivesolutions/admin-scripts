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

import deployers

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

APT_SERVERS = (
    "servidor1.hive"
)

DNS_CONFIG = {
    "node1.bemisc.com" : {
        "base_dir" : "/var/named/chroot/etc/bind/dns_registers",
        "service" : "named"
    }
}

DHCP_CONFIG = {}

def service_update():
    for hostname in deployers.servers.SERVERS_MAP:
        ssh = deployers.get_ssh(hostname)
        uptime_s = deployers.uptime(ssh)
        deployers.print_host(hostname, uptime_s)

        if hostname in DNS_SERVERS:
            config = DNS_CONFIG.get(hostname, {})
            deployers.update_dns(ssh, **config)
            deployers.print_host(hostname, "updated dns")

        if hostname in DHCP_SERVERS:
            config = DHCP_CONFIG.get(hostname, {})
            deployers.update_dhcp(ssh, **config)
            deployers.print_host(hostname, "updated dhcp")

        if hostname in APT_SERVERS:
            deployers.update_apt(ssh)
            deployers.print_host(hostname, "software upgraded")

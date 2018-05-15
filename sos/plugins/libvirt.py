# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

# You should have received a copy of the GNU General Public License along
# with this program; if not, write to the Free Software Foundation, Inc.,
# 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301 USA.

from sos.plugins import Plugin, RedHatPlugin, UbuntuPlugin, DebianPlugin
import glob
import os


class Libvirt(Plugin, RedHatPlugin, UbuntuPlugin, DebianPlugin):
    """libvirt virtualization API
    """

    plugin_name = 'libvirt'
    profiles = ('system', 'virt')

    def setup(self):
        libvirt_keytab = "/etc/libvirt/krb5.tab"

        # authentication databases used for libvirt SASL authentication
        self.add_forbidden_path([
            "/etc/libvirt/passwd.db",
            "/etc/libvirt/krb5.tab",
            "/var/lib/libvirt/qemu/*/master-key.aes",
            "/etc/libvirt/secrets"
        ])

        self.add_copy_spec([
            "/etc/libvirt/libvirt.conf",
            "/etc/libvirt/libvirtd.conf",
            "/etc/libvirt/lxc.conf",
            "/etc/libvirt/nwfilter/*.xml",
            "/etc/libvirt/qemu/*.xml",
            "/etc/libvirt/qemu.conf",
            "/var/run/libvirt/",
            "/etc/libvirt/qemu/networks/*.xml",
            "/etc/libvirt/qemu/networks/autostart/*.xml",
            "/etc/libvirt/storage/*.xml",
            "/etc/libvirt/storage/autostart/*.xml",
            "/etc/libvirt/qemu-lockd.conf",
            "/etc/libvirt/virtlockd.conf"
        ])

        if not self.get_option("all_logs"):
            self.add_copy_spec("/var/log/libvirt/libvirtd.log", sizelimit=5)
            self.add_copy_spec("/var/log/libvirt/qemu/*.log", sizelimit=5)
            self.add_copy_spec("/var/log/libvirt/lxc/*.log", sizelimit=5)
            self.add_copy_spec("/var/log/libvirt/uml/*.log", sizelimit=5)
        else:
            self.add_copy_spec("/var/log/libvirt")

        if os.path.exists(self.join_sysroot(libvirt_keytab)):
            self.add_cmd_output("klist -ket %s" % libvirt_keytab)

        self.add_cmd_output("ls -lR /var/lib/libvirt/qemu")

        # get details of processes of KVM hosts
        for pidfile in glob.glob("/var/run/libvirt/*/*.pid"):
            pid = open(pidfile).read().splitlines()[0]
            for pf in ["environ", "cgroup", "maps", "numa_maps", "limits"]:
                self.add_copy_spec("/proc/%s/%s" % (pid, pf))

    def postproc(self):
        match_exp = r"(\s*passwd=\s*')([^']*)('.*)"
        libvirt_path_exps = [
            "/etc/libvirt/qemu/.*\.xml",
            "/var/run/libvirt/qemu/.*\.xml",
            "/etc/libvirt/.*\.conf"
        ]
        for path_exp in libvirt_path_exps:
            self.do_path_regex_sub(path_exp, match_exp, r"\1******\3")

# vim: set et ts=4 sw=4 :

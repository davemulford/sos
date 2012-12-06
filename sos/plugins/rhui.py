### This program is free software; you can redistribute it and/or modify
## it under the terms of the GNU General Public License as published by
## the Free Software Foundation; either version 2 of the License, or
## (at your option) any later version.

## This program is distributed in the hope that it will be useful,
## but WITHOUT ANY WARRANTY; without even the implied warranty of
## MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
## GNU General Public License for more details.

## You should have received a copy of the GNU General Public License
## along with this program; if not, write to the Free Software
## Foundation, Inc., 675 Mass Ave, Cambridge, MA 02139, USA.

from sos.plugins import Plugin, RedHatPlugin
import os

class rhui(Plugin, RedHatPlugin):
    """Red Hat Update Infrastructure for Cloud Providers data
    """

    rhui_debug_path = "/usr/share/rh-rhua/rhui-debug.py"

    packages = [ "rh-rhui-tools" ]
    files = [ rhui_debug_path ]

    def setup(self):
        if self.isInstalled("pulp-cds"):
            cds = "--cds"
        else:
            cds = ""

        rhui_debug_dst_path = os.path.join(self.cInfo['dstroot'],
                self.cInfo['cmddir'], self.name())
        try:
            os.mkdir(rhui_debug_dst_path)
        except:
            return

        self.collectExtOutput("python %s %s --dir %s"
                % (self.rhui_debug_path, cds, rhui_debug_dst_path),
                suggest_filename="rhui-debug")
        return

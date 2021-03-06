__author__ = 'sonia'
#! /usr/bin/env python

#    Copyright (C) 2012-2014  Octets - octets.etsmtl.ca
#
#    This file is part of SeaGoatVision.
#
#    SeaGoatVision is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.



#Configurations -> TemplateMedia
from SeaGoatVision.server.media.implementation.IPC_Sonar import IPC_Sonar



class ConfIpc_sonar:

    def __init__(self):
        self.media = IPC_Sonar
        self.name = "ipc"
        self.device = "/tmp/seagoatvision_media.ipc_sonar"

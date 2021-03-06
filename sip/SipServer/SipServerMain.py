''' 
Copyright (C) 2020 Yee Young Han <websearch@naver.com> (http://blog.naver.com/websearch)

This program is free software; you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation; either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program; if not, write to the Free Software
Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA  02111-1307  USA
'''

import sys
import time
from .SipServerSetup import SipServerSetup
from .SipServer import SipServer

if( len(sys.argv) == 1 ):
  print( "[Usage] python -m sip.SipServer.SipServerMain {setup file path}")
  exit()

strSetupFileName = sys.argv[1]
clsSetupFile = SipServerSetup()

if( clsSetupFile.Read( strSetupFileName ) == False ):
  print( "lsSetupFile.Read(" + strSetupFileName + ") error" )
  exit()

clsSipServer = SipServer()
if( clsSipServer.Start( clsSetupFile ) == False ):
  exit()

while True:
  time.sleep(1.0)
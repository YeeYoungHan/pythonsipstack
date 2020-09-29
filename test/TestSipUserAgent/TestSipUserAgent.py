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

import socket
import time
from sip.SipPlatform.Log import Log, LogLevel
from sip.SipUserAgent.SipUserAgent import SipUserAgent
from sip.SipUserAgent.SipServerInfo import SipServerInfo
from sip.SipStack.SipStackSetup import SipStackSetup

class CallBack():

  def EventRegister( self, clsServerInfo, iStatus ):
    Log.Print( LogLevel.DEBUG, "EventRegister(" + clsServerInfo.strUserId + "@" + clsServerInfo.strIp + ":" + str(clsServerInfo.iPort) + ") status(" + str(iStatus) + ")" )

Log.SetLevel( LogLevel.DEBUG | LogLevel.NETWORK | LogLevel.INFO )

clsSetup = SipStackSetup()
clsSetup.strLocalIp = socket.gethostbyname(socket.gethostname())

clsServerInfo = SipServerInfo()
#clsServerInfo.strIp = "192.168.150.131"
clsServerInfo.strIp = "192.168.150.10"
clsServerInfo.strUserId = "1000"
clsServerInfo.strPassWord = "1234"

clsSipUserAgent = SipUserAgent()
clsSipUserAgent.InsertRegisterInfo( clsServerInfo )

clsCallBack = CallBack()

if( clsSipUserAgent.Start( clsSetup, clsCallBack ) == False ):
  print( "clsSipUserAgent.Start() error" )

while True:
  time.sleep(1)


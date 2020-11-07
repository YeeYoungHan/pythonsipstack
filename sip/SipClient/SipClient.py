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
from ..SipPlatform.Log import Log, LogLevel
from ..SipStack.SipStackSetup import SipStackSetup
from ..SipUserAgent.SipUserAgent import SipUserAgent
from ..SipUserAgent.SipUserAgentCallBack import SipUserAgentCallBack
from ..SipUserAgent.SipServerInfo import SipServerInfo

class SipClient(SipUserAgentCallBack):

  from .SipClientUserAgent import EventRegister, EventIncomingRequestAuth, EventIncomingCall, EventCallStart, EventCallEnd

  def __init__( self ):
    self.clsUserAgent = SipUserAgent()
    self.strCallId = ''
  
  def Start( self, clsSetupFile ):
    clsSetup = SipStackSetup()

    if( len(clsSetupFile.strLocalIp) == 0 ):
      clsSetup.strLocalIp = socket.gethostbyname(socket.gethostname())
    else:
      clsSetup.strLocalIp = clsSetupFile.strLocalIp
    
    clsSetup.iLocalUdpPort = clsSetupFile.iUdpPort

    clsSipServerInfo = SipServerInfo()
    clsSipServerInfo.strIp = clsSetupFile.strSipServerIp
    clsSipServerInfo.strDomain = clsSetupFile.strSipDomain
    clsSipServerInfo.strUserId = clsSetupFile.strSipUserId
    clsSipServerInfo.strPassWord = clsSetupFile.strSipPassWord

    if( self.clsUserAgent.InsertRegisterInfo( clsSipServerInfo ) == False ):
      Log.Print( LogLevel.ERROR, "clsUserAgent.InsertRegisterInfo error" )
      return False

    if( self.clsUserAgent.Start( clsSetup, self ) == False ):
      Log.Print( LogLevel.ERROR, "clsUserAgent.Start error" )
      return False
    
    self.clsUserAgent.clsSipStack.AddCallBack( self )
    self.clsSetupFile = clsSetupFile

    return True
  
  def StartCall( self, strTo ):
    

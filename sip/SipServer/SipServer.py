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
from ..SipStack.SipStackCallback import SipStackCallBack
from ..SipStack.SipStackSetup import SipStackSetup
from ..SipUserAgent.SipUserAgent import SipUserAgent
from ..SipUserAgent.SipUserAgentCallBack import SipUserAgentCallBack
from .CallMap import CallMap
from .NonceMap import NonceMap
from .SipServerMap import SipServerMap
from .UserMap import UserMap

class SipServer(SipUserAgentCallBack,SipStackCallBack):

  from .SipServerRegister import AddChallenge, SendUnAuthorizedResponse, CheckAuthorization, RecvRequestRegister

  def __init__( self ):
    self.clsUserAgent = SipUserAgent()
    self.clsCallMap = CallMap( self.clsUserAgent )
    self.clsNonceMap = NonceMap()
    self.clsSipServerMap = SipServerMap()
    self.clsUserMap = UserMap()
  
  def Start( self, clsSetupFile ):
    clsSetup = SipStackSetup()

    if( len(clsSetupFile.strLocalIp) == 0 ):
      clsSetup.strLocalIp = socket.gethostbyname(socket.gethostname())
    else:
      clsSetup.strLocalIp = clsSetupFile.strLocalIp
    
    clsSetup.iLocalUdpPort = clsSetupFile.iUdpPort
    clsSetup.iUdpThreadCount = clsSetupFile.iUdpThreadCount

    if( self.clsUserAgent.Start( clsSetup, self ) == False ):
      Log.Print( LogLevel.ERROR, "clsUserAgent.Start error" )
      return False
    
    self.clsUserAgent.clsSipStack.AddCallBack( self )
    self.clsSetupFile = clsSetupFile

    return True
  
  def RecvRequest( self, clsMessage ):
    if( clsMessage.IsMethod("REGISTER") ):
      return self.RecvRequestRegister( clsMessage )

    return False
  
  def SendResponse( self, clsMessage, iStatusCode ):
    clsResponse = clsMessage.CreateResponseWithToTag( iStatusCode )
    self.clsUserAgent.clsSipStack.SendSipMessage( clsResponse )
    return True
  
  def StopCall( self, strCallId, iStatusCode ):
    self.clsUserAgent.StopCall( strCallId, iStatusCode )

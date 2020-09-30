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

import time
from ..SipPlatform.Log import Log, LogLevel
from ..SipParser.SipStatusCode import SipStatusCode
  
def ClearLogin( self, clsServerInfo, iStatusCode ):
  clsServerInfo.ClearLogin()
  clsServerInfo.iNextSendTime = time.time() + 60
  self.clsCallBack.EventRegister( clsServerInfo, iStatusCode )

def RecvRegisterResponse( self, clsMessage ):
  strUserId = clsMessage.clsFrom.clsUri.strUser
  clsDeleteServerList = []
  bRes = False

  self.clsRegisterMutex.acquire()
  for clsServerInfo in self.clsRegisterList:
    if( clsServerInfo.strUserId == strUserId and clsServerInfo.strIp == clsMessage.strClientIp ):
      iStatusCode = clsMessage.iStatusCode

      if( iStatusCode == SipStatusCode.SIP_OK ):
        if( clsServerInfo.iLoginTimeout == 0 ):
          clsServerInfo.ClearLogin()
        else:
          clsServerInfo.bLogin = True
          clsServerInfo.iLoginTime = time.time()
          clsServerInfo.iResponseTime = clsServerInfo.iLoginTime

          iExpires = clsMessage.GetExpires()
          if( iExpires > 0 and iExpires != clsServerInfo.iLoginTimeout ):
            clsServerInfo.iLoginTimeout = iExpires
        
        self.clsCallBack.EventRegister( clsServerInfo, iStatusCode )

        if( clsServerInfo.iLoginTimeout == 0 ):
          clsDeleteServerList.append( clsServerInfo )
      
      elif( iStatusCode == SipStatusCode.SIP_UNAUTHORIZED or iStatusCode == SipStatusCode.SIP_PROXY_AUTHENTICATION_REQUIRED ):
        if( clsServerInfo.bAuth ):
          self.ClearLogin( clsServerInfo, iStatusCode )
        else:
          if( self.clsSipStack.clsSetup.bUseRegisterSession ):
            clsServerInfo.SetChallenge( clsMessage )
          
          clsResponse = clsServerInfo.CreateRegister( self.clsSipStack, clsMessage )
          self.clsSipStack.SendSipMessage( clsResponse )
      
      elif( iStatusCode == SipStatusCode.SIP_INTERVAL_TOO_BRIEF ):
        clsHeader = clsMessage.GetHeader( "Min-Expires" )
        if( clsHeader == None ):
          Log.Print( LogLevel.ERROR, "Min-Expires header is not found" )
          self.ClearLogin( clsServerInfo, iStatusCode )
        else:
          iMinExpires = int( clsHeader.strValue )
          if( iMinExpires < 0 ):
            Log.Print( LogLevel.ERROR, "Min-Expires header's value is not correct" )
            self.ClearLogin( clsServerInfo, iStatusCode )
          
          clsServerInfo.iLoginTimeout = iMinExpires
          clsResponse = clsServerInfo.CreateRegister( self.clsSipStack, clsMessage )
          self.clsSipStack.SendSipMessage( clsResponse )
        
      else:
        self.ClearLogin( clsServerInfo, iStatusCode )

      bRes = True
      break
  
  for clsDeleteServerInfo in clsDeleteServerList:
    self.clsRegisterList.remove( clsDeleteServerInfo )
  self.clsRegisterMutex.release()

  return bRes

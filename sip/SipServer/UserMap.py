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
import threading
from ..SipPlatform.Log import Log, LogLevel
from ..SipParser.SipTransport import SipTransport, SipGetTransport

class UserInfo():

  def __init__( self ):
    self.strIp = ''
    self.iPort = 0
    self.eTransport = SipTransport.UDP
    self.iLoginTime = 0.0
    self.iLoginTimeout = 0
    self.strGroupId = ''

class UserMap():

  def __init__( self ):
    self.clsMutex = threading.Lock()
    self.clsMap = {}
  
  def Insert( self, clsMessage, clsContact, clsXmlUser ):
    strUserId = clsMessage.clsFrom.clsUri.strUserId
    if( len(strUserId) == 0 ):
      return False
    
    clsUserInfo = UserInfo()
    clsUserInfo.strIp, clsUserInfo.iPort = clsMessage.GetTopViaIpPort()
    clsUserInfo.iLoginTimeout = clsMessage.GetExpires()

    if( clsUserInfo.iLoginTimeout == 0 ):
      return False
    
    clsUserInfo.eTransport = clsMessage.eTransport
    clsUserInfo.iLoginTime = time.time()
    clsUserInfo.strGroupId = clsXmlUser.strGroupId

    self.clsMutex.acquire()
    Log.Print( LogLevel.DEBUG, "user(" + strUserId + ") set (" + clsUserInfo.strIp + ":" + str(clsUserInfo.iPort) + ":" + SipGetTransport(clsUserInfo.eTransport) + ") group(" + clsUserInfo.strGroupId + ")" )
    self.clsMap[strUserId] = clsUserInfo
    self.clsMutex.release()

    if( clsContact != None ):
      clsContact.clsUri.strProtocol = "sip"
      clsContact.clsUri.strUser = strUserId
      clsContact.clsUri.strHost = clsUserInfo.strIp
      clsContact.clsUri.iPort = clsUserInfo.iPort
      clsContact.clsUri.InsertTransport( clsUserInfo.eTransport )
    
    return True
  
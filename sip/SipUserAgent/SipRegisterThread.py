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

def SipRegisterThread( clsUserAgent ):

  while( clsUserAgent.bStopEvent == False ):
    iTime = time.time()

    clsUserAgent.clsRegisterMutex.acquire()
    for clsServerInfo in clsUserAgent.clsRegisterList:
      if( clsServerInfo.bLogin == False ):
        if( clsServerInfo.iSendTime == 0.0 ):
          if( clsServerInfo.iNextSendTime != 0.0 and clsServerInfo.iNextSendTime > iTime ):
            continue
          
          clsRequest = clsServerInfo.CreateRegister( clsUserAgent.clsSipStack, None )
          if( clsUserAgent.clsSipStack.SendSipMessage( clsRequest ) ):
            clsServerInfo.iSendTime = iTime
            clsServerInfo.iResponseTime = 0.0
      else:
        if( ( ( iTime - clsServerInfo.iLoginTime ) > ( clsServerInfo.iLoginTimeout / 2 ) and clsServerInfo.iResponseTime != 0.0 ) or clsServerInfo.iLoginTimeout == 0 ):
          clsRequest = clsServerInfo.CreateRegister( clsUserAgent.clsSipStack, None )
          if( clsUserAgent.clsSipStack.SendSipMessage( clsRequest ) ):
            clsServerInfo.iSendTime = iTime
            clsServerInfo.iResponseTime = 0.0
        elif( clsServerInfo.iNatTimeout > 0 ):
          if( ( iTime - clsServerInfo.iSendTime ) >= clsServerInfo.iNatTimeout ):
            clsUserAgent.clsSipStack.SendIpPort( "\r\n", clsServerInfo.strIp, clsServerInfo.iPort, clsServerInfo.eTransport )
            clsServerInfo.iSendTime = iTime

    clsUserAgent.clsRegisterMutex.release()

    time.sleep(1.0)
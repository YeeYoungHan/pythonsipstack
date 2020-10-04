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

import select
from ..SipPlatform.Log import Log, LogLevel
from ..SipParser.SipTransport import SipTransport

def SipUdpThread( clsSipStack ):

  clsSipStack.clsThreadCount.Increase()

  read_list = [ clsSipStack.hUdpSocket ]
  
  while( clsSipStack.bStopEvent == False ):
    iRecvLen = 0

    clsSipStack.clsUdpRecvMutex.acquire()
    try:
      read_socket_list, write_socket_list, except_socket_list = select.select( read_list, [], [], 1.0 )
      for read_socket in read_socket_list:
        szPacket, clsClientIpPort = read_socket.recvfrom( 8192 )
        iRecvLen = len(szPacket)
    except Exception as other:
      Log.Print( LogLevel.LOG_ERROR, "SipUdpThread exception - " + other )
    clsSipStack.clsUdpRecvMutex.release()

    if( iRecvLen > 0 ):
      strPacket = szPacket.decode()
      strIp = clsClientIpPort[0]
      iPort = clsClientIpPort[1]
      Log.Print( LogLevel.NETWORK, "UdpRecv(" + strIp + ":" + str(iPort) + ") [" + strPacket + "]" )
      clsSipStack.RecvSipPacket( strPacket, strIp, iPort, SipTransport.UDP )
  
  clsSipStack.clsThreadCount.Decrease()

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
import threading
import time
from ..SipPlatform.SafeCount import SafeCount
from ..SipPlatform.Log import Log, LogLevel
from ..SipParser.SipTransport import SipTransport, SipGetProtocol
from ..SipParser.SipStatusCode import SipStatusCode
from .SipStackThread import SipStackThread
from .SipUdpThread import SipUdpThread
from .SipNICTList import SipNICTList
from .SipICTList import SipICTList
from .SipNISTList import SipNISTList
from .SipISTList import SipISTList

class SipStack():

  from .SipStackComm import SendSipMessage, RecvSipMessage, RecvSipPacket, Send, SendIpPort, CheckSipMessage

  def __init__( self ):
    self.clsMutex = threading.Lock()
    self.clsUdpSendMutex = threading.Lock()
    self.clsUdpRecvMutex = threading.Lock()
    self.hUdpSocket = None
    self.bStopEvent = False
    self.bStarted = False
    self.clsThreadCount = SafeCount()
    self.clsNICT = SipNICTList(self)
    self.clsICT = SipICTList(self)
    self.clsNIST = SipNISTList(self)
    self.clsIST = SipISTList(self)
    self.clsCallBackList = []
  
  def Start( self, clsSetup ):
    self.clsSetup = clsSetup

    p = threading.Thread( target=SipStackThread, args=(self,))
    p.daemon = True
    p.start()

    if( clsSetup.iLocalUdpPort > 0 ):
      self.hUdpSocket = socket.socket( socket.AF_INET, socket.SOCK_DGRAM )
      self.hUdpSocket.bind( ('0.0.0.0', 8000) )

      p = threading.Thread( target=SipUdpThread, args=(self,))
      p.daemon = True
      p.start()
    
    self.bStarted = True
  
  def Stop( self ):
    if( self.bStarted == False or self.bStopEvent ):
      return
    
    self.bStopEvent = True

    if( self.clsSetup.iLocalUdpPort > 0 ):
      client = socket.socket( socket.AF_INET, socket.SOCK_DGRAM )

      for i in range( 0, self.clsSetup.iLocalUdpPort ):
        client.sendto( b'', ('127.0.0.1', self.clsSetup.iLocalUdpPort) )

    while self.clsThreadCount.GetCount() > 0 :
      time.sleep( 0.02 )
    
    if( self.hUdpSocket != None ):
      self.hUdpSocket.close()
      self.hUdpSocket = None
    
    self.DeleteAllTransaction()

    self.bStarted = False

  def Execute( self ):
    iTime = time.time()

    self.clsNICT.Execute( iTime )
    self.clsICT.Execute( iTime )
    self.clsNIST.Execute( iTime )
    self.clsIST.Execute( iTime )
  
  def DeleteAllTransaction( self ):
    self.clsNICT.DeleteAll()

  def RecvRequest( self, clsMessage ):
    bSendResponse = False

    for clsCallBack in self.clsCallBackList:
      if( clsCallBack.RecvRequest( clsMessage ) == True ):
        bSendResponse = True

    if( bSendResponse == False ):
      clsResponse = clsMessage.CreateResponseWithToTag( SipStatusCode.SIP_NOT_IMPLEMENTED )
      self.SendSipMessage( clsResponse )
  
  def RecvResponse( self, clsMessage ):
    for clsCallBack in self.clsCallBackList:
      clsCallBack.RecvResponse( clsMessage )

  def AddCallBack( self, clsCallBack ):
    self.clsCallBackList.append( clsCallBack )
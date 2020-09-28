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
from ..SipParser.SipParameter import SearchSipParameter
from ..SipParser.SipFrom import SipFrom
from ..SipParser.SipMessage import SipMessage
from ..SipParser.SipStatusCode import SipStatusCode
from .SipUdpThread import SipUdpThread
from .SipNICTList import SipNICTList
from .SipStackVersion import SipStackVersion

class SipStack():

  def __init__( self ):
    self.clsMutex = threading.Lock()
    self.clsUdpSendMutex = threading.Lock()
    self.clsUdpRecvMutex = threading.Lock()
    self.hUdpSocket
    self.bStopEvent = False
    self.bStarted = False
    self.clsThreadCount = SafeCount()
    self.clsNICT = SipNICTList()
    self.clsCallBackList = []
  
  def Start( self, clsSetup ):
    self.clsSetup = clsSetup

    if( clsSetup.iLocalUdpPort > 0 ):
      self.hUdpSocket = socket.socket( socket.AF_INET, socket.SOCK_DGRAM )
      self.hUdpSocket.bind( ('0.0.0.0', 8000) )

      p = threading.Thread( target=SipUdpThread, args=(self))
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
  
  def DeleteAllTransaction( self ):
    self.clsNICT.DeleteAll()

  def SendSipMessage( self, clsMessage ):

    self.CheckSipMessage( clsMessage )

    if( clsMessage.IsRequest() ):
      if( clsMessage.IsMethod("INVITE") or clsMessage.IsMethod("ACK") ):
        if( self.clsICT.Insert( clsMessage ) ):
          self.Send( clsMessage, False )
          return True
      else:
        if( self.clsNICT.Insert( clsMessage ) ):
          self.Send( clsMessage, False )
          return True
    else:
      if( clsMessage.IsMethod("INVITE") ):
        if( self.clsIST.Insert( clsMessage ) ):
          self.Send( clsMessage, False )
          return True
      else:
        if( self.clsNIST.Insert( clsMessage ) ):
          self.Send( clsMessage, False )
          return True
    
    return False

  def RecvSipMessage( self, clsMessage ):

    if( clsMessage.IsRequest() ):

      if( clsMessage.IsMethod("INVITE") or clsMessage.IsMethod("ACK") ):
        if( self.clsIST.Insert( clsMessage ) ):
          self.RecvRequest( clsMessage )
          return True
      else:
        if( self.clsNIST.Insert( clsMessage ) ):
          self.RecvRequest( clsMessage )
          return True
    
    else:

      if( clsMessage.IsMethod("INVITE") ):
        if( clsMessage.iStatusCode >= 200 ):
          self.clsNICT.DeleteCancel( clsMessage )

        if( self.clsICT.Insert( clsMessage ) ):
          self.RecvResponse( clsMessage )
          return True
      
      else:
        if( self.clsNICT.Insert( clsMessage ) ):
          self.RecvResponse( clsMessage )
          return True

    return False
      

  def RecvSipMessage( self, strPacket, strIp, iPort, eTransport ):
    clsMessage = SipMessage()

    if( clsMessage.Parse( strPacket ) == -1 ):
      return False
    
    if( clsMessage.IsRequest() ):
      clsMessage.AddIpPortToTopVia( strIp, iPort )
    
    clsMessage.strClientIp = strIp
    clsMessage.iClientPort = iPort
    clsMessage.eTransport = eTransport

    self.RecvSipMessage( clsMessage )
  
  def Send( self, clsMessage, bCheckMessage ):

    strIp = ''
    iPort = -1
    eTransport = SipTransport.UDP

    if( bCheckMessage ):
      self.CheckSipMessage( clsMessage )
    
    if( clsMessage.IsRequest() ):
      if( len(clsMessage.clsRouteList) == 0 ):
        if( len(clsMessage.clsReqUri.strHost) == 0 ):
          return False
        
        strIp = clsMessage.clsReqUri.strHost
        iPort = clsMessage.clsReqUri.iPort
        eTransport = clsMessage.clsReqUri.SelectTransport()
      else:
        clsRoute = clsMessage.clsRouteList[0]
        strIp = clsRoute.clsUri.strHost
        iPort = clsRoute.clsUri.iPort
        eTransport = clsRoute.clsUri.SelectTransport()
    else:
      if( len(clsMessage.clsViaList) == 0 ):
        return False
      
      clsVia = clsMessage.clsViaList[0]

      strPort = SearchSipParameter( clsVia, "rport" )
      if( len(strPort) > 0 ):
        iPort = int(strPort)
      else:
        iPort = clsVia.iPort
      
      strIp = SearchSipParameter( clsVia, "received" )
      if( len(strIp) == 0 ):
        strIp = clsVia.strHost

      strTransport = SearchSipParameter( clsVia, "transport" )
      if( len(strTransport) > 0 ):
        if( strTransport == "tcp" ):
          eTransport = SipTransport.TCP
        elif( strTransport == "tls" ):
          eTransport = SipTransport.TLS
      else:
        strTransport = clsVia.strTransport.lower()

        if( strTransport == "tcp" ):
          eTransport = SipTransport.TCP
        elif( strTransport == "tls" ):
          eTransport = SipTransport.TLS
      
      if( iPort <= 0 ):
        iPort = 5060
      
      if( len(strIp) == 0 ):
        return False
      
      if( len(clsMessage.strPacket) == 0 ):
        clsMessage.strPacket = str(clsMessage)
      
      szPacket = clsMessage.strPacket.encode()

      if( eTransport == SipTransport.UDP ):
        self.clsUdpSendMutex.acquire()
        self.hUdpSocket.sendto( szPacket, (strIp, iPort) )
        self.clsUdpSendMutex.release()

        Log.Print( LogLevel.NETWORK, "UdpSend(" + strIp + ":" + str(iPort) + ") [" + clsMessage.strPacket + "]" )
    
    return True
  
  def Send( self, strPacket, strIp, iPort, eTransport ):

    szPacket = strPacket.encode()

    if( eTransport == SipTransport.UDP ):
      self.clsUdpSendMutex.acquire()
      self.hUdpSocket.sendto( szPacket, (strIp, iPort) )
      self.clsUdpSendMutex.release()

  def CheckSipMessage( self, clsMessage ):

    if( clsMessage.IsRequest() ):
      if( len(clsMessage.clsViaList) == 0 ):
        iPort = self.clsSetup.GetLocalPort( clsMessage.eTransport )
        if( iPort == 0 ):
          iPort = 5060
        clsMessage.AddVia( self.clsSetup.strLocalIp, iPort, '', clsMessage.eTransport )
    
    if( len(clsMessage.strSipVersion) == 0 ):
      clsMessage.strSipVersion = "SIP/2.0"
    
    if( len(clsMessage.clsContactList) == 0 ):
      eTransport = SipTransport.UDP

      if( clsMessage.IsRequest() ):
        if( len(clsMessage.clsRouteList) == 0 ):
          eTransport = clsMessage.clsReqUri.SelectTransport()
        else:
          eTransport = clsMessage.clsRouteList[0].clsUri.SelectTransport()
      else:
        if( len(clsMessage.clsViaList) != 0 ):
          strTransport = SearchSipParameter( clsMessage.clsViaList, "transport" )
          if( strTransport == "tcp" ):
            eTransport = SipTransport.TCP
          elif( strTransport == "tls" ):
            eTransport = SipTransport.TLS
      
      clsContact = SipFrom()

      clsContact.clsUri.strProtocol = SipGetProtocol( eTransport )
      if( clsMessage.IsRequest() ):
        clsContact.clsUri.strUser = clsMessage.clsFrom.clsUri.strUser
      else:
        clsContact.clsUri.strUser = clsMessage.clsTo.clsUri.strUser
      
      clsContact.clsUri.strHost = self.clsSetup.strLocalIp

      if( eTransport == SipTransport.UDP ):
        clsContact.clsUri.iPort = self.clsSetup.iLocalUdpPort
      
      clsContact.clsUri.InsertTransport( eTransport )
      clsMessage.clsContactList.append( clsContact )
    
    if( len(self.clsSetup.strUserAgent) == 0 ):
      clsMessage.strUserAgent = SipStackVersion.SIP_USER_AGENT
    else:
      clsMessage.strUserAgent = self.clsSetup.strUserAgent
    
    if( clsMessage.iMaxForwards == -1 ):
      clsMessage.iMaxForwards = 70
  
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
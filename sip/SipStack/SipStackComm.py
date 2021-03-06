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

from ..SipPlatform.Log import Log, LogLevel
from ..SipParser.SipTransport import SipTransport, SipGetProtocol
from ..SipParser.SipParameter import SearchSipParameter
from ..SipParser.SipFrom import SipFrom
from ..SipParser.SipMessage import SipMessage
from ..SipParser.SipStatusCode import SipStatusCode
from .SipStackVersion import SipStackVersion

def SendSipMessage( self, clsMessage ):
  """ 입력된 SIP 메시지를 네트워크로 전송한다.

  Args:
      clsMessage (SipMessage): SIP 메시지 객체

  Returns:
      bool: 성공하면 True 를 리턴하고 그렇지 않으면 False 를 리턴한다.
  """
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
  """ SIP 메시지 수신 처리 메소드

  Args:
      clsMessage (SipMessage): SIP 메시지 객체

  Returns:
      bool: 성공하면 True 를 리턴하고 그렇지 않으면 False 를 리턴한다.
  """
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
    

def RecvSipPacket( self, strPacket, strIp, iPort, eTransport ):
  """ SIP 메시지 수신 처리 메소드

  Args:
      strPacket (string): 수신한 SIP 메시지 문자열
      strIp (string): SIP 메시지 전송 IP 주소
      iPort (int): SIP 메시지 전송 포트 번호
      eTransport (int): SIP 메시지 전송 SIP transport 숫자

  Returns:
      bool: 수신한 SIP 메시지 파싱에 성공하면 True 를 리턴하고 그렇지 않으면 False 를 리턴한다.
  """
  clsMessage = SipMessage()

  if( clsMessage.Parse( strPacket ) == -1 ):
    return False
  
  if( clsMessage.IsRequest() ):
    clsMessage.AddIpPortToTopVia( strIp, iPort, eTransport )
  
  clsMessage.strClientIp = strIp
  clsMessage.iClientPort = iPort
  clsMessage.eTransport = eTransport

  self.RecvSipMessage( clsMessage )

  return True

def Send( self, clsMessage, bCheckMessage ):
  """ SIP 메시지를 전송한다.

  Args:
      clsMessage (SipMessage): SIP 메시지 객체
      bCheckMessage (bool): SIP 메시지 객체의 유효성을 검사하면 True 를 입력하고 그렇지 않으면 False 를 입력

  Returns:
      bool: SIP 메시지 전송에 성공하면 True 를 리턴하고 그렇지 않으면 False 를 리턴한다.
  """
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

    strPort = clsVia.SelectParam( "rport" )
    if( len(strPort) > 0 ):
      iPort = int(strPort)
    else:
      iPort = clsVia.iPort
    
    strIp = clsVia.SelectParam( "received" )
    if( len(strIp) == 0 ):
      strIp = clsVia.strHost

    strTransport = clsVia.SelectParam( "transport" )
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

def SendIpPort( self, strPacket, strIp, iPort, eTransport ):
  """ SIP 메시지 문자열을 입력된 IP 주소, 포트 번호, SIP transport 로 전송한다.

  Args:
      strPacket (string): SIP 메시지 문자열
      strIp (string): IP 주소
      iPort (int): 포트 번호
      eTransport (int): SIP transport 숫자
  """
  szPacket = strPacket.encode()

  if( eTransport == SipTransport.UDP ):
    self.clsUdpSendMutex.acquire()
    self.hUdpSocket.sendto( szPacket, (strIp, iPort) )
    self.clsUdpSendMutex.release()

def CheckSipMessage( self, clsMessage ):
  """ 전송할 SIP 메시지의 유효성을 검사하여서 유효하지 않은 항목을 유효하게 저장한다.

  Args:
      clsMessage (SipMessage): SIP 메시지 객체
  """
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
        strTransport = clsMessage.clsViaList[0].SelectParam( "transport" )
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

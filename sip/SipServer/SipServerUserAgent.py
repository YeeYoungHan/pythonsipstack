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
from ..SipParser.SipFrom import SipFrom
from ..SipParser.SipTransport import SipTransport
from ..SipParser.SipStatusCode import SipStatusCode
from .SipServerRegister import ECheckAuthResult
from .XmlUser import XmlUser, SelectUser
from .UserMap import UserInfo
from ..SipUserAgent.RtpDirection import RtpDirection

def CheckAuthrization( self, clsMessage ):
  if( len(clsMessage.clsAuthorizationList) == 0 ):
    self.SendUnAuthorizedResponse( clsMessage )
    return False
  
  bRes, clsXmlUser = self.CheckAuthorization( clsMessage.clsAuthorizationList[0], clsMessage.strSipMethod )
  if( bRes == ECheckAuthResult.NONCE_NOT_FOUND ):
    self.SendUnAuthorizedResponse( clsMessage )
    return False
  elif( bRes == ECheckAuthResult.ERROR ):
    self.SendResponse( clsMessage, SipStatusCode.SIP_FORBIDDEN )
    return False
  
  self.clsUserMap.Insert( clsMessage, None, clsXmlUser )
  
  return True

def EventRegister( self, clsServerInfo, iStatus ):
  self.clsSipServerMap.Set( clsServerInfo, iStatus )

def EventIncomingRequestAuth( self, clsMessage ):
  strIp, iPort = clsMessage.GetTopViaIpPort( )
  if( len(strIp) == 0 ):
    Log.Print( LogLevel.ERROR, "EventIncomingRequestAuth - GetTopViaIpPort error" )
    self.SendResponse( clsMessage, SipStatusCode.SIP_BAD_REQUEST )
    return False
  
  # IP-PBX 에서 전송한 SIP 요청 메시지는 인증 허용으로 처리한다.
  if( self.clsSipServerMap.Select( strIp, clsMessage.clsTo.clsUri.strUser ) ):
    Log.Print( LogLevel.DEBUG, "EventIncomingRequestAuth ip(" + strIp + ") user(" + clsMessage.clsTo.clsUri.strUser + ") IP-PBX => allowed" )
    return True
  
  clsUserInfo = self.clsUserMap.Select( clsMessage.clsFrom.clsUri.strUser )
  if( clsUserInfo == None ):
    # IP-PBX 에서 수신한 BYE 메시지를 정상적으로 처리하기 위한 기능
    if( clsMessage.IsMethod( "BYE" ) ):
      strCallId = clsMessage.GetCallId()
      if( self.clsCallMap.Select( strCallId ) ):
        Log.Print( LogLevel.DEBUG, "EventIncomingRequestAuth BYE CallId(" + strCallId + ") is found" )
        return True
    
    bRes, strDestId = self.clsSipServerMap.SelectIncomingRoute( strIp, clsMessage.clsTo.clsUri.strUser )
    if( bRes ):
      Log.Print( LogLevel.DEBUG, "EventIncomingRequestAuth ip(" + strIp + ") user(" + clsMessage.clsTo.clsUri.strUser + ") IP-PBX dest_user(" + strDestId + ")" )
      return True
    
    if( self.CheckAuthrization( clsMessage ) == False ):
      return False
    
    clsUserInfo = self.clsUserMap.Select( clsMessage.clsFrom.clsUri.strUser )
    if( clsUserInfo == None ):
      return False
    
  if( strIp != clsUserInfo.strIp or iPort != clsUserInfo.iPort ):
    if( self.CheckAuthrization( clsMessage ) == False ):
      return False
    
    self.clsUserMap.SetIpPort( clsMessage.clsFrom.clsUri.strUser, strIp, iPort )
  
  return True

def EventIncomingCall( self, strCallId, strFrom, strTo, clsRtp ):
  Log.Print( LogLevel.DEBUG, "EventIncomingCall(" + strCallId + "," + strFrom + "," + strTo + ")" )

  bRoutePrefix = False

  if( len(strTo) == 0 ):
    return self.StopCall( strCallId, SipStatusCode.SIP_DECLINE )
  
  clsXmlUser = SelectUser( strTo, self.clsSetupFile.strUserXmlFolder )
  if( clsXmlUser == None ):
    # 로그인 대상 사용자가 아니면 연동할 IP-PBX 가 존재하는지 검사한다.
    bRes, clsXmlSipServer, strResTo = self.clsSipServerMap.SelectRoutePrefix( strTo )
    if( bRes ):
      clsXmlUser = XmlUser()
      clsXmlUser.strId = clsXmlSipServer.strUserId
      clsXmlUser.strPassWord = clsXmlSipServer.strPassWord

      clsUserInfo = UserInfo()
      clsUserInfo.strIp = clsXmlSipServer.strIp
      clsUserInfo.iPort = clsXmlSipServer.iPort
      clsUserInfo.eTransport = SipTransport.UDP

      strFrom = clsXmlUser.strId
      strTo = strResTo

      bRoutePrefix = True
      Log.Print( LogLevel.DEBUG, "EventIncomingCall routePrefix IP-PBX(" + clsUserInfo.strIp + ":" + str(clsUserInfo.iPort) + ")" )
    else:
      bRes, strResTo = self.clsSipServerMap.SelectIncomingRoute( "", strTo )
      if( bRes ):
        clsXmlUser = SelectUser( strResTo, self.clsSetupFile.strUserXmlFolder )
        if( clsXmlUser == None ):
          Log.Print( LogLevel.DEBUG, "EventIncomingCall to(" + strTo + ") is not found - dest to(" + strResTo + ")" )
          return self.StopCall( strCallId, SipStatusCode.SIP_NOT_FOUND )
      elif( self.clsSetupFile.IsCallPickupId( strTo ) ):
        return self.PickUp( strCallId, strFrom, strTo, clsRtp )
      else:
        Log.Print( LogLevel.DEBUG, "EventIncomingCall to(" + strTo + ") is not found in XML or DB" )
        return self.StopCall( strCallId, SipStatusCode.SIP_NOT_FOUND )

  if( clsXmlUser.bDnd ):
    # 사용자가 DND 로 설정되어 있으면 통화 요청을 거절한다.
    Log.Print( LogLevel.DEBUG, "EventIncomingCall to(" + strTo + ") is DND" )
    return self.StopCall( strCallId, SipStatusCode.SIP_DECLINE )

  if( len(clsXmlUser.strCallForward) > 0 ):
    Log.Print( LogLevel.DEBUG, "EventIncomingCall to(" + strTo + ") is CallForward(" + clsXmlUser.strCallForward + ")" )

    # 사용자가 착신전환 설정되어 있으면 착신전환 처리한다.
    clsInvite = self.clsUserAgent.DeleteIncomingCall( strCallId )
    if( clsInvite != None ):
      clsResponse = clsInvite.CreateResponseWithToTag( SipStatusCode.SIP_MOVED_TEMPORARILY )

      clsContact = SipFrom()
      clsContact.clsUri.strProtocol = "sip"
      clsContact.clsUri.strUser = clsXmlUser.strCallForward
      clsContact.clsUri.strHost = self.clsSetupFile.strLocalIp
      clsContact.clsUri.iPort = self.clsSetupFile.iUdpPort

      clsResponse.clsContactList.append( clsContact )

      self.clsUserAgent.clsSipStack.SendSipMessage( clsResponse )
      return
    else:
      Log.Print( LogLevel.DEBUG, "EventIncomingCall(" + strCallId + ") INVITE it not found" )
    
    return self.StopCall( strCallId, SipStatusCode.SIP_MOVED_TEMPORARILY )

  if( bRoutePrefix == False ):
    clsUserInfo = self.clsUserMap.Select( strTo )
    if( clsUserInfo == None ):
      Log.Print( LogLevel.DEBUG, "EventIncomingCall(" + strCallId + ") to(" + strTo + ") is not found" )
      return self.StopCall( strCallId, SipStatusCode.SIP_NOT_FOUND )
  
  clsRoute = clsUserInfo.GetCallRoute()
  #clsRoute.b100rel = self.clsUserAgent.Is100rel( strCallId )

  strNewCallId = self.clsUserAgent.CreateCall( strFrom, strTo, clsRtp, clsRoute )
  if( len(strNewCallId) == 0 ):
    Log.Print( LogLevel.DEBUG, "EventIncomingCall(" + strCallId + ") CreateCall errr" )
    return self.StopCall( strCallId, SipStatusCode.SIP_INTERNAL_SERVER_ERROR )
  
  self.clsCallMap.Insert( strCallId, strNewCallId )

  if( self.clsUserAgent.StartCreatedCall( strNewCallId) == False ):
    self.clsCallMap.Delete( strCallId )
    Log.Print( LogLevel.DEBUG, "EventIncomingCall(" + strCallId + ") StartCreatedCall errr" )
    return self.StopCall( strCallId, SipStatusCode.SIP_INTERNAL_SERVER_ERROR )

def EventCallRing( self, strCallId, iSipStatus, clsRtp ):
  Log.Print( LogLevel.DEBUG, "EventCallRing(" + strCallId + "," + str(iSipStatus) + ")" )

  clsCallInfo = self.clsCallMap.SelectCallInfo( strCallId )
  if( clsCallInfo != None ):
    if( iSipStatus == SipStatusCode.SIP_SESSION_PROGRESS ):
      iRSeq = self.clsUserAgent.GetRSeq( strCallId )
      if( iRSeq != -1 ):
        self.clsUserAgent.SetRSeq( clsCallInfo.strPeerCallId, iRSeq )
      
      self.clsUserAgent.RingCall( clsCallInfo.strPeerCallId, clsRtp )
  else:
    clsCallInfo = self.clsTransCallMap.SelectCallInfo( strCallId )
    if( clsCallInfo != None ):
      self.clsUserAgent.SendNotify( clsCallInfo.strPeerCallId, iSipStatus )

def EventCallStart( self, strCallId, clsRtp ):
  Log.Print( LogLevel.DEBUG, "EventCallStart(" + strCallId + ")" )

  clsCallInfo = self.clsCallMap.SelectCallInfo( strCallId )
  if( clsCallInfo != None ):
    if( self.clsUserAgent.IsConnected( clsCallInfo.strPeerCallId ) ):
      self.clsUserAgent.SendReInvite( clsCallInfo.strPeerCallId, clsRtp )
    else:
      self.clsUserAgent.AcceptCall( clsCallInfo.strPeerCallId, clsRtp )
  else:
    clsCallInfo = self.clsTransCallMap.SelectCallInfo( strCallId )
    if( clsCallInfo != None ):
      self.clsUserAgent.SendNotify( clsCallInfo.strPeerCallId, SipStatusCode.SIP_OK )

      strReferToCallId = self.clsCallMap.SelectCallId( clsCallInfo.strPeerCallId )
      if( len(strReferToCallId) > 0 ):
        self.clsUserAgent.StopCall( clsCallInfo.strPeerCallId, 0 )
        self.clsCallMap.Delete( clsCallInfo.strPeerCallId )
      
      self.clsUserAgent.SendReInvite( strReferToCallId, clsRtp )
      self.clsCallMap.Insert( strReferToCallId, strCallId )
      self.clsTransCallMap.Delete( strCallId )
    else:
      self.clsUserAgent.StopCall( strCallId, 0 )
  
def EventCallEnd( self, strCallId, iSipStatus ):
  Log.Print( LogLevel.DEBUG, "EventCallEnd(" + strCallId + "," + str(iSipStatus) + ")" )
  
  clsCallInfo = self.clsCallMap.SelectCallInfo( strCallId )
  if( clsCallInfo != None ):
    self.clsUserAgent.StopCall( clsCallInfo.strPeerCallId, 0 )
    self.clsCallMap.Delete( strCallId )
  else:
    clsCallInfo = self.clsTransCallMap.SelectCallInfo( strCallId )
    if( clsCallInfo != None ):
      self.clsUserAgent.SendNotify( clsCallInfo.strPeerCallId, iSipStatus )
      self.clsTransCallMap.Delete( strCallId )

def EventReInvite( self, strCallId, clsRemoteRtp, clsLocalRtp ):
  Log.Print( LogLevel.DEBUG, "EventReInvite(" + strCallId + ")" )

  clsCallInfo = self.clsCallMap.SelectCallInfo( strCallId )
  if( clsCallInfo != None ):
    self.clsUserAgent.SendReInvite( clsCallInfo.strPeerCallId, clsRemoteRtp )

def EventPrack( self, strCallId, clsRtp ):
  Log.Print( LogLevel.DEBUG, "EventPrack(" + strCallId + ")" )
  
  clsCallInfo = self.clsCallMap.SelectCallInfo( strCallId )
  if( clsCallInfo != None ):
    self.clsUserAgent.SendPrack( clsCallInfo.strPeerCallId, clsRtp )
  
def EventTransfer( self, strCallId, strReferToCallId, bScreenedTransfer ):
  Log.Print( LogLevel.DEBUG, "EventTransfer(" + strCallId + "," + strReferToCallId + "," + str(bScreenedTransfer) + ")" )

  clsCallInfo = self.clsCallMap.SelectCallInfo( strCallId )
  if( clsCallInfo == None ):
    return False
  
  clsReferToCallInfo = self.clsCallMap.SelectCallInfo( strReferToCallId )
  if( clsReferToCallInfo == None ):
    return False
  
  self.clsCallMap.Delete( strCallId )
  self.clsCallMap.Delete( strReferToCallId )

  clsRtp = self.clsUserAgent.GetRemoteCallRtp( clsCallInfo.strPeerCallId )
  if( clsRtp == None ):
    return False
  clsRtp.eDirection = RtpDirection.SEND_RECV

  if( bScreenedTransfer ):
    clsReferToRtp = self.clsUserAgent.GetRemoteCallRtp( clsReferToCallInfo.strPeerCallId )
    if( clsReferToRtp == None ):
      return False
    clsReferToRtp.eDirection = RtpDirection.SEND_RECV

    self.clsCallMap.Insert( clsCallInfo.strPeerCallId, clsReferToCallInfo.strPeerCallId )
    self.clsUserAgent.SendReInvite( clsCallInfo.strPeerCallId, clsReferToRtp )
    self.clsUserAgent.SendReInvite( clsReferToCallInfo.strPeerCallId, clsRtp )
  
  self.clsUserAgent.StopCall( strCallId, 0 )
  self.clsUserAgent.StopCall( strReferToCallId, SipStatusCode.SIP_REQUEST_TERMINATED )

  if( bScreenedTransfer == False ):
    strFromId = self.clsUserAgent.GetToId( clsCallInfo.strPeerCallId )
    strToId = self.clsUserAgent.GetToId( clsReferToCallInfo.strPeerCallId )

    clsUserInfo = self.clsUserMap.Select( strToId )
    if( clsUserInfo != None ):
      clsRoute = clsUserInfo.GetCallRoute()

      self.clsUserAgent.StopCall( clsReferToCallInfo.strPeerCallId, 0 )
      strNewCallId = self.clsUserAgent.StartCall( strFromId, strToId, clsRtp, clsRoute )

      self.clsCallMap.Insert( strNewCallId, clsCallInfo.strPeerCallId )
    else:
      self.clsUserAgent.StopCall( clsCallInfo.strPeerCallId, 0 )
      self.clsUserAgent.StopCall( clsReferToCallInfo.strPeerCallId, 0 )
  
  return True


def EventBlindTransfer( self, strCallId, strReferToId ):
  Log.Print( LogLevel.DEBUG, "EventBlindTransfer(" + strCallId + "," + strReferToId + ")" )

  strPeerCallId = self.clsCallMap.SelectCallId( strCallId )
  if( len(strPeerCallId) == 0 ):
    return False
  
  strToId = self.clsUserAgent.GetToId( strPeerCallId )
  if( len(strToId) == 0 ):
    return False
  
  clsUserInfo = self.clsUserMap.Select( strReferToId )
  if( clsUserInfo == None ):
    return False
  
  clsRtp = self.clsUserAgent.GetRemoteCallRtp( strPeerCallId )
  if( clsRtp == None ):
    return False
  clsRtp.eDirection = RtpDirection.SEND_RECV

  clsRoute = clsUserInfo.GetCallRoute()
  strNewCallId = self.clsUserAgent.StartCall( strToId, strReferToId, clsRtp, clsRoute )
  if( len(strNewCallId) == 0 ):
    return False
  
  self.clsTransCallMap.Insert( strCallId, strNewCallId )

  return True

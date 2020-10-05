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
from ..SipParser.SipUtility import SipMakeTag
from .SipDialog import SipDialog
  
def RecvInviteRequest( self, clsMessage ):
  strCallId = clsMessage.GetCallId()
  if( len(strCallId) == 0 ):
    self.clsSipStack.SendSipMessage( clsMessage.CreateResponse( SipStatusCode.SIP_BAD_REQUEST, '' ) )
    return True
  
  clsRtp = self.GetSipCallRtp( clsMessage )
  if( clsRtp == None ):
    self.clsSipStack.SendSipMessage( clsMessage.CreateResponse( SipStatusCode.SIP_NOT_ACCEPTABLE_HERE, '' ) )
    return True
  
  clsResponse = None
  
  # ReINVITE 인지 검사한다.
  bReINVITE = False
  self.clsDialogMutex.acquire()
  clsDialog = self.clsDialogMap.get(strCallId)
  if( clsDialog != None ):
    bReINVITE = True
    clsDialog.SetRemoteRtp( clsRtp )
    clsLocalRtp = clsDialog.SelectLocalRtp( )
  self.clsDialogMutex.release()

  if( bReINVITE ):
    self.clsCallBack.EventReInvite( strCallId, clsRtp, clsLocalRtp )
  
    self.clsDialogMutex.acquire()
    clsDialog = self.clsDialogMap.get(strCallId)
    if( clsDialog != None ):
      clsDialog.SetLocalRtp( clsRtp )
      clsResponse = clsMessage.CreateResponse( SipStatusCode.SIP_OK, '' )
      clsResponse = clsDialog.AddSdp( clsResponse )
    self.clsDialogMutex.release()

    if( clsResponse != None ):
      self.clsSipStack.SendSipMessage( clsResponse )

  # 새로운 INVITE 인 경우
  strTag = SipMakeTag( )

  if( self.clsCallBack.EventIncomingRequestAuth( clsMessage ) == False ):
    return True

  # 180 Ring 을 전송한다.
  clsResponse = clsMessage.CreateResponse( SipStatusCode.SIP_RINGING, strTag )
  self.clsSipStack.SendSipMessage( clsResponse )

  # Dialog 를 생성한다.
  clsDialog = SipDialog( self.clsSipStack )

  clsDialog.strFromId = clsMessage.clsTo.clsUri.strUser
  clsDialog.strFromTag = strTag
  clsDialog.eTransport = clsMessage.eTransport

  clsDialog.strToId = clsMessage.clsFrom.clsUri.strUser
  clsDialog.strToTag = clsMessage.clsFrom.SelectParam( "tag" )

  clsDialog.strCallId = strCallId
  clsDialog.SetRemoteRtp( clsRtp )

  clsDialog.strContactIp, clsDialog.iContactPort = clsMessage.GetTopViaIpPort()

  if( len(clsMessage.clsContactList) > 0 ):
    clsDialog.strContactUri = str(clsMessage.clsContactList[0])
  
  clsDialog.iInviteTime = time.time()
  clsDialog.clsInviteRecv = clsMessage
  clsDialog.clsInviteRecv.clsTo.InsertParam( "tag", strTag )

  if( len(clsDialog.clsInviteRecv.clsRecordRouteList) > 0 ):
    clsDialog.clsRouteList = clsDialog.clsInviteRecv.clsRecordRouteList
  
  clsDialog.bSendCall = False

  # Dialog 를 저장한다.
  bError = False

  self.clsDialogMutex.acquire()
  if( self.clsDialogMap.get(strCallId) == None ):
    self.clsDialogMap[strCallId] = clsDialog
  else:
    bError = True
  self.clsDialogMutex.release()

  if( bError == False ):
    self.clsCallBack.EventIncomingCall( strCallId, clsMessage.clsFrom.clsUri.strUser, clsMessage.clsTo.clsUri.strUser, clsRtp )

  return True

def RecvInviteResponse( self, clsMessage ):
  if( clsMessage.iStatusCode == SipStatusCode.SIP_TRYING ):
    return True
  
  strCallId = clsMessage.GetCallId()
  clsRtp = self.GetSipCallRtp( clsMessage )
  bFound = False
  bReInvite = False
  bStopCall = False
  clsInvite = None
  clsAck = None

  self.clsDialogMutex.acquire()
  clsDialog = self.clsDialogMap.get(strCallId)
  if( clsDialog != None ):
    clsDialog.strToTag = clsMessage.clsTo.SelectParam( "tag" )
    if( clsRtp != None ):
      clsDialog.SetRemoteRtp( clsRtp )
    
    if( clsMessage.iStatusCode == SipStatusCode.SIP_SESSION_PROGRESS or clsMessage.iStatusCode == SipStatusCode.SIP_RINGING ):
      clsHeader = clsMessage.GetHeader( "RSeq" )
      if( clsHeader != None and len(clsHeader.strValue) > 0 ):
        clsDialog.iRSeq = int(clsHeader.strValue)
    
    if( clsMessage.iStatusCode >= SipStatusCode.SIP_OK ):
      if( clsMessage.iStatusCode != SipStatusCode.SIP_CONNECT_ERROR ):
        clsAck = clsDialog.CreateAck( clsMessage.iStatusCode )
      
      if( clsMessage.iStatusCode < SipStatusCode.SIP_MULTIPLE_CHOICES ):
        bCreateAck = False

        if( len(clsMessage.clsRecordRouteList) > 0 ):
          clsDialog.clsRouteList.clear()

          for clsFrom in clsMessage.clsRecordRouteList:
            clsDialog.clsRouteList.insert( 0 )
          
          bCreateAck = True
        
        if( len(clsMessage.clsContactList) > 0 ):
          clsDialog.strContactUri = str(clsMessage.clsContactList[0])
          bCreateAck = True
        
        if( bCreateAck ):
          clsAck = clsDialog.CreateAck( clsMessage.iStatusCode )
        
        if( clsDialog.iStartTime == 0.0 ):
          clsDialog.iStartTime = time.time()
        else:
          bReInvite = True

        if( clsDialog.iCancelTime != 0.0 ):
          bStopCall = True
      
      elif( clsMessage.iStatusCode == SipStatusCode.SIP_UNAUTHORIZED or clsMessage.iStatusCode == SipStatusCode.SIP_PROXY_AUTHENTICATION_REQUIRED ):
        if( clsDialog.iCancelTime == 0.0 ):
          clsDialog.strToTag = ''

          clsInvite = clsDialog.CreateInvite( )
          strUserId = clsMessage.clsFrom.clsUri.strUser

          self.clsRegisterMutex.acquire()
          for clsServerInfo in self.clsRegisterList:
            if( clsServerInfo.strUserId == strUserId ):
              clsServerInfo.AddAuth( clsInvite, clsMessage )
              break
          self.clsRegisterMutex.release()

      else:
        if( clsDialog.iStartTime == 0.0 ):
          clsDialog.iEndTime = time.time()

          if( clsMessage.iStatusCode == SipStatusCode.SIP_MOVED_TEMPORARILY ):
            if( clsDialog.iCancelTime == 0.0 ):
              if( len(clsMessage.clsContactList) > 0 ):
                clsDialog.strToId = clsMessage.clsContactList[0].clsUri.strUser
                clsInvite = clsDialog.CreateInvite()
                clsInvite.clsReqUri = clsMessage.clsContactList[0].clsUri
        else:
          bReInvite = True    

    bFound = True
  self.clsDialogMutex.release()

  if( clsAck != None ):
    self.clsSipStack.SendSipMessage( clsAck )
  
  if( clsInvite != None ):
    self.clsSipStack.SendSipMessage( clsInvite )
    # 인증 정보를 포함한 INVITE 메시지를 전송한 경우, 응용으로 callback 호출하지 않는다.
    bFound = False
  
  if( bStopCall ):
    # CANCEL 전송 후, INVITE 200 OK 수신하였으면 BYE 를 전송한다.
    self.StopCall( strCallId )
    bFound = False
  
  if( bFound ):
    if( bReInvite ):
      self.clsCallBack.EventReInviteResponse( strCallId, clsMessage.iStatusCode, clsRtp )
    else:
      if( clsMessage.iStatusCode > SipStatusCode.SIP_TRYING and clsMessage.iStatusCode < SipStatusCode.SIP_OK ):
        self.clsCallBack.EventCallRing( strCallId, clsMessage.iStatusCode, clsRtp )
      elif( clsMessage.iStatusCode >= SipStatusCode.SIP_OK and clsMessage.iStatusCode < SipStatusCode.SIP_MULTIPLE_CHOICES ):
        self.clsCallBack.EventCallStart( strCallId, clsRtp )
      else:
        self.clsCallBack.EventCallEnd( strCallId, clsMessage.iStatusCode )
        self.Delete( strCallId )

  return True

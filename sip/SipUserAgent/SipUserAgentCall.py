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

import copy
import time
import random
from ..SipPlatform.Log import Log, LogLevel
from ..SipParser.SipUtility import SipMakeTag, SipMakeBranch, SipMakeCallIdName
from ..SipParser.SipStatusCode import SipStatusCode
from ..SipParser.SipFrom import SipFrom
from ..SipStack.SipStack import SipStack
from .SipDialog import SipDialog
from .RtpDirection import RtpDirection

def StartCall( self, strFrom, strTo, clsRtp, clsRoute ):
  """ 통화 요청을 전송한다. SIP INVITE 메시지를 전송한다.

  Args:
      strFrom (string): 발신자 전화번호
      strTo (string): 수신자 전화번호
      clsRtp (SipCallRtp): 로컬 RTP 정보 저장 객체
      clsRoute (SipCallRoute): 수신자 통신 정보 저장 객체

  Returns:
      string: 성공하면 SIP Call-ID 문자열을 리턴하고 그렇지 않으면 공백 문자열을 리턴한다.
  """
  if( len(strFrom) == 0 or len(strTo) == 0 ):
    return ''
  
  if( len(clsRoute.strDestIp) == 0 or clsRoute.iDestPort <= 0 or clsRoute.iDestPort > 65535 ):
    return ''
  
  clsDialog = SipDialog( self.clsSipStack )

  clsDialog.strFromId = strFrom
  clsDialog.strToId = strTo

  clsDialog.SetLocalRtp( clsRtp )

  clsDialog.strContactIp = clsRoute.strDestIp
  clsDialog.iContactPort = clsRoute.iDestPort
  clsDialog.eTransport = clsRoute.eTransport
  clsDialog.b100rel = clsRoute.b100rel

  clsDialog.strFromTag = SipMakeTag()
  clsDialog.strViaBranch = SipMakeBranch()
  clsDialog.iInviteTime = time.time()

  bInsert = False

  while bInsert == False:
    clsDialog.strCallId = SipMakeCallIdName() + "@" + self.clsSipStack.clsSetup.strLocalIp

    self.clsDialogMutex.acquire()
    if( self.clsDialogMap.get( clsDialog.strCallId ) == None ):
      clsMessage = clsDialog.CreateInvite()
      self.clsDialogMap[clsDialog.strCallId] = clsDialog
      bInsert = True
    self.clsDialogMutex.release()
  
  if( clsMessage ):
    self.clsSipStack.SendSipMessage( clsMessage )
  
  return clsDialog.strCallId

def StopCall( self, strCallId, iSipCode ):
  """ 통화 요청을 중지시키거나 연결된 통화를 종료시킨다.

  Args:
      strCallId (string): SIP Call-ID 문자열
      iSipCode (int): 응답 SIP 코드
  """
  clsMessage = None

  self.clsDialogMutex.acquire()
  clsDialog = self.clsDialogMap.get( strCallId )
  if( clsDialog != None ):
    if( clsDialog.iStartTime != 0.0 ):
      if( clsDialog.iEndTime == 0.0 ):
        clsMessage = clsDialog.CreateBye()
        del self.clsDialogMap[strCallId]
    else:
      if( clsDialog.clsInviteRecv != None ):
        if( iSipCode > 0 ):
          clsMessage = clsDialog.clsInviteRecv.CreateResponse( iSipCode, '' )
        else:
          clsMessage = clsDialog.clsInviteRecv.CreateResponse( SipStatusCode.SIP_DECLINE, '' )
        del self.clsDialogMap[strCallId]
      elif( clsDialog.iCancelTime == 0.0 and clsDialog.iEndTime == 0.0 ):
        clsMessage = clsDialog.CreateCancel()
        clsDialog.iCancelTime = time.time()
  self.clsDialogMutex.release()

  if( clsMessage != None ):
    self.clsSipStack.SendSipMessage( clsMessage )

def StopCallForward( self, strCallId, strForward ):
  """ 수신한 통화 요청을 종료시키면서 착신전환 전화번호를 알려 준다.

  Args:
      strCallId (string): SIP Call-ID 문자열
      strForward (string): 착신전환 전화번호
  """
  clsMessage = None

  self.clsDialogMutex.acquire()
  clsDialog = self.clsDialogMap.get( strCallId )
  if( clsDialog != None ):
    if( clsDialog.iStartTime == 0.0 and clsDialog.clsInviteRecv != None ):
      clsMessage = clsDialog.clsInviteRecv.CreateResponse( SipStatusCode.SIP_MOVED_TEMPORARILY, '' )
  self.clsDialogMutex.release()

  if( clsMessage != None ):
    clsContact = copy(clsMessage.clsFrom)
    clsContact.clsUri.strUser = strForward
    clsMessage.clsContactList.append( clsContact )

    self.clsSipStack.SendSipMessage( clsMessage )
  
def RingCall( self, strCallId, clsRtp ):
  """ 183 응답 메시지를 전송한다.

  Args:
      strCallId (string): SIP Call-ID 문자열
      clsRtp (SipCallRtp): 로컬 RTP 정보 저장 객체
  """
  clsMessage = None

  self.clsDialogMutex.acquire()
  clsDialog = self.clsDialogMap.get( strCallId )
  if( clsDialog != None ):
    if( clsDialog.iStartTime == 0.0 and clsDialog.clsInviteRecv != None ):
      clsDialog.SetLocalRtp( clsRtp )
      clsMessage = clsDialog.clsInviteRecv.CreateResponse( SipStatusCode.SIP_SESSION_PROGRESS, '' )
      if( clsDialog.clsInviteRecv.Is100rel() ):
        iRSeq = clsDialog.clsInviteRecv.clsCSeq.iDigit + random.randint( 1, 1000000000 )
        clsMessage.AddHeader( "RSeq", str(iRSeq) )
      clsMessage = clsDialog.AddSdp( clsMessage )
  self.clsDialogMutex.release()

  if( clsMessage != None ):
    self.clsSipStack.SendSipMessage( clsMessage )

def RingCallStatus( self, strCallId, iSipStatus, clsRtp ):
  """ 수신된 통화에 대한 ring 응답 메시지를 전송한다.

  Args:
      strCallId (string): SIP Call-ID 문자열
      iSipStatus (int): 응답 SIP 코드
      clsRtp (SipCallRtp): 로컬 RTP 정보 저장 객체
  """
  clsMessage = None

  self.clsDialogMutex.acquire()
  clsDialog = self.clsDialogMap.get( strCallId )
  if( clsDialog != None ):
    if( clsDialog.iStartTime == 0.0 and clsDialog.clsInviteRecv != None ):
      
      clsMessage = clsDialog.clsInviteRecv.CreateResponse( iSipStatus, '' )

      if( clsRtp != None ):
        clsDialog.SetLocalRtp( clsRtp )
        clsMessage = clsDialog.AddSdp( clsMessage )

      if( clsDialog.iRSeq != -1 ):
        clsMessage.AddHeader( "Allow", "PRACK, INVITE, ACK, BYE, CANCEL, REFER, NOTIFY, MESSAGE" )
        clsMessage.AddHeader( "Require", "100rel" )
        clsMessage.AddHeader( "RSeq", str(clsDialog.iRSeq) )
      
  self.clsDialogMutex.release()

  if( clsMessage != None ):
    self.clsSipStack.SendSipMessage( clsMessage )

def AcceptCall( self, strCallId, clsRtp ):
  """ 수신된 통화를 연결시킨다.

  Args:
      strCallId (string): SIP Call-ID 문자열
      clsRtp (SipCallRtp): 로컬 RTP 정보 저장 객체

  Returns:
      bool: 성공하면 True 를 리턴하고 그렇지 않으면 False 를 리턴한다.
  """
  clsMessage = None

  self.clsDialogMutex.acquire()
  clsDialog = self.clsDialogMap.get( strCallId )
  if( clsDialog != None ):
    if( clsDialog.iStartTime == 0.0 and clsDialog.clsInviteRecv != None ):
      clsDialog.SetLocalRtp( clsRtp )
      clsMessage = clsDialog.clsInviteRecv.CreateResponse( SipStatusCode.SIP_OK, '' )
      clsDialog.iStartTime = time.time()
      clsDialog.clsInviteRecv = None
      clsMessage = clsDialog.AddSdp( clsMessage )
  self.clsDialogMutex.release()

  if( clsMessage != None ):
    self.clsSipStack.SendSipMessage( clsMessage )
    return True
  
  return False

def HoldCall( self, strCallId, eDirection ):
  """ 통화를 hold 시킨다.

  Args:
      strCallId (string): SIP Call-ID 문자열
      eDirection (int): RtpDirection 숫자
  """
  clsMessage = None

  self.clsDialogMutex.acquire()
  clsDialog = self.clsDialogMap.get( strCallId )
  if( clsDialog != None ):
    clsDialog.eLocalDirection = eDirection
    clsMessage = clsDialog.CreateInvite()
  self.clsDialogMutex.release()

  if( clsMessage != None ):
    self.clsSipStack.SendSipMessage( clsMessage )

def ResumeCall( self, strCallId ):
  """ 통화를 resume 시킨다.

  Args:
      strCallId (string): SIP Call-ID 문자열
  """
  clsMessage = None

  self.clsDialogMutex.acquire()
  clsDialog = self.clsDialogMap.get( strCallId )
  if( clsDialog != None ):
    clsDialog.eLocalDirection = RtpDirection.SEND_RECV
    clsMessage = clsDialog.CreateInvite()
  self.clsDialogMutex.release()

  if( clsMessage != None ):
    self.clsSipStack.SendSipMessage( clsMessage )

def GetCallCount( self ):
  """ 통화 개수를 리턴한다.

  Returns:
      int: 통화 개수를 리턴한다.
  """
  self.clsDialogMutex.acquire()
  iCount = len(self.clsDialogMap)
  self.clsDialogMutex.release()

  return iCount

def GetCallIdList( self ):
  """ 모든 통화 SIP Call-ID 리스트를 리턴한다.

  Returns:
      list: 모든 통화 SIP Call-ID 리스트를 리턴한다.
  """
  clsCallIdList = []

  self.clsDialogMutex.acquire()
  for strCallId in self.clsDialogMap.keys():
    clsCallIdList.append( strCallId )
  self.clsDialogMutex.release()

  return clsCallIdList

def StopCallAll( self ):
  """ 모든 통화를 종료시킨다.
  """
  clsCallIdList = self.GetCallIdList()

  for strCallId in clsCallIdList:
    self.StopCall( strCallId, 0 )

def CreateCall( self, strFrom, strTo, clsRtp, clsRoute ):
  """ 통화 요청을 위한 다이얼로그를 생성하고 SIP INVITE 메시지를 생성한다.
      본 메소드를 호출하면 다이얼로그 및 SIP INVITE 메시지만 생성되지 SIP INVITE 메시지는 전송되지 않는다.
      본 메소드를 호출한 후, StartCreatedCall() 메소드를 호출해야 SIP INVITE 메시지가 전송된다.

  Args:
      strFrom (string): 발신자 전화번호
      strTo (string): 수신자 전화번호
      clsRtp (SipCallRtp): 로컬 RTP 정보 저장 객체
      clsRoute (SipCallRoute): 수신자 통신 정보 저장 객체

  Returns:
      string: 성공하면 SIP Call-ID 문자열을 리턴하고 그렇지 않으면 공백 문자열을 리턴한다.
  """
  if( len(strFrom) == 0 or len(strTo) == 0 ):
    return ''
  
  if( len(clsRoute.strDestIp) == 0 or clsRoute.iDestPort <= 0 or clsRoute.iDestPort > 65535 ):
    return ''
  
  clsDialog = SipDialog( self.clsSipStack )

  clsDialog.strFromId = strFrom
  clsDialog.strToId = strTo

  clsDialog.SetLocalRtp( clsRtp )

  clsDialog.strContactIp = clsRoute.strDestIp
  clsDialog.iContactPort = clsRoute.iDestPort
  clsDialog.eTransport = clsRoute.eTransport
  clsDialog.b100rel = clsRoute.b100rel

  clsDialog.strFromTag = SipMakeTag()
  clsDialog.strViaBranch = SipMakeBranch()
  clsDialog.iInviteTime = time.time()

  bInsert = False

  while bInsert == False:
    clsDialog.strCallId = SipMakeCallIdName() + "@" + self.clsSipStack.clsSetup.strLocalIp

    self.clsDialogMutex.acquire()
    if( self.clsDialogMap.get( clsDialog.strCallId ) == None ):
      clsDialog.clsInviteSend = clsDialog.CreateInvite()
      self.clsDialogMap[clsDialog.strCallId] = clsDialog
      bInsert = True
    self.clsDialogMutex.release()
  
  return clsDialog.strCallId

def StartCreatedCall( self, strCallId ):
  """ CreateCall() 메소드로 생성된 SIP INVITE 메시지로 통화 요청한다.

  Args:
      strCallId (string): SIP Call-ID 문자열

  Returns:
      bool: 성공하면 True 를 리턴하고 그렇지 않으면 False 를 리턴한다.
  """
  clsMessage = None

  self.clsDialogMutex.acquire()
  clsDialog = self.clsDialogMap.get( strCallId )
  if( clsDialog != None and clsDialog.clsInviteSend != None ):
    clsMessage = clsDialog.clsInviteSend
    clsDialog.clsInviteSend = None
  self.clsDialogMutex.release()

  if( clsMessage ):
    return self.clsSipStack.SendSipMessage( clsMessage )
  
  return False

def TransferCallBlind( self, strCallId, strTo ):
  """ 통화를 전달한다. ( blind transfer )

  Args:
      strCallId (string): SIP Call-ID 문자열
      strTo (string): 통화를 전달받을 전화번호
  """
  clsMessage = None

  self.clsDialogMutex.acquire()
  clsDialog = self.clsDialogMap.get( strCallId )
  if( clsDialog != None ):
    clsMessage = clsDialog.CreateRefer()
    strReferTo = "<sip:" + strTo + "@" + clsDialog.strContactIp + ":" + clsDialog.iContactPort + ">"
    strReferBy = "<sip:" + clsDialog.strFromId + "@" + self.clsSipStack.clsSetup.strLocalIp + ":" + self.clsSipStack.clsSetup.iLocalUdpPort
  self.clsDialogMutex.release()

  if( clsMessage ):
    clsMessage.AddHeader( "Refer-To", strReferTo )
    clsMessage.AddHeader( "Referred-By", strReferBy )
    self.clsSipStack.SendSipMessage( clsMessage )

def TransferCall( self, strCallId, strToCallId ):
  """ 통화를 전달한다. ( screened, unscreened transfer )

  Args:
      strCallId (string): 현재 통화에 대한 SIP Call-ID 문자열
      strToCallId (string): 전달할 통화에 대한 SIP Call-ID 문자열
  """
  clsMessage = None

  self.clsDialogMutex.acquire()
  clsDialog = self.clsDialogMap.get( strToCallId )
  if( clsDialog != None ):
    strReplaces = strToCallId.replace( "@", "%40" ) + "%3B" + "to-tag%3D" + clsDialog.strToTag + "%3B" + "from-tag%3D" + clsDialog.strFromTag
    strReferTo = "<sip:" + clsDialog.strToId + "@" + clsDialog.strContactIp + ":" + clsDialog.iContactPort + "?Replaces=" + strReplaces + ">"
    strReferBy = "<sip:" + clsDialog.strFromId + "@" + self.clsSipStack.clsSetup.strLocalIp + ":" + self.clsSipStack.clsSetup.iLocalUdpPort

    clsDialog = self.clsDialogMap.get( strCallId )
    if( clsDialog != None ):
      clsMessage = clsDialog.CreateRefer()
  self.clsDialogMutex.release()

  if( clsMessage ):
    clsMessage.AddHeader( "Refer-To", strReferTo )
    clsMessage.AddHeader( "Referred-By", strReferBy )
    self.clsSipStack.SendSipMessage( clsMessage )

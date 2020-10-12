
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

from .SipCallRoute import SipCallRoute
from .RtpDirection import RtpDirection

def GetRemoteCallRtp( self, strCallId ):
  """ 상대방 RTP 정보를 가져온다.

  Args:
      strCallId (string): SIP Call-ID 문자열

  Returns:
      SipCallRtp: 성공하면 상대방 RTP 정보를 저장한 객체를 리턴하고 그렇지 않으면 None 를 리턴한다.
  """
  clsRtp = None

  self.clsDialogMutex.acquire()
  clsDialog = self.clsDialogMap.get(strCallId)
  if( clsDialog != None ):
    clsRtp = clsDialog.SelectRemoteRtp( )
  self.clsDialogMutex.release()

  return clsRtp

def GetToId( self, strCallId ):
  """ TO 전화번호를 가져온다.

  Args:
      strCallId (string): SIP Call-ID 문자열

  Returns:
      string: 성공하면 TO 전화번호를 리턴하고 그렇지 않으면 공백 문자열을 리턴한다.
  """
  strToId = ''

  self.clsDialogMutex.acquire()
  clsDialog = self.clsDialogMap.get(strCallId)
  if( clsDialog != None ):
    strToId = clsDialog.strToId
  self.clsDialogMutex.release()

  return strToId

def GetFromId( self, strCallId ):
  """ From 전화번호를 가져온다.

  Args:
      strCallId (string): SIP Call-ID 문자열

  Returns:
      string: 성공하면 From 전화번호를 리턴하고 그렇지 않으면 공백 문자열을 리턴한다.
  """
  strFromId = ''

  self.clsDialogMutex.acquire()
  clsDialog = self.clsDialogMap.get(strCallId)
  if( clsDialog != None ):
    strFromId = clsDialog.strFromId
  self.clsDialogMutex.release()

  return strFromId

def GetContact( self, strCallId ):
  """ 상대방 통신 정보를 가져온다.

  Args:
      strCallId (string): SIP Call-ID 문자열

  Returns:
      SipCallRoute: 상대방 통신 정보를 저장하는 객체
  """
  clsRoute = None

  self.clsDialogMutex.acquire()
  clsDialog = self.clsDialogMap.get(strCallId)
  if( clsDialog != None ):
    clsRoute = SipCallRoute()
    clsRoute.strDestIp = clsDialog.strContactIp
    clsRoute.iDestPort = clsDialog.iContactPort
    clsRoute.eTransport = clsDialog.eTransport
  self.clsDialogMutex.release()

  return clsRoute

def GetInviteHeaderValue( self, strCallId, strName ):
  """ 수신된 SIP INVITE 메시지에서 입력된 헤더 이름에 대한 헤더 값을 가져온다.

  Args:
      strCallId (string): SIP Call-ID 문자열
      strName (string): 헤더 이름

  Returns:
      string: 성공하면 수신된 SIP INVITE 메시지에서 입력된 헤더 이름에 대한 헤더 값을 리턴하고 그렇지 않으면 공백 문자열을 리턴한다.
  """
  strValue = ''

  self.clsDialogMutex.acquire()
  clsDialog = self.clsDialogMap.get(strCallId)
  if( clsDialog != None ):
    if( clsDialog.clsInviteRecv != None ):
      clsHeader = clsDialog.clsInviteRecv.GetHeader( strName )
      if( clsHeader != None ):
        strValue = clsHeader.strValue
  self.clsDialogMutex.release()

  return strValue

def GetRSeq( self, strCallId ):
  """ RSeq 값을 리턴한다.

  Args:
      strCallId (string): SIP Call-ID 문자열

  Returns:
      int: 성공하면 다이얼로그의 RSeq 값을 리턴하고 그렇지 않으면 -1 를 리턴한다.
  """
  iRSeq = -1

  self.clsDialogMutex.acquire()
  clsDialog = self.clsDialogMap.get(strCallId)
  if( clsDialog != None ):
    iRSeq = clsDialog.iRSeq
  self.clsDialogMutex.release()

  return iRSeq

def SetRSeq( self, strCallId, iRSeq ):
  """ RSeq 값을 저장한다.

  Args:
      strCallId (string): SIP Call-ID 문자열
      iRSeq (int): RSeq 값
  """
  self.clsDialogMutex.acquire()
  clsDialog = self.clsDialogMap.get(strCallId)
  if( clsDialog != None ):
    clsDialog.iRSeq = iRSeq
  self.clsDialogMutex.release()

def IsRingCall( self, strCallId, strTo ):
  """ 통화 RING 중인지 검사한다.

  Args:
      strCallId (string): SIP Call-ID 문자열
      strTo (string): 수신자 전화번호

  Returns:
      bool: 통화 RING 중이면 True 를 리턴하고 그렇지 않으면 False 를 리턴한다.
  """
  bRes = False

  self.clsDialogMutex.acquire()
  clsDialog = self.clsDialogMap.get(strCallId)
  if( clsDialog != None ):
    if( clsDialog.IsConnected() == False ):
      if( len(strTo) > 0 ):
        if( clsDialog.strToId == strTo ):
          bRes = True
      else:
        bRes = True
  self.clsDialogMutex.release()

  return bRes

def Is100rel( self, strCallId ):
  """ 100rel 설정 여부를 확인한다.

  Args:
      strCallId (string): SIP Call-ID 문자열

  Returns:
      bool: 100rel 설정되어 있으면 True 를 리턴하고 그렇지 않으면 False 를 리턴한다.
  """
  b100rel = False

  self.clsDialogMutex.acquire()
  clsDialog = self.clsDialogMap.get(strCallId)
  if( clsDialog != None ):
    b100rel = clsDialog.b100rel
    if( b100rel == False and clsDialog.clsInviteRecv != None ):
      b100rel = clsDialog.clsInviteRecv.Is100rel()
  self.clsDialogMutex.release()

  return b100rel

def IsHold( self, strCallId ):
  """ 통화 hold 중인지 검사한다.

  Args:
      strCallId (string): SIP Call-ID 문자열

  Returns:
      bool: 통화 hold 중이면 True 를 리턴하고 그렇지 않으면 False 를 리턴한다.
  """
  bHold = False

  self.clsDialogMutex.acquire()
  clsDialog = self.clsDialogMap.get(strCallId)
  if( clsDialog != None ):
    if( clsDialog.eLocalDirection != RtpDirection.SEND_RECV ):
      bHold = True
  self.clsDialogMutex.release()

  return bHold

def IsConnected( self, strCallId ):
  """ 통화가 연결된 상태인지 검사한다.

  Args:
      strCallId (string): SIP Call-ID 문자열

  Returns:
      bool: 통화가 연결된 상태이면 True 를 리턴하고 그렇지 않으면 False 를 리턴한다.
  """
  bConnected = False

  self.clsDialogMutex.acquire()
  clsDialog = self.clsDialogMap.get(strCallId)
  if( clsDialog != None ):
    if( clsDialog.iStartTime != 0.0 ):
      bConnected = True
  self.clsDialogMutex.release()

  return bConnected

def DeleteIncomingCall( self, strCallId ):
  """ 수신 통화를 삭제한다.

  Args:
      strCallId (string): SIP Call-ID 문자열

  Returns:
      SipMessage: 성공하면 수신 통화의 SIP 메시지 저장 객체를 리턴하고 그렇지 않으면 None 를 리턴한다.
  """
  clsMessage = None

  self.clsDialogMutex.acquire()
  clsDialog = self.clsDialogMap.get(strCallId)
  if( clsDialog != None ):
    if( clsDialog.iStartTime == 0.0 and clsDialog.clsInviteRecv != None ):
      clsMessage = clsDialog.clsInviteRecv
      del self.clsDialogMap[strCallId]
  self.clsDialogMutex.release()

  return clsMessage

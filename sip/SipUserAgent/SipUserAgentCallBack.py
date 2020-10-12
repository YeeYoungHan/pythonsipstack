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

import os

class SipUserAgentCallBack():
  """ SIP UserAgent 의 이벤트 수신 callback 인터페이스
  """

  def EventIncomingCall( self, strCallId, strFrom, strTo, clsRtp ):
    """ 전화 수신 이벤트 핸들러

    Args:
        strCallId (string): SIP Call-ID 문자열
        strFrom (string): 발신자 전화번호
        strTo (string): 수신자 전화번호
        clsRtp (SipCallRtp): 발신자 RTP 정보 저장 객체
    """
    return
  
  def EventCallRing( self, strCallId, iSipStatus, clsRtp ):
    """ SIP 통화 발신에 대한 ring 수신 이벤트 핸들러

    Args:
        strCallId (string): SIP Call-ID 문자열
        iSipStatus (int): SIP 응답 코드
        clsRtp (SipCallRtp): 상대방 RTP 정보 저장 객체
    """
    return
  
  def EventCallStart( self, strCallId, clsRtp ):
    """ SIP 통화 시작 이벤트 핸들러. 통화 발신인 경우에만 호출된다.

    Args:
        strCallId (string): SIP Call-ID 문자열
        clsRtp (SipCallRtp): 상대방 RTP 정보 저장 객체
    """
    return
  
  def EventCallEnd( self, strCallId, iSipStatus ):
    """ SIP 통화 종료 이벤트 핸들러

    Args:
        strCallId (string): SIP Call-ID 문자열
        iSipStatus (int): SIP 응답 코드
    """
    return

  def EventRegister( self, clsServerInfo, iStatus ):
    """ SIP REGISTER 성공/실패 이벤트 핸들러

    Args:
        clsServerInfo (SipServerInfo): SIP 서버 로그인 정보 저장 객체
        iStatus (int): SIP 응답 코드
    """
    return
  
  def EventReInvite( self, strCallId, clsRemoteRtp, clsLocalRtp ):
    """ SIP ReINVITE 수신 이벤트 핸들러

    Args:
        strCallId (string): SIP Call-ID 문자열
        clsRemoteRtp (SipCallRtp): 상대방 RTP 정보 저장 객체
        clsLocalRtp (SipCallRtp): 로컬 RTP 정보 저장 객체
    """
    return
  
  def EventReInviteResponse( self, strCallId, iSipStatus, clsRemoteRtp ):
    """ SIP ReINVITE 응답 수신 이벤트 핸들러

    Args:
        strCallId (string): SIP Call-ID 문자열
        iSipStatus (int): SIP 응답 코드
        clsRemoteRtp (SipCallRtp): 상대방 RTP 정보 저장 객체
    """
    return
  
  def EventPrack( self, strCallId, clsRtp ):
    """ SIP PRACK 요청 수신 이벤트 핸들러

    Args:
        strCallId (string): SIP Call-ID 문자열
        clsRtp (SipCallRtp): 상대방 RTP 정보 저장 객체
    """
    return
  
  def EventTransfer( self, strCallId, strReferToCallId, bScreenedTransfer ):
    """ 통화 전달 이벤트 핸들러 ( screened, unscreened transfer )

    Args:
        strCallId (string): SIP Call-ID 문자열
        strReferToCallId (string): 전화를 전달받을 SIP Call-ID 문자열
        bScreenedTransfer (bool): Screened Transfer 이면 True 가 입력되고 그렇지 않으면 False 가 입력된다.

    Returns:
        bool: 성공하면 True 를 리턴하고 그렇지 않으면 False 를 리턴한다.
    """
    return False
  
  def EventBlindTransfer( self, strCallId, strReferToId ):
    """ 통화 전달 이벤트 핸들러 ( blind transfer )

    Args:
        strCallId (string): SIP Call-ID 문자열
        strReferToId (string): 전화를 전달받을 전화번호

    Returns:
        bool: 성공하면 True 를 리턴하고 그렇지 않으면 False 를 리턴한다.
    """
    return False
  
  def EventTransferResponse( self, strCallId, iSipStatus ):
    """ SIP 통화 전달 응답 수신 이벤트 핸들러

    Args:
        strCallId (string): SIP Call-ID 문자열
        iSipStatus (int): SIP 응답 코드
    """
    return
  
  def EventMessage( self, strFrom, strTo, clsMessage ):
    """ SIP MESSAGE 수신 이벤트 핸들러

    Args:
        strFrom (string): 발신자 전화번호
        strTo (string): 수신자 전화번호
        clsMessage (SipMessage): 수신한 SIP 메시지 저장 객체

    Returns:
        [type]: [description]
    """
    return False
  
  def EventIncomingRequestAuth( self, clsMessage ):
    """ 수신된 SIP 요청 메시지를 허용할지를 응용에서 결정할 수 있는 이벤트 핸들러

    Args:
        clsMessage (SipMessage): 수신한 SIP 메시지 저장 객체

    Returns:
        bool: 허용된 SIP 요청 메시지이면 True 를 리턴하고 그렇지 않으면 False 를 리턴한다.
    """
    return True
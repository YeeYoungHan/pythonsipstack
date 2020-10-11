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

from ..SipParser.SipStatusCode import SipStatusCode

class SipStackCallBack():
  """ SipStack 의 이벤트를 응용으로 전달하는 callback 인터페이스
  """

  def RecvRequest( self, clsMessage ):
    """ SIP 요청 메시지 수신 이벤트 핸들러

    Args:
        clsMessage (SipMessage): SIP 메시지 객체

    Returns:
        bool: 응용에서 응답 메시지를 전송하였고 다음 callback 에서 처리할 필요가 없는 경우에는 True 를 리턴하고 그렇지 않으면 False 를 리턴한다.
    """
    return False
  
  def RecvResponse( self, clsMessage ):
    """ SIP 응답 메시지 수신 이벤트 핸들러

    Args:
        clsMessage (SipMessage): SIP 메시지 객체

    Returns:
        bool: 응용에서 응답 메시지를 처리하였고 다음 callback 에서 처리할 필요가 없는 경우에는 True 를 리턴하고 그렇지 않으면 False 를 리턴한다.
    """
    return False
  
  def SendTimeout( self, clsMessage ):
    """ SIP 메시지 전송 timeout 이벤트 핸들러

    Args:
        clsMessage (SipMessage): SIP 메시지 객체

    Returns:
        bool: 응용에서 SIP 메시지를 처리하였고 다음 callback 에서 처리할 필요가 없는 경우에는 True 를 리턴하고 그렇지 않으면 False 를 리턴한다.
    """
    return False

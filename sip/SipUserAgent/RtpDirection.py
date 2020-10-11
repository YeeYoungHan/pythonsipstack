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

class RtpDirection():
  """ RTP 전송/수신 관련 숫자를 저장하는 클래스
  """
  SEND_RECV = 0
  SEND = 1
  RECV = 2
  INACTIVE = 3

def GetRtpDirectionString( eDirection ):
  """ 입력된 RTP 전송/수신 관련 숫자에 대한 SDP 에 저장할 문자열을 리턴한다.

  Args:
      eDirection (int): 입력된 RTP 전송/수신 관련 숫자

  Returns:
      string: 입력된 RTP 전송/수신 관련 숫자에 대한 SDP 에 저장할 문자열을 리턴한다.
  """
  if( eDirection == RtpDirection.SEND_RECV ):
    return "sendrecv"
  elif( eDirection == RtpDirection.SEND ):
    return "sendonly"
  elif( eDirection == RtpDirection.RECV ):
    return "recvonly"
  elif( eDirection == RtpDirection.INACTIVE ):
    return "inactive"
  
  return "sendrecv"
  
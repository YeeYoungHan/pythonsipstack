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

class SipTransport():
  """ SIP transport 상수 저장 클래스
  """
  UDP = 0
  TCP = 1
  TLS = 2

def SipGetTransport( eTransport ):
  """ SIP transport 에 해당하는 문자열을 리턴한다.

  Args:
      eTransport (int): SIP transport 숫자

  Returns:
      string: SIP transport 에 해당하는 문자열을 리턴한다.
  """
  if( eTransport == SipTransport.UDP ):
    return "UDP"
  elif( eTransport == SipTransport.TCP ):
    return "TCP"
  elif( eTransport == SipTransport.TLS ):
    return "TLS"

  return "UDP"

def SipGetProtocol( eTransport ):
  """ SIP transport 에 해당하는 sip 프로토콜 문자열을 리턴한다.

  Args:
      eTransport (int): SIP transport 숫자

  Returns:
      string: SIP transport 에 해당하는 sip 프로토콜 문자열을 리턴한다.
  """
  if( eTransport == SipTransport.TLS ):
    return "sips"
  
  return "sip"
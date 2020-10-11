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

from ..SipParser.SipTransport import SipTransport

class SipCallRoute():
  """ SIP 메시지를 전송할 대상 호스트 및 프로토콜 정보를 저장하는 클래스
  """

  def __init__( self ):
    self.strDestIp = ''
    self.iDestPort = 0
    self.eTransport = SipTransport.UDP
    self.b100rel = False
    
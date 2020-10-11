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

class SipStackSetup():
  """ SIP stack 설정 정보를 저장하는 클래스
  """

  def __init__( self ):
    self.strLocalIp = ''
    self.iLocalUdpPort = 5060
    self.iUdpThreadCount = 1
    self.strUserAgent = ""
    self.iStackExecutePeriod = 0.02
    self.iTimerD = 32.0
    self.iTimerJ = 32.0
    self.bIpv6 = False
    self.bUseRegisterSession = False
  
  def GetLocalPort( self, eTransport ):
    """ SIP transport 에 해당하는 포트 번호를 리턴한다.

    Args:
        eTransport (int): SIP transport 정수

    Returns:
        int: SIP transport 에 해당하는 포트 번호를 리턴한다.
    """
    if( eTransport == SipTransport.UDP ):
      return self.iLocalUdpPort
    
    return self.iLocalUdpPort

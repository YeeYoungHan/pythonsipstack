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

from .RtpDirection import RtpDirection, GetRtpDirectionString

class SipCallRtp():
  """ SIP 통화에 사용할 RTP 정보를 저장하는 클래스
  """

  def __init__( self ):
    self.strIp = ''
    self.iPort = -1
    self.iCodec = -1
    self.eDirection = RtpDirection.SEND_RECV
    self.clsCodecList = []
  
  def __repr__( self ):
    strText = "SipCallRtp(" + self.strIp + ":" + str(self.iPort) + ") codec(" + str(self.iCodec) + ")"
    strText += " direction(" + GetRtpDirectionString(self.eDirection) + ") codec list" + str(self.clsCodecList)

    return strText

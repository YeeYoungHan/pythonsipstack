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

from sip.SdpParser.SdpMessage import SdpMessage

def Test( strInput, strOutput ):
  clsSdp = SdpMessage()

  if( clsSdp.Parse( strInput ) == -1 ):
    print( "sdp(" + strInput + ") parse error" )
    exit()
  
  strSdp = str( clsSdp )

  if( strSdp != strOutput ):
    print( "sdp(" + strInput + ") output(" + strOutput + ") != result(" + strSdp + ")" )
    exit()

Test( "v=0\r\n"
  "o=jdoe 2890844526 2890842807 IN IP4 10.47.16.5\r\n"
  "s=SDP Seminar\r\n"
  "i=A Seminar on the session description protocol\r\n"
  "u=http://www.example.com/seminars/sdp.pdf\r\n"
  "e=j.doe@example.com (Jane Doe)\r\n"
  "c=IN IP4 224.2.17.12/127\r\n"
  "t=2873397496 2873404696\r\n"
  "a=recvonly\r\n"
  "m=audio 49170 RTP/AVP 0\r\n"
  "m=video 51372 RTP/AVP 99\r\n"
  "a=rtpmap:99 h263-1998/90000\r\n",
  "v=0\r\n"
  "o=jdoe 2890844526 2890842807 IN IP4 10.47.16.5\r\n"
  "s=SDP Seminar\r\n"
  "i=A Seminar on the session description protocol\r\n"
  "u=http://www.example.com/seminars/sdp.pdf\r\n"
  "e=j.doe@example.com (Jane Doe)\r\n"
  "c=IN IP4 224.2.17.12/127\r\n"
  "t=2873397496 2873404696\r\n"
  "a=recvonly\r\n"
  "m=audio 49170 RTP/AVP 0\r\n"
  "m=video 51372 RTP/AVP 99\r\n"
  "a=rtpmap:99 h263-1998/90000\r\n" )
Test( "v=0\r\n"
  "o=jdoe 2890844526 2890842807 IN IP4 10.47.16.5\r\n"
  "s=SDP Seminar\r\n"
  "i=A Seminar on the session description protocol\r\n"
  "u=http://www.example.com/seminars/sdp.pdf\r\n"
  "e=j.doe@example.com (Jane Doe)\r\n"
  "c=IN IP4 224.2.17.12/127\r\n"
  "b=X-YZ:128\r\n",
  "v=0\r\n"
  "o=jdoe 2890844526 2890842807 IN IP4 10.47.16.5\r\n"
  "s=SDP Seminar\r\n"
  "i=A Seminar on the session description protocol\r\n"
  "u=http://www.example.com/seminars/sdp.pdf\r\n"
  "e=j.doe@example.com (Jane Doe)\r\n"
  "c=IN IP4 224.2.17.12/127\r\n"
  "b=X-YZ:128\r\n" )
Test( "v=0\r\n"
  "o=CiscoSystemsSIP-GW-UserAgent 7393 3874 IN IP4 192.10.228.41\r\n"
  "s=SIP Call\r\n"
  "c=IN IP4 192.10.228.41\r\n"
  "t=0 0\r\n"
  "m=audio 24864 RTP/AVP 0 101\r\n"
  "c=IN IP4 192.10.228.41\r\n"
  "a=rtpmap:0 PCMU/8000\r\n"
  "a=rtpmap:101 telephone-event/8000\r\n"
  "a=fmtp:101 0-16\r\n"
  "a=ptime:20\r\n"
  "\r\n"
  "--uniqueBoundary\r\n"
  "Content-Type: application/gtd\r\n"
  "Content-Disposition: signal;handling=optional\r\n"
  "\r\n"
  "IAM,\r\n"
  "PRN,isdn*,,NET5*,\r\n"
  "USI,rate,c,s,c,1\r\n"
  "USI,lay1,alaw\r\n"
  "TMR,00\r\n"
  "CPN,00,,1,2936\r\n"
  "CGN,04,,1,y,4,01075066103\r\n"
  "CPC,09\r\n"
  "FCI,,,,,,,y,\r\n"
  "GCI,5c2f3c7d861811e789221005ca2bd880\r\n"
  "--uniqueBoundary\r\n",
  "v=0\r\n"
  "o=CiscoSystemsSIP-GW-UserAgent 7393 3874 IN IP4 192.10.228.41\r\n"
  "s=SIP Call\r\n"
  "c=IN IP4 192.10.228.41\r\n"
  "t=0 0\r\n"
  "m=audio 24864 RTP/AVP 0 101\r\n"
  "c=IN IP4 192.10.228.41\r\n"
  "a=rtpmap:0 PCMU/8000\r\n"
  "a=rtpmap:101 telephone-event/8000\r\n"
  "a=fmtp:101 0-16\r\n"
  "a=ptime:20\r\n" )
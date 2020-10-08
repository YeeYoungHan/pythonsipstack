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

import sys
import time
from sip.SipParser.SipMessage import SipMessage

def Test( strText ):
  if( len(sys.argv) == 1 ):
    print( "[Usage] python -m test.TestSipParser.TestSpeed {loop count}")
    exit()
  
  iLoopCount = int(sys.argv[1])
  i = 0

  iStartTime = time.time()

  while i < iLoopCount:
    clsMessage = SipMessage()

    if( clsMessage.Parse( strText ) == -1 ):
      print( "clsMessage.Parse error" )
    i += 1

  iEndTime = time.time()
  iTime = iEndTime - iStartTime
  strPps = "%.2f" % ( iLoopCount / iTime )

  print( "test time = " + str(iTime) + " sec" )
  print( "parse time = " + strPps + " pps" )


Test( "OPTIONS sip:carol@chicago.com SIP/2.0\r\n"
  "Route: <sip:server10.biloxi.com;lr>\r\n"
  "Via: SIP/2.0/UDP 192.168.1.100:5060;branch=123456\r\n"
  "Max-Forwards: 70\r\n"
  "To: <sip:carol@chicago.com>\r\n"
  "From: Alice <sip:alice@atlanta.com>;tag=1928301774\r\n"
  "CSeq: 1 OPTIONS\r\n"
  "Call-ID: carol@192.168.1.100\r\n"
  "Contact: <sip:alice@pc33.atlanta.com>\r\n"
  "Content-Type: application/sdp\r\n"
  "Accept: application/sdp; level=1, application/x-private; level=2; g=1, text/html\r\n"
  "Accept-Encoding: gzip;q=1.0, identity; q=0.5, *;q=0\r\n"
  "Accept-Language: da, en-gb;q=0.8, en;q=0.7\r\n"
  "\r\n" )
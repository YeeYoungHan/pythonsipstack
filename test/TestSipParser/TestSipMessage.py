
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

from sip.SipParser import SipMessage

def Test( strInput, strOutput ):
  clsMessage = SipMessage.SipMessage()

  if( clsMessage.Parse( strInput ) == -1 ):
    print( "sip message(" + strInput + ") parse error(" + str(clsMessage) + ")" )
    exit()
  
  strMessage = str( clsMessage )

  if( strMessage != strOutput ):
    print( "sip message(" + strInput + ") output(" + strOutput + ") != result(" + strMessage + ")" )
    exit()

# Body
Test(	"OPTIONS sip:carol@chicago.com SIP/2.0\r\n"
	    "To: <sip:carol@chicago.com>\r\n"
	    "From: Alice <sip:alice@atlanta.com>;tag=1928301774\r\n"
			"Content-Length: 3\r\n"
			"\r\n"
			"123",
			"OPTIONS sip:carol@chicago.com SIP/2.0\r\n"
	    "From: \"Alice\" <sip:alice@atlanta.com>;tag=1928301774\r\n"
	    "To: <sip:carol@chicago.com>\r\n"
			"Content-Length: 3\r\n"
			"\r\n"
			"123" )

# Contact expires 필드
Test(	"SIP/2.0 200 OK\r\n"
			"Via: SIP/2.0/UDP 203.255.208.41:5062;rport=5062;branch=z9hG4bKLss4c3bb3ef441d8671f-b0ce901;received=192.168.216.1\r\n"
			"From: <sip:1000@192.168.216.133>;tag=12345678\r\n"
			"To: <sip:1000@192.168.216.133>;tag=Nr51y7H661NXK\r\n"
			"Call-ID: 12345678@203.255.208.41\r\n"
			"CSeq: 2 REGISTER\r\n"
			"Contact: <sip:1000@203.255.208.41:5062>;expires=300\r\n"
			"Date: Tue, 13 Jul 2010 00:32:10 GMT\r\n"
			"User-Agent: FreeSWITCH-mod_sofia/1.0.6-svn-exported\r\n"
			"Allow: INVITE, ACK, BYE, CANCEL, OPTIONS, MESSAGE, UPDATE, INFO, REGISTER, REFER, NOTIFY, PUBLISH, SUBSCRIBE\r\n"
			"Supported: timer, precondition, path, replaces\r\n"
			"Content-Length: 0\r\n"
			"\r\n",
			"SIP/2.0 200 OK\r\n"
			"Via: SIP/2.0/UDP 203.255.208.41:5062;rport=5062;branch=z9hG4bKLss4c3bb3ef441d8671f-b0ce901;received=192.168.216.1\r\n"
			"From: <sip:1000@192.168.216.133>;tag=12345678\r\n"
			"To: <sip:1000@192.168.216.133>;tag=Nr51y7H661NXK\r\n"
			"Call-ID: 12345678@203.255.208.41\r\n"
			"CSeq: 2 REGISTER\r\n"
			"Contact: <sip:1000@203.255.208.41:5062>;expires=300\r\n"
			"Content-Length: 0\r\n"
			"User-Agent: FreeSWITCH-mod_sofia/1.0.6-svn-exported\r\n"
			"Date: Tue, 13 Jul 2010 00:32:10 GMT\r\n"
			"Allow: INVITE, ACK, BYE, CANCEL, OPTIONS, MESSAGE, UPDATE, INFO, REGISTER, REFER, NOTIFY, PUBLISH, SUBSCRIBE\r\n"
			"Supported: timer, precondition, path, replaces\r\n"
			"\r\n" )

# Min-Expires
Test(	"OPTIONS sip:carol@chicago.com SIP/2.0\r\n"
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
			"Expires: 7200\r\n"
			"Min-Expires: 60\r\n"
			"\r\n",
			"OPTIONS sip:carol@chicago.com SIP/2.0\r\n"
			"Via: SIP/2.0/UDP 192.168.1.100:5060;branch=123456\r\n"
			"Route: <sip:server10.biloxi.com;lr>\r\n"
			"Max-Forwards: 70\r\n"
	    "From: \"Alice\" <sip:alice@atlanta.com>;tag=1928301774\r\n"
	    "To: <sip:carol@chicago.com>\r\n"
			"Call-ID: carol@192.168.1.100\r\n"
			"CSeq: 1 OPTIONS\r\n"
			"Contact: <sip:alice@pc33.atlanta.com>\r\n"
			"Content-Type: application/sdp\r\n"
			"Content-Length: 0\r\n"
			"Expires: 7200\r\n"
      "Accept: application/sdp; level=1, application/x-private; level=2; g=1, text/html\r\n"
			"Accept-Encoding: gzip;q=1.0, identity; q=0.5, *;q=0\r\n"
			"Accept-Language: da, en-gb;q=0.8, en;q=0.7\r\n"
			"Min-Expires: 60\r\n"
			"\r\n" )

# Expires
Test(	"OPTIONS sip:carol@chicago.com SIP/2.0\r\n"
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
			"Expires: 7200\r\n"
			"\r\n",
			"OPTIONS sip:carol@chicago.com SIP/2.0\r\n"
			"Via: SIP/2.0/UDP 192.168.1.100:5060;branch=123456\r\n"
			"Route: <sip:server10.biloxi.com;lr>\r\n"
			"Max-Forwards: 70\r\n"
	    "From: \"Alice\" <sip:alice@atlanta.com>;tag=1928301774\r\n"
	    "To: <sip:carol@chicago.com>\r\n"
			"Call-ID: carol@192.168.1.100\r\n"
			"CSeq: 1 OPTIONS\r\n"
			"Contact: <sip:alice@pc33.atlanta.com>\r\n"
			"Content-Type: application/sdp\r\n"
			"Content-Length: 0\r\n"
			"Expires: 7200\r\n"
			"Accept: application/sdp; level=1, application/x-private; level=2; g=1, text/html\r\n"
			"Accept-Encoding: gzip;q=1.0, identity; q=0.5, *;q=0\r\n"
			"Accept-Language: da, en-gb;q=0.8, en;q=0.7\r\n"
			"\r\n" )

# Header
Test(	"OPTIONS sip:carol@chicago.com SIP/2.0\r\n"
			"Route: <sip:server10.biloxi.com;lr>\r\n"
			"Via: SIP/2.0/UDP 192.168.1.100:5060;branch=123456\r\n"
	    "To: <sip:carol@chicago.com>\r\n"
	    "From: Alice <sip:alice@atlanta.com>;tag=1928301774\r\n"
			"CSeq: 1 OPTIONS\r\n"
			"Call-ID: carol@192.168.1.100\r\n"
			"Contact: <sip:alice@pc33.atlanta.com>\r\n"
			"Content-Type: application/sdp\r\n"
			"Ip: 192.168.0.200\r\n"
			"\r\n",
			"OPTIONS sip:carol@chicago.com SIP/2.0\r\n"
			"Via: SIP/2.0/UDP 192.168.1.100:5060;branch=123456\r\n"
			"Route: <sip:server10.biloxi.com;lr>\r\n"
	    "From: \"Alice\" <sip:alice@atlanta.com>;tag=1928301774\r\n"
	    "To: <sip:carol@chicago.com>\r\n"
			"Call-ID: carol@192.168.1.100\r\n"
			"CSeq: 1 OPTIONS\r\n"
			"Contact: <sip:alice@pc33.atlanta.com>\r\n"
			"Content-Type: application/sdp\r\n"
			"Content-Length: 0\r\n"
			"Ip: 192.168.0.200\r\n"
			"\r\n" )

# Content-Type
Test(	"OPTIONS sip:carol@chicago.com SIP/2.0\r\n"
			"Route: <sip:server10.biloxi.com;lr>\r\n"
			"Via: SIP/2.0/UDP 192.168.1.100:5060;branch=123456\r\n"
	    "To: <sip:carol@chicago.com>\r\n"
	    "From: Alice <sip:alice@atlanta.com>;tag=1928301774\r\n"
			"CSeq: 1 OPTIONS\r\n"
			"Call-ID: carol@192.168.1.100\r\n"
			"Contact: <sip:alice@pc33.atlanta.com>\r\n"
			"Content-Type: application/sdp\r\n"
			"\r\n",
			"OPTIONS sip:carol@chicago.com SIP/2.0\r\n"
			"Via: SIP/2.0/UDP 192.168.1.100:5060;branch=123456\r\n"
			"Route: <sip:server10.biloxi.com;lr>\r\n"
	    "From: \"Alice\" <sip:alice@atlanta.com>;tag=1928301774\r\n"
	    "To: <sip:carol@chicago.com>\r\n"
			"Call-ID: carol@192.168.1.100\r\n"
			"CSeq: 1 OPTIONS\r\n"
			"Contact: <sip:alice@pc33.atlanta.com>\r\n"
			"Content-Type: application/sdp\r\n"
			"Content-Length: 0\r\n"
			"\r\n" )

# Proxy-Authenticate
Test(	"OPTIONS sip:carol@chicago.com SIP/2.0\r\n"
			"Route: <sip:server10.biloxi.com;lr>\r\n"
			"Via: SIP/2.0/UDP 192.168.1.100:5060;branch=123456\r\n"
	    "To: <sip:carol@chicago.com>\r\n"
	    "From: Alice <sip:alice@atlanta.com>;tag=1928301774\r\n"
			"CSeq: 1 OPTIONS\r\n"
			"Call-ID: carol@192.168.1.100\r\n"
			"Contact: <sip:alice@pc33.atlanta.com>\r\n"
			"WWW-Authenticate: Digest realm=\"biloxi.com\", nonce=\"dcd98b7102dd2f0e8b11d0f600bfb0c093\", "
				"domain=\"biloxi.com\", opaque=\"5ccc069c403ebaf9f0171e9517f40e41\", qop=auth\r\n"
			"Proxy-Authenticate: Digest realm=\"biloxi1.com\", nonce=\"dcd98b7102dd2f0e8b11d0f600bfb0c093\", "
				"domain=\"biloxi1.com\", opaque=\"5ccc069c403ebaf9f0171e9517f40e41\", qop=auth-int\r\n"
			"Proxy-Authenticate: Digest realm=\"biloxi2.com\", nonce=\"dcd98b7102dd2f0e8b11d0f600bfb0c094\", "
				"domain=\"biloxi2.com\", opaque=\"5ccc069c403ebaf9f0171e9517f40e43\", qop=auth-int\r\n"
			"\r\n",
			"OPTIONS sip:carol@chicago.com SIP/2.0\r\n"
			"Via: SIP/2.0/UDP 192.168.1.100:5060;branch=123456\r\n"
			"Route: <sip:server10.biloxi.com;lr>\r\n"
	    "From: \"Alice\" <sip:alice@atlanta.com>;tag=1928301774\r\n"
	    "To: <sip:carol@chicago.com>\r\n"
			"Call-ID: carol@192.168.1.100\r\n"
			"CSeq: 1 OPTIONS\r\n"
			"Contact: <sip:alice@pc33.atlanta.com>\r\n"
			"WWW-Authenticate: Digest realm=\"biloxi.com\", domain=\"biloxi.com\", nonce=\"dcd98b7102dd2f0e8b11d0f600bfb0c093\", "
				"opaque=\"5ccc069c403ebaf9f0171e9517f40e41\", qop=auth\r\n"
			"Proxy-Authenticate: Digest realm=\"biloxi1.com\", domain=\"biloxi1.com\", nonce=\"dcd98b7102dd2f0e8b11d0f600bfb0c093\", "
				"opaque=\"5ccc069c403ebaf9f0171e9517f40e41\", qop=auth-int\r\n"
			"Proxy-Authenticate: Digest realm=\"biloxi2.com\", domain=\"biloxi2.com\", nonce=\"dcd98b7102dd2f0e8b11d0f600bfb0c094\", "
				"opaque=\"5ccc069c403ebaf9f0171e9517f40e43\", qop=auth-int\r\n"
			"Content-Length: 0\r\n"
			"\r\n" )
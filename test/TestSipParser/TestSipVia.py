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

from sip.SipParser import SipVia

def Test( strInput, strOutput ):
  clsVia = SipVia.SipVia()

  if( clsVia.Parse( strInput, 0 ) == -1 ):
    print( "sip via(" + strInput + ") parse error" )
    exit()
  
  strVia = str( clsVia )

  if( strVia != strOutput ):
    print( "sip via(" + strInput + ") output(" + strOutput + ") != result(" + strVia + ")" )
    exit()

Test( "SIP/2.0/UDP 192.168.1.100", "SIP/2.0/UDP 192.168.1.100" )
Test( "SIP/2.0/UDP 192.168.1.100:5060", "SIP/2.0/UDP 192.168.1.100:5060" )
Test( "SIP/2.0/UDP 192.168.1.100:5060;ttl=60;maddr=200.201.203.205;received=203.44.2.2;branch=1234567890",
	    "SIP/2.0/UDP 192.168.1.100:5060;ttl=60;maddr=200.201.203.205;received=203.44.2.2;branch=1234567890" )
Test( "SIP/2.0/UDP 192.168.1.100:5060 ;ttl=60;maddr=200.201.203.205;received=203.44.2.2;branch=1234567890",
	    "SIP/2.0/UDP 192.168.1.100:5060;ttl=60;maddr=200.201.203.205;received=203.44.2.2;branch=1234567890" )
Test( "SIP/2.0/UDP 192.168.1.100:5060 ; ttl=60;maddr=200.201.203.205;received=203.44.2.2;branch=1234567890",
	    "SIP/2.0/UDP 192.168.1.100:5060;ttl=60;maddr=200.201.203.205;received=203.44.2.2;branch=1234567890" )
Test( "SIP/2.0/UDP 192.168.1.100;ttl=60;maddr=200.201.203.205;received=203.44.2.2;branch=1234567890",
	    "SIP/2.0/UDP 192.168.1.100;ttl=60;maddr=200.201.203.205;received=203.44.2.2;branch=1234567890" )
Test( "SIP/2.0/UDP 192.168.1.100:5060;ttl=60;maddr=200.201.203.205;received=203.44.2.2;branch=1234567890,SIP/2.0/UDP 1.1.1.1:5060;ttl=60;maddr=2.2.2.2;received=3.3.3.3;branch=0987654321",
	    "SIP/2.0/UDP 192.168.1.100:5060;ttl=60;maddr=200.201.203.205;received=203.44.2.2;branch=1234567890" )

# IPv6 테스트
Test( "SIP/2.0/UDP [5f05:2000:80ad:5800:58:800:2023:1d71]",
	    "SIP/2.0/UDP [5f05:2000:80ad:5800:58:800:2023:1d71]" )
Test( "SIP/2.0/UDP [5f05:2000:80ad:5800:58:800:2023:1d71]:5060",
	    "SIP/2.0/UDP [5f05:2000:80ad:5800:58:800:2023:1d71]:5060" )
Test( "SIP/2.0/UDP [5f05:2000:80ad:5800:58:800:2023:1d71]:5060;ttl=60;maddr=200.201.203.205;received=203.44.2.2;branch=1234567890",
	    "SIP/2.0/UDP [5f05:2000:80ad:5800:58:800:2023:1d71]:5060;ttl=60;maddr=200.201.203.205;received=203.44.2.2;branch=1234567890" )    
Test( "SIP/2.0/UDP [5f05:2000:80ad:5800:58:800:2023:1d71]:5060 ;ttl=60;maddr=200.201.203.205;received=203.44.2.2;branch=1234567890",
	    "SIP/2.0/UDP [5f05:2000:80ad:5800:58:800:2023:1d71]:5060;ttl=60;maddr=200.201.203.205;received=203.44.2.2;branch=1234567890" )
Test( "SIP/2.0/UDP [5f05:2000:80ad:5800:58:800:2023:1d71]:5060 ; ttl=60;maddr=200.201.203.205;received=203.44.2.2;branch=1234567890",
	    "SIP/2.0/UDP [5f05:2000:80ad:5800:58:800:2023:1d71]:5060;ttl=60;maddr=200.201.203.205;received=203.44.2.2;branch=1234567890" )
Test( "SIP/2.0/UDP [5f05:2000:80ad:5800:58:800:2023:1d71];ttl=60;maddr=200.201.203.205;received=203.44.2.2;branch=1234567890",
	    "SIP/2.0/UDP [5f05:2000:80ad:5800:58:800:2023:1d71];ttl=60;maddr=200.201.203.205;received=203.44.2.2;branch=1234567890" )
Test( "SIP/2.0/UDP [5f05:2000:80ad:5800:58:800:2023:1d71]:5060;ttl=60;maddr=200.201.203.205;received=203.44.2.2;branch=1234567890,SIP/2.0/UDP 1.1.1.1:5060;ttl=60;maddr=2.2.2.2;received=3.3.3.3;branch=0987654321",
	    "SIP/2.0/UDP [5f05:2000:80ad:5800:58:800:2023:1d71]:5060;ttl=60;maddr=200.201.203.205;received=203.44.2.2;branch=1234567890" )
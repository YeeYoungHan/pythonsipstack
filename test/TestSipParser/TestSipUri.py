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

from sip.SipParser import SipUri

def Test( strInput ):
  clsSipUri = SipUri.SipUri()
  if( clsSipUri.Parse( strInput, 0 ) == - 1 ):
    print( "sip uri(" + strInput + ") parse error" )
    exit()

  strOutput = str( clsSipUri )

  #print( strOutput )

  if( strInput != strOutput ):
    print( "sip uri(" + strInput + ") != result(" + strOutput + ")" )
    exit()

'''
Test( "sip:alice@atlanta.com:5060" )
Test( "sip:alice@atlanta.com" )
Test( "sip:alice:secretword@atlanta.com;transport=tcp" )
'''
Test( "sips:alice@atlanta.com?subject=project%20x&priority=urgent" )
Test( "sip:+1-212-555-1212:1234@gateway.com;user=phone" )
Test( "sip:+1-212-555-1212:1234@gateway.com:5080;user=phone" )
Test( "sips:1212@gateway.com" )
Test( "sip:alice@192.0.2.4" )
Test( "sip:atlanta.com;method=REGISTER?to=alice%40atlanta.com" )
Test( "sip:alice;day=tuesday@atlanta.com" )
Test( "sip:alice@atlanta.com;maddr=239.255.255.1;ttl=15" )
Test( "sip:alice@atlanta.com" )
Test( "tel:1212@gateway.com" )

# IPv6 테스트
Test( "sip:alice@[5f05:2000:80ad:5800:58:800:2023:1d71]:5060" )
Test( "sip:alice@[5f05:2000:80ad:5800:58:800:2023:1d71]" )
Test( "sip:alice:secretword@[5f05:2000:80ad:5800:58:800:2023:1d71];transport=tcp" )
Test( "sips:alice@[5f05:2000:80ad:5800:58:800:2023:1d71]?subject=project%20x&priority=urgent" )
Test( "sip:+1-212-555-1212:1234@[5f05:2000:80ad:5800:58:800:2023:1d71];user=phone" )
Test( "sip:+1-212-555-1212:1234@[5f05:2000:80ad:5800:58:800:2023:1d71]:5080;user=phone" )
Test( "sips:1212@[5f05:2000:80ad:5800:58:800:2023:1d71]" )
Test( "sip:alice@[5f05:2000:80ad:5800:58:800:2023:1d71]" )
Test( "sip:[5f05:2000:80ad:5800:58:800:2023:1d71];method=REGISTER?to=alice%40atlanta.com" )
Test( "sip:alice;day=tuesday@[5f05:2000:80ad:5800:58:800:2023:1d71]" )
Test( "sip:alice@[5f05:2000:80ad:5800:58:800:2023:1d71];maddr=239.255.255.1;ttl=15" )
Test( "sip:alice@[5f05:2000:80ad:5800:58:800:2023:1d71]" )
Test( "tel:1212@[5f05:2000:80ad:5800:58:800:2023:1d71]" )

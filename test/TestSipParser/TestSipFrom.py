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

from sip.SipParser.SipFrom import SipFrom

def Test( strInput, strOutput ):
  clsFrom = SipFrom()

  if( clsFrom.Parse( strInput, 0 ) == -1 ):
    print( "sip from(" + strInput + ") parse error" )
    exit()
  
  strFrom = str( clsFrom )

  if( strFrom != strOutput ):
    print( "sip from(" + strInput + ") output(" + strOutput + ") != result(" + strFrom + ")" )
    exit()

Test( "<sip:1000@203.255.208.41:5062>;expires=300", "<sip:1000@203.255.208.41:5062>;expires=300" )
Test( "\"Bob\" <sips:bob@biloxi.com:5060> ;tag=a48s", "\"Bob\" <sips:bob@biloxi.com:5060>;tag=a48s" )
Test( "\"Bob\" <sips:bob@biloxi.com> ;tag=a48s", "\"Bob\" <sips:bob@biloxi.com>;tag=a48s" )
Test( "\"Bob \" <sips:bob@biloxi.com> ;tag=a48s", "\"Bob \" <sips:bob@biloxi.com>;tag=a48s" )
Test( "\" Bob\" <sips:bob@biloxi.com> ;tag=a48s", "\" Bob\" <sips:bob@biloxi.com>;tag=a48s" )
Test( "\"Bob\" <sips:bob@biloxi.com>;tag=a48s;ttl=22343", "\"Bob\" <sips:bob@biloxi.com>;tag=a48s;ttl=22343" )
Test( "sip:+12125551212@phone2net.com;tag=887s", "<sip:+12125551212@phone2net.com>;tag=887s" )
Test( "<sip:+12125551212@phone2net.com>;tag=887s", "<sip:+12125551212@phone2net.com>;tag=887s" )
Test( "Anonymous <sip:c8oqz84zk7z@privacy.org>;tag=hyh8", "\"Anonymous\" <sip:c8oqz84zk7z@privacy.org>;tag=hyh8" )
Test( "Anonymous   <sip:c8oqz84zk7z@privacy.org>;tag=hyh8", "\"Anonymous\" <sip:c8oqz84zk7z@privacy.org>;tag=hyh8" )
Test( "sip:alice@atlanta.com", "<sip:alice@atlanta.com>" )
Test( "sip:alice:secretword@atlanta.com;transport=tcp", "<sip:alice:secretword@atlanta.com>;transport=tcp" )
Test( "<sip:alice:secretword@atlanta.com;transport=tcp>", "<sip:alice:secretword@atlanta.com;transport=tcp>" )
Test( "sips:alice@atlanta.com?subject=project%20x&priority=urgent", "<sips:alice@atlanta.com?subject=project%20x&priority=urgent>" )
Test( "<sips:alice@atlanta.com?subject=project%20x&priority=urgent>", "<sips:alice@atlanta.com?subject=project%20x&priority=urgent>" )
Test( "sip:+1-212-555-1212:1234@gateway.com;user=phone", "<sip:+1-212-555-1212:1234@gateway.com>;user=phone" )
Test( "<sip:+1-212-555-1212:1234@gateway.com;user=phone>", "<sip:+1-212-555-1212:1234@gateway.com;user=phone>" )
Test( "<sip:+1-212-555-1212:1234@gateway.com;user=phone>", "<sip:+1-212-555-1212:1234@gateway.com;user=phone>" )
Test( "sips:1212@gateway.com", "<sips:1212@gateway.com>" )
Test( "sip:alice@192.0.2.4", "<sip:alice@192.0.2.4>" )
Test( "<sip:1001@192.168.0.2;x-nearend;x-refci=26528012;x-nearendclusterid=StandAloneCluster;x-nearenddevice=SEP002545941441;x-nearendaddr=1001;x-farendrefci=26528013;x-farendclusterid=StandAloneCluster;x-farenddevice=SEPF02929E28A35;x-farendaddr=1000>;tag=84501~ec4d89fd-07f4-46f8-99c5-63220364acb6-26528017"
		, "<sip:1001@192.168.0.2;x-nearend;x-refci=26528012;x-nearendclusterid=StandAloneCluster;x-nearenddevice=SEP002545941441;x-nearendaddr=1001;x-farendrefci=26528013;x-farendclusterid=StandAloneCluster;x-farenddevice=SEPF02929E28A35;x-farendaddr=1000>;tag=84501~ec4d89fd-07f4-46f8-99c5-63220364acb6-26528017" )

Test( "<sip:atlanta.com;method=REGISTER?to=alice%40atlanta.com>", "<sip:atlanta.com;method=REGISTER?to=alice%40atlanta.com>" )
Test( "<sip:alice;day=tuesday@atlanta.com>", "<sip:alice;day=tuesday@atlanta.com>" )
Test( "<sip:alice@atlanta.com;maddr=239.255.255.1;ttl=15>", "<sip:alice@atlanta.com;maddr=239.255.255.1;ttl=15>" )

# Diversion 테스트
Test( "<sip:+19195551002>;reason=user-busy;privacy=\"full\";counter=4", "<sip:+19195551002>;reason=user-busy;privacy=\"full\";counter=4" )

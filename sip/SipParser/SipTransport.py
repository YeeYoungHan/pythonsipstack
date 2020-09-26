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

from enum import Enum

class SipTransport(Enum):
  E_SIP_UDP = 0
  E_SIP_TCP = 1
  E_SIP_TLS = 2

def SipGetTransport( clsTransport ):
  if( clsTransport == SipTransport.E_SIP_UDP ):
    return "UDP"
  elif( clsTransport == SipTransport.E_SIP_TCP ):
    return "TCP"
  elif( clsTransport == SipTransport.E_SIP_TLS ):
    return "TLS"

  return "UDP"

def SipGetProtocol( clsTransport ):
  if( clsTransport == SipTransport.E_SIP_TLS ):
    return "sips"
  
  return "sip"
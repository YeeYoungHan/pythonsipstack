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

from ..SipParser.SipStatusCode import SipStatusCode

def RecvMessageRequest( self, clsMessage ):
  if( self.clsCallBack.EventIncomingRequestAuth( clsMessage ) == False ):
    return True
    
  if( self.clsCallBack.EventMessage( clsMessage.clsFrom.clsUri.strUser, clsMessage.clsTo.clsUri.strUser, clsMessage ) ):
    self.clsSipStack.SendSipMessage( clsMessage.CreateResponse( SipStatusCode.SIP_OK, '' ) )
    return True
  
  self.clsSipStack.SendSipMessage( clsMessage.CreateResponse( SipStatusCode.SIP_DECLINE, '' ) )
  return True
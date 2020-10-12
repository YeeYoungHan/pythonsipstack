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

def RecvPrackRequest( self, clsMessage ):
  """ SIP PRACK 요청 메시지 수신 이벤트 핸들러

  Args:
      clsMessage (SipMessage): SIP 메시지 객체

  Returns:
      bool: True 를 리턴한다.
  """
  strCallId = clsMessage.GetCallId()
  if( len(strCallId) == 0 ):
    self.clsSipStack.SendSipMessage( clsMessage.CreateResponse( SipStatusCode.SIP_BAD_REQUEST, '' ) )
    return True
  
  if( self.clsCallBack.EventIncomingRequestAuth( clsMessage ) == False ):
    return True
  
  bFound = False
  
  self.clsDialogMutex.acquire()
  clsDialog = self.clsDialogMap.get(strCallId)
  if( clsDialog != None ):
    bFound = True
  self.clsDialogMutex.release()

  if( bFound ):
    clsResponse = clsMessage.CreateResponse( SipStatusCode.SIP_OK, '' )
  else:
    clsResponse = clsMessage.CreateResponse( SipStatusCode.SIP_CALL_TRANSACTION_DOES_NOT_EXIST, '' )
  
  if( clsResponse != None ):
    self.clsSipStack.SendSipMessage( clsResponse )

    clsRtp = self.GetSipCallRtp( clsMessage )
    self.clsCallBack.EventPrack( strCallId, clsRtp )

  return True
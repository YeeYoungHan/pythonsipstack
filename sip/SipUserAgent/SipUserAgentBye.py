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

import time
from ..SipPlatform.Log import Log, LogLevel
from ..SipParser.SipStatusCode import SipStatusCode
  
def RecvByeRequest( self, clsMessage ):
  """ SIP BYE 요청 메시지 수신 이벤트 핸들러

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

  self.clsSipStack.SendSipMessage( clsMessage.CreateResponse( SipStatusCode.SIP_OK, '' ) )

  bRes = False

  self.clsDialogMutex.acquire()
  clsDialog = self.clsDialogMap.get(strCallId)
  if( clsDialog != None ):
    clsDialog.iEndTime = time.time()
    bRes = True
  self.clsDialogMutex.release()

  if( bRes ):
    self.clsCallBack.EventCallEnd( strCallId, SipStatusCode.SIP_OK )
    self.Delete( strCallId )

  return True

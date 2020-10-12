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

from ..SipParser.SipMessage import SipMessage
from ..SipParser.SipStatusCode import SipStatusCode

def RecvNotifyRequest( self, clsMessage ):
  """ SIP NOTIFY 요청 메시지 수신 이벤트 핸들러

  Args:
      clsMessage (SipMessage): SIP 메시지 객체

  Returns:
      bool: True 를 리턴한다.
  """
  strCallId = clsMessage.GetCallId()
  if( len(strCallId) == 0 ):
    self.clsSipStack.SendSipMessage( clsMessage.CreateResponse( SipStatusCode.SIP_BAD_REQUEST, '' ) )
    return True
  
  bFound = False
  
  self.clsDialogMutex.acquire()
  clsDialog = self.clsDialogMap.get(strCallId)
  if( clsDialog != None ):
    bFound = True
  self.clsDialogMutex.release()

  if( bFound ):
    if( clsMessage.clsContentType.IsEqual( "message", "sipfrag" ) ):
      clsHeader = clsMessage.GetHeader( "Event" )
      if( clsHeader != None ):
        if( clsHeader.strValue.find( "refer" ) != -1 ):
          clsSipBody = SipMessage()

          clsSipBody.Parse( clsMessage.strBody )
          if( clsSipBody.iStatusCode > 0 ):
            self.clsCallBack.EventTransferResponse( strCallId, clsSipBody.iStatusCode )
    
    self.clsSipStack.SendSipMessage( clsMessage.CreateResponse( SipStatusCode.SIP_OK, '' ) )
    return True
  
  self.clsSipStack.SendSipMessage( clsMessage.CreateResponse( SipStatusCode.SIP_NOT_FOUND, '' ) )

  return True
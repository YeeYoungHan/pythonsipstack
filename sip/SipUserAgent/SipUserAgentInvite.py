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
from ..SipParser.SipUtility import SipMakeTag
  
def RecvInviteRequest( self, clsMessage ):
  strCallId = clsMessage.GetCallId()
  if( len(strCallId) == 0 ):
    self.clsSipStack.SendSipMessage( clsMessage.CreateResponse( SipStatusCode.SIP_BAD_REQUEST ) )
    return True
  
  clsRtp = self.GetSipCallRtp( clsMessage )
  if( clsRtp == None ):
    self.clsSipStack.SendSipMessage( clsMessage.CreateResponse( SipStatusCode.SIP_NOT_ACCEPTABLE_HERE ) )
    return True
  
  clsResponse = None
  
  # ReINVITE 인지 검사한다.
  bReINVITE = False
  self.clsDialogMutex.acquire()
  clsDialog = self.clsDialogMap.get(strCallId)
  if( clsDialog != None ):
    bReINVITE = True
    clsDialog.SetRemoteRtp( clsRtp )
    clsLocalRtp = clsDialog.SelectLocalRtp( )
  self.clsDialogMutex.release()

  if( bReINVITE ):
    self.clsCallBack.EventReInvite( strCallId, clsRtp, clsLocalRtp )
  
    self.clsDialogMutex.acquire()
    clsDialog = self.clsDialogMap.get(strCallId)
    if( clsDialog != None ):
      clsDialog.SetLocalRtp( clsRtp )
      clsResponse = clsMessage.CreateResponse( SipStatusCode.SIP_OK )
      clsResponse = clsDialog.AddSdp( clsResponse )
    self.clsDialogMutex.release()

    if( clsResponse != None ):
      self.clsSipStack.SendSipMessage( clsResponse )

  # 새로운 INVITE 인 경우
  strTag = SipMakeTag( )

  # 180 Ring 을 전송한다.

  return True

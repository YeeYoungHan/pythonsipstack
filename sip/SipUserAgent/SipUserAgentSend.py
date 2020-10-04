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

from ..SipParser.SipStatusCode import GetReasonPhrase

def SendReInvite( self, strCallId, clsRtp ):
  clsMessage = None

  self.clsDialogMutex.acquire()
  clsDialog = self.clsDialogMap.get(strCallId)
  if( clsDialog != None ):
    clsDialog.SetLocalRtp( clsRtp )
    clsMessage = clsDialog.CreateInvite()
  self.clsDialogMutex.release()

  if( clsMessage != None ):
    self.clsSipStack.SendSipMessage( clsMessage )

def SendNotify( self, strCallId, iSipCode ):
  clsMessage = None

  self.clsDialogMutex.acquire()
  clsDialog = self.clsDialogMap.get(strCallId)
  if( clsDialog != None ):
    clsMessage = clsDialog.CreateNotify()
  self.clsDialogMutex.release()

  if( clsMessage != None ):
    clsMessage.clsContentType.Set( "message", "sipfrag" )
    clsMessage.clsContentType.InsertParam(  "version", "2.0" )
    clsMessage.AddHeader( "Event", "refer" )

    if( iSipCode >= 200 ):
      clsMessage.AddHeader( "Subscription-State",  "terminated" )
    else:
      clsMessage.AddHeader( "Subscription-State",  "active" )
    
    clsMessage.strBody = "SIP/2.0 " + str(iSipCode) + " " + GetReasonPhrase(iSipCode)
    clsMessage.iContentLength = len(clsMessage.strBody)

    self.clsSipStack.SendSipMessage( clsMessage )

def SendDtmf( self, strCallId, strDtmf ):
  clsMessage = None

  self.clsDialogMutex.acquire()
  clsDialog = self.clsDialogMap.get(strCallId)
  if( clsDialog != None ):
    clsMessage = clsDialog.CreateInfo()
  self.clsDialogMutex.release()

  if( clsMessage != None ):
    clsMessage.clsContentType.Set( "application", "dtmf-relay" )

    clsMessage.strBody = "Signal=" + strDtmf[:1] + "\r\nDuration=160"
    clsMessage.iContentLength = len(clsMessage.strBody)

    self.clsSipStack.SendSipMessage( clsMessage )

def SendPrack( self, strCallId, clsRtp ):
  clsMessage = None

  self.clsDialogMutex.acquire()
  clsDialog = self.clsDialogMap.get(strCallId)
  if( clsDialog != None ):
    # 통화 연결되지 않고 발신한 경우에만 PRACK 메시지를 생성한다.
    if( clsDialog.iStartTime == 0.0 and clsDialog.clsInviteRecv == None ):
      clsMessage = clsDialog.CreatePrack()
      if( clsRtp != None ):
        clsDialog.SetLocalRtp( clsRtp )
        clsMessage = clsDialog.AddSdp( clsMessage )
  self.clsDialogMutex.release()

  if( clsMessage != None ):
    self.clsSipStack.SendSipMessage( clsMessage )
    
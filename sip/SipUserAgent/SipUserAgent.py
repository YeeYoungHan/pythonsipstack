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
from ..SipStack.SipStack import SipStack
from .SipRegisterThread import SipRegisterThread

import threading

class SipUserAgent():

  from .SipUserAgentCall import StartCall
  from .SipUserAgentLogin import InsertRegisterInfo
  from .SipUserAgentSipStack import RecvRequest, RecvResponse
  from .SipUserAgentRegister import RecvRegisterResponse
  from .SipUserAgentInvite import RecvInviteRequest
  from .SipUserAgentCancel import RecvCancelRequest
  from .SipUserAgentBye import RecvByeRequest

  def __init__( self ):
    self.clsRegisterList = []
    self.clsRegisterMutex = threading.Lock()
    self.clsDialogMutex = threading.Lock()
    self.clsMutex = threading.Lock()
    self.clsSipStack = SipStack()
    self.bStopEvent = False
    self.bStart = False
    self.clsDialogMap = {}
    self.iSeq = 0
  
  def Start( self, clsSetup, clsCallBack ):
    if( self.bStart ):
      return False

    self.clsSipStack.AddCallBack( self )
    self.clsCallBack = clsCallBack

    self.clsSipStack.Start( clsSetup )

    p = threading.Thread( target=SipRegisterThread, args=(self,))
    p.daemon = True
    p.start()

    self.bStart = True

    return True
  
  def Stop( self ):
    if( self.bStart == False ):
      return False
    
    self.bStopEvent = True
    self.clsSipStack.Stop()

    self.bStart = False

    return True
  
  def Delete( self, strCallId ):
    self.clsDialogMutex.acquire()
    clsDialog = self.clsDialogMap.get( strCallId )
    if( clsDialog != None ):
      del self.clsDialogMap[strCallId]
    self.clsDialogMutex.release()

  def GetSipCallRtp( self, clsMessage ):
    if( clsMessage.clsContentType.IsEqual( "application", "sdp" ) and len(clsMessage.strBody) > 0 ):
      
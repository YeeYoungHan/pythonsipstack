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
from ..SipParser.SipUtility import SipIpv6Parse
from ..SdpParser.SdpMessage import SdpMessage
from ..SipStack.SipStack import SipStack
from .SipCallRtp import SipCallRtp
from .RtpDirection import RtpDirection
from .SipDialog import IsUseCodec
from .SipRegisterThread import SipRegisterThread

import threading

class SipUserAgent():

  from .SipUserAgentCall import StartCall, StopCall, StopCallForward, RingCall, RingCallStatus, AcceptCall, HoldCall, ResumeCall, GetCallCount, GetCallIdList
  from .SipUserAgentCall import StopCallAll, CreateCall, StartCreatedCall, TransferCallBlind, TransferCall
  from .SipUserAgentLogin import InsertRegisterInfo
  from .SipUserAgentSipStack import RecvRequest, RecvResponse, SendTimeout
  from .SipUserAgentUtil import GetRemoteCallRtp, GetToId, GetFromId, GetContact, GetInviteHeaderValue, GetRSeq, SetRSeq
  from .SipUserAgentUtil import IsRingCall, Is100rel, IsHold, IsConnected, DeleteIncomingCall
  from .SipUserAgentSend import SendReInvite, SendNotify, SendDtmf, SendPrack
  
  from .SipUserAgentInvite import RecvInviteRequest, RecvInviteResponse
  from .SipUserAgentCancel import RecvCancelRequest
  from .SipUserAgentBye import RecvByeRequest
  from .SipUserAgentMessage import RecvMessageRequest
  from .SipUserAgentNotify import RecvNotifyRequest
  from .SipUserAgentOptions import RecvOptionsRequest
  from .SipUserAgentPrack import RecvPrackRequest
  from .SipUserAgentRefer import RecvReferRequest, RecvReferResponse
  from .SipUserAgentRegister import RecvRegisterResponse
  

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
      clsSdp = SdpMessage()

      if( clsSdp.Parse( clsMessage.strBody ) == -1 ):
        Log.Print( LogLevel.ERROR, "GetSipCallRtp sdp parse error [" + clsMessage.strBody + "]" )
        return None
      
      clsRtp = SipCallRtp()
      clsRtp.strIp = SipIpv6Parse( clsSdp.clsConnection.strAddr )

      if( len(clsSdp.clsMediaList) == 0 ):
        Log.Print( LogLevel.ERROR, "GetSipCallRtp media is not found" )
        return None
      
      clsMedia = clsSdp.clsMediaList[0]

      if( len(clsRtp.strIp) == 0 ):
        clsRtp.strIp = SipIpv6Parse( clsMedia.clsConnection.strAddr )
      
      clsRtp.iPort = clsMedia.iPort

      for strFmt in clsMedia.clsFmtList:
        iCodec = int(strFmt)
        if( IsUseCodec( iCodec ) == False ):
          continue

        if( clsRtp.iCodec == -1 or clsRtp.iCodec == 0 ):
          clsRtp.iCodec = iCodec
          clsRtp.clsCodecList.insert( 0, iCodec )
        else:
          clsRtp.clsCodecList.append( iCodec )

      clsRtp.eDirection = RtpDirection.SEND_RECV

      for clsAttribute in clsMedia.clsAttributeList:
        if( clsAttribute.strName == "sendrecv" ):
          clsRtp.eDirection = RtpDirection.SEND_RECV
        elif( clsAttribute.strName == "sendonly" ):
          clsRtp.eDirection = RtpDirection.SEND
        elif( clsAttribute.strName == "recvonly" ):
          clsRtp.eDirection = RtpDirection.RECV
        elif( clsAttribute.strName == "inactive" ):
          clsRtp.eDirection = RtpDirection.INACTIVE
      
      return clsRtp
    
    return None
        

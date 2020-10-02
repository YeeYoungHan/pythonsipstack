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
from ..SipParser.SipTransport import SipTransport
from ..SipParser.SipUtility import SipMakeBranch
from .RtpDirection import RtpDirection, GetRtpDirectionString
from .SipCallRtp import SipCallRtp

class SipDialog():

  def __init__( self, clsSipStack ):
    self.strFromId = ''
    self.strFromTag = ''
    self.strToId = ''
    self.strToTag = ''
    self.strCallId = ''
    self.strViaBranch = ''
    self.iSeq = 0
    self.iNextSeq = 0
    self.strContactIp = ''
    self.iContactPort = -1
    self.eTransport = SipTransport.UDP
    self.strLocalRtpIp = ''
    self.iLocalRtpPort = -1
    self.eLocalDirection = RtpDirection.SEND_RECV
    self.strRemoteRtpIp = ''
    self.iRemoteRtpPort = -1
    self.eRemoteDirection = RtpDirection.SEND_RECV
    self.iCodec = -1
    self.clsCodecList = []
    self.strContactUri = ''
    self.iRSeq = -1
    self.b100rel = False
    self.iInviteTime = 0.0
    self.iCancelTime = 0.0
    self.iStartTime = 0.0
    self.iEndTime = 0.0
    self.clsInvite = None
    self.clsRouteList = []
    self.bSendCall = True
    self.clsSipStack = clsSipStack
  
  def CreateInvite( self ):
    clsMessage = CreateMessage( "INVITE" )
    if( clsMessage == None ):
      return None
    
    self.strBranch = SipMakeBranch( )
    clsMessage.AddVia( self.clsSipStack.clsSetup.strLocalIp, self.clsSipStack.clsSetup.GetLocalPort(self.eTransport), self.strBranch, self.eTransport )

    if( self.b100rel ):
      clsMessage.AddHeader( "Allow", "PRACK, INVITE, ACK, BYE, CANCEL, REFER, NOTIFY, MESSAGE" )
      clsMessage.AddHeader( "Supported", "100rel" )
      clsMessage.AddHeader( "Require", "100rel" )
    
    clsMessage = self.AddSdp( clsMessage )

    return clsMessage
  
  def CreateAck( self, iStatusCode ):
    clsMessage = CreateMessage( "ACK" )
    if( clsMessage == None ):
      return None

    if( iStatusCode / 100 != 2 ):
      clsMessage.AddVia( self.clsSipStack.clsSetup.strLocalIp, self.clsSipStack.clsSetup.GetLocalPort(self.eTransport), self.strBranch, self.eTransport )
    
    return clsMessage
  
  def CreateCancel( self ):
    clsMessage = CreateMessage( "CANCEL" )
    if( clsMessage == None ):
      return None

    clsMessage.AddVia( self.clsSipStack.clsSetup.strLocalIp, self.clsSipStack.clsSetup.GetLocalPort(self.eTransport), self.strBranch, self.eTransport )
    
    return clsMessage
  
  def CreateBye( self ):
    clsMessage = CreateMessage( "BYE" )
    if( clsMessage == None ):
      return None
    
    return clsMessage
  
  def CreateNotify( self ):
    clsMessage = CreateMessage( "NOTIFY" )
    if( clsMessage == None ):
      return None
    
    return clsMessage
  
  def CreateRefer( self ):
    clsMessage = CreateMessage( "REFER" )
    if( clsMessage == None ):
      return None
    
    return clsMessage
  
  def CreatePrack( self ):
    clsMessage = CreateMessage( "PRACK" )
    if( clsMessage == None ):
      return None
    
    strRAck = str(self.iRSeq) + " " + str(self.iSeq) + " INVITE"
    clsMessage.AddMessage( "RAck", strRAck )
    
    return clsMessage
  
  def CreateInfo( self ):
    clsMessage = CreateMessage( "INFO" )
    if( clsMessage == None ):
      return None
    
    return clsMessage
  
  def AddSdp( self, clsMessage ):
    strAddrType = "IP4"

    if( self.strLocalRtpIp.find(':') != -1 ):
      strAddrType = "IP6"
    
    strText = "v=0\r\n" + "o=PSS 4 2 IN " + strAddrType + " " + self.strLocalRtpIp + "\r\n" + "s=PSS\r\n"
    strText += "c=IN " + strAddrType + " " + self.strLocalRtpIp + "\r\n"
    strText += "t=0 0\r\n"

    if( clsMessage.IsRequest() and len(self.clsCodecList) > 0 ):
      strText += "m=audio " + str(self.iLocalRtpPort) + " RTP/AVP"

      for iCodec in self.clsCodecList:
        if( iCodec == 0 or iCodec == 3 or iCodec == 4 or iCodec == 8 or iCodec == 18 ):
          strText += " " + str(iCodec)
      
      strText += " 101\r\n"

      for iCodec in self.clsCodecList:
        if( iCodec == 0 ):
          strText += "a=rtpmap:0 PCMU/8000\r\n"
        elif( iCodec == 3 ):
          strText += "a=rtpmap:3 GSM/8000\r\n"
        elif( iCodec == 4 ):
          strText += "a=rtpmap:4 G723/8000\r\n"
        elif( iCodec == 8 ):
          strText += "a=rtpmap:8 PCMA/8000\r\n" 
        elif( iCodec == 18 ):
          strText += "a=rtpmap:18 G729/8000\r\n"

    else:
      if( self.iCodec == 0 ):
        strText += "a=rtpmap:0 PCMU/8000\r\n"
      elif( self.iCodec == 3 ):
        strText += "a=rtpmap:3 GSM/8000\r\n"
      elif( self.iCodec == 4 ):
        strText += "a=rtpmap:4 G723/8000\r\n"
      elif( self.iCodec == 8 ):
        strText += "a=rtpmap:8 PCMA/8000\r\n" 
      elif( self.iCodec == 18 ):
        strText += "a=rtpmap:18 G729/8000\r\n"
    
    strText += "a=rtpmap:101 telephone-event/8000\r\n"
    strText += "a=fmtp:101 0-15\r\n"
    strText += "a=" + GetRtpDirectionString(self.eLocalDirection) + "\r\n"

    clsMessage.strBody = strText
    clsMessage.iContentLength = len(strText)
    clsMessage.clsContentType.Set( "application", "sdp" )
  
    return clsMessage

  def SetLocalRtp( self, clsRtp ):
    self.strLocalRtpIp = clsRtp.strIp
    self.iLocalRtpPort = clsRtp.iPort
    self.iCodec = clsRtp.iCodec
    self.clsCodecList = clsRtp.clsCodecList
    self.eLocalDirection = clsRtp.eDirection

    if( self.eLocalDirection == RtpDirection.SEND_RECV or self.eLocalDirection == RtpDirection.INACTIVE ):
      self.eRemoteDirection = self.eLocalDirection
    elif( self.eLocalDirection == RtpDirection.SEND ):
      self.eRemoteDirection = RtpDirection.RECV
    elif( self.eLocalDirection == RtpDirection.RECV ):
      self.eRemoteDirection = RtpDirection.SEND
  
  def SetRemoteRtp( self, clsRtp ):
    # ReINVITE 에서 hold 인 경우 IP 주소가 0.0.0.0 으로 수신되어서 Transfer 할 때에 정상적으로 SDP IP 주소가 전달되지 않기 위해서 수정함.
    if( clsRtp.strIp != "0.0.0.0" ):
      self.strRemoteRtpIp = clsRtp.strIp
    
    self.iRemoteRtpPort = clsRtp.iPort
    self.iCodec = clsRtp.iCodec
    self.eRemoteDirection = clsRtp.eDirection

    if( self.eRemoteDirection == RtpDirection.SEND_RECV or self.eRemoteDirection == RtpDirection.INACTIVE ):
      self.eLocalDirection = self.eRemoteDirection
    elif( self.eRemoteDirection == RtpDirection.SEND ):
      self.eLocalDirection = RtpDirection.RECV
    elif( self.eRemoteDirection == RtpDirection.RECV ):
      self.eLocalDirection = RtpDirection.SEND

  def SelectLocalRtp( self ):
    clsRtp = SipCallRtp()

    clsRtp.strIp = self.strLocalRtpIp
    clsRtp.iPort = self.iLocalRtpPort
    clsRtp.iCodec = self.iCodec
    clsRtp.eDirection = self.eLocalDirection
  
    return clsRtp
  
  def SelectRemoteRtp( self ):
    clsRtp = SipCallRtp()

    clsRtp.strIp = self.strRemoteRtpIp
    clsRtp.iPort = self.iRemoteRtpPort
    clsRtp.iCodec = self.iCodec
    clsRtp.eDirection = self.eRemoteDirection
  
    return clsRtp

  def CreateMessage( self, strSipMethod ):
    clsMessage = SipMessage()

    if( clsMessage.clsCallId.Parse( self.strCallId ) == -1 ):
      return None
    
    clsMessage.eTransport = self.eTransport
    clsMessage.strSipMethod = strSipMethod

    if( len(self.strContactUri) > 0 ):
      clsMessage.clsReqUri.Parse( self.strContactUri )
    else:
      clsMessage.clsReqUri.Set( "sip", self.strToId, self.strContactIp, self.iContactPort )
      clsMessage.clsReqUri.InsertTransport( self.eTransport )
    
    if( strSipMethod == "PARCK" ):
      self.iNextSeq = self.iSeq + 2
      iSeq = self.iSeq + 1
    elif( strSipMethod != "ACK" and strSipMethod != "CANCEL" ):
      if( self.iNextSeq != 0 ):
        self.iSeq = self.iNextSeq
        self.iNextSeq = 0
      else:
        self.iSeq += 1
      iSeq = self.iSeq
    else:
      iSeq = self.iSeq
    
    clsMessage.clsCSeq.Set( iSeq, strSipMethod )

    clsMessage.clsFrom.clsUri.Set( "sip", self.strFromId, clsSipStack.clsSetup.strLocalIp, clsSipStack.clsSetup.iLocalUdpPort )
    clsMessage.clsFrom.InsertParam( "tag", self.strFromTag )

    clsMessage.clsTo.clsUri.Set( "sip", self.strToId, self.strContactIp, self.iContactPort )
    if( len(self.strToTag) > 0 ):
      clsMessage.clsTo.InsertParam( "tag", self.strToTag )
    
    strProtocol = "sip"
    iPort = clsSipStack.clsSetup.iLocalUdpPort

    if( clsSipStack.clsSetup.strLocalIp.find( ":" ) != -1 ):
      strUri = "<" + strProtocol + ":" + self.strFromId + "@[" + clsSipStack.clsSetup.strLocalIp + "]:" + iPort + ">"
    else:
      strUri = "<" + strProtocol + ":" + self.strFromId + "@" + clsSipStack.clsSetup.strLocalIp + ":" + iPort + ">"
    
    clsMessage.AddHeader( "P-Asserted-Identity", strUri )
    clsMessage.AddHeader( "Diversion", strUri )

    if( len(self.clsRouteList) > 0 ):
      clsMessage.clsRouteList = self.clsRouteList
    else:
      clsMessage.AddRoute( self.strContactIp, self.iContactPort, self.eTransport )
    
    return clsMessage
  
  def IsConnected( self ):
    if( self.iStartTime != 0.0 and self.iEndTime == 0.0 ):
      return True
    
    return False
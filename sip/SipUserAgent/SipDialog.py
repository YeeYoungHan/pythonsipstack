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
from .SipCallRtp import RtpDirection

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
    
    strBranch = SipMakeBranch( )
    clsMessage.AddVia( self.clsSipStack.clsSetup.strLocalIp, self.clsSipStack.clsSetup.GetLocalPort(self.eTransport), strBranch, self.eTransport )

    if( self.b100rel ):
      clsMessage.AddHeader( "Allow", "PRACK, INVITE, ACK, BYE, CANCEL, REFER, NOTIFY, MESSAGE" )
      clsMessage.AddHeader( "Supported", "100rel" )
      clsMessage.AddHeader( "Require", "100rel" )
    
    clsMessage = self.AddSdp( clsMessage )

    return clsMessage

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
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

from ..SipPlatform.Log import Log, LogLevel
from ..SipParser.SipStatusCode import SipStatusCode
from ..SipStack.SipStackCallback import SipStackCallBack
from ..SipUserAgent.SipUserAgent import SipUserAgent
from ..SipUserAgent.SipUserAgentCallBack import SipUserAgentCallBack
from .CallMap import CallMap

class SipServer(SipUserAgentCallBack,SipStackCallBack):

  def __init__( self ):
    self.clsUserAgent = SipUserAgent()
    self.clsCallMap = CallMap()
  
  def Start( self, clsSetup ):
    if( self.clsUserAgent.Start( clsSetup, self ) == False ):
      Log.Print( LogLevel.ERROR, "clsUserAgent.Start error" )
      return False
    
    self.clsUserAgent.clsSipStack.AddCallBack( self )

    return True
  
  def EventIncomingCall( self, strCallId, strFrom, strTo, clsRtp ):
    clsRoute = self.clsUserAgent.GetContact( strCallId )
    if( clsRoute == None ):
      Log.Print( LogLevel.ERROR, "EventIncomingCall clsUserAgent.GetContact(" + strCallId + ") error" )
      self.clsUserAgent.StopCall( strCallId, 0 )
      return
    
    strNewCallId = self.clsUserAgent.CreateCall( strFrom, strTo, clsRtp, clsRoute )
    if( len(strNewCallId) == 0 ):
      Log.Print( LogLevel.ERROR, "EventIncomingCall clsUserAgent.CreateCall() error" )
      self.clsUserAgent.StopCall( strCallId, 0 )
      return
    
    self.clsCallMap.Insert( strCallId, strNewCallId )

    if( self.clsUserAgent.StartCreatedCall( strNewCallId ) == False ):
      Log.Print( LogLevel.ERROR, "EventIncomingCall clsUserAgent.StartCreatedCall() error" )
      self.clsUserAgent.StopCall( strCallId, 0 )
      self.clsCallMap.Delete( strCallId )
      return
  
  def EventCallRing( self, strCallId, iSipStatus, clsRtp ):
    return
  
  def EventCallStart( self, strCallId, clsRtp ):
    strCallId2 = self.clsCallMap.Select( strCallId )
    if( len(strCallId2) == 0 ):
      Log.Print( LogLevel.ERROR, "EventCallStart clsCallMap.Select(" + strCallId + ") error" )
      self.clsUserAgent.StopCall( strCallId, 0 )
      return
    
    if( self.clsUserAgent.AcceptCall( strCallId2, clsRtp ) == False ):
      Log.Print( LogLevel.ERROR, "EventCallStart clsUserAgent.AcceptCall(" + strCallId2 + ") error" )
      self.clsUserAgent.StopCall( strCallId, 0 )
      self.clsCallMap.Delete( strCallId )
      return
  
  def EventCallEnd( self, strCallId, iSipStatus ):
    strCallId2 = self.clsCallMap.Select( strCallId )
    if( len(strCallId2) == 0 ):
      Log.Print( LogLevel.ERROR, "EventCallEnd clsCallMap.Select(" + strCallId + ") error" )
      return
    
    self.clsUserAgent.StopCall( strCallId2, iSipStatus )
    self.clsCallMap.Delete( strCallId )

  def EventRegister( self, clsServerInfo, iStatus ):
    return
  
  def EventReInvite( self, strCallId, clsRemoteRtp, clsLocalRtp ):
    return
  
  def EventReInviteResponse( self, strCallId, iSipStatus, clsRemoteRtp ):
    return
  
  def EventPrack( self, strCallId, clsRtp ):
    return
  
  def EventTransfer( self, strCallId, strReferToCallId, bScreenedTransfer ):
    return False
  
  def EventBlindTransfer( self, strCallId, strReferToId ):
    return False
  
  def EventTransferResponse( self, strCallId, iSipStatus ):
    return
  
  def EventMessage( self, strFrom, strTo, clsMessage ):
    return False
  
  def RecvRequest( self, clsMessage ):
    if( clsMessage.IsMethod("REGISTER") ):
      self.clsUserAgent.clsSipStack.SendSipMessage( clsMessage.CreateResponse( SipStatusCode.SIP_OK, '' ) )
      return True

    return False

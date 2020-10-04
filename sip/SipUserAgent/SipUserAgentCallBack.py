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

class SipUserAgentCallBack():

  def EventIncomingCall( self, strCallId, strFrom, strTo, clsRtp ):
    return
  
  def EventCallRing( self, strCallId, iSipStatus, clsRtp ):
    return
  
  def EventCallStart( self, strCallId, clsRtp ):
    return
  
  def EventCallEnd( self, strCallId, iSipStatus ):
    return

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
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

from ..SipParser.SipStatusCode import SipStatusCode

def EventRegister( self, clsServerInfo, iStatus ):
  print( "sip server(" + clsServerInfo.strIp + ") login status(" + str(iStatus) + ")" )

def EventIncomingCall( self, strCallId, strFrom, strTo, clsRtp ):
  print( "EventIncomingCall(" + strCallId + "," + strFrom + "," + strTo + ")" )

  if( self.CanNewCall() == False ):
    self.clsUserAgent.StopCall( strCallId, SipStatusCode.SIP_BUSY_HERE )
    print( "Send Response(486)" )
    return
  
  self.strCallId = strCallId
  self.clsDestRtp = clsRtp

def EventCallRing( self, strCallId, iSipStatus, clsRtp ):
  print( "EventCallRing(" + strCallId + "," + str(iSipStatus) + ")" )

def EventCallStart( self, strCallId, clsRtp ):
  print( "EventCallStart(" + strCallId + ")" )

  self.clsDestRtp = clsRtp
  self.clsRtpThread.SetDestIpPort( clsRtp.strIp, clsRtp.iPort )

def EventCallEnd( self, strCallId, iSipStatus ):
  print( "EventCallEnd(" + strCallId + "," + str(iSipStatus) + ")" )

  if( self.strCallId == strCallId ):
    self.strCallId = ''
    self.StopCall()

def EventReInvite( self, strCallId, clsRemoteRtp, clsLocalRtp ):
  print( "EventReInvite(" + strCallId + ")" )

  self.clsDestRtp = clsRemoteRtp
  self.clsRtpThread.SetDestIpPort( clsRemoteRtp.strIp, clsRemoteRtp.iPort )

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

from .SipCallRoute import SipCallRoute
from .RtpDirection import RtpDirection

def GetRemoteCallRtp( self, strCallId ):
  clsRtp = None

  self.clsDialogMutex.acquire()
  clsDialog = self.clsDialogMap.get(strCallId)
  if( clsDialog != None ):
    clsRtp = clsDialog.SelectRemoteRtp( )
  self.clsDialogMutex.release()

  return clsRtp

def GetToId( self, strCallId ):
  strToId = ''

  self.clsDialogMutex.acquire()
  clsDialog = self.clsDialogMap.get(strCallId)
  if( clsDialog != None ):
    strToId = clsDialog.strToId
  self.clsDialogMutex.release()

  return strToId

def GetFromId( self, strCallId ):
  strFromId = ''

  self.clsDialogMutex.acquire()
  clsDialog = self.clsDialogMap.get(strCallId)
  if( clsDialog != None ):
    strFromId = clsDialog.strFromId
  self.clsDialogMutex.release()

  return strFromId

def GetContact( self, strCallId ):
  clsRoute = None

  self.clsDialogMutex.acquire()
  clsDialog = self.clsDialogMap.get(strCallId)
  if( clsDialog != None ):
    clsRoute = SipCallRoute()
    clsRoute.strDestIp = clsDialog.strContactIp
    clsRoute.iDestPort = clsDialog.iContactPort
    clsRoute.eTransport = clsDialog.eTransport
  self.clsDialogMutex.release()

  return clsRoute

def GetInviteHeaderValue( self, strCallId, strName ):
  strValue = ''

  self.clsDialogMutex.acquire()
  clsDialog = self.clsDialogMap.get(strCallId)
  if( clsDialog != None ):
    if( clsDialog.clsInviteRecv != None ):
      clsHeader = clsDialog.clsInviteRecv.GetHeader( strName )
      if( clsHeader != None ):
        strValue = clsHeader.strValue
  self.clsDialogMutex.release()

  return strValue

def GetRSeq( self, strCallId ):
  iRSeq = -1

  self.clsDialogMutex.acquire()
  clsDialog = self.clsDialogMap.get(strCallId)
  if( clsDialog != None ):
    iRSeq = clsDialog.iRSeq
  self.clsDialogMutex.release()

  return iRSeq

def SetRSeq( self, strCallId, iRSeq ):
  self.clsDialogMutex.acquire()
  clsDialog = self.clsDialogMap.get(strCallId)
  if( clsDialog != None ):
    clsDialog.iRSeq = iRSeq
  self.clsDialogMutex.release()

def IsRingCall( self, strCallId, strTo ):
  bRes = False

  self.clsDialogMutex.acquire()
  clsDialog = self.clsDialogMap.get(strCallId)
  if( clsDialog != None ):
    if( clsDialog.IsConnected() == False ):
      if( len(strTo) > 0 ):
        if( clsDialog.strToId == strTo ):
          bRes = True
      else:
        bRes = True
  self.clsDialogMutex.release()

  return bRes

def Is100rel( self, strCallId ):
  b100rel = False

  self.clsDialogMutex.acquire()
  clsDialog = self.clsDialogMap.get(strCallId)
  if( clsDialog != None ):
    b100rel = clsDialog.b100rel
    if( b100rel == False and clsDialog.clsInviteRecv != None ):
      b100rel = clsDialog.clsInviteRecv.Is100rel()
  self.clsDialogMutex.release()

  return b100rel

def IsHold( self, strCallId ):
  bHold = False

  self.clsDialogMutex.acquire()
  clsDialog = self.clsDialogMap.get(strCallId)
  if( clsDialog != None ):
    if( clsDialog.eLocalDirection != RtpDirection.SEND_RECV ):
      bHold = True
  self.clsDialogMutex.release()

  return bHold

def IsConnected( self, strCallId ):
  bConnected = False

  self.clsDialogMutex.acquire()
  clsDialog = self.clsDialogMap.get(strCallId)
  if( clsDialog != None ):
    if( clsDialog.iStartTime != 0.0 ):
      bConnected = True
  self.clsDialogMutex.release()

  return bConnected

def DeleteIncomingCall( self, strCallId ):
  clsMessage = None

  self.clsDialogMutex.acquire()
  clsDialog = self.clsDialogMap.get(strCallId)
  if( clsDialog != None ):
    if( clsDialog.iStartTime == 0.0 and clsDialog.clsInviteRecv != None ):
      clsMessage = clsDialog.clsInviteRecv
      del self.clsDialogMap[strCallId]
  self.clsDialogMutex.release()

  return clsMessage

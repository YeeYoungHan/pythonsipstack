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

import copy
import time
import random
from ..SipPlatform.Log import Log, LogLevel
from ..SipParser.SipUtility import SipMakeTag, SipMakeBranch, SipMakeCallIdName
from ..SipParser.SipStatusCode import SipStatusCode
from ..SipParser.SipFrom import SipFrom
from ..SipStack.SipStack import SipStack
from .SipDialog import SipDialog
from .RtpDirection import RtpDirection

def StartCall( self, strFrom, strTo, clsRtp, clsRoute ):
  if( len(strFrom) == 0 or len(strTo) == 0 ):
    return ''
  
  if( len(clsRoute.strDestIp) == 0 or clsRoute.iDestPort <= 0 or clsRoute.iDestPort > 65535 ):
    return ''
  
  clsDialog = SipDialog( self.clsSipStack )

  clsDialog.strFromId = strFrom
  clsDialog.strToId = strTo

  clsDialog.SetLocalRtp( clsRtp )

  clsDialog.strContactIp = clsRoute.strDestIp
  clsDialog.iContactPort = clsRoute.iDestPort
  clsDialog.eTransport = clsRoute.eTransport
  clsDialog.b100rel = clsRoute.b100rel

  clsDialog.strFromTag = SipMakeTag()
  clsDialog.strViaBranch = SipMakeBranch()
  clsDialog.iInviteTime = time.time()

  bInsert = False

  while bInsert == False:
    clsDialog.strCallId = SipMakeCallIdName() + "@" + self.clsSipStack.clsSetup.strLocalIp

    self.clsDialogMutex.acquire()
    if( self.clsDialogMap.get( clsDialog.strCallId ) == None ):
      clsMessage = clsDialog.CreateInvite()
      clsDialogMap[clsDialog.strCallId] = clsDialog
      bInsert = True
    self.clsDialogMutex.release()
  
  return clsDialog.strCallId

def StopCall( self, strCallId, iSipCode ):
  clsMessage = None

  self.clsDialogMutex.acquire()
  clsDialog = self.clsDialogMap.get( strCallId )
  if( clsDialog != None ):
    if( clsDialog.iStartTime != 0.0 ):
      if( clsDialog.iEndTime == 0.0 ):
        clsMessage = clsDialog.CreateBye()
        del self.clsDialogMap[strCallId]
    else:
      if( clsDialog.clsInvite != None ):
        if( iSipCode > 0 ):
          clsMessage = clsDialog.clsInvite.CreateResponse( iSipCode )
        else:
          clsMessage = clsDialog.clsInvite.CreateResponse( SipStatusCode.SIP_DECLINE, '' )
        del self.clsDialogMap[strCallId]
      elif( clsDialog.iCancelTime == 0.0 and clsDialog.iEndTime == 0.0 ):
        clsMessage = clsDialog.CreateCancel()
        clsDialog.iCancelTime = time.time()
  self.clsDialogMutex.release()

  if( clsMessage != None ):
    self.clsSipStack.SendSipMessage( clsMessage )

def StopCallForward( self, strCallId, strForward ):
  clsMessage = None

  self.clsDialogMutex.acquire()
  clsDialog = self.clsDialogMap.get( strCallId )
  if( clsDialog != None ):
    if( clsDialog.iStartTime == 0.0 and clsDialog.clsInvite != None ):
      clsMessage = clsDialog.clsInvite.CreateResponse( SipStatusCode.SIP_MOVED_TEMPORARILY, '' )
  self.clsDialogMutex.release()

  if( clsMessage != None ):
    clsContact = copy(clsMessage.clsFrom)
    clsContact.clsUri.strUser = strForward
    clsMessage.clsContactList.append( clsContact )

    self.clsSipStack.SendSipMessage( clsMessage )
  
def RingCall( self, strCallId, clsRtp ):
  clsMessage = None

  self.clsDialogMutex.acquire()
  clsDialog = self.clsDialogMap.get( strCallId )
  if( clsDialog != None ):
    if( clsDialog.iStartTime == 0.0 and clsDialog.clsInvite != None ):
      clsDialog.SetLocalRtp( clsRtp )
      clsMessage = clsDialog.clsInvite.CreateResponse( SipStatusCode.SIP_SESSION_PROGRESS, '' )
      if( clsDialog.clsInvite.Is100rel() ):
        iRSeq = clsDialog.clsInvite.clsCSeq.iDigit + random.randint( 1, 1000000000 )
        clsMessage.AddHeader( "RSeq", str(iRSeq) )
      clsMessage = clsDialog.AddSdp( clsMessage )
  self.clsDialogMutex.release()

  if( clsMessage != None ):
    self.clsSipStack.SendSipMessage( clsMessage )

def RingCallStatus( self, strCallId, iSipStatus, clsRtp ):
  clsMessage = None

  self.clsDialogMutex.acquire()
  clsDialog = self.clsDialogMap.get( strCallId )
  if( clsDialog != None ):
    if( clsDialog.iStartTime == 0.0 and clsDialog.clsInvite != None ):
      
      clsMessage = clsDialog.clsInvite.CreateResponse( iSipStatus, '' )

      if( clsRtp != None ):
        clsDialog.SetLocalRtp( clsRtp )
        clsMessage = clsDialog.AddSdp( clsMessage )

      if( clsDialog.iRSeq != -1 ):
        clsMessage.AddHeader( "Allow", "PRACK, INVITE, ACK, BYE, CANCEL, REFER, NOTIFY, MESSAGE" )
        clsMessage.AddHeader( "Require", "100rel" )
        clsMessage.AddHeader( "RSeq", str(clsDialog.iRSeq) )
      
  self.clsDialogMutex.release()

  if( clsMessage != None ):
    self.clsSipStack.SendSipMessage( clsMessage )

def AcceptCall( self, strCallId, clsRtp ):
  clsMessage = None

  self.clsDialogMutex.acquire()
  clsDialog = self.clsDialogMap.get( strCallId )
  if( clsDialog != None ):
    if( clsDialog.iStartTime == 0.0 and clsDialog.clsInvite != None ):
      clsDialog.SetLocalRtp( clsRtp )
      clsMessage = clsDialog.clsInvite.CreateResponse( SipStatusCode.SIP_OK, '' )
      clsDialog.iStartTime = time.time()
      clsDialog.clsInvite = None
      clsMessage = clsDialog.AddSdp( clsMessage )
  self.clsDialogMutex.release()

  if( clsMessage != None ):
    self.clsSipStack.SendSipMessage( clsMessage )

def HoldCall( self, strCallId, eDirection ):
  clsMessage = None

  self.clsDialogMutex.acquire()
  clsDialog = self.clsDialogMap.get( strCallId )
  if( clsDialog != None ):
    clsDialog.eLocalDirection = eDirection
    clsMessage = clsDialog.CreateInvite()
  self.clsDialogMutex.release()

  if( clsMessage != None ):
    self.clsSipStack.SendSipMessage( clsMessage )

def ResumeCall( self, strCallId ):
  clsMessage = None

  self.clsDialogMutex.acquire()
  clsDialog = self.clsDialogMap.get( strCallId )
  if( clsDialog != None ):
    clsDialog.eLocalDirection = RtpDirection.SEND_RECV
    clsMessage = clsDialog.CreateInvite()
  self.clsDialogMutex.release()

  if( clsMessage != None ):
    self.clsSipStack.SendSipMessage( clsMessage )

def GetCallCount( self ):
  self.clsDialogMutex.acquire()
  iCount = len(self.clsDialogMap)
  self.clsDialogMutex.release()

  return iCount

def GetCallIdList( self ):
  clsCallIdList = []

  self.clsDialogMutex.acquire()
  for strCallId in self.clsDialogMap.keys():
    clsCallIdList.append( strCallId )
  self.clsDialogMutex.release()

  return clsCallIdList

def StopCallAll( self ):
  clsCallIdList = self.GetCallIdList()

  for strCallId in clsCallIdList:
    self.StopCall( strCallId )

def CreateCall( self, strFrom, strTo, clsRtp, clsRoute ):
  if( len(strFrom) == 0 or len(strTo) == 0 ):
    return ''
  
  if( len(clsRoute.strDestIp) == 0 or clsRoute.iDestPort <= 0 or clsRoute.iDestPort > 65535 ):
    return ''
  
  clsDialog = SipDialog( self.clsSipStack )

  clsDialog.strFromId = strFrom
  clsDialog.strToId = strTo

  clsDialog.SetLocalRtp( clsRtp )

  clsDialog.strContactIp = clsRoute.strDestIp
  clsDialog.iContactPort = clsRoute.iDestPort
  clsDialog.eTransport = clsRoute.eTransport
  clsDialog.b100rel = clsRoute.b100rel

  clsDialog.strFromTag = SipMakeTag()
  clsDialog.strViaBranch = SipMakeBranch()
  clsDialog.iInviteTime = time.time()

  bInsert = False

  while bInsert == False:
    clsDialog.strCallId = SipMakeCallIdName() + "@" + self.clsSipStack.clsSetup.strLocalIp

    self.clsDialogMutex.acquire()
    if( self.clsDialogMap.get( clsDialog.strCallId ) == None ):
      clsMessage = clsDialog.CreateInvite()
      clsDialogMap[clsDialog.strCallId] = clsDialog
      bInsert = True
    self.clsDialogMutex.release()
  
  if( self.clsSipStack.SendSipMessage( clsMessage ) == False ):
    self.Delete( clsDialog.strCallId )
    return ''
  
  return clsDialog.strCallId

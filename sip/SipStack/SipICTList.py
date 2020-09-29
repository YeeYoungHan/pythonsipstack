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

import threading
import time
from ..SipParser.SipMessage import SipMessage
from ..SipParser.SipStatusCode import SipStatusCode
from ..SipParser.SipTransport import SipTransport
from .SipInviteTransaction import SipInviteTransaction
from .SipTransactionList import SipTransactionList

class SipICTList(SipTransactionList):

  def __init__( self, clsSipStack ):
    self.clsMutex = threading.Lock()
    self.clsMap = {}
    self.clsSipStack = clsSipStack
    self.iTimerD = 32.0

  def Insert( self, clsMessage ):
    bRes = False
    strKey = super().GetKey( clsMessage )

    if( clsMessage.IsRequest() ):
      clsMessage.MakePacket()
      
      self.clsMutex.acquire()
      clsTransaction = self.clsMap.get( strKey )
      if( clsTransaction == None ):
        if( clsMessage.IsMethod( "ACK" ) ):
          for strKey in self.clsMap:
            clsTransaction = self.clsMap[strKey]
            if( clsTransaction.clsRequest.clsCallId == clsMessage.clsCallId ):
              if( clsTransaction.clsAck == None ):
                if( clsTransaction.clsResponse != None and clsTransaction.clsResponse.iStatusCode == SipStatusCode.SIP_UNAUTHORIZED ):
                  del self.clsMap[strKey]
                else:
                  clsTransaction.clsAck = clsMessage
                  clsTransaction.iStopTime = time.time()
                bRes = True
                break
        else:
          clsTransaction = SipInviteTransaction()
          clsTransaction.clsRequest = clsMessage
          clsTransaction.iStartTime = time.time()
          self.clsMap[strKey] = clsTransaction
          bRes = True
      else:
        if( clsMessage.IsMethod( "ACK" ) ):
          clsTransaction.clsAck = clsMessage
          clsTransaction.iStopTime = time.time()
          bRes = True
      self.clsMutex.release()

    else:

      self.clsMutex.acquire()
      clsTransaction = self.clsMap.get( strKey )
      if( clsTransaction != None ):
        if( clsTransaction.clsResponse != None ):
          if( clsTransaction.iStatusCode != clsMessage.iStatusCode ):
            clsTransaction.clsResponse = clsMessage
            clsTransaction.iStatusCode = clsMessage.iStatusCode
            bRes = True
        else:
          clsTransaction.clsResponse = clsMessage
          clsTransaction.iStatusCode = clsMessage.iStatusCode

          if( clsMessage.iStatusCode == SipStatusCode.SIP_CONNECT_ERROR ):
            clsTransaction.iStopTime = time.time()

          bRes = True

        if( clsTransaction.iRingTime == 0.0 ):
          clsTransaction.iRingTime = time.time()

        if( clsTransaction.clsAck != None ):
          self.clsSipStack.Send( clsTransaction.clsAck, False )
        
      self.clsMutex.release()
    
    return bRes
  
  def Execute( self, iTime ):
    clsDeleteList = []
    clsResponseList = []

    self.clsMutex.acquire()
    for strKey in self.clsMap:
      clsTransaction = self.clsMap[strKey]
      if( clsTransaction.iStopTime > 0 ):
        if( iTime - clsTransaction.iStopTime >= self.iTimerD ):
          clsDeleteList.append( strKey )
      elif( clsTransaction.iStatusCode == 0 ):
        if( (iTime - clsTransaction.iStartTime) >= super().arrICTReSendTime[clsTransaction.iReSendCount] ):
          clsTransaction.iReSendCount += 1
          if( clsTransaction.iReSendCount == super().MAX_ICT_RESEND_COUNT ):
            if( clsTransaction.clsResponse == None ):
              clsResponse = clsTransaction.clsRequest.CreateResponse( SipStatusCode.SIP_REQUEST_TIME_OUT, '' )
              clsResponseList.append( clsResponse )
              clsDeleteList.append( strKey )
          else:
            if( clsTransaction.clsRequest.eTransport == SipTransport.UDP ):
              self.clsSipStack.Send( clsTransaction.clsRequest, False )
      elif( clsTransaction.iRingTime > 0 ):
        if( (iTime - clsTransaction.iRingTime) >= 300.0 ):
          clsResponse = clsTransaction.clsRequest.CreateResponse( SipStatusCode.SIP_REQUEST_TIME_OUT, '' )
          clsResponseList.append( clsResponse )
          clsDeleteList.append( strKey )

    for strKey in clsDeleteList:
      del self.clsMap[strKey]
    self.clsMutex.release()

    for clsResponse in clsResponseList:
      self.clsSipStack.RecvResponse( clsResponse )
  
  def DeleteCancel( self, clsMessage ):
    strKey = super().GetKey( "CANCEL" )

    self.clsMutex.acquire()
    clsTransaction = self.clsMap.get( strKey )
    if( clsTransaction != None ):
      del clsMap[strKey]
    self.clsMutex.release()
  
  def DeleteAll( self ):
    self.clsMutex.acquire()
    self.clsMap.clear()
    self.clsMutex.release()

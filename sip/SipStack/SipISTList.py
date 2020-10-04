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

class SipISTList(SipTransactionList):

  def __init__( self, clsSipStack ):
    self.clsMutex = threading.Lock()
    self.clsMap = {}
    self.clsSipStack = clsSipStack

  def Insert( self, clsMessage ):
    bRes = False
    strKey = super().GetKey( clsMessage )

    if( clsMessage.IsRequest() ):
      self.clsMutex.acquire()
      clsTransaction = self.clsMap.get( strKey )
      if( clsTransaction == None ):
        if( clsMessage.IsMethod( "ACK" ) ):
          for strKey in self.clsMap:
            clsTransaction = self.clsMap[strKey]
            if( clsTransaction.clsRequest.IsEqualCallIdSeq( clsMessage ) ):
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

          clsResponse = clsTransaction.clsRequest.CreateResponse( SipStatusCode.SIP_TRYING, '' )
          clsTransaction.clsResponse = clsResponse
          self.clsSipStack.Send( clsResponse, True )
      else:
        if( clsMessage.IsMethod( "ACK" ) ):
          if( clsTransaction.clsResponse != None and clsTransaction.clsResponse.iStatusCode == SipStatusCode.SIP_UNAUTHORIZED ):
            # INVITE 에 대한 응답 메시지가 401 인 ACK 메시지를 수신하면 Transaction 을 바로 삭제한다.
            del self.clsMap[strKey]
          elif( clsTransaction.clsAck == None ):
            clsTransaction.clsAck = clsMessage
            clsTransaction.iStopTime = time.time()
            bRes = True
        elif( clsTransaction.clsResponse != None ):
          self.clsSipStack.Send( clsTransaction.clsResponse, False )
      self.clsMutex.release()

    else:
      clsMessage.MakePacket()

      self.clsMutex.acquire()
      clsTransaction = self.clsMap.get( strKey )
      if( clsTransaction != None ):
        if( clsTransaction.clsResponse == None or clsMessage.iStatusCode > clsTransaction.iStatusCode ):
          clsTransaction.clsResponse = clsMessage
          clsTransaction.iStatusCode = clsMessage.iStatusCode
          bRes = True

          if( clsMessage.iStatusCode >= 200 ):
            clsTransaction.iStartTime = time.time()
      self.clsMutex.release()
    
    return bRes
  
  def Execute( self, iTime ):
    clsDeleteList = []
    clsResponseList = []

    self.clsMutex.acquire()
    for strKey in self.clsMap:
      clsTransaction = self.clsMap[strKey]
      if( clsTransaction.iStopTime > 0 ):
        if( iTime - clsTransaction.iStopTime >= 5.0 ):
          clsDeleteList.append( strKey )
      elif( clsTransaction.iStatusCode >= 200 and clsTransaction.clsAck == None ):
        if( (iTime - clsTransaction.iStartTime) >= super().arrICTReSendTime[clsTransaction.iReSendCount] ):
          clsTransaction.iReSendCount += 1
          if( clsTransaction.iReSendCount == super().MAX_ICT_RESEND_COUNT ):
            clsTransaction.iStopTime = iTime
            clsResponseList.append( clsTransaction.clsResponse )
          else:
            if( clsTransaction.clsResponse.eTransport == SipTransport.UDP ):
              self.clsSipStack.Send( clsTransaction.clsResponse, False )

    for strKey in clsDeleteList:
      del self.clsMap[strKey]
    self.clsMutex.release()

    for clsResponse in clsResponseList:
      self.clsSipStack.SendTimeout( clsResponse )
  
  def DeleteAll( self ):
    self.clsMutex.acquire()
    self.clsMap.clear()
    self.clsMutex.release()

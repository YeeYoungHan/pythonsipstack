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

from ..SipParser.SipUri import SipUri
from ..SipParser.SipStatusCode import SipStatusCode

def RecvReferRequest( self, clsMessage ):
  """ SIP REFER 요청 메시지 수신 이벤트 핸들러

  Args:
      clsMessage (SipMessage): SIP 메시지 객체

  Returns:
      bool: SIP 메시지를 처리하였으면 True 를 리턴하고 그렇지 않으면 False 를 리턴한다.
  """
  strCallId = clsMessage.GetCallId()
  if( len(strCallId) == 0 ):
    self.clsSipStack.SendSipMessage( clsMessage.CreateResponse( SipStatusCode.SIP_BAD_REQUEST, '' ) )
    return True
  
  if( self.clsCallBack.EventIncomingRequestAuth( clsMessage ) == False ):
    return True
  
  bFound = False
  
  self.clsDialogMutex.acquire()
  clsDialog = self.clsDialogMap.get(strCallId)
  if( clsDialog != None ):
    bFound = True
  self.clsDialogMutex.release()

  if( bFound ):
    clsHeader = clsMessage.GetHeader( "Refer-To" )
    if( clsHeader == None ):
      # RFC-3515 : An agent responding to a REFER method MUST return a 400 (Bad Request) if the request contained zero or more than one Refer-To header field values.
      clsResponse = clsMessage.CreateResponse( SipStatusCode.SIP_BAD_REQUEST, '' )
    else:
      strReferToCallId = GetCallIdFromReferTo( clsHeader.strValue )
      if( len(strReferToCallId) == 0 ):
        # Blind Transfer
        clsReferToUri = SipUri()
        if( clsReferToUri.Parse( clsHeader.strValue, 0 ) == -1 ):
          clsResponse = clsMessage.CreateResponse( SipStatusCode.SIP_BAD_REQUEST, '' )
        else:
          if( self.clsCallBack.EventBlindTransfer( strCallId, clsReferToUri.strUser ) ):
            clsResponse = clsMessage.CreateResponse( SipStatusCode.SIP_ACCEPTED, '' )
          else:
            clsResponse = clsMessage.CreateResponse( SipStatusCode.SIP_NOT_FOUND, '' )
      else:
        # Screened / Unscreened Transfer
        bScreenedTransfer = True
        bFound = False
      
        self.clsDialogMutex.acquire()
        clsDialog = self.clsDialogMap.get(strCallId)
        if( clsDialog != None ):
          if( clsDialog.iStartTime == 0.0 ):
            bScreenedTransfer = False
          bFound = True
        self.clsDialogMutex.release()

        if( bFound == False ):
          clsResponse = clsMessage.CreateResponse( SipStatusCode.SIP_NOT_FOUND, '' )
        else:
          if( self.clsCallBack.EventTransfer( strCallId, strReferToCallId, bScreenedTransfer ) ):
            clsResponse = clsMessage.CreateResponse( SipStatusCode.SIP_ACCEPTED, '' )
          else:
            clsResponse = clsMessage.CreateResponse( SipStatusCode.SIP_NOT_FOUND, '' )
  else:
    clsResponse = clsMessage.CreateResponse( SipStatusCode.SIP_CALL_TRANSACTION_DOES_NOT_EXIST, '' )
  
  if( clsResponse != None ):
    self.clsSipStack.SendSipMessage( clsResponse )
    return True

  return False

def RecvReferResponse( self, clsMessage ):
  """ SIP REFER 응답 메시지 수신 이벤트 핸들러

  Args:
      clsMessage (SipMessage): SIP 메시지 객체

  Returns:
      bool: SIP 메시지를 처리하였으면 True 를 리턴하고 그렇지 않으면 False 를 리턴한다.
  """
  strCallId = clsMessage.GetCallId()
  if( len(strCallId) == 0 ):
    return True
  
  self.clsDialogMutex.acquire()
  clsDialog = self.clsDialogMap.get(strCallId)
  if( clsDialog != None ):
    bFound = True
  self.clsDialogMutex.release()

  if( bFound ):
    self.clsCallBack.EventTransferResponse( strCallId, clsMessage.iStatusCode )
    return True
  
  return False


def GetCallIdFromReferTo( strValue ):
  """ ReferTo 헤더 값에서 SIP Call-ID 문자열을 가져온다.

  Args:
      strValue (string): ReferTo 헤더 값 문자열

  Returns:
      string: 성공하면 SIP Call-ID 문자열을 리턴하고 그렇지 않으면 공백 문자열을 리턴한다.
  """
  iPos = strValue.find( "Replaces=" )
  if( iPos == -1 ):
    return ''
  
  iPos += 9
  strValue = strValue[iPos:]
  iPos = strValue.find( "%3B" )
  if( iPos == -1 ):
    iPos = strValue.find( "%3b" )
    if( iPos == -1 ):
      return ''
  
  return strValue[:iPos].replace( "%40", "@" )
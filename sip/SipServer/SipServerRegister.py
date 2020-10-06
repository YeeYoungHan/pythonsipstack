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

from ..SipPlatform.SipMd5 import SipMd5String
from ..SipParser.SipChallenge import SipChallenge
from ..SipParser.SipFrom import SipFrom
from ..SipParser.SipStatusCode import SipStatusCode
from .XmlUser import SelectUser

def AddChallenge( self, clsResponse ):
  clsChallenge = SipChallenge()

  clsChallenge.strType = "Digest"
  clsChallenge.strNonce = self.clsNonceMap.GetNewValue()
  clsChallenge.strRealm = self.clsSetupFile.strRealm

  clsResponse.clsWwwAuthenticateList.append( clsChallenge )

def SendUnAuthorizedResponse( self, clsMessage ):
  clsResponse = clsMessage.CreateResponseWithToTag( SipStatusCode.SIP_UNAUTHORIZED )
  self.AddChallenge( clsResponse )
  self.clsUserAgent.clsSipStack.SendSipMessage( clsResponse )
  return True

class ECheckAuthResult():
  OK = 0
  NONCE_NOT_FOUND = 1
  ERROR = 2

def CheckAuthorization( self, clsCredential, strMethod ):
  if( len(clsCredential.strUserName) == 0 ):
    return ECheckAuthResult.ERROR, None
  
  if( self.clsNonceMap.Select( clsCredential.strNonce, True ) == False ):
    return ECheckAuthResult.NONCE_NOT_FOUND, None
  
  clsXmlUser = SelectUser( clsCredential.strUserName, self.clsSetupFile.strUserXmlFolder )
  if( clsXmlUser == None ):
    return ECheckAuthResult.ERROR, None
  
  if( CheckAuthorizationResponse( clsCredential.strUserName, clsCredential.strRealm, clsCredential.strNonce, clsCredential.strUri, clsCredential.strResponse, clsXmlUser.strPassWord, strMethod ) == False ):
    return ECheckAuthResult.ERROR, None
  
  return ECheckAuthResult.OK, clsXmlUser

def RecvRequestRegister( self, clsMessage ):
  
  if( clsMessage.iExpires != 0 and self.clsSetupFile.iMinRegisterTimeout != 0 ):
    if( clsMessage.iExpires < self.clsSetupFile.iMinRegisterTimeout ):
      clsResponse = clsMessage.CreateResponseWithToTag( SipStatusCode.SIP_INTERVAL_TOO_BRIEF )
      clsResponse.AddHeader( "Min-Expires", self.clsSetupFile.iMinRegisterTimeout )
      self.clsUserAgent.clsSipStack.SendSipMessage( clsResponse )
      return True

  if( len(clsMessage.clsAuthorizationList) == 0 ):
    return self.SendUnAuthorizedResponse( clsMessage )
  
  iResult, clsXmlUser = self.CheckAuthorization( clsMessage.clsAuthorizationList[0], clsMessage.strSipMethod )
  if( iResult == ECheckAuthResult.NONCE_NOT_FOUND ):
    return self.SendUnAuthorizedResponse( clsMessage )
  elif( iResult == ECheckAuthResult.ERROR ):
    return self.SendResponse( clsMessage, SipStatusCode.SIP_FORBIDDEN )
  
  if( clsMessage.GetExpires() == 0 ):
    self.clsUserMap.Delete( clsMessage.clsFrom.clsUri.strUser )
    return self.SendResponse( clsMessage, SipStatusCode.SIP_OK )
  
  clsContact = SipFrom()
  
  if( self.clsUserMap.Insert( clsMessage, clsContact, clsXmlUser ) ):
    clsResponse = clsMessage.CreateResponseWithToTag( SipStatusCode.SIP_OK )
    clsResponse.clsContactList.append( clsContact )
    self.clsUserAgent.clsSipStack.SendSipMessage( clsResponse )
  else:
    return self.SendResponse( clsMessage, SipStatusCode.SIP_BAD_REQUEST )

  return True

def CheckAuthorizationResponse( strUserName, strRealm, strNonce, strUri, strResponse, strPassWord, strMethod ):
  strA1 = SipMd5String( strUserName + ":" + strRealm + ":" + strPassWord )
  strA2 = SipMd5String( strMethod + ":" + strUri )
  strWant = SipMd5String( strA1 + ":" + strNonce + ":" + strA2 )

  if( strWant == strResponse ):
    return True

  return False
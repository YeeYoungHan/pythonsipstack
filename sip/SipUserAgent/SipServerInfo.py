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

from ..SipParser.SipTransport import SipTransport
from ..SipParser.SipCallId import SipCallId
from ..SipParser.SipChallenge import SipChallenge
from ..SipParser.SipCredential import SipCredential
from ..SipParser.SipMessage import SipMessage
from ..SipParser.SipStatusCode import SipStatusCode
from ..SipPlatform.SipMd5 import SipMd5String

class SipServerInfo():

  def __init__( self ):
    self.strIp = ''
    self.iPort = 5060
    self.strDomain = ''
    self.strUserId = ''
    self.strAuthId = ''
    self.strPassWord = ''
    self.iLoginTimeout = 3600
    self.eTransport = SipTransport.UDP
    self.iNatTimeout = 0
    self.bLogin = False
    self.iLoginTime = 0.0
    self.iSendTime = 0.0
    self.iResponseTime = 0.0
    self.iNextSendTime = 0.0
    self.clsCallId = SipCallId()
    self.iSeqNo = 0
    self.bAuth = False
    self.clsChallenge = SipChallenge()
    self.iChallengeStatusCode = 0
    self.iNonceCount = 1
  
  def __eq__( self, clsServerInfo ):
    if( clsServerInfo == None ):
      return False
      
    if( self.strIp == clsServerInfo.strIp and self.strUserId == clsServerInfo.strUserId and self.iPort == clsServerInfo.iPort and self.eTransport == clsServerInfo.eTransport ):
      return True
    
    return False
  
  def ClearLogin( self ):
    self.bLogin = False
    self.iLoginTime = 0.0
    self.iSendTime = 0.0
    self.iResponseTime = 0.0
    self.clsCallId.Clear()
    self.clsChallenge.Clear()
    self.iChallengeStatusCode = 0
    self.iNonceCount = 1
  
  def CreateRegister( self, clsSipStack, clsResponse ):
    clsRequest = SipMessage()

    # REGISTER sip:127.0.0.1 SIP/2.0
    clsRequest.strSipMethod = "REGISTER"
    clsRequest.clsReqUri.Set( "sip", "", self.strDomain, self.iPort )

    # To
    clsRequest.clsTo.clsUri.Set( "sip", self.strUserId, self.strDomain, self.iPort )

    # From
    clsRequest.clsFrom.clsUri.Set( "sip", self.strUserId, self.strDomain, self.iPort )
    clsRequest.clsFrom.InsertTag()

    # CSeq: 1 REGISTER
    self.iSeqNo += 1
    if( self.iSeqNo >= 2000000000 ):
      self.iSeqNo = 1
    clsRequest.clsCSeq.iDigit = self.iSeqNo
    clsRequest.clsCSeq.strMethod = "REGISTER"

    # Route
    clsRequest.AddRoute( self.strIp, self.iPort, self.eTransport )

    # Call-Id
    if( self.clsCallId.Empty() ):
      clsRequest.clsCallId.Make( clsSipStack.clsSetup.strLocalIp )
      self.clsCallId = clsRequest.clsCallId
    else:
      clsRequest.clsCallId = self.clsCallId
    
    self.bAuth = False

    if( clsResponse != None ):
      self.bAuth = self.AddAuthResponse( clsRequest, clsResponse )
    elif( len(self.clsChallenge.strAlgorithm) > 0 ):
      self.iNonceCount += 1
      self.bAuth = self.AddAuthChallenge( clsRequest, self.clsChallenge, self.iChallengeStatusCode, self.iNonceCount )
    
    clsRequest.eTransport = self.eTransport

    return clsRequest

  def SetChallenge( self, clsResponse ):
    if( clsResponse.iStatusCode == SipStatusCode.SIP_PROXY_AUTHENTICATION_REQUIRED ):
      if( len(clsResponse.clsProxyAuthenticateList) == 0 ):
        return False
      clsChallenge = clsResponse.clsProxyAuthenticateList[0]
    else:
      if( len(clsResponse.clsWwwAuthenticateList) == 0 ):
        return False
      clsChallenge = clsResponse.clsWwwAuthenticateList[0]
    
    if( len(clsChallenge.strQop) == 0 ):
      return False
    
    if( len(clsChallenge.strQop) < 4 or clsChallenge.strQop[:4] != "auth" ):
      return False
    
    self.clsChallenge = clsChallenge
    self.iChallengeStatusCode = clsResponse.iStatusCode
  
  def AddAuthResponse( self, clsRequest, clsResponse ):
    if( clsResponse.iStatusCode == SipStatusCode.SIP_PROXY_AUTHENTICATION_REQUIRED ):
      if( len(clsResponse.clsProxyAuthenticateList) == 0 ):
        return False
      clsChallenge = clsResponse.clsProxyAuthenticateList[0]
    else:
      if( len(clsResponse.clsWwwAuthenticateList) == 0 ):
        return False
      clsChallenge = clsResponse.clsWwwAuthenticateList[0]
    
    self.AddAuthChallenge( clsRequest, clsChallenge, clsResponse.iStatusCode, 1 )
  
  def AddAuthChallenge( self, clsRequest, clsChallenge, iStatusCode, iNonceCount ):
    clsCredential = SipCredential()

    clsCredential.strType = clsChallenge.strType

    if( len(self.strAuthId) == 0 ):
      clsCredential.strUserName = self.strUserId
    else:
      clsCredential.strUserName = self.strAuthId
    
    clsCredential.strRealm = clsChallenge.strRealm
    clsCredential.strNonce = clsChallenge.strNonce
    clsCredential.strAlgorithm = clsChallenge.strAlgorithm
    clsCredential.strOpaque = clsChallenge.strOpaque

    clsCredential.strUri = "sip:" + self.strDomain

    if( len(clsChallenge.strQop) >=4 or clsChallenge.strQop[:4] == "auth" ):

      if( clsChallenge.strQop.find(',') != -1 ):
        strQop = clsChallenge.strQop.split(',')[0]
      else:
        strQop = clsChallenge.strQop
      
      clsCredential.strQop = strQop

      clsCredential.strNonceCount = '%08d' % self.iNonceCount
      clsCredential.strCnonce = "1"

      strA1 = clsCredential.strUserName + ":" + clsCredential.strRealm + ":" + self.strPassWord
      strA1 = SipMd5String( strA1 )

      if( strQop == "auth-int" ):
        strA2 = clsRequest.strSipMethod + ":" + clsCredential.strUri + ":" + SipMd5String( clsRequest.strBody )
      else:
        strA2 = clsRequest.strSipMethod + ":" + clsCredential.strUri
      
      strA2 = SipMd5String( strA2 )

      strResponse = strA1 + ":" + clsCredential.strNonce + ":" + clsCredential.strNonceCount + ":" + clsCredential.strCnonce + ":" + clsCredential.strQop + ":" + strA2
      clsCredential.strResponse = SipMd5String( strResponse )

    else:

      strA1 = clsCredential.strUserName + ":" + clsCredential.strRealm + ":" + self.strPassWord
      strA1 = SipMd5String( strA1 )

      strA2 = clsRequest.strMethod + ":" + clsCredential.strUri
      strA2 = SipMd5String( strA2 )

      strResponse = strA1 + ":" + clsCredential.strNonce + ":" + strA2
      clsCredential.strResponse = SipMd5String( strResponse )

    if( iStatusCode == SipStatusCode.SIP_PROXY_AUTHENTICATION_REQUIRED ):
      clsRequest.clsProxyAuthorizationList.append( clsCredential )
    else:
      clsRequest.clsAuthorizationList.append( clsCredential )
    
    return True
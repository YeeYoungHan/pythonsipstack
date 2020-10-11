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

from copy import copy
from .SipUri import SipUri
from .SipFrom import SipFrom, ParseSipFrom
from .SipCSeq import SipCSeq
from .SipCallId import SipCallId
from .SipContentType import SipContentType
from .SipTransport import SipTransport, SipGetTransport, SipGetProtocol
from .SipHeader import SipHeader
from .SipVia import SipVia, ParseSipVia
from .SipCredential import ParseSipCredential
from .SipChallenge import ParseSipChallenge
from .SipStatusCode import SipStatusCode, GetReasonPhrase
from .SipUtility import SipMakeBranch

class SipMessage():

  def __init__( self ):
    self.strSipMethod = ''
    self.clsReqUri = SipUri()
    self.strSipVersion = ''
    self.iStatusCode = -1
    self.strReasonPhrase = ''
    self.clsFrom = SipFrom()
    self.clsTo = SipFrom()
    self.clsViaList = []
    self.clsContactList = []
    self.clsRecordRouteList = []
    self.clsRouteList = []
    self.clsAuthorizationList = []
    self.clsWwwAuthenticateList = []
    self.clsProxyAuthorizationList = []
    self.clsProxyAuthenticateList = []
    self.clsHeaderList = []
    self.clsCSeq = SipCSeq()
    self.clsCallId = SipCallId()
    self.clsContentType = SipContentType()
    self.iContentLength = 0
    self.iExpires = -1
    self.iMaxForwards = -1
    self.strUserAgent = ''
    self.strBody = ''
    self.strPacket = ''
    self.eTransport = SipTransport.UDP
    self.strClientIp = ''
    self.iClientPort = 0


  def Parse( self, strText ):
    """ SIP 메시지를 파싱한다.

    Args:
        strText (string): SIP 메시지를 포함한 문자열

    Returns:
        int: 파싱에 성공하면 파싱한 길이를 리턴하고 그렇지 않으면 -1 를 리턴한다.
    """
    iTextLen = len(strText)
    if( iTextLen <= 4 ):
      return -1
    
    if( strText[0:4] == "SIP/" ):
      iCurPos = self.ParseStatusLine( strText )
    else:
      iCurPos = self.ParseRequestLine( strText )
    
    if( iCurPos == -1 ):
      return -1
    
    clsHeader = SipHeader()

    while( iCurPos < iTextLen ):
      iPos = clsHeader.Parse( strText, iCurPos )
      if( iPos == -1 ):
        return -1
      iCurPos = iPos

      if( len(clsHeader.strName) == 0 ):
        break

      if( clsHeader.strName == "Via" or clsHeader.strName == "v" ):
        ParseSipVia( self.clsViaList, clsHeader.strValue )
      elif( clsHeader.strName == "Max-Forwards" ):
        self.iMaxForwards = int(clsHeader.strValue)
      elif( clsHeader.strName == "From" or clsHeader.strName == "f" ):
        self.clsFrom.Parse( clsHeader.strValue, 0 )
      elif( clsHeader.strName == "To" or clsHeader.strName == "t" ):
        self.clsTo.Parse( clsHeader.strValue, 0 )
      elif( clsHeader.strName == "CSeq" ):
        self.clsCSeq.Parse( clsHeader.strValue, 0 )
      elif( clsHeader.strName == "Call-ID" or clsHeader.strName == "i" ):
        self.clsCallId.Parse( clsHeader.strValue, 0 )
      elif( clsHeader.strName == "Contact" or clsHeader.strName == "m" ):
        ParseSipFrom( self.clsContactList, clsHeader.strValue )
      elif( clsHeader.strName == "Record-Route" ):
        ParseSipFrom( self.clsRecordRouteList, clsHeader.strValue )
      elif( clsHeader.strName == "Route" ):
        ParseSipFrom( self.clsRouteList, clsHeader.strValue )
      elif( clsHeader.strName == "Authorization" ):
        ParseSipCredential( self.clsAuthorizationList, clsHeader.strValue )
      elif( clsHeader.strName == "WWW-Authenticate" ):
        ParseSipChallenge( self.clsWwwAuthenticateList, clsHeader.strValue )
      elif( clsHeader.strName == "Proxy-Authorization" ):
        ParseSipCredential( self.clsProxyAuthorizationList, clsHeader.strValue )
      elif( clsHeader.strName == "Proxy-Authenticate" ):
        ParseSipChallenge( self.clsProxyAuthenticateList, clsHeader.strValue )
      elif( clsHeader.strName == "Content-Type" or clsHeader.strName == "c" ):
        self.clsContentType.Parse( clsHeader.strValue, 0 )
      elif( clsHeader.strName == "Content-Length" or clsHeader.strName == "l" ):
        self.iContentLength = int(clsHeader.strValue)
      elif( clsHeader.strName == "Expires" ):
        self.iExpires = int(clsHeader.strValue)
      elif( clsHeader.strName == "User-Agent" ):
        self.strUserAgent = clsHeader.strValue
      else:
        self.clsHeaderList.append( copy(clsHeader) )
    
    if( self.iContentLength > 0 ):
      if( self.iContentLength > ( iTextLen - iCurPos ) ):
        return -1
      
      self.strBody = strText[iCurPos:iCurPos+self.iContentLength]
      return iCurPos + self.iContentLength
    
    return iCurPos

  def __str__( self ):
    """ SIP 메시지 문자열을 리턴한다.

    Returns:
        string: SIP 메시지 문자열을 리턴한다.
    """
    if( len(self.strSipVersion) == 0 ):
      self.strSipVersion = "SIP/2.0"
    
    if( self.iStatusCode > 0 ):
      if( len(self.strReasonPhrase) == 0 ):
        self.strReasonPhrase = GetReasonPhrase( self.iStatusCode )
      strText = self.strSipVersion + " " + str(self.iStatusCode) + " " + self.strReasonPhrase + "\r\n"
    else:
      strText = self.strSipMethod + " " + str(self.clsReqUri) + " " + self.strSipVersion + "\r\n"

    strText += self.ListToString( self.clsViaList, "Via" )
    strText += self.ListToString( self.clsRecordRouteList, "Record-Route" )
    strText += self.ListToString( self.clsRouteList, "Route" )
        
    if( self.iMaxForwards >= 0 ):
      strText += "Max-Forwards: " + str(self.iMaxForwards) + "\r\n"
    
    strText += "From: " + str(self.clsFrom) + "\r\n"
    strText += "To: " + str(self.clsTo) + "\r\n"

    if( self.clsCallId.Empty() == False ):
      strText += "Call-ID: " + str(self.clsCallId) + "\r\n"
    
    if( self.clsCSeq.Empty() == False ):
      strText += "CSeq: " + str(self.clsCSeq) + "\r\n"

    strText += self.ListToString( self.clsContactList, "Contact" )
    strText += self.ListToString( self.clsAuthorizationList, "Authorization" )
    strText += self.ListToString( self.clsWwwAuthenticateList, "WWW-Authenticate" )
    strText += self.ListToString( self.clsProxyAuthorizationList, "Proxy-Authorization" )
    strText += self.ListToString( self.clsProxyAuthenticateList, "Proxy-Authenticate" )

    if( self.clsContentType.Empty() == False ):
      strText += "Content-Type: " + str(self.clsContentType) + "\r\n"
      
    strText += "Content-Length: " + str(self.iContentLength) + "\r\n"

    if( self.iExpires >= 0 ):
      strText += "Expires: " + str(self.iExpires) + "\r\n"

    if( len(self.strUserAgent) > 0 ):
      strText += "User-Agent: " + self.strUserAgent + "\r\n"
    
    for clsHeader in self.clsHeaderList:
      strText += clsHeader.strName + ": " + clsHeader.strValue + "\r\n"
    
    strText += "\r\n"

    if( self.iContentLength > 0 ):
      strText += self.strBody
    
    return strText
  
  def MakePacket( self ):
    """ strPacket 멤버 변수에 값이 저장되어 있지 않다면 SIP 메시지 문자열을 생성하여서 strPacket 멤버 변수 저장한다.
        SIP stack 에서 재전송할 때에 SIP 메시지 문자열을 생성하지 않고 기존에 생성된 SIP 메시지 문자열을 이용하여서 전송하기 위한 기능
    """
    if( len(self.strPacket) == 0 ):
      self.strPacket = str(self)
  
  def IsRequest( self ):
    """ SIP 요청 메시지인지 검사한다.

    Returns:
        bool: SIP 요청 메시지이면 True 를 리턴하고 그렇지 않으면 False 를 리턴한다.
    """
    if( len(self.strSipMethod) == 0 ):
      return False
    
    return True
  
  def IsMethod( self, strMethod ):
    """ 입력된 SIP 메소드와 동일한 메시지인지 검사한다.

    Args:
        strMethod (string): SIP 메소드 문자열

    Returns:
        bool: 입력된 SIP 메소드와 동일한 메시지이면 True 를 리턴하고 그렇지 않으면 False 를 리턴한다.
    """
    if( len(self.strSipMethod) > 0 ):
      if( self.strSipMethod == strMethod ):
        return True
    else:
      if( self.clsCSeq.strMethod == strMethod ):
        return True
    
    return False

  def IsEqualCallId( self, clsMessage ):
    """ 입력된 SIP 메시지 객체와 동일한 SIP Call-ID 인지 검사한다.

    Args:
        clsMessage (SipMessage): SIP 메시지 객체

    Returns:
        bool: 입력된 SIP 메소드와 동일한 SIP Call-ID 이면 True 를 리턴하고 그렇지 않으면 False 를 리턴한다.
    """
    return self.clsCallId == clsMessage.clsCallId

  def IsEqualCallIdSeq( self, clsMessage ):
    """ 입력된 SIP 메시지 객체와 동일한 SIP Call-ID 이고 CSeq 의 숫자도 동일한지 검사한다.

    Args:
        clsMessage (SipMessage): SIP 메시지 객체

    Returns:
        bool: 입력된 SIP 메소드와 동일한 SIP Call-ID 이고 CSeq 의 숫자도 동일하면 True 를 리턴하고 그렇지 않으면 False 를 리턴한다.
    """
    if( self.clsCallId == clsMessage.clsCallId and self.clsCSeq.iDigit == clsMessage.clsCSeq.iDigit ):
      return True
    
    return False

  def Is100rel( self ):
    """ 100rel 을 사용하는지 검사한다.

    Returns:
        bool: 100rel 을 사용하면 True 를 리턴하고 그렇지 않으면 False 를 리턴한다.
    """
    clsHeader = self.GetHeader( "Supported" )
    if( clsHeader != None and clsHeader.strValue.find( "100rel" ) != -1 ):
        return True
    
    clsHeader = self.GetHeader( "Requires" )
    if( clsHeader != None and clsHeader.strValue.find( "100rel" ) != -1 ):
        return True
      
    return False

  def GetCallId( self ):
    """ SIP Call-ID 문자열을 리턴한다.

    Returns:
        string: SIP Call-ID 문자열을 리턴한다.
    """
    return str(self.clsCallId)

  def GetExpires( self ):
    """ 만료 시간(초단위)을 리턴한다.

    Returns:
        int: 만료 시간이 존재하면 만료 시간(초단위)을 리턴하고 그렇지 않으면 0 을 리턴한다.
    """
    if( self.iExpires != -1 ):
      return self.iExpires
    
    if( len(self.clsContactList) == 0 ):
      return 0
    
    strExpires = self.clsContactList[0].SelectParam( "expires" )
    if( len(strExpires) > 0 ):
      return int(strExpires)
    
    return 0

  def GetHeader( self, strName ):
    """ 입력된 이름과 일치하는 SIP 헤더의 값을 저장한 객체를 리턴한다.

    Args:
        strName (string): 헤더 이름

    Returns:
        SipHeader: 입력된 이름과 일치하는 SIP 헤더의 값을 저장한 객체를 리턴한다.
    """
    strName = strName.lower()

    for clsHeader in self.clsHeaderList:
      if( clsHeader.strName.lower() == strName ):
        return clsHeader
    
    return None

  def GetTopViaIpPort( self ):
    """ 최상위 Via 헤더의 IP, Port 를 리턴한다.

    Returns:
        (IP,Port): 최상위 Via 헤더의 IP, Port 를 튜플로 리턴한다.
    """
    if( len(self.clsViaList) == 0 ):
      return '', 0

    strIp = self.clsViaList[0].SelectParam( "received" )
    if( len(strIp) == 0 ):
      strIp = self.clsViaList[0].strHost
    
    strPort = self.clsViaList[0].SelectParam( "rport" )
    if( len(strPort) > 0 ):
      iPort = int(strPort)
    else:
      iPort = self.clsViaList[0].iPort
    
    return strIp, iPort
  
  def AddIpPortToTopVia( self, strIp, iPort, eTransport ):
    """ 최상위 Via 헤더에 IP, Port, transport 를 저장한다.

    Args:
        strIp (string): IP 주소
        iPort (int): Port 번호
        eTransport (int): transport 정수
    """
    if( len(self.clsViaList) == 0 ):
      return

    self.clsViaList[0].AddIpPort( strIp, iPort, eTransport )

  def AddVia( self, strIp, iPort, strBranch, eTransport ):
    """ Via 헤더를 추가한다.

    Args:
        strIp (string): IP 주소
        iPort (int): Port 번호
        strBranch (string): branch 문자열
        eTransport (int): transport 정수
    """
    clsVia = SipVia()

    clsVia.strProtocolName = "SIP"
    clsVia.strProtocolVersion = "2.0"
    clsVia.strTransport = SipGetTransport( eTransport )
    clsVia.strHost = strIp
    clsVia.iPort = iPort
    clsVia.InsertParam( "rport", "" )

    if( len(strBranch) == 0 ):
      strBranch = SipMakeBranch()
    
    clsVia.InsertParam( "branch", strBranch )

    self.clsViaList.append( clsVia )
  
  def AddRoute( self, strIp, iPort, eTransport ):
    """ Route 헤더를 추가한다.

    Args:
        strIp (string): IP 주소
        iPort (int): Port 번호
        eTransport (int): transport 정수
    """
    clsFrom = SipFrom()

    clsFrom.clsUri.strProtocol = SipGetProtocol( eTransport )
    clsFrom.clsUri.strHost = strIp
    clsFrom.clsUri.iPort = iPort

    clsFrom.clsUri.InsertParam( "lr", "" )
    clsFrom.clsUri.InsertTransport( eTransport )

    self.clsRouteList.insert( 0, clsFrom )

  def AddRecordRoute( self, strIp, iPort, eTransport ):
    """ Record-Route 헤더를 추가한다.

    Args:
        strIp (string): IP 주소
        iPort (int): Port 번호
        eTransport (int): transport 정수
    """
    clsFrom = SipFrom()

    clsFrom.clsUri.strProtocol = SipGetProtocol( eTransport )
    clsFrom.clsUri.strHost = strIp
    clsFrom.clsUri.iPort = iPort

    clsFrom.clsUri.InsertParam( "lr", "" )
    clsFrom.clsUri.InsertTransport( eTransport )

    self.clsRecordRouteList.insert( 0, clsFrom )

  def AddHeader( self, strName, strValue ):
    """ SIP 헤더를 추가한다.

    Args:
        strName (string): SIP 헤더 이름 문자열
        strValue (string): SIP 헤더 값 문자열
    """
    clsHeader = SipHeader()

    clsHeader.strName = strName
    clsHeader.strValue = strValue

    self.clsHeaderList.append( clsHeader )

  def CreateResponse( self, iStatusCode, strToTag ):
    """ SIP 응답 메시지를 생성한다.

    Args:
        iStatusCode (int): SIP 응답 코드
        strToTag (string): SIP To 헤더에 저장할 tag 문자열, SIP To 헤더에 tag 문자열을 저장하지 않을 경우 공백 문자열을 입력하라

    Returns:
        SipMessage: SIP 응답 메시지를 리턴한다.
    """
    clsResponse = SipMessage()

    clsResponse.iStatusCode = iStatusCode
    clsResponse.clsTo = self.clsTo
    clsResponse.clsFrom = self.clsFrom
    clsResponse.clsViaList = self.clsViaList
    clsResponse.clsCallId = self.clsCallId
    clsResponse.clsCSeq = self.clsCSeq
    clsResponse.eTransport = self.eTransport

    if( iStatusCode != SipStatusCode.SIP_TRYING ):
      clsResponse.clsRecordRouteList = self.clsRecordRouteList

    if( len(strToTag) > 0 ):
      clsResponse.clsTo.InsertParam( "tag", strToTag )
    
    return clsResponse
  
  def CreateResponseWithToTag( self, iStatusCode ):
    """ SIP 요청 메시지에 To 헤더의 tag 값이 존재하지 않으면 To 헤더에 tag 값을 저장한 SIP 응답 메시지를 생성하고 그렇지 않으면 To 헤더의 tag 값을 수정하지 않은 SIP 응답 메시지를 생성한다.

    Args:
        iStatusCode (int): SIP 응답 코드

    Returns:
        SipMessage: SIP 응답 메시지를 리턴한다.
    """
    clsResponse = SipMessage()

    clsResponse.iStatusCode = iStatusCode
    clsResponse.clsTo = self.clsTo
    clsResponse.clsFrom = self.clsFrom
    clsResponse.clsViaList = self.clsViaList
    clsResponse.clsCallId = self.clsCallId
    clsResponse.clsCSeq = self.clsCSeq
    clsResponse.eTransport = self.eTransport

    if( iStatusCode != SipStatusCode.SIP_TRYING ):
      clsResponse.clsRecordRouteList = self.clsRecordRouteList

    if( len(clsResponse.clsTo.SelectParam( "tag" )) == 0 ):
      clsResponse.clsTo.InsertTag( )
    
    return clsResponse

  def ParseStatusLine( self, strText ):
    iTextLen = len(strText)
    iPos = 0
    iType = 0
    iStartPos = -1

    while( iPos < iTextLen ):
      if( iType != 2 ):
        if( strText[iPos] == ' ' ):
          if( iType == 0 ):
            self.strSipVersion = strText[0:iPos]
          elif( iType == 1 ):
            self.iStatusCode = int( strText[iStartPos:iPos] )

          iStartPos = iPos + 1
          iType += 1
      else:
        if( strText[iPos] == '\r' ):
          if( iPos + 1 >= iTextLen or strText[iPos+1] != '\n' ):
            return -1
          
          self.strReasonPhrase = strText[iStartPos:iPos]
          return iPos + 2
      
      iPos += 1
    
    return -1


  def ParseRequestLine( self, strText ):
    iTextLen = len(strText)
    iPos = 0
    iType = 0
    iStartPos = -1

    while( iPos < iTextLen ):
      if( iType != 2 ):
        if( strText[iPos] == ' ' ):
          if( iType == 0 ):
            self.strSipMethod = strText[0:iPos]
          elif( iType == 1 ):
            strUri = strText[iStartPos:iPos]
            if( self.clsReqUri.Parse( strUri, 0 ) == -1 ):
              return -1

          iStartPos = iPos + 1
          iType += 1
      else:
        if( strText[iPos] == '\r' ):
          if( iPos + 1 >= iTextLen or strText[iPos+1] != '\n' ):
            return -1
          
          self.strSipVersion = strText[iStartPos:iPos]
          return iPos + 2
      
      iPos += 1
    
    return -1
  
  def ListToString( self, clsList, strName ):
    strText = ''
    for clsRow in clsList:
      strText += strName + ": " + str(clsRow) + "\r\n"
    
    return strText

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

from .SipUtility import SipIpv6Print
from .SipParameter import ParseSipParameter, MakeSipParameterString, InsertSipParameter, SearchSipParameter
from .SipTransport import SipTransport

class SipUri():

  def __init__( self ):
    self.strProtocol = ''
    self.strUser = ''
    self.strHost = ''
    self.iPort = 0
    self.clsUriParamList = []
    self.clsHeaderList = []

  def Parse( self, strText, iStartPos ):
    """ SIP Uri 를 파싱한다.

    Args:
        strText (string): SIP Uri 헤더의 값을 포함한 문자열
        iStartPos (int): strText 에서 분석을 시작할 위치

    Returns:
        int: 파싱에 성공하면 파싱한 길이를 리턴하고 그렇지 않으면 -1 를 리턴한다.
    """
    iPos = self.ParseProtocol( strText, iStartPos )
    if( iPos == -1 ):
      return -1
    iCurPos = iPos

    iPos = self.ParseUser( strText, iCurPos )
    if( iPos != -1 ):
      iCurPos = iPos

    iPos = self.ParseHost( strText, iCurPos )
    if( iPos == -1 ):
      return -1
    iCurPos = iPos

    iTextLen = len(strText)
    while( iCurPos < iTextLen ):
      if( strText[iCurPos] == '?' ):
        iCurPos += 1
        break

      if( strText[iCurPos] == ';' or strText[iCurPos] == ' ' or strText[iCurPos] == '\t' ):
        iCurPos += 1
        continue

      iPos = ParseSipParameter( self.clsUriParamList, strText, iCurPos )
      if( iPos == -1 ):
        return -1
      iCurPos = iPos

    while( iCurPos < iTextLen ):
      if( strText[iCurPos] == ' ' or strText[iCurPos] == '\t' or strText[iCurPos] == '&' ):
        iCurPos += 1
        continue

      iPos = ParseSipParameter( self.clsHeaderList, strText, iCurPos )
      if( iPos == -1 ):
        return -1
      iCurPos = iPos

    return iCurPos

  def __str__( self ):
    """ SIP Uri 문자열을 리턴한다.

    Returns:
        string: SIP Uri 문자열을 리턴한다.
    """
    strUri = self.strProtocol + ":"
    
    if( len( self.strUser ) > 0 ):
      strUri += self.strUser + "@"
    
    strUri += SipIpv6Print( self.strHost )
    
    if( self.iPort ):
      strUri += ":" + str(self.iPort)

    strUri += MakeSipParameterString( self.clsUriParamList )

    i = 0
    for clsParam in self.clsHeaderList:
      if( i == 0 ):
        strUri += '?'
      else:
        strUri += '&'

      strUri += str( clsParam )
      i += 1
    
    return strUri

  def Clear( self ):
    """ 멤버 변수를 초기화 시킨다.
    """
    self.strProtocol = ''
    self.strUser = ''
    self.strHost = ''
    self.iPort = 0
    self.clsUriParamList.clear()
    self.clsHeaderList.clear()
  
  def InsertParam( self, strName, strValue ):
    """ uri param 을 추가한다.

    Args:
        strName (string): param 이름
        strValue (string): param 값
    """
    InsertSipParameter( self.clsUriParamList, strName, strValue )

  def InsertTransport( self, eTransport ):
    """ SIP URI 에 transport tag 를 추가한다.

    Args:
        eTransport (int): SIP transport 숫자
    """
    if( eTransport == SipTransport.TCP ):
      InsertSipParameter( self.clsUriParamList, "transport", "tcp" )
    elif( eTransport == SipTransport.TLS ):
      InsertSipParameter( self.clsUriParamList, "transport", "tls" )

  def SelectTransport( self ):
    """ SIP URI 에서 전송 프로토콜을 가져온다.

    Returns:
        int: SIP transport 숫자
    """
    if( self.strProtocol == "sips" ):
      return SipTransport.TLS
    
    strValue = SearchSipParameter( self.clsUriParamList, "transport" )
    if( len(strValue) > 0 ):
      strValue = strValue.lower()
      if( strValue == "tcp" ):
        return SipTransport.TCP
      elif( strValue == "tls" ):
        return SipTransport.TLS
    
    return SipTransport.UDP
  
  def Set( self, strProtocol, strUser, strHost, iPort ):
    """ 멤버 변수에 입력된 데이터를 저장한다.

    Args:
        strProtocol (string): SIP 프로토콜 문자열
        strUser (string): 사용자 아이디 문자열
        strHost (string): 도메인 이름 또는 IP 주소 문자열
        iPort (int): 포트 번호
    """
    if( len(strProtocol) > 0 ):
      self.strProtocol = strProtocol
    else:
      self.strProtocol = "sip"
    
    self.strUser = strUser
    self.strHost = strHost

    if( iPort == 5060 ):
      self.iPort = 0
    else:
      self.iPort = iPort

  def ParseProtocol( self, strText, iStartPos ):
    for i in range( iStartPos, len(strText) ):
      if( strText[i] == ':' ):
        self.strProtocol = strText[iStartPos:i]
        return i + 1
    return -1

  def ParseUser( self, strText, iStartPos ):
    for i in range( iStartPos, len(strText) ):
      if( strText[i] == '@' ):
        self.strUser = strText[iStartPos:i]
        return i + 1
    return -1

  def ParseHost( self, strText, iStartPos ):
    iPortPos = -1
    iLen = len(strText)

    if( strText[iStartPos] == '[' ):
      bIpFound = False

      iPos = iStartPos + 1
      while( iPos < iLen ):
        if( bIpFound == False ):
          if( strText[iPos] == ']' ):
            self.strHost = strText[iStartPos+1:iPos]
            bIpFound = True
        elif( strText[iPos] == ':' ):
          iPortPos = iPos + 1
        elif( strText[iPos] == ';' or strText[iPos] == '?' ):
          iEndPos = iPos
          break
        iPos += 1

      if( bIpFound == False ):
        return -1

      if( iPortPos != -1 and iPortPos < iPos ):
        self.iPort = int( strText[iPortPos:iPos] )

      return iPos
      
    else:

      iPos = iStartPos
      while( iPos < iLen ):
        if( strText[iPos] == ':' ):
          self.strHost = strText[iStartPos:iPos]
          iPortPos = iPos + 1
        elif( strText[iPos] == ';' or strText[iPos] == '?' or strText[iPos] == '>' ):
          break
        iPos += 1          

      if( iPortPos == -1 ):
        if( iPos > iStartPos ):
          self.strHost = strText[iStartPos:iPos]
          return iPos
      else:
        if( iPortPos < iPos ):
          self.iPort = int( strText[iPortPos:iPos] )
        return iPos
    
    return -1


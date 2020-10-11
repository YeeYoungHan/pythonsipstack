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

from .SipParameter import ParseSipParameter
from ..SipPlatform.StringUtility import DeQuoteString

class SipChallenge():
  """ SIP WWW-Authenticate, Proxy-Authenticate 헤더의 값을 저장하는 클래스
  """

  def __init__( self ):
    self.strType = ''
    self.strRealm = ''
    self.strDomain = ''
    self.strNonce = ''
    self.strOpaque = ''
    self.strStale = ''
    self.strAlgorithm = ''
    self.strQop = ''
    self.clsParamList = []
  
  def Parse( self, strText, iStartPos ):
    """ SIP WWW-Authenticate, Proxy-Authenticate 헤더의 값을 파싱한다.

    Args:
        strText (string): SIP Chanllenge 헤더의 값을 포함한 문자열
        iStartPos (int): strText 에서 분석을 시작할 위치

    Returns:
        int: 파싱에 성공하면 파싱한 길이를 리턴하고 그렇지 않으면 -1 를 리턴한다.
    """
    self.Clear()

    iPos = iStartPos
    iTextLen = len(strText)

    while( iPos < iTextLen ):
      if( strText[iPos] == ' ' or strText[iPos] == '\t' ):
        self.strType = strText[iStartPos:iPos]
        iPos += 1
        break
      iPos += 1

    if( len(self.strType) == 0 ):
      return -1

    iCurPos = iPos
    clsParamList = []

    while( iCurPos < iTextLen ):
      if( strText[iCurPos] == ' ' or strText[iCurPos] == '\t' or strText[iCurPos] == ',' ):
        iCurPos += 1
        continue

      iPos = ParseSipParameter( clsParamList, strText, iCurPos )
      if( iPos == -1 ):
        return -1
      iCurPos = iPos

    for clsParam in clsParamList:
      if( clsParam.strName == "realm" ):
        self.strRealm = DeQuoteString( clsParam.strValue )
      elif( clsParam.strName == "domain" ):
        self.strDomain = DeQuoteString( clsParam.strValue )
      elif( clsParam.strName == "nonce" ):
        self.strNonce = DeQuoteString( clsParam.strValue )
      elif( clsParam.strName == "opaque" ):
        self.strOpaque = DeQuoteString( clsParam.strValue )
      elif( clsParam.strName == "stale" ):
        self.strStale = clsParam.strValue
      elif( clsParam.strName == "algorithm" ):
        self.strAlgorithm = clsParam.strValue
      elif( clsParam.strName == "qop" ):
        self.strQop = DeQuoteString( clsParam.strValue )
      else:
        self.clsParamList.append( clsParam )
    
    return iPos

  def __str__( self ):
    """ SIP WWW-Authenticate, Proxy-Authenticate 헤더의 값 문자열을 리턴한다.

    Returns:
        string: SIP WWW-Authenticate, Proxy-Authenticate 헤더의 값 문자열을 리턴한다.
    """
    strText = ""
    strText = SetQuoteString( strText, "realm", self.strRealm )
    strText = SetQuoteString( strText, "domain", self.strDomain )
    strText = SetQuoteString( strText, "nonce", self.strNonce )
    strText = SetQuoteString( strText, "opaque", self.strOpaque )
    strText = SetString( strText, "stale", self.strStale )
    strText = SetString( strText, "algorithm", self.strAlgorithm )
    strText = SetString( strText, "qop", self.strQop )

    for clsParam in self.clsParamList:
      strText = SetString( strText, clsParam.strName, clsParam.strValue )
    
    return self.strType + " " + strText

  def Clear( self ):
    """ 멤버 변수를 초기화 시킨다.
    """
    self.strType = ''
    self.strRealm = ''
    self.strDomain = ''
    self.strNonce = ''
    self.strOpaque = ''
    self.strStale = ''
    self.strAlgorithm = ''
    self.strQop = ''
    self.clsParamList.clear()
    
def SetString( strText, strName, strValue ):
  if( len(strValue) == 0 ):
    return strText
  
  if( len(strText) > 0 ):
    strText += ", "

  return strText + strName + "=" + strValue

def SetQuoteString( strText, strName, strValue ):
  if( len(strValue) == 0 ):
    return strText
  
  if( len(strText) > 0 ):
    strText += ", "
  
  return strText + strName + "=\"" + strValue + "\""
  
def ParseSipChallenge( clsList, strText ):
  """ SIP challenge 문자열을 파싱하여서 challenge 리스트에 저장한다.

  Args:
      clsList (list): challenge 리스트
      strText (string): SIP challenge 문자열

  Returns:
      int: 성공하면 파싱한 문자열 길이를 리턴하고 그렇지 않으면 -1 을 리턴한다.
  """
  clsChallenge = SipChallenge()

  iPos = clsChallenge.Parse( strText, 0 )
  if( iPos == -1 ):
    return -1
  
  clsList.append( clsChallenge )

  return iPos
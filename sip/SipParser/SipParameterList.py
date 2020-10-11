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

from .SipParameter import SipParameter

class SipParameterList():
  """ SIP 파라미터 리스트 저장 클래스
  """

  def __init__( self ):
    self.clsParamList = []

  def HeaderListParamParse( self, strText, iStartPos ):
    """ SIP Header 가 , 로 구분되어서 N 개 저장되는 SIP Header 의 parameter list 를 파싱한다.

    Args:
        strText (string): parameter 리스트 문자열
        iStartPos (int): strText 에서 분석을 시작할 위치

    Returns:
        int: 파싱에 성공하면 파싱한 길이를 리턴하고 그렇지 않으면 -1 를 리턴한다.
    """
    iCurPos = iStartPos
    iTextLen = len(strText)

    while( iCurPos < iTextLen ):
      if( strText[iCurPos] == ' ' or strText[iCurPos] == '\t' or strText[iCurPos] == ';' ):
        iCurPos += 1
        continue
      elif( strText[iCurPos] == ',' ):
        break

      iPos = self.ParamParse( strText, iCurPos )
      if( iPos == -1 ):
        return -1
      iCurPos = iPos
    
    return iCurPos

  def ParamParse( self, strText, iStartPos ):
    """ parameter 리스트 문자열을 파싱하여서 parameter 리스트 객체에 저장한다.

    Args:
        strText (string): parameter 리스트 문자열
        iStartPos (int): strText 에서 분석을 시작할 위치

    Returns:
        int: 파싱에 성공하면 파싱한 길이를 리턴하고 그렇지 않으면 -1 를 리턴한다.
    """
    clsParam = SipParameter()
  
    iPos = clsParam.Parse( strText, iStartPos )
    if( iPos == -1 ):
      return -1
    
    self.clsParamList.append( clsParam )

    return iPos

  def InsertParam( self, strName, strValue ):
    """ parameter list 에서 입력된 이름과 값을 저장한다.

    Args:
        strName (string): parameter 이름
        strValue (string): parameter 값
    """
    clsParam = SipParameter()

    clsParam.strName = strName
    clsParam.strValue = strValue

    self.clsParamList.append( clsParam )

  def SelectParam( self, strName ):
    """ parameter list 에서 입력된 이름을 검색한다.

    Args:
        strName (string): parameter 이름

    Returns:
        string: parameter list 에서 입력된 이름이 존재하면 해당 이름의 값 문자열을 리턴하고 그렇지 않으면 공백 문자열을 리턴한다.
    """
    for clsParam in self.clsParamList:
      if( clsParam.strName.lower() == strName ):
        return clsParam.strValue
    
    return ''

  def UpdateParam( self, strName, strValue ):
    """ parameter list 에서 입력된 이름에 대한 값을 수정한다.

    Args:
        strName (string): parameter 이름
        strValue (string): parameter 값

    Returns:
        bool: parameter 이름이 존재하면 true 를 리턴하고 그렇지 않으면 false 를 리턴한다.
    """
    for clsParam in self.clsParamList:
      if( clsParam.strName.lower() == strName ):
        clsParam.strValue = strValue
        return True
    
    return False

  def ClearParam( self ):
    """ SIP 파라미터 리스트를 초기화시킨다.
    """
    self.clsParamList.clear()

  def __str__( self ):
    """ SIP 파라미터 리스트 문자열을 리턴한다.

    Returns:
        string: SIP 파라미터 리스트 문자열을 리턴한다.
    """
    strText = ''

    for clsParam in self.clsParamList:
      strText += ';' + str( clsParam )

    return strText

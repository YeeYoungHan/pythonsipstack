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

from .SipParameterList import SipParameterList

class SipReason( SipParameterList ):
  """ SIP Reason 헤더의 값 저장 클래스

  Args:
      SipParameterList (SipParameterList): SIP 파라미터 리스트 저장 클래스
  """

  def __init__( self ):
    super().__init__()
    self.strProtocol = ''
  
  def Parse( self, strText, iStartPos ):
    """ SIP Reason 헤더의 값을 파싱한다.

    Args:
        strText (string): SIP Reason 헤더의 값을 포함한 문자열
        iStartPos (int): strText 에서 분석을 시작할 위치

    Returns:
        int: 파싱에 성공하면 파싱한 길이를 리턴하고 그렇지 않으면 -1 를 리턴한다.
    """
    self.Clear()

    iPos = iStartPos
    iTextLen = len(strText)
    bParam = False

    while( iPos < iTextLen ):
      if( strText[iPos] == ';' ):
        self.strProtocol = strText[iStartPos:iPos]
        bParam = True
        break
      if( strText[iPos] == ',' ):
        self.strProtocol = strText[iStartPos:iPos]
        break
      iPos += 1
    
    iCurPos = iPos

    if( len(self.strProtocol) == 0 ):
      self.strProtocol = strText[iStartPos:iCurPos]
    
    if( bParam ):
      iPos = super().HeaderListParamParse( strText, iCurPos )
      if( iPos == -1 ):
        return -1
      iCurPos = iPos

      for clsParam in super().clsParamList:
        if( len(clsParam.strValue) > 0 and clsParam.strValue[0] == '"' ):
          clsParam.strValue.replace( '"', '' )
    
    return iCurPos

  def __str__( self ):
    """ SIP Reason 헤더의 값 문자열을 리턴한다.

    Returns:
        string: SIP Reason 헤더의 값 문자열을 리턴한다.
    """
    return self.strProtocol + super().__str__()

  def Clear( self ):
    """ 멤버 변수를 초기화 시킨다.
    """
    self.strProtocol = ''
    super().ClearParam()
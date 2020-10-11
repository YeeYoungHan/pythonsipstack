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

class SipContentType(SipParameterList):

  def __init__( self ):
    super().__init__()
    self.strType = ''
    self.strSubType = ''
  
  def Parse( self, strText, iStartPos ):
    """ SIP Content-Type 헤더의 값을 파싱한다.

    Args:
        strText (string): SIP Content-Type 헤더의 값을 포함한 문자열
        iStartPos (int): strText 에서 분석을 시작할 위치
    """
    self.Clear()

    iPos = iStartPos
    iTextLen = len(strText)
    iSubTypePos = -1
    iParamPos = -1

    while( iPos < iTextLen ):
      if( strText[iPos] == '/' ):
        self.strType = strText[iStartPos:iPos]
        iSubTypePos = iPos + 1
      elif( iSubTypePos != -1 ):
        if( strText[iPos] == ';' or strText[iPos] == ',' ):
          self.strSubType = strText[iSubTypePos:iPos]
          iParamPos = iPos + 1
          break
      elif( strText[iPos] == ',' ):
        break
      
      iPos += 1
    
    if( len(self.strType) == 0 ):
      self.strType = strText[iStartPos:]
    elif( iSubTypePos != -1 and len(self.strSubType) == 0 ):
      self.strSubType = strText[iSubTypePos:]
    
    if( iParamPos != -1 ):
      super().HeaderListParamParse( strText, iParamPos )


  def __str__( self ):
    """ SIP Content-Type 헤더의 값 문자열을 리턴한다.

    Returns:
        string: SIP Content-Type 헤더의 값 문자열을 리턴한다.
    """
    return self.strType + "/" + self.strSubType + super().__str__()

  def Clear( self ):
    """ 멤버 변수를 초기화 시킨다.
    """
    self.strType = ''
    self.strSubType = ''
    super().ClearParam()

  def IsEqual( self, strType, strSubType ):
    """ 입력된 type, subtype 과 현재 객체의 값이 일치하는지 검사한다.

    Args:
        strType (string): type 문자열
        strSubType (string): subtype 문자열

    Returns:
        bool: 입력된 type, subtype 과 현재 객체의 값이 일치하면 True 를 리턴하고 그렇지 않으면 False 를 리턴한다.
    """
    if( self.strType == strType and self.strSubType == strSubType ):
      return True
    
    return False

  def Empty( self ):
    """ 멤버 변수에 값이 저장되지 않았는지 검사한다.

    Returns:
        bool: 멤버 변수에 값이 저장되지 않았으면 True 를 리턴하고 그렇지 않으면 False 를 리턴한다.
    """
    if( len(self.strType) == 0 or len(self.strSubType) == 0 ):
      return True

    return False
  
  def Set( self, strType, strSubType ):
    """ 입력된 type, subtype 과 현재 객체의 값을 저장한다.

    Args:
        strType (string): type 문자열
        strSubType (string): subtype 문자열
    """
    self.strType = strType
    self.strSubType = strSubType
  
  def __eq__( self, clsContentType ):
    """ SIP Content-Type 객체가 동일한 값을 저장하고 있는지 검사한다.

    Args:
        clsCallId (SipContentType): SIP Content-Type 객체

    Returns:
        bool: SIP Content-Type 객체가 동일한 값을 가지고 있다면 True 를 리턴하고 그렇지 않으면 False 를 리턴한다.
    """
    if( self.strType == clsContentType.strType and self.strSubType == clsContentType.strSubType ):
      return True
    
    return False

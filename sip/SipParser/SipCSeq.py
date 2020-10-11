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

class SipCSeq():
  """ SIP CSeq 헤더의 값을 저장하는 클래스
  """

  def __init__( self ):
    self.iDigit = -1
    self.strMethod = ''
  
  def Parse( self, strText, iStartPos ):
    """ SIP CSeq 헤더의 값을 파싱한다.

    Args:
        strText (string): SIP CSeq 헤더의 값을 포함한 문자열
        iStartPos (int): strText 에서 분석을 시작할 위치
    """
    self.Clear()

    iPos = iStartPos
    iTextLen = len(strText)

    while( iPos < iTextLen ):
      if( self.iDigit == -1 ):
        if( strText[iPos] == ' ' ):
          strDigit = strText[iStartPos:iPos]
          self.iDigit = int( strDigit )
      elif( strText[iPos] == ' ' or strText[iPos] == '\t' ):
        iPos += 1
        continue
      else:
        self.strMethod = strText[iPos:]
        break

      iPos += 1

  def __str__( self ):
    """ SIP CSeq 헤더의 값 문자열을 리턴한다.

    Returns:
        string: SIP CSeq 헤더의 값 문자열을 리턴한다.
    """
    return str(self.iDigit) + " " + self.strMethod
  
  def Clear( self ):
    """ 멤버 변수를 초기화 시킨다.
    """
    self.iDigit = -1
    self.strMethod = ''
  
  def Empty( self ):
    """ 멤버 변수에 값이 저장되지 않았는지 검사한다.

    Returns:
        bool: 멤버 변수에 값이 저장되지 않았으면 True 를 리턴하고 그렇지 않으면 False 를 리턴한다.
    """
    if( self.iDigit == -1 ):
      return True
    
    return False

  def Set( self, iDigit, strMethod ):
    """ 입력된 숫자 및 메소드 문자열로 멤버 변수에 저장한다.

    Args:
        iDigit (int): 숫자
        strMethod (string): 메소드 이름
    """
    self.iDigit = iDigit
    self.strMethod = strMethod
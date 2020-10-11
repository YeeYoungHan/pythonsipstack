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

class SipParameter():

  def __init__( self ):
    self.strName = ''
    self.strValue = ''

  def Parse( self, strText, iStartPos ):
    """ SIP 파라미터 이름, 값을 파싱한다.

    Args:
        strText (string): SIP 파라미터 이름, 값을 포함한 문자열
        iStartPos (int): strText 에서 분석을 시작할 위치

    Returns:
        int: 파싱에 성공하면 파싱한 길이를 리턴하고 그렇지 않으면 -1 를 리턴한다.
    """
    self.Clear()

    iPos = iStartPos
    iValuePos = -1
    iTextLen = len(strText)
    bStartQuote = False

    while( iPos < iTextLen ):
      if( strText[iPos] == '"' ):
        if( bStartQuote ):
          bStartQuote = False
        else:
          bStartQuote = True
      elif( strText[iPos] == '=' ):
        if( bStartQuote ):
          continue
        self.strName = strText[iStartPos:iPos]
        iValuePos = iPos + 1
      elif( strText[iPos] == ',' or strText[iPos] == ';' or strText[iPos] == '&' or strText[iPos] == '?' ):
        if( bStartQuote ):
          continue
        break
      elif( strText[iPos] == '\r' ):
        break

      iPos += 1

    if( iPos > iStartPos ):
      if( iValuePos != -1 ):
        self.strValue = strText[iValuePos:iPos]
      else:
        self.strName = strText[iStartPos:iPos]
      return iPos
    
    return -1

  def __str__( self ):
    """ SIP 파라미터 이름, 값 문자열을 리턴한다.

    Returns:
        string: SIP 파라미터 이름, 값 문자열을 리턴한다.
    """
    if( len(self.strName) == 0 ):
      return ""

    if( len(self.strValue) == 0 ):
      return self.strName
    
    return self.strName + "=" + self.strValue

  def Clear( self ):
    """ 멤버 변수를 초기화 시킨다.
    """
    self.strName = ''
    self.strValue = ''


def ParseSipParameter( clsList, strText, iStartPos ):
  """ parameter 리스트 문자열을 파싱하여서 parameter 리스트 객체에 저장한다.

  Args:
      clsList (list): parameter 리스트 객체
      strText (string): parameter 리스트 문자열
      iStartPos (int): strText 에서 분석을 시작할 위치

  Returns:
      [type]: [description]
  """
  clsParam = SipParameter()
  
  iPos = clsParam.Parse( strText, iStartPos )
  if( iPos == -1 ):
    return -1
  
  clsList.append( clsParam )

  return iPos

def SearchSipParameter( clsList, strName ):
  """ parameter 리스트에서 parameter 이름에 대한 값을 검색한다.

  Args:
      clsList (list): parameter 리스트 객체
      strName (string): parameter 이름

  Returns:
      string: parameter 리스트에서 parameter 이름이 존재하면 해당 parameter 의 값을 리턴하고 그렇지 않으면 공백 문자열을 리턴한다.
  """
  for clsParam in clsList:
    if( clsParam.strName == strName ):
      return clsParam.strValue
  
  return ''

def InsertSipParameter( clsList, strName, strValue ):
  """ parameter 리스트에 paramter 를 추가한다.

  Args:
      clsList (list): parameter 리스트 객체
      strName (string): parameter 이름
      strValue (string): parameter 값
  """
  clsParam = SipParameter()

  clsParam.strName = strName
  clsParam.strValue = strValue

  clsList.append( clsParam )

def MakeSipParameterString( clsList ):
  """ parameter 리스트 객체를 parameter 리스트 문자열로 생성하여 리턴한다.

  Args:
      clsList (list): parameter 리스트 객체

  Returns:
      string: parameter 리스트 문자열의 길이를 리턴한다.
  """
  strText = ''

  for clsParam in clsList:
    strText += ';' + str( clsParam )

  return strText

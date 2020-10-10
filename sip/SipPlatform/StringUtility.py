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

import os

def DeQuoteString( strInput ):
  """ 문자열의 시작과 끝에 " 가 존재하면 문자열의 시작과 끝의 " 를 제거한 문자열을 리턴한다.

  Args:
      strInput (string): 문자열

  Returns:
      string: 문자열의 시작과 끝의 " 를 제거한 문자열을 리턴한다.
  """
  iLen = len(strInput)

  if( iLen > 0 ):
    if( strInput[0] != '"' or strInput[iLen-1] != '"' ):
      return strInput
    else:
      return strInput[1:iLen-1]
  
  return ''
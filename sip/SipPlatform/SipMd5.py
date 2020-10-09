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

import hashlib

def SipMd5String( strInput ):
  """ 입력된 문자열을 MD5 로 변환한 후, HEX 문자열을 생성하여서 리턴한다.

  Args:
      strInput (string): 입력 문자열

  Returns:
      string: 입력된 문자열을 MD5 연산후, HEX 로 변환한 문자열을 리턴한다.
  """
  clsMd5 = hashlib.md5()
  clsMd5.update( strInput.encode() )
  strMd5 = clsMd5.hexdigest()

  return strMd5

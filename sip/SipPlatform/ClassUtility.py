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

def HasMethod( clsObject, strMethod ):
  """ 객체에 메소드가 존재하는지 확인한다.

  Args:
      clsObject (object): 객체
      strMethod (string): 메소드 이름

  Returns:
      bool: 객체에 메소드가 존재하면 True 를 리턴하고 그렇지 않으면 False 를 리턴한다.
  """
  return callable( getattr( clsObject, strMethod, None ) )

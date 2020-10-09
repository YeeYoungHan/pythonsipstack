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

import threading

class SafeCount():
  """ thread safe 하게 숫자를 +1 증가하고 -1 감소할 수 있는 클래스
  """

  def __init__( self ):
    self.clsMutex = threading.Lock()
    self.iCount = 0
  
  def Increase( self ):
    """ +1 증가시킨다.
    """
    self.clsMutex.acquire()
    self.iCount += 1
    self.clsMutex.release()
  
  def Decrease( self ):
    """ -1 감소시킨다.
    """
    self.clsMutex.acquire()
    self.iCount -= 1
    self.clsMutex.release()
  
  def GetCount( self ):
    """ 현재 숫자를 리턴한다.

    Returns:
        int: 현재 숫자를 리턴한다.
    """
    self.clsMutex.acquire()
    iCount = self.iCount
    self.clsMutex.release()

    return iCount
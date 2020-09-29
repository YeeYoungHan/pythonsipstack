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

from datetime import datetime
import os
import threading
import platform

class LogLevel():
  ERROR = 0x0001
  INFO = 0x0010
  DEBUG = 0x0100
  NETWORK = 0x0200
  SYSTEM = 0x0400

class Log():

  strDirName = ''
  strDate = ''
  iLevel = LogLevel.ERROR | LogLevel.SYSTEM
  bOpen = False
  iIndex = 1
  iLogSize = 0
  iMaxLogSize = 10000000
  bWindow = False
  clsMutex = threading.Lock()

  @classmethod
  def SetDirectory( cls, strDirName ):
    if( os.path.isdir( strDirName ) == False ):
      os.mkdir( strDirName )
    cls.strDirName = strDirName
    if( platform.system() == 'Windows' ):
      cls.bWindow = True

  @classmethod
  def Print( cls, eLevel, strText ):
    if( ( cls.iLevel & eLevel ) == 0 ):
      return
    
    if( eLevel == LogLevel.ERROR ):
      strHeader = "[ERROR] "
    elif( eLevel == LogLevel.INFO ):
      strHeader = "[INFO] "
    elif( eLevel == LogLevel.DEBUG ):
      strHeader = "[DEBUG] "
    elif( eLevel == LogLevel.NETWORK ):
      strHeader = "[NETWORK] "
    elif( eLevel == LogLevel.SYSTEM ):
      strHeader = "[SYSTEM] "
    
    clsTime = datetime.now()
    strDate = clsTime.strftime("%Y%m%d")
    strTime = clsTime.strftime("%H:%M:%S.%f")

    strLog = "[" + strTime + "] " + strHeader + "[" + str(threading.get_ident()) + "] " + strText

    if( len(cls.strDirName) > 0 ):
      if( cls.bWindow ):
        strLog += "\r\n"
      else:
        strLog += "\n"

      bOpen = False

      cls.clsMutex.acquire()

      if( cls.strDate != strDate ):
        cls.iIndex = 1
        bOpen = True
      elif( cls.iLogSize > cls.iMaxLogSize ):
        cls.iIndex += 1
        bOpen = True
      
      if( bOpen ):
        if( cls.bOpen ):
          cls.fd.close()
          cls.bOpen = False
          cls.iLogSize = 0

        strFileName = cls.strDirName + "/" + strDate + "_" + str(cls.iIndex) + ".txt"

        cls.fd = open( strFileName, "ab" )
        cls.bOpen = True
      
      arrBuf = strLog.encode()

      cls.iLogSize = len( arrBuf )
      cls.fd.write( arrBuf )
      cls.fd.flush()

      cls.clsMutex.release()
    else:
      print( strLog )

  @classmethod
  def SetLevel( cls, iLevel ):
    cls.iLevel = LogLevel.ERROR | LogLevel.SYSTEM
    cls.iLevel |= iLevel

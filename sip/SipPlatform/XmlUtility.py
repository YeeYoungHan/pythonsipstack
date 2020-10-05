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

def XmlGetDataString( clsParent, strName, strValue ):
  clsChild = clsParent.find( strName )
  if( clsChild != None ):
    return clsChild.text
  
  return strValue

def XmlGetDataInt( clsParent, strName, iValue ):
  clsChild = clsParent.find( strName )
  if( clsChild != None ):
    return int(clsChild.text)
  
  return iValue

def XmlGetDataBool( clsParent, strName, bValue ):
  clsChild = clsParent.find( strName )
  if( clsChild != None and clsChild.text.lower() == "true" ):
    return True
  
  return bValue

def XmlGetAttrString( clsNode, strName, strValue ):
  strAttr = clsNode.attrib.get( strName )
  if( strAttr != None ):
    return strAttr
  
  return strValue

def XmlGetAttrInt( clsNode, strName, iValue ):
  strAttr = clsNode.attrib.get( strName )
  if( strAttr != None ):
    return int(strAttr)
  
  return iValue

def XmlGetAttrBool( clsNode, strName, bValue ):
  strAttr = clsNode.attrib.get( strName )
  if( strAttr != None and strAttr.lower() == "true" ):
    return True
  
  return bValue
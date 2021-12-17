# Copyright (C) 2020 U S Σ R Δ T O R
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.
#

from userbot import LOGS
from telethon.tl.types import DocumentAttributeFilename 

def __list_all_modules():
    from os.path import dirname, basename, isfile
    import glob

    mod_paths = glob.glob(dirname(__file__) + "/*.py")
    all_modules = [
        basename(f)[:-3] for f in mod_paths
        if isfile(f) and f.endswith(".py") and not f.endswith("__init__.py")
    ]
    return all_modules


ALL_MODULES = sorted(__list_all_modules())
LOGS.info("Yüklənəcək modullar: %s", str(ALL_MODULES))
__all__ = ALL_MODULES + ["ALL_MODULES"]


async def MEDIACHECK(reply): 
 type = "img" 
 if reply and reply.media: 
  if reply.photo: 
   data = reply.photo 
  elif reply.document: 
   if DocumentAttributeFilename(file_name='AnimatedSticker.tgs') in reply.media.document.attributes: 
    return False 
   if reply.gif or reply.video: 
    type = "vid" 
   if reply.audio or reply.voice: 
    return False 
   data = reply.media.document 
  else: 
   return False 
 else: 
  return False 
 if not data or data is None: 
  return False 
 else: 
  return (data, type)

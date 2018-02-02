# -*- coding: UTF-8 -*-
import win32gui as w32
hwnd=w32.FindWindow(None,u"阴阳师-网易游戏")
print w32.GetWindowRect(hwnd)
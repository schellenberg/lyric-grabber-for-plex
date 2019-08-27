# -*- coding: utf-8 -*-

###########################################################################
## Python code generated with wxFormBuilder (version Oct 26 2018)
## http://www.wxformbuilder.org/
##
## PLEASE DO *NOT* EDIT THIS FILE!
###########################################################################

import wx
import wx.xrc

###########################################################################
## Class frameMain
###########################################################################

class frameMain ( wx.Frame ):

	def __init__( self, parent ):
		wx.Frame.__init__ ( self, parent, id = wx.ID_ANY, title = u"Plex Lyric Grabber", pos = wx.DefaultPosition, size = wx.Size( 800,600 ), style = wx.CAPTION|wx.CLOSE_BOX|wx.SYSTEM_MENU|wx.TAB_TRAVERSAL )

		self.SetSizeHints( wx.DefaultSize, wx.DefaultSize )

		bSizerFrameMain = wx.BoxSizer( wx.VERTICAL )

		bSizerMainFrame = wx.BoxSizer( wx.VERTICAL )

		self.m_panelMain = wx.Panel( self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL )
		bSizerMainPanel = wx.BoxSizer( wx.VERTICAL )

		bSizerPanelMain = wx.BoxSizer( wx.VERTICAL )

		bSizerFolderSelect = wx.BoxSizer( wx.VERTICAL )

		self.m_staticTextInstructions = wx.StaticText( self.m_panelMain, wx.ID_ANY, u"Select your Plex music library folder...", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticTextInstructions.Wrap( -1 )

		bSizerFolderSelect.Add( self.m_staticTextInstructions, 0, wx.ALL|wx.ALIGN_CENTER_HORIZONTAL, 5 )

		self.m_dirPicker1 = wx.DirPickerCtrl( self.m_panelMain, wx.ID_ANY, wx.EmptyString, u"Select a folder", wx.DefaultPosition, wx.DefaultSize, wx.DIRP_DEFAULT_STYLE )
		bSizerFolderSelect.Add( self.m_dirPicker1, 0, wx.ALL|wx.ALIGN_CENTER_HORIZONTAL, 5 )

		self.m_buttonSearch = wx.Button( self.m_panelMain, wx.ID_ANY, u"Begin Lyric Search", wx.DefaultPosition, wx.DefaultSize, 0 )
		bSizerFolderSelect.Add( self.m_buttonSearch, 0, wx.ALL|wx.ALIGN_CENTER_HORIZONTAL, 5 )

		self.m_staticTextTimeWarning = wx.StaticText( self.m_panelMain, wx.ID_ANY, u"Note that selecting a large folder of music can cause the search to take a very long time...", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticTextTimeWarning.Wrap( -1 )

		self.m_staticTextTimeWarning.SetFont( wx.Font( wx.NORMAL_FONT.GetPointSize(), wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_ITALIC, wx.FONTWEIGHT_NORMAL, False, wx.EmptyString ) )

		bSizerFolderSelect.Add( self.m_staticTextTimeWarning, 0, wx.ALL|wx.ALIGN_CENTER_HORIZONTAL, 5 )


		bSizerFolderSelect.Add( ( 0, 30), 0, 0, 5 )

		self.m_staticText6 = wx.StaticText( self.m_panelMain, wx.ID_ANY, u"Log", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText6.Wrap( -1 )

		self.m_staticText6.SetFont( wx.Font( wx.NORMAL_FONT.GetPointSize(), wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD, False, wx.EmptyString ) )

		bSizerFolderSelect.Add( self.m_staticText6, 0, wx.ALL|wx.ALIGN_CENTER_HORIZONTAL, 5 )

		self.m_staticTextLog = wx.StaticText( self.m_panelMain, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.Size( 750,365 ), 0 )
		self.m_staticTextLog.Wrap( -1 )

		bSizerFolderSelect.Add( self.m_staticTextLog, 0, wx.ALL|wx.ALIGN_CENTER_HORIZONTAL, 5 )


		bSizerPanelMain.Add( bSizerFolderSelect, 1, wx.EXPAND, 5 )


		bSizerMainPanel.Add( bSizerPanelMain, 1, wx.ALL|wx.EXPAND, 0 )


		self.m_panelMain.SetSizer( bSizerMainPanel )
		self.m_panelMain.Layout()
		bSizerMainPanel.Fit( self.m_panelMain )
		bSizerMainFrame.Add( self.m_panelMain, 1, wx.EXPAND|wx.ALL, 0 )


		bSizerFrameMain.Add( bSizerMainFrame, 1, wx.ALL|wx.EXPAND, 0 )


		self.SetSizer( bSizerFrameMain )
		self.Layout()

		self.Centre( wx.BOTH )

	def __del__( self ):
		pass



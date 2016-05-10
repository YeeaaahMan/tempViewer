# -*- coding: utf-8 -*-
import wx
import wx.xrc
import wx.aui
import wxmplot
import gpuz, coretemp

def msg(s, panel):
    pass

def spl1t_proc_name(text):
    a = text.split(u" ")
    result = []
    for i in range(0,5,2):
        result.append(u" ".join(a[i:i+2]))
    return u"\n".join(result)

class MainFrame ( wx.Frame ):

    def __init__( self, parent ):
        wx.Frame.__init__ ( self, parent, id = wx.ID_ANY, title = u"tempViewer", pos = wx.DefaultPosition, size = wx.Size( 1260,800 ), style = wx.DEFAULT_FRAME_STYLE|wx.TAB_TRAVERSAL )

        self.SetSizeHintsSz( wx.DefaultSize, wx.DefaultSize )

        bSizerMain = wx.BoxSizer( wx.VERTICAL )

        self.m_panel = wx.Panel( self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL )
        bSizerPanel = wx.BoxSizer( wx.VERTICAL )

        self.m_auiNB = wx.aui.AuiNotebook( self.m_panel, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.aui.AUI_NB_DEFAULT_STYLE|wx.NO_BORDER )

        bSizerPanel.Add( self.m_auiNB, 1, wx.EXPAND|wx.ALL, 5 )

        bSizerLower = wx.BoxSizer( wx.HORIZONTAL )

        self.openFile_button = wx.Button( self.m_panel, wx.ID_ANY, u"Open File", wx.DefaultPosition, wx.DefaultSize, 0 )
        bSizerLower.Add( self.openFile_button, 0, wx.ALL, 5 )

        self.chooseFile_button = wx.Button(self.m_panel, wx.ID_ANY, u"Choose file", wx.DefaultPosition, wx.DefaultSize, 0 )
        bSizerLower.Add( self.chooseFile_button, 0, wx.ALL, 5 )

        bSizerPanel.Add( bSizerLower, 0, wx.EXPAND, 5)

        self.m_panel.SetSizer( bSizerPanel )
        self.m_panel.Layout()
        bSizerPanel.Fit( self.m_panel )
        bSizerMain.Add( self.m_panel, 1, wx.EXPAND, 5 )


        self.SetSizer( bSizerMain )
        self.Layout()
        self.m_statusBar = self.CreateStatusBar( 1, wx.ST_SIZEGRIP, wx.ID_ANY )

        self.Centre( wx.BOTH )

        # Connect Events
        self.openFile_button.Bind( wx.EVT_BUTTON, self.openFile )
        self.chooseFile_button.Bind(wx.EVT_BUTTON, self.OnOpen )

    def __del__( self ):
        pass


    # Virtual event handlers, overide them in your derived class
    def openFile( self, event ):
        new_page = CoreTempPanel(myApp.main_frame.m_auiNB)
        myApp.main_frame.m_auiNB.AddPage(new_page, u"CoreTemp")
        new_page = GPUzPanel(myApp.main_frame.m_auiNB)
        myApp.main_frame.m_auiNB.AddPage(new_page, u"GPU-Z")

    def OnOpen(self, event):

        openFileDialog = wx.FileDialog(self, "Open CoreTemp/GPU-Z log-file or ZIP-archive", "", "",
                                       "CT/GPU-Z files (*.csv,*.txt)|*.csv;*.txt", wx.FD_OPEN | wx.FD_FILE_MUST_EXIST)

        if openFileDialog.ShowModal() == wx.ID_CANCEL:
            return     # the user changed idea...

        File_Path = openFileDialog.GetPath()
        File_Name = File_Path.split("\\")[-1]
        if File_Name[-3:] == "csv":
            new_page = CoreTempPanel(myApp.main_frame.m_auiNB, file_path = File_Path)
        elif File_Name[-3:] == "txt":
            new_page = GPUzPanel(myApp.main_frame.m_auiNB, file_path = File_Path)
        myApp.main_frame.m_auiNB.AddPage(new_page, File_Name, select=True)


class GPUzPanel ( wx.Panel ):

    def __init__( self, parent , file_path="GPU-Z Sensor Log.txt"):
        wx.Panel.__init__ ( self, parent, id = wx.ID_ANY, pos = wx.DefaultPosition, size = wx.Size( 500,300 ), style = wx.TAB_TRAVERSAL )
        self.S = gpuz.open_gpuz(file_path)

        bSizerMain = wx.BoxSizer( wx.VERTICAL )

        self.m_scrolledWindow1 = wx.ScrolledWindow( self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.HSCROLL|wx.VSCROLL )
        self.m_scrolledWindow1.SetScrollRate( 5, 5 )
        bSizerList = wx.BoxSizer( wx.VERTICAL )

        """
        self.example_button = wx.Button( self.m_scrolledWindow1, wx.ID_ANY, u"GPUZs", wx.DefaultPosition, wx.DefaultSize, 0 )
        bSizerList.Add( self.example_button, 0, wx.ALL, 5 )
        """
        for dimension in [u'\xb0C', u'MHz', u'GPU Load [%]', u'RPM']:
            for item in self.S["index"][1:]:
                if dimension in item:
                    Y = self.S["sensors"][item]
                    Y[0] = 0
                    self.graph_panel = wxmplot.PlotPanel(self.m_scrolledWindow1, size=(1200, 230), fontsize=6,  messenger = msg)
                    self.graph_panel.plot( self.S["sensors"]["Date"], Y, use_dates=True, title= item)
                    bSizerList.Add( self.graph_panel, 0, wx.ALL, 5 )

        self.m_scrolledWindow1.SetSizer( bSizerList )
        self.m_scrolledWindow1.Layout()
        bSizerList.Fit( self.m_scrolledWindow1 )
        bSizerMain.Add( self.m_scrolledWindow1, 1, wx.EXPAND, 5 )


        self.SetSizer( bSizerMain )
        self.Layout()

    def __del__( self ):
        pass

class CoreTempPanel ( wx.Panel ):

    def __init__( self, parent, file_path="CT-Log 2016-04-02 01-15-54.csv"):
        wx.Panel.__init__ ( self, parent, id = wx.ID_ANY, pos = wx.DefaultPosition, size = wx.Size( 500,-1 ), style = wx.TAB_TRAVERSAL )
        self.S = coretemp.open_coretemp(file_path)

        bSizerMain = wx.BoxSizer( wx.HORIZONTAL )

        sbSizerInfo = wx.StaticBoxSizer( wx.StaticBox( self, wx.ID_ANY, u"Info" ), wx.VERTICAL )

        """for item in sorted(self.S["info"].keys()):
            if item != u"Processor:":
                self.m_staticText1 = wx.StaticText( sbSizerInfo.GetStaticBox(), wx.ID_ANY, u"{0} {1}".format(item, self.S["info"][item]), wx.DefaultPosition, wx.DefaultSize, 0 )
                self.m_staticText1.Wrap( -1 )
                sbSizerInfo.Add( self.m_staticText1, 0, wx.BOTTOM|wx.RIGHT|wx.LEFT, 10 )
            else:
                self.m_staticText11 = wx.StaticText( sbSizerInfo.GetStaticBox(), wx.ID_ANY, item, wx.DefaultPosition, wx.DefaultSize, 0 )
                self.m_staticText11.Wrap( -1 )
                sbSizerInfo.Add( self.m_staticText11, 0, wx.RIGHT|wx.LEFT, 10 )

                self.m_hyperlink11 = wx.HyperlinkCtrl( sbSizerInfo.GetStaticBox(), wx.ID_ANY, self.S["info"][item], u"https://www.google.by/search?q={0} cpu world".format(self.S["info"][item]), wx.DefaultPosition, wx.DefaultSize, wx.HL_DEFAULT_STYLE )
                sbSizerInfo.Add( self.m_hyperlink11, 0, wx.BOTTOM|wx.RIGHT|wx.LEFT, 10 )
        """
        # CPUID:
        self.m_staticText1 = wx.StaticText( sbSizerInfo.GetStaticBox(), wx.ID_ANY, u"{0} {1}".format(u"CPUID:", self.S["info"][u"CPUID:"]), wx.DefaultPosition, wx.DefaultSize, 0 )
        self.m_staticText1.Wrap( -1 )
        sbSizerInfo.Add( self.m_staticText1, 0, wx.BOTTOM|wx.RIGHT|wx.LEFT, 5 )

        # Processor:
        self.m_staticText11 = wx.StaticText( sbSizerInfo.GetStaticBox(), wx.ID_ANY, u"Processor:", wx.DefaultPosition, wx.DefaultSize, 0 )
        self.m_staticText11.Wrap( -1 )
        sbSizerInfo.Add( self.m_staticText11, 0, wx.RIGHT|wx.LEFT, 5 )
        self.m_hyperlink11 = wx.HyperlinkCtrl( sbSizerInfo.GetStaticBox(), wx.ID_ANY, spl1t_proc_name(self.S["info"][u"Processor:"]), u"https://www.google.by/search?q={0} cpu world".format(self.S["info"][u"Processor:"]), wx.DefaultPosition, wx.DefaultSize, wx.HL_DEFAULT_STYLE )
        sbSizerInfo.Add( self.m_hyperlink11, 0, wx.BOTTOM|wx.RIGHT|wx.LEFT, 5 )

        # Platform:,LGA 775 (Socket T)
        self.m_staticText1 = wx.StaticText( sbSizerInfo.GetStaticBox(), wx.ID_ANY, u"{0}\n{1}".format(u"Platform:", self.S["info"][u"Platform:"]), wx.DefaultPosition, wx.DefaultSize, 0 )
        self.m_staticText1.Wrap( -1 )
        sbSizerInfo.Add( self.m_staticText1, 0, wx.BOTTOM|wx.RIGHT|wx.LEFT, 5 )

        # Revision:
        self.m_staticText1 = wx.StaticText( sbSizerInfo.GetStaticBox(), wx.ID_ANY, u"{0} {1}".format(u"Revision:", self.S["info"][u"Revision:"]), wx.DefaultPosition, wx.DefaultSize, 0 )
        self.m_staticText1.Wrap( -1 )
        sbSizerInfo.Add( self.m_staticText1, 0, wx.BOTTOM|wx.RIGHT|wx.LEFT, 5 )

        # Lithography:
        self.m_staticText1 = wx.StaticText( sbSizerInfo.GetStaticBox(), wx.ID_ANY, u"{0} {1}".format(u"Lithography:", self.S["info"][u"Lithography:"]), wx.DefaultPosition, wx.DefaultSize, 0 )
        self.m_staticText1.Wrap( -1 )
        sbSizerInfo.Add( self.m_staticText1, 0, wx.BOTTOM|wx.RIGHT|wx.LEFT, 5 )

        # Session start:
        self.m_staticText1 = wx.StaticText( sbSizerInfo.GetStaticBox(), wx.ID_ANY, u"{0}\n{1}".format(u"Session start:", self.S["info"][u"Session start:"]), wx.DefaultPosition, wx.DefaultSize, 0 )
        self.m_staticText1.Wrap( -1 )
        sbSizerInfo.Add( self.m_staticText1, 0, wx.BOTTOM|wx.RIGHT|wx.LEFT, 5 )

        # Session end:
        if u"Session end:" in self.S["info"]:
            self.m_staticText1 = wx.StaticText( sbSizerInfo.GetStaticBox(), wx.ID_ANY, u"{0}\n{1}".format(u"Session end:", self.S["info"][u"Session end:"]), wx.DefaultPosition, wx.DefaultSize, 0 )
        else:
            self.m_staticText1 = wx.StaticText( sbSizerInfo.GetStaticBox(), wx.ID_ANY, u"{0}\n{1}".format(u"Session end:", u"Report interrupted."), wx.DefaultPosition, wx.DefaultSize, 0 )
        self.m_staticText1.Wrap( -1 )
        sbSizerInfo.Add( self.m_staticText1, 0, wx.BOTTOM|wx.RIGHT|wx.LEFT, 5 )


        bSizerMain.Add( sbSizerInfo, 0, wx.EXPAND|wx.ALL, 5 )

        bSizerLeft = wx.BoxSizer( wx.VERTICAL )

        self.m_scrolledWindow1 = wx.ScrolledWindow( self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.HSCROLL|wx.VSCROLL )
        self.m_scrolledWindow1.SetScrollRate( 5, 5 )
        bSizerList = wx.BoxSizer( wx.VERTICAL )

        bSizerHor = wx.BoxSizer( wx.HORIZONTAL )
        for core in self.S["core"]:
            Y = self.S["sensors"][core][u'Temp. (\xb0)']
            Y[0] = 0
            self.graph_panel = wxmplot.PlotPanel(self.m_scrolledWindow1, size=(500, 250), fontsize=6,  messenger = msg)
            self.graph_panel.plot( self.S["Time"], Y, use_dates=True, title= core + ' '+ u'Temp. (\xb0)')
            bSizerHor.Add( self.graph_panel, 0, wx.ALL, 5 )
        bSizerList.Add( bSizerHor, 0, wx.EXPAND, 5 )

        bSizerHor = wx.BoxSizer( wx.HORIZONTAL )
        for core in self.S["core"]:
            Y = self.S["sensors"][core][u'Core load (%)']
            Y[0] = 0
            self.graph_panel = wxmplot.PlotPanel(self.m_scrolledWindow1, size=(500, 250), fontsize=6, messenger = msg)
            self.graph_panel.plot( self.S["Time"], Y, use_dates=True, title= core + ' '+ u'Core load (%)')
            bSizerHor.Add( self.graph_panel, 0, wx.ALL, 5 )
        bSizerList.Add( bSizerHor, 0, wx.EXPAND, 5 )

        bSizerHor = wx.BoxSizer( wx.HORIZONTAL )
        for core in self.S["core"]:
            Y = self.S["sensors"][core][u'Core speed (MHz)']
            Y[0] = 0
            self.graph_panel = wxmplot.PlotPanel(self.m_scrolledWindow1, size=(500, 250), fontsize=6, messenger = msg)
            self.graph_panel.plot( self.S["Time"], Y, use_dates=True, title= core + ' '+ u'Core speed (MHz)')
            bSizerHor.Add( self.graph_panel, 0, wx.ALL, 5 )
        bSizerList.Add( bSizerHor, 0, wx.EXPAND, 5 )
        """
        self.example_button = wx.Button( self.m_scrolledWindow1, wx.ID_ANY, u"CoreTempS", wx.DefaultPosition, wx.Size( -1,300 ), 0 )
        bSizerList.Add( self.example_button, 0, wx.ALL, 5 )

        self.example_button1 = wx.Button( self.m_scrolledWindow1, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.Size( -1,300 ), 0 )
        bSizerList.Add( self.example_button1, 0, wx.ALL, 5 )
        """

        self.m_scrolledWindow1.SetSizer( bSizerList )
        self.m_scrolledWindow1.Layout()
        bSizerList.Fit( self.m_scrolledWindow1 )
        bSizerLeft.Add( self.m_scrolledWindow1, 1, wx.EXPAND, 5 )


        bSizerMain.Add( bSizerLeft, 1, wx.EXPAND, 5 )


        self.SetSizer( bSizerMain )
        self.Layout()

    def __del__( self ):
        pass


class myApp(wx.App):
    """ app"""
    def __init__(self, redirect=True):
        wx.App.__init__(self, redirect)

    def OnInit(self):
        self.main_frame = MainFrame(parent=None)
        self.main_frame.Show()
        #self.settings = MyFrame2(parent=None)
        self.SetTopWindow(self.main_frame)
        return True


if __name__ == '__main__':
    # (1) Text redirection starts here
    myApp = myApp(redirect=True)
    # (2) The main event loop is entered here
    myApp.MainLoop()
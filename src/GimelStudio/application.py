## ----------------------------------------------------------------------------
## Gimel Studio Copyright 2020 Noah Rahm, Correct Syntax. All rights reserved.
##
## Licensed under the Apache License, Version 2.0 (the "License");
## you may not use this file except in compliance with the License.
## You may obtain a copy of the License at
##
##    http://www.apache.org/licenses/LICENSE-2.0
##
## Unless required by applicable law or agreed to in writing, software
## distributed under the License is distributed on an "AS IS" BASIS,
## WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
## See the License for the specific language governing permissions and
## limitations under the License.
##
## FILE: application.py
## AUTHOR(S): Noah Rahm
## PURPOSE: Main application class which ties all the elements into one window
## ----------------------------------------------------------------------------

import os
import webbrowser
import wx
import wx.lib.agw.aui as aui

from GimelStudio.meta import (__NAME__, __AUTHOR__, __VERSION__,
                              __BUILD__, __RELEASE__, __DEBUG__,
                              __TITLE__)

#from GimelStudio.project import Project
from GimelStudio.renderer import Renderer
# from GimelStudio.program import (ProgramUpdateChecker, AboutGimelStudioDialog,
#                                  GimelStudioLicenseDialog)
#from GimelStudio.node_importer import *
#from GimelStudio.nodedef import NODE_REGISTRY 

from GimelStudio.node_registry import NodeRegistry
from GimelStudio.node_graph import NodeGraph, NodeGraphDropTarget
from GimelStudio.node_property_panel import NodePropertyPanel
from GimelStudio.image_viewport import ImageViewport

from GimelStudio.utils import ConvertImageToWx
    
    #UserPreferencesManager, ImageViewport,
 #NodePropertyPanel,
                            #AssetLibrary)

from GimelStudio.stylesheet import *
from GimelStudio.datafiles.icons import *



 
# Create IDs



class MainApplication(wx.Frame):
    def __init__(self, arguments):
        wx.Frame.__init__(self, None, title=__TITLE__,
                          pos=(0, 0), size=(1000, 800))

        self._arguments = arguments

        # Set the program icon
        self.SetIcon(ICON_GIMELSTUDIO_ICO.GetIcon())

        # Init project, renderer and user preferences manager
        # self._project = Project(
        #     self,
        #     __VERSION__,
        #     __BUILD__,
        #     __RELEASE__
        #     )
        self._renderer = Renderer(
            self
            )
        # self._userprefmanager = UserPreferencesManager(
        #     self
        #     )

        # Load the user preferences from the .json file
        # otherwise use the default, built-in preferences.
        #self._userprefmanager.Load()

        # Setup the AUI window manager and configure settings so
        # that we get the light white theme that we want instead
        # of the yucky default colors. :)
        self._mgr = aui.AuiManager()
        self._mgr.SetManagedWindow(self) 
        self._mgr.SetAGWFlags(
            self._mgr.GetAGWFlags() ^ aui.AUI_MGR_LIVE_RESIZE
            )
        self._mgr.GetArtProvider().SetMetric(
            aui.AUI_DOCKART_SASH_SIZE,
            6
            )
        self._mgr.GetArtProvider().SetMetric(
            aui.AUI_DOCKART_PANE_BORDER_SIZE,
            2
            )
        self._mgr.GetArtProvider().SetMetric(
            aui.AUI_DOCKART_GRADIENT_TYPE, 
            aui.AUI_GRADIENT_NONE
            )
        self._mgr.GetArtProvider().SetColour(
            aui.AUI_DOCKART_BACKGROUND_COLOUR, 
            wx.Colour(STYLE_APPLICATION_BG)
            )
        self._mgr.GetArtProvider().SetColour(
            aui.AUI_DOCKART_INACTIVE_CAPTION_COLOUR, 
            wx.Colour(STYLE_DOCK_PANEL_BG)
            )
        self._mgr.GetArtProvider().SetColour(
            aui.AUI_DOCKART_INACTIVE_CAPTION_TEXT_COLOUR, 
            wx.Colour(STYLE_DOCK_PANEL_CAPTION_TEXT_FG)
            )
        self._mgr.GetArtProvider().SetColour(
            aui.AUI_DOCKART_BORDER_COLOUR, 
            wx.Colour(STYLE_DOCK_PANEL_BG)
            )
        self._mgr.GetArtProvider().SetColour(
            aui.AUI_DOCKART_SASH_COLOUR, 
            wx.Colour(STYLE_APPLICATION_BG)
            )
        self._mgr.GetArtProvider().SetColour(
            aui.AUI_DOCKART_GRIPPER_COLOUR, 
            wx.Colour(STYLE_APPLICATION_BG)
            )

        # Init the panes
        self._imageViewport = ImageViewport(
            self
            )
        self._nodeRegistry = NodeRegistry(
            self
            )

        self._nodePropertyPanel = NodePropertyPanel(
            self,
            (400, 800)
            )

        self._nodeGraph = NodeGraph(
            self,
            (2000, 2000)
            )
        # Drag image from dir or Node Registry into 
        # node graph to create image node
        self._nodeGraph.SetDropTarget(NodeGraphDropTarget(self._nodeGraph))


        # self._assetlibrary = AssetLibrary(
        #     self,
        #     )

        # Add the panes to the manager
        self._mgr.AddPane(
            self._nodePropertyPanel, 
            aui.AuiPaneInfo()
            .Right()
            .Name("NodeProperties")
            .Caption("Node Properties")
            .Icon(ICON_PANEL_NODE_PROPERTY_PANEL_DARK.GetBitmap())
            .CloseButton(visible=False)
            .BestSize(400, 400)
            )
        self._mgr.AddPane(
            self._nodeRegistry, 
            aui.AuiPaneInfo()
            .Left() 
            .Name("NodeRegistry")
            .Caption("Node Registry")
            .Icon(ICON_PANEL_NODE_REGISTRY_DARK.GetBitmap())
            .CloseButton(visible=False)
            .BestSize(400, 400)
            )
        self._mgr.AddPane(
            self._imageViewport, 
            aui.AuiPaneInfo()
            .Center()
            .Name("ImageViewport")
            .Caption("Image Viewport")
            .Icon(ICON_PANEL_IMAGE_VIEWPORT_DARK.GetBitmap())
            .CloseButton(visible=False)
            .BestSize(400, 400)
            )

        self._mgr.AddPane(
            self._nodeGraph, 
            aui.AuiPaneInfo()
            .Center()
            .Name("NodeGraph")
            .Caption("Node Graph")
            .Icon(ICON_PANEL_NODE_GRAPH_DARK.GetBitmap())
            .CloseButton(visible=False)
            .FloatingSize(wx.Size(200, 200))
            )





        # Maximize the window
        self.Maximize()

        # Tell the AUI window manager to "commit" all the changes just made.
        self._mgr.Update()

         

        #self._nodeRegistry.RegisterNode('outputcomposite')
        #print(self._nodeRegistry._registryBase.GetRegisteredNodes())
        self._nodeRegistry._InitNodes()
        print(self._nodeRegistry.GetRegisteredNodes())


        self._nodeGraph.AddNode(
            'gimelstudiocorenode_outputcomposite', pos=wx.Point(300, 300))

        self._nodeGraph.AddNode(
            'gimelstudiocorenode_image', pos=wx.Point(200, 240))
        
        self._nodeGraph.AddNode(
            'corenode_blur', pos=wx.Point(250, 200))

        
    def GetArguments(self):
        return self._arguments

    def GetAUIManager(self):
        return self._mgr
    
    def GetRenderer(self):
        return self._renderer

    def GetProject(self):
        return self._project

    def GetUserPrefManager(self):
        return self._userprefmanager

    def GetImageViewport(self):
        return self._imageViewport

    def GetNodePropertyPanel(self):
        return self._nodePropertyPanel

    def GetNodeGraph(self):
        return self._nodeGraph

    def GetNodeRegistry(self): 
        return self._nodeRegistry

    def GetAutoRenderBoolean(self):
        return self._autoRenderCheckbox.GetValue()

    def OnAboutGimelStudioDialog(self, event):
        dialog = AboutGimelStudioDialog(self)
        dialog.ShowDialog()

    def OnGimelStudioLicenseDialog(self, event):
        dialog = GimelStudioLicenseDialog(self)
        dialog.ShowDialog()

    def OnExportImage(self, event):
        wildcard = "JPG file (*.jpg)|*.jpg|" \
                   "PNG file (*.png)|*.png|" \
                   "All files (*.*)|*.*"

        image = self._renderer.GetRenderedImage()

        dlg = wx.FileDialog(
            self, 
            message="Export rendered image as...", 
            defaultDir=os.getcwd(),
            defaultFile="image.png", 
            wildcard=wildcard, 
            style=wx.FD_SAVE | wx.FD_OVERWRITE_PROMPT
            )

        # This sets the default filter that the user will initially see. 
        # Otherwise, the first filter in the list will be used by default.
        dlg.SetFilterIndex(2)

        if dlg.ShowModal() == wx.ID_OK:
            busy = wx.BusyInfo("Exporting Image...")
            path = dlg.GetPath()
            image.save(path)
            #self.statusbar.SetStatusText("Image saved as: {}".format(path))
            
        dlg.Destroy()
        del busy

    def OnRenderImage(self, event):
        self.Render()

    def OnTakeFeedbackSurvey(self, event):
        """ Go to the feedback survey webpage. """
        # Will be removed after BETA stage
        url = ("https://www.surveymonkey.com/r/RSRD556")
        webbrowser.open(url) 

    def OnToggleFullscreen(self, event):
        if self.IsMaximized() == False:
            self.Maximize()
        elif self.IsMaximized() == True:
            self.Restore()

    def OnSaveFileAs(self, event):
        wildcard = "GIMEL STUDIO PROJECT file (*.gimel-studio-project)|*.gimel-studio-project|" \
                   "All files (*.*)|*.*"

        dlg = wx.FileDialog(
            self, message="Save project file as...",
            defaultDir='',
            defaultFile='default.gimel-studio-project',
            wildcard=wildcard,
            style=wx.FD_SAVE | wx.FD_OVERWRITE_PROMPT
            )

        if dlg.ShowModal() == wx.ID_OK:
            busy = wx.BusyInfo("Saving File...")
            # This returns a Python list of files that were selected.
            paths = dlg.GetPaths()
            self._project.SaveProjectFile(paths[0])
            self.SetTitle("{0} - {1}".format(
                __TITLE__,
                dlg.GetFilename()
                ))
            del busy
            
    
    def OnOpenFile(self, event):
        wildcard = "GIMEL STUDIO PROJECT file (*.gimel-studio-project)|*.gimel-studio-project|" \
                   "All files (*.*)|*.*"
        styles = wx.FD_OPEN | wx.FD_CHANGE_DIR | wx.FD_FILE_MUST_EXIST | wx.FD_PREVIEW
                   
        dlg = wx.FileDialog(
            self, message="Open project file...",
            defaultDir='',
            wildcard=wildcard,
            style=styles
            )

        if dlg.ShowModal() == wx.ID_OK:
            busy = wx.BusyInfo("Loading File...")
            wx.Yield()
            # This returns a Python list of files that were selected.
            paths = dlg.GetPaths()
            self._project.OpenProjectFile(paths[0])
            self.SetTitle("{0} - {1}".format(
                __TITLE__,
                dlg.GetFilename()
                ))    
            del busy    
            


    def OnQuit(self, event):
        quitdialog = wx.MessageDialog(
            self, 
            "Do you really want to quit? You will lose any unsaved data.", 
            "Quit Gimel Studio?", 
            wx.YES_NO|wx.YES_DEFAULT
            )

        if quitdialog.ShowModal() == wx.ID_YES:
            quitdialog.Destroy()
            self._mgr.UnInit()
            del self._mgr
            self.Destroy()
        else:
            event.Veto()


    def BuildMenuBar(self):
        # Menubar        
        self.mainmenubar = wx.MenuBar()

        # File menu
        self.filemenu = wx.Menu()

        self.openfile_menuitem = wx.MenuItem(
            self.filemenu, 
            ID_MENU_OPENFILEMENUITEM, 
            "Open Project File...", 
            "Open and load a Gimel Studio project file"
            )
        self.filemenu.Append(self.openfile_menuitem)
        self.savefile_menuitem = wx.MenuItem(
            self.filemenu, 
            ID_MENU_SAVEFILEASMENUITEM, 
            "Save Project File As...", 
            "Save the current project as a Gimel Studio project file"
            )
        self.filemenu.Append(self.savefile_menuitem)
        self.filemenu.AppendSeparator()
        self.quit_menuitem = wx.MenuItem(
            self.filemenu, 
            ID_MENU_QUITMENUITEM, 
            "Quit", 
            "Quit Gimel Studio"
            )
        self.filemenu.Append(self.quit_menuitem)     

        self.mainmenubar.Append(self.filemenu, "File")


        # View menu
        self.viewmenu = wx.Menu()
        self.togglefullscreen_menuitem = wx.MenuItem(
            self.viewmenu, 
            ID_MENU_TOGGLEFULLSCREENMENUITEM, 
            "Fullscreen",  
            "Set the window size to fullscreen", wx.ITEM_CHECK
            )
        self.viewmenu.Append(self.togglefullscreen_menuitem)
        self.viewmenu.Check(ID_MENU_TOGGLEFULLSCREENMENUITEM, True)

        # self.p_menuitem = wx.MenuItem(
        #     self.viewmenu, 
        #     ID_MENU_pMENUITEM, 
        #     "Fullscrddddddeen",  
        #     "Setn",
        #     )
        # self.viewmenu.Append(self.p_menuitem)

        self.mainmenubar.Append(self.viewmenu, "View")

 
        # Help menu
        self.helpmenu = wx.Menu()

        self.takefeedbacksurvey_menuitem = wx.MenuItem(
            self.helpmenu, 
            ID_MENU_TAKEFEEDBACKSURVEYMENUITEM, 
            "Feedback Survey", 
            "Take a short survey online about Gimel Studio"
            )
        #self.takefeedbacksurvey_menuitem.SetBitmap(ICON_MENU_ABOUTGIMELSTUDIO.GetBitmap())
        self.helpmenu.Append(self.takefeedbacksurvey_menuitem)
        
        self.license_menuitem = wx.MenuItem(
            self.helpmenu, 
            ID_MENU_LICENSEMENUITEM, 
            "License", 
            "Show Gimel Studio license"
            )
        #self.about_menuitem.SetBitmap(ICON_MENU_ABOUTGIMELSTUDIO.GetBitmap())
        self.helpmenu.Append(self.license_menuitem)

        self.about_menuitem = wx.MenuItem(
            self.helpmenu, 
            ID_MENU_ABOUTMENUITEM, 
            "About", 
            "Show information about GimelStudio"
            )
        #self.about_menuitem.SetBitmap(ICON_MENU_ABOUTGIMELSTUDIO.GetBitmap())
        self.helpmenu.Append(self.about_menuitem)

        self.mainmenubar.Append(self.helpmenu, "Help")


        self.SetMenuBar(self.mainmenubar)

        # Menubar bindings

        self.Bind(wx.EVT_MENU, self.OnOpenFile, id=ID_MENU_OPENFILEMENUITEM)
        #self.Bind(wx.EVT_MENU, self.OnSaveFile, id=ID_MENU_SAVEFILEMENUITEM)
        self.Bind(wx.EVT_MENU, self.OnSaveFileAs, id=ID_MENU_SAVEFILEASMENUITEM)
        self.Bind(wx.EVT_MENU, self.OnQuit, id=ID_MENU_QUITMENUITEM)
        self.Bind(wx.EVT_MENU, self.OnToggleFullscreen, id=ID_MENU_TOGGLEFULLSCREENMENUITEM)
        self.Bind(wx.EVT_MENU, self.OnTakeFeedbackSurvey, id=ID_MENU_TAKEFEEDBACKSURVEYMENUITEM)
        self.Bind(wx.EVT_MENU, self.OnAboutGimelStudioDialog, id=ID_MENU_ABOUTMENUITEM)
        self.Bind(wx.EVT_MENU, self.OnGimelStudioLicenseDialog, id=ID_MENU_LICENSEMENUITEM)

    
    def GetRenderedImage(self):
        return self._renderer.GetRenderedImage()

    def Render(self):
        busy = wx.BusyInfo("Rendering Image...")
        wx.Yield()
        self._renderer.Render(self._nodeGraph.GetNodes())
        render_time = self._renderer.GetRenderTime()
        render_image = self.GetRenderedImage()
        if render_image != None:
            self._imageViewport.UpdateViewerImage(
                ConvertImageToWx(render_image),
                render_time
                )
            self._nodeGraph.UpdateAllNodes()
            #self._nodeGraph.RefreshGraph()  
        del busy



    def RestartProgram(newArgs):
        """
        Restart the program so that the node registry is refreshed.
        """
        python = sys.executable
        os.execl(python, python, *newArgs)
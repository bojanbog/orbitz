import wx

from opengl_orbits import OrbitzGLCanvas
from body import EARTH_R

def reverse_dict(d):
    return dict((v, k) for k, v in d.iteritems())


class VizWindow(wx.Frame):
    """Main visualization window"""
    ID_First_Body = wx.NewId(); ID_Last_Body = wx.NewId(); ID_Next_Body = wx.NewId(); ID_Prev_Body = wx.NewId()
    ID_Body_Pos_Symbol = wx.NewId(); ID_Body_Pos_RV = wx.NewId(); ID_Body_Pos_Point = wx.NewId(); ID_Body_Pos_Cycle = wx.NewId()
    Body_Pos_Modes = {ID_Body_Pos_Symbol: 0, ID_Body_Pos_RV: 1, ID_Body_Pos_Point: 2}; Body_Pos_Modes_REV = reverse_dict(Body_Pos_Modes)
    ID_Body_Orbit_Symbols = wx.NewId(); ID_Body_Orbit_Only = wx.NewId(); ID_Body_No_Orbit = wx.NewId(); ID_Body_Orbit_Cycle = wx.NewId()
    Body_Orbit_Modes = {ID_Body_Orbit_Symbols: 0, ID_Body_Orbit_Only: 1, ID_Body_No_Orbit: 2}; Body_Orbit_Modes_REV = reverse_dict(Body_Orbit_Modes)
    ID_Bodies_Pos_Symbol = wx.NewId(); ID_Bodies_Pos_RV = wx.NewId(); ID_Bodies_Pos_Point = wx.NewId(); ID_Bodies_Pos_Cycle = wx.NewId()
    Bodies_Pos_Modes = {ID_Bodies_Pos_Symbol: 0, ID_Bodies_Pos_RV: 1, ID_Bodies_Pos_Point: 2}; Bodies_Pos_Modes_REV = reverse_dict(Bodies_Pos_Modes)
    ID_Bodies_Orbit_Symbols = wx.NewId(); ID_Bodies_Orbit_Only = wx.NewId(); ID_Bodies_No_Orbit = wx.NewId(); ID_Bodies_Orbit_Cycle = wx.NewId()
    Bodies_Orbit_Modes = {ID_Bodies_Orbit_Symbols:0, ID_Bodies_Orbit_Only: 1, ID_Bodies_No_Orbit: 2}; Bodies_Orbit_Modes_REV = reverse_dict(Bodies_Orbit_Modes)
    ID_Start_Sim = wx.NewId(); ID_Pause_Sim = wx.NewId()
    ID_Timer = wx.NewId()
    ID_Exit = wx.NewId()

    def bind_multiple_ids(self, event_handler, ids):
        for id_ in ids:
            self.Bind(wx.EVT_MENU, event_handler, id=id_)

    def _create_menu(self):
        body_menu = wx.Menu()
        body_menu.Append(self.ID_First_Body, '&First\tHome')
        body_menu.Append(self.ID_Next_Body, '&Previous\tPgDn')
        body_menu.Append(self.ID_Prev_Body, '&Next\tPgUp')
        body_menu.Append(self.ID_Last_Body, '&Last\tEnd')
        body_menu.AppendSeparator()
        body_posviz_submenu = wx.Menu()
        body_posviz_submenu.Append(self.ID_Body_Pos_Symbol, 'Symbol', kind=wx.ITEM_RADIO)
        body_posviz_submenu.Append(self.ID_Body_Pos_RV, 'Radius vector', kind=wx.ITEM_RADIO)
        body_posviz_submenu.Append(self.ID_Body_Pos_Point, 'Point', kind=wx.ITEM_RADIO)
        body_posviz_submenu.Append(self.ID_Body_Pos_Cycle, 'Cycle mode\tF5')
        body_menu.AppendMenu(0, 'Position visualization', body_posviz_submenu)
        body_vizmode_submenu = wx.Menu()
        body_vizmode_submenu.Append(self.ID_Body_Orbit_Symbols, 'Orbit and symbols', kind=wx.ITEM_RADIO)
        body_vizmode_submenu.Append(self.ID_Body_Orbit_Only, 'Orbit only', kind=wx.ITEM_RADIO)
        body_vizmode_submenu.Append(self.ID_Body_No_Orbit, 'No orbit', kind=wx.ITEM_RADIO)
        body_vizmode_submenu.Append(self.ID_Body_Orbit_Cycle, 'Cycle mode\tF6')
        body_menu.AppendMenu(0, 'Orbit visualization', body_vizmode_submenu)

        viz_menu = wx.Menu()
        viz_posviz_submenu = wx.Menu()
        viz_posviz_submenu.Append(self.ID_Bodies_Pos_Symbol, 'Symbol', kind=wx.ITEM_RADIO)
        viz_posviz_submenu.Append(self.ID_Bodies_Pos_RV, 'Radius vector', kind=wx.ITEM_RADIO)
        viz_posviz_submenu.Append(self.ID_Bodies_Pos_Point, 'Point', kind=wx.ITEM_RADIO)
        viz_posviz_submenu.Append(self.ID_Bodies_Pos_Cycle, 'Cycle mode\tShift+F5')
        viz_menu.AppendMenu(0, 'Position', viz_posviz_submenu)
        viz_vizmode_submenu = wx.Menu()
        viz_vizmode_submenu.Append(self.ID_Bodies_Orbit_Symbols, 'Orbit and symbols', kind=wx.ITEM_RADIO)
        viz_vizmode_submenu.Append(self.ID_Bodies_Orbit_Only, 'Orbit only', kind=wx.ITEM_RADIO)
        viz_vizmode_submenu.Append(self.ID_Bodies_No_Orbit, 'No orbit', kind=wx.ITEM_RADIO)
        viz_vizmode_submenu.Append(self.ID_Bodies_Orbit_Cycle, 'Cycle mode\tShift+F6')
        viz_menu.AppendMenu(0, 'Orbit', viz_vizmode_submenu)
        viz_menu.AppendSeparator()
        viz_menu.Append(0, 'Show &planet\tF7', kind=wx.ITEM_CHECK)

        sim_menu = wx.Menu()
        sim_menu.Append(self.ID_Start_Sim, '&Start\tSpace')
        sim_menu.Append(self.ID_Pause_Sim, '&Pause\tPause')

        menubar = wx.MenuBar()
        menubar.Append(body_menu, '&Body')
        menubar.Append(viz_menu, '&Visualization')
        menubar.Append(sim_menu, '&Simulation')
        menubar.Enable(self.ID_Pause_Sim, False)
        return menubar

    def __init__(self, sim):
        wx.Frame.__init__(self, None, title="Orbital Academy v0.1", size=(1024, 1024),
                          style=wx.MINIMIZE_BOX | wx.MAXIMIZE_BOX | wx.RESIZE_BORDER | wx.SYSTEM_MENU | wx.CAPTION)
        self.sim = sim
        self.sim_state_change_callback = None  # Object to call if sim state changes
        self.main_panel = wx.Panel(self)
        self.gl_canvas = OrbitzGLCanvas(self.main_panel, self.sim)
        self.switch_view_north()

        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.Add(self.gl_canvas, 1, wx.EXPAND)
        self.main_panel.SetSizer(sizer)

        self.menu = self._create_menu(); self.SetMenuBar(self.menu)
        self.bind_multiple_ids(self.OnBodyChange, [self.ID_First_Body, self.ID_Last_Body, self.ID_Next_Body, self.ID_Prev_Body])
        self.bind_multiple_ids(self.OnBodyPos, [self.ID_Body_Pos_Symbol, self.ID_Body_Pos_RV, self.ID_Body_Pos_Point, self.ID_Body_Pos_Cycle])
        self.bind_multiple_ids(self.OnBodyOrbit, [self.ID_Body_Orbit_Symbols, self.ID_Body_Orbit_Only, self.ID_Body_No_Orbit, self.ID_Body_Orbit_Cycle])
        self.bind_multiple_ids(self.OnBodiesPos, [self.ID_Bodies_Pos_Symbol, self.ID_Bodies_Pos_RV, self.ID_Bodies_Pos_Point, self.ID_Bodies_Pos_Cycle])
        self.bind_multiple_ids(self.OnBodiesOrbit, [self.ID_Bodies_Orbit_Symbols, self.ID_Bodies_Orbit_Only, self.ID_Bodies_No_Orbit, self.ID_Bodies_Orbit_Cycle])
        self.Bind(wx.EVT_MENU, self.OnStartSim, id=self.ID_Start_Sim)
        self.Bind(wx.EVT_MENU, self.OnPauseSim, id=self.ID_Pause_Sim)
        self.Bind(wx.EVT_CLOSE, self.OnCloseWindow)

        self.timer = wx.Timer(self, self.ID_Timer)
        self.Bind(wx.EVT_TIMER, self.OnTimer, id=self.ID_Timer)

    def set_camera_pos(self, vector, up, right):
        """Switches the view to a North top-down view from the default distance."""
        self.gl_canvas.camera_vector = vector
        self.gl_canvas.camera_up = up
        self.gl_canvas.camera_right = right
        self.gl_canvas.Refresh()

    def switch_view_north(self, earth_radii_distance=6.0):
        """Switches the view to a North top-down view from the default distance."""
        self.set_camera_pos((0.0, 0.0, earth_radii_distance * EARTH_R), (0.0, 1.0, 0.0), (1.0, 0.0, 0.0))

    def OnBodyChange(self, evt):
        evtid = evt.GetId()
        if evtid == self.ID_First_Body:
            self.sim.selected_body = 0
        elif evtid == self.ID_Next_Body:
            self.sim.selected_body += 1
        elif evtid == self.ID_Prev_Body:
            self.sim.selected_body -= 1
        elif evtid == self.ID_Last_Body:
            self.sim.selected_body = len(self.sim.bodies) - 1
        else:
            assert 'Unknown event ID!'
        self.sim.selected_body %= len(self.sim.bodies)
        self.gl_canvas.Refresh()

    def OnBodyPos(self, evt):
        evtid = evt.GetId(); curr_body = self.sim.current_body()
        if evtid == self.ID_Body_Pos_Cycle:
            curr_body.pos_viz_mode = (curr_body.pos_viz_mode + 1) % 3
        else:
            curr_body.pos_viz_mode = self.Body_Pos_Modes[evtid]
        self.menu.Check(self.Body_Pos_Modes_REV[curr_body.pos_viz_mode], True)
        self.gl_canvas.Refresh()

    def OnBodyOrbit(self, evt):
        evtid = evt.GetId(); curr_body = self.sim.current_body()
        if evtid == self.ID_Body_Orbit_Cycle:
            curr_body.orbit_viz_mode = (curr_body.orbit_viz_mode + 1) % 3
        else:
            curr_body.orbit_viz_mode = self.Body_Orbit_Modes[evtid]
        self.menu.Check(self.Body_Orbit_Modes_REV[curr_body.orbit_viz_mode], True)
        self.gl_canvas.Refresh()

    def OnBodiesPos(self, evt):
        evtid = evt.GetId()
        if evtid == self.ID_Bodies_Pos_Cycle:
            self.sim.pos_viz_mode = (self.sim.pos_viz_mode + 1) % 3
        else:
            self.sim.pos_viz_mode = self.Bodies_Pos_Modes[evtid]
        self.menu.Check(self.Bodies_Pos_Modes_REV[self.sim.pos_viz_mode], True)
        self.menu.Check(self.Body_Pos_Modes_REV[self.sim.pos_viz_mode], True)
        for body in self.sim.bodies:
            body.pos_viz_mode = self.sim.pos_viz_mode
        self.gl_canvas.Refresh()

    def OnBodiesOrbit(self, evt):
        evtid = evt.GetId()
        if evtid == self.ID_Bodies_Orbit_Cycle:
            self.sim.orbit_viz_mode = (self.sim.orbit_viz_mode + 1) % 3
        else:
            self.sim.orbit_viz_mode = self.Bodies_Orbit_Modes[evtid]
        self.menu.Check(self.Bodies_Orbit_Modes_REV[self.sim.orbit_viz_mode], True)
        self.menu.Check(self.Body_Orbit_Modes_REV[self.sim.orbit_viz_mode], True)
        for body in self.sim.bodies:
            body.orbit_viz_mode = self.sim.orbit_viz_mode
        self.gl_canvas.Refresh()

    def OnStartSim(self, evt):
        old_sim_state = self.sim.state
        self.sim.start()
        if self.sim.state == 'running':
            self.menu.Enable(self.ID_Start_Sim, False)
            self.menu.Enable(self.ID_Pause_Sim, True)
            self.timer.Start(40)
        if old_sim_state != self.sim.state and self.sim_state_change_callback:
            self.sim_state_change_callback.OnSimStateChange()

    def OnPauseSim(self, evt):
        old_sim_state = self.sim.state
        self.sim.pause()
        if self.sim.state == 'paused':
            self.menu.Enable(self.ID_Pause_Sim, False)
            self.menu.Enable(self.ID_Start_Sim, True)
            self.timer.Stop()
        if old_sim_state != self.sim.state and self.sim_state_change_callback:
            self.sim_state_change_callback.OnSimStateChange()

    def OnTimer(self, evt):
        old_sim_state = self.sim.state
        self.sim.step_time()
        if self.sim.state == 'running':
            for body in self.sim.bodies:
                body.calc_state_vectors(self.sim.time)
        self.gl_canvas.Refresh()
        if old_sim_state != self.sim.state and self.sim_state_change_callback:
            self.sim_state_change_callback.OnSimStateChange()

    def OnCloseWindow(self, evt):
        # Don't let user close this window
        pass

    def OnClose(self, evt):
        self.timer.Stop()
        self.Destroy()

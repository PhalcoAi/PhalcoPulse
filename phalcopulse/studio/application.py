# File: phalcopulse/studio/application.py

import pygame
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *
import time
import numpy as np
import math

from .scene import PhalcoPulseFX
from .camera import Camera
from ..ui.manager import UIManager
from ..ui.widgets import Button, Slider, Checkbox


class PhalcoPulseStudio:
    def __init__(self, scene_fx, width=1600, height=900):
        pygame.init()
        pygame.font.init()

        self.scene = scene_fx
        if not isinstance(self.scene, PhalcoPulseFX):
            raise TypeError("scene_fx must be an instance of a PhalcoPulseFX subclass.")

        self.display = (width, height)
        self.screen = pygame.display.set_mode(self.display, DOUBLEBUF | OPENGL | RESIZABLE)
        pygame.display.set_caption("PhalcoPulse Studio")

        self.camera = Camera()
        self.ui_manager = UIManager(self)

        self.font_m = pygame.font.Font(None, 24)
        self.font_l = pygame.font.Font(None, 30)
        self.colors = {
            'bg': (0.08, 0.09, 0.1, 1.0), 'panel': (0.12, 0.13, 0.15, 0.9),
            'accent': (1.0, 0.55, 0.0), 'accent_hover': (1.0, 0.65, 0.15),
            'grid_major': (0.25, 0.25, 0.25), 'grid_minor': (0.18, 0.18, 0.18),
            'axis_x': (0.9, 0.3, 0.3), 'axis_y': (0.3, 0.9, 0.3), 'axis_z': (0.3, 0.3, 0.9),
            'text': (230, 230, 230), 'text_dim': (160, 160, 160),
        }
        self.ui_padding = 15
        self.is_paused = False
        self.show_grid = True
        self.show_axes = True
        self.simulation_speed = 1.0
        self.light_intensity = 0.8
        self.clock = pygame.time.Clock()
        self.start_time = time.time()

        self._setup_default_ui()
        self._setup_opengl()

    def _setup_default_ui(self):
        def set_sim_speed(val): self.simulation_speed = val

        def set_light(val): self.light_intensity = val

        def set_grid_visible(val): self.show_grid = val

        def set_axes_visible(val): self.show_axes = val

        self.ui_manager.add_widget("play_pause_button", Button(rect=(0, 0, 0, 0), text="Pause/Play",
                                                               callback=lambda: setattr(self, 'is_paused',
                                                                                        not self.is_paused)))
        self.ui_manager.add_widget("reset_view_button",
                                   Button(rect=(0, 0, 0, 0), text="Reset View", callback=self.camera.reset))
        self.ui_manager.add_widget("grid_checkbox",
                                   Checkbox(rect=(0, 0, 0, 0), label="Show Grid", is_checked=self.show_grid,
                                            callback=set_grid_visible))
        self.ui_manager.add_widget("axes_checkbox",
                                   Checkbox(rect=(0, 0, 0, 0), label="Show Axes", is_checked=self.show_axes,
                                            callback=set_axes_visible))
        self.ui_manager.add_widget("speed_slider", Slider(rect=(0, 0, 0, 0), label="Sim Speed", min_val=0, max_val=3.0,
                                                          initial_val=self.simulation_speed, callback=set_sim_speed))
        self.ui_manager.add_widget("light_slider", Slider(rect=(0, 0, 0, 0), label="Light", min_val=0, max_val=1.5,
                                                          initial_val=self.light_intensity, callback=set_light))

    def _update_ui_layout(self):
        panel_width = 260
        panel_x = self.display[0] - panel_width
        p = self.ui_padding
        y = self.display[1] - p - 35
        btn_w = (panel_width - p * 3) // 2

        self.ui_manager.widgets["play_pause_button"].rect.update(panel_x + p, y, btn_w, 35)
        self.ui_manager.widgets["reset_view_button"].rect.update(panel_x + p * 2 + btn_w, y, btn_w, 35)
        y -= 50

        checkbox_w = (panel_width - p * 2)
        self.ui_manager.widgets["grid_checkbox"].rect.update(panel_x + p, y, checkbox_w, 20)
        y -= 30
        self.ui_manager.widgets["axes_checkbox"].rect.update(panel_x + p, y, checkbox_w, 20)
        y -= 50

        slider_w = panel_width - p * 2
        self.ui_manager.widgets["speed_slider"].rect.update(panel_x + p, y - 20, slider_w, 20)
        y -= 55
        self.ui_manager.widgets["light_slider"].rect.update(panel_x + p, y - 20, slider_w, 20)

    def _setup_opengl(self):
        glEnable(GL_DEPTH_TEST)
        glEnable(GL_LIGHTING);
        glEnable(GL_LIGHT0)
        glLightfv(GL_LIGHT0, GL_AMBIENT, (0.3, 0.3, 0.3, 1))
        glEnable(GL_DEPTH_TEST);
        glEnable(GL_BLEND)
        glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
        glEnable(GL_LINE_SMOOTH);
        glEnable(GL_COLOR_MATERIAL)
        glColorMaterial(GL_FRONT_AND_BACK, GL_AMBIENT_AND_DIFFUSE)
        self._resize_viewport(self.display[0], self.display[1])

    def _resize_viewport(self, width, height):
        self.display = (width, height if height > 0 else 1)
        glViewport(0, 0, self.display[0], self.display[1])
        glMatrixMode(GL_PROJECTION);
        glLoadIdentity()
        gluPerspective(45, (self.display[0] / self.display[1]), 0.1, 500.0)
        glMatrixMode(GL_MODELVIEW);
        glLoadIdentity()
        self._update_ui_layout()

    def _handle_events(self):
        for event in pygame.event.get():
            self.ui_manager.handle_event(event)

            if event.type == pygame.QUIT:
                pygame.quit();
                quit()
            elif event.type == VIDEORESIZE:
                self._resize_viewport(*event.dict['size'])
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE: self.is_paused = not self.is_paused
                if event.key == pygame.K_r: self.camera.reset()

            if not self.ui_manager.is_mouse_over_ui:
                if event.type == pygame.MOUSEBUTTONDOWN:
                    self.camera.mouse_buttons['left'] = (event.button == 1)
                    self.camera.mouse_buttons['right'] = (event.button == 3)
                    self.camera.handle_scroll(event.button)
                    self.camera.last_mouse_pos = event.pos
                elif event.type == pygame.MOUSEBUTTONUP:
                    self.camera.mouse_buttons['left'] = False
                    self.camera.mouse_buttons['right'] = False
                elif event.type == pygame.MOUSEMOTION:
                    self.camera.handle_mouse_move(event.pos, self.camera.mouse_buttons)

    def _draw_environment(self):
        glPushAttrib(GL_LIGHTING_BIT | GL_LINE_BIT | GL_CURRENT_BIT)
        glDisable(GL_LIGHTING)
        if self.show_grid: self._draw_adaptive_grid()
        if self.show_axes:
            glLineWidth(2.0);
            glBegin(GL_LINES)
            glColor3fv(self.colors['axis_x']);
            glVertex3f(0, 0, 0);
            glVertex3f(1, 0, 0)
            glColor3fv(self.colors['axis_y']);
            glVertex3f(0, 0, 0);
            glVertex3f(0, 1, 0)
            glColor3fv(self.colors['axis_z']);
            glVertex3f(0, 0, 0);
            glVertex3f(0, 0, 1)
            glEnd()
        glPopAttrib()

    def _draw_adaptive_grid(self):
        cam_dist = np.linalg.norm(self.camera.translation)
        base_spacing = 10 ** math.floor(math.log10(cam_dist) if cam_dist > 1 else 0)
        glLineWidth(1.0)
        if cam_dist < base_spacing * 5:
            minor_spacing = base_spacing / 10.0
            if minor_spacing > 0.01:
                glColor3fv(self.colors['grid_minor']);
                glBegin(GL_LINES)
                grid_range = 50 * base_spacing
                for i in np.arange(-500, 501, 1):
                    pos = i * minor_spacing
                    if abs(pos) > grid_range: continue
                    glVertex3f(pos, 0, -grid_range);
                    glVertex3f(pos, 0, grid_range)
                    glVertex3f(-grid_range, 0, pos);
                    glVertex3f(grid_range, 0, pos)
                glEnd()
        major_spacing = base_spacing
        glColor3fv(self.colors['grid_major']);
        glBegin(GL_LINES)
        grid_range = 50 * major_spacing
        for i in np.arange(-50, 51, 1):
            pos = i * major_spacing
            glVertex3f(pos, 0, -grid_range);
            glVertex3f(pos, 0, grid_range)
            glVertex3f(-grid_range, 0, pos);
            glVertex3f(grid_range, 0, pos)
        glEnd()

    def run(self):
        print("PhalcoPulse Studio: Starting main loop.")
        try:
            self.scene.setup(self.ui_manager)
        except TypeError:
            self.scene.setup()

        while True:
            raw_delta_time = self.clock.tick(144) / 1000.0
            sim_delta_time = raw_delta_time * self.simulation_speed
            if self.is_paused: sim_delta_time = 0

            self._handle_events()
            glClearColor(*self.colors['bg']);
            glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
            glMatrixMode(GL_MODELVIEW);
            glLoadIdentity()
            self.camera.apply_transformations()

            light_val = self.light_intensity
            glLightfv(GL_LIGHT0, GL_POSITION, (5, 5, -5, 1));
            glLightfv(GL_LIGHT0, GL_DIFFUSE, (light_val, light_val, light_val, 1))

            self._draw_environment()
            glPushMatrix()
            self.scene.loop(sim_delta_time)
            self.ui_manager.draw()
            glPopMatrix()

            pygame.display.flip()

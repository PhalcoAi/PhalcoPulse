# File: phalcopulse/studio/ui.py

import pygame
from OpenGL.GL import *
from OpenGL.GLU import *
import time


def draw_ui(app):
    """
    Draws the entire UI by calling helper functions.
    This is the main entry point for UI rendering.

    Args:
        app: The main PhalcoPulseStudio application instance.
    """
    glPushAttrib(GL_ALL_ATTRIB_BITS)
    glMatrixMode(GL_PROJECTION);
    glPushMatrix();
    glLoadIdentity()
    gluOrtho2D(0, app.display[0], 0, app.display[1])
    glMatrixMode(GL_MODELVIEW);
    glPushMatrix();
    glLoadIdentity()
    glDisable(GL_LIGHTING);
    glDisable(GL_DEPTH_TEST)

    app.ui_rects.clear()
    panel_width = 260
    panel_x = app.display[0] - panel_width
    _draw_panels(app, panel_x, panel_width)
    _draw_widgets(app, panel_x, panel_width)

    glMatrixMode(GL_PROJECTION);
    glPopMatrix()
    glMatrixMode(GL_MODELVIEW);
    glPopMatrix()
    glPopAttrib()


# --- UI Helper Functions ---

def _render_text(app, x, y, text, font, color=None):
    if color is None: color = app.colors['text']
    text_surface = font.render(text, True, color)
    text_data = pygame.image.tostring(text_surface, "RGBA", True)
    glRasterPos2d(x, y)
    glDrawPixels(text_surface.get_width(), text_surface.get_height(), GL_RGBA, GL_UNSIGNED_BYTE, text_data)


def _draw_panels(app, panel_x, panel_width):
    help_bar_height = 40
    glColor4fv(app.colors['panel']);
    glRectf(panel_x, 0, app.display[0], app.display[1])
    glColor4fv(app.colors['panel']);
    glRectf(0, 0, panel_x, help_bar_height)
    help_text = "[L-DRAG] Rotate | [R-DRAG] Pan | [WHEEL] Zoom | [SPACE] Pause | [R] Reset"
    _render_text(app, app.ui_padding, 12, help_text, app.font_m, app.colors['text_dim'])


def _draw_widgets(app, panel_x, panel_width):
    y_pos = app.display[1] - app.ui_padding - 25
    _render_text(app, panel_x + app.ui_padding, y_pos, "Controls", app.font_l)
    y_pos -= 50

    btn_h, btn_w = 35, (panel_width - app.ui_padding * 3) // 2
    play_rect = pygame.Rect(panel_x + app.ui_padding, y_pos, btn_w, btn_h)
    reset_rect = pygame.Rect(play_rect.right + app.ui_padding, y_pos, btn_w, btn_h)
    _draw_button(app, play_rect, "Pause" if not app.is_paused else "Play", 'play_button')
    _draw_button(app, reset_rect, "Reset", 'reset_button');
    y_pos -= 50

    _draw_checkbox(app, panel_x + app.ui_padding, y_pos, "Show Grid", app.show_grid, 'grid_button')
    _draw_checkbox(app, panel_x + 130, y_pos, "Show Axes", app.show_axes, 'axes_button');
    y_pos -= 50

    slider_w = panel_width - app.ui_padding * 2
    _draw_slider(app, panel_x + app.ui_padding, y_pos, slider_w, "Sim Speed", app.simulation_speed, 0.0, 3.0,
                 'sim_speed_slider');
    y_pos -= 55
    _draw_slider(app, panel_x + app.ui_padding, y_pos, slider_w, "Light", app.light_intensity, 0.0, 1.5,
                 'light_slider');
    y_pos -= 70

    _render_text(app, panel_x + app.ui_padding, y_pos, "Info", app.font_l);
    y_pos -= 40
    info = [
        f"FPS: {app.clock.get_fps():.1f}", f"Time: {time.time() - app.start_time:.1f}s", "",
        "Camera Position:",
        f"  X: {app.camera.translation[0]:.2f}", f"  Y: {app.camera.translation[1]:.2f}",
        f"  Z: {app.camera.translation[2]:.2f}", "",
        "Camera Rotation:",
        f"  Pitch: {app.camera.rotation[0]:.1f}\N{DEGREE SIGN}", f"  Yaw: {app.camera.rotation[1]:.1f}\N{DEGREE SIGN}",
    ]
    for line in info:
        _render_text(app, panel_x + app.ui_padding, y_pos, line, app.font_m, app.colors['text_dim']);
        y_pos -= 28


def _draw_button(app, rect, text, name):
    app.ui_rects[name] = rect
    is_hovered = app.hovered_ui_element == name
    color = app.colors['accent_hover'] if is_hovered else app.colors['accent']
    glColor3fv(color);
    glRectf(rect.left, rect.top, rect.right, rect.bottom)
    text_surf = app.font_m.render(text, True, app.colors['text'])
    text_x = rect.centerx - text_surf.get_width() / 2
    text_y = rect.centery - text_surf.get_height() / 2
    _render_text(app, text_x, text_y, text, app.font_m)


def _draw_checkbox(app, x, y, label, is_checked, name):
    box_rect = pygame.Rect(x, y, 20, 20);
    app.ui_rects[name] = box_rect
    is_hovered = app.hovered_ui_element == name
    glColor3fv(app.colors['accent_hover'] if is_hovered else app.colors['accent'])
    glRectf(box_rect.left, box_rect.top, box_rect.right, box_rect.bottom)
    if is_checked: glColor3f(0.8, 0.8, 0.8); glRectf(x + 4, y + 4, x + 16, y + 16)
    _render_text(app, x + 30, y + 3, label, app.font_m)


def _draw_slider(app, x, y, w, label, value, min_val, max_val, name):
    _render_text(app, x, y, f"{label}: {value:.2f}", app.font_m)
    slider_rect = pygame.Rect(x, y - 25, w, 20);
    app.ui_rects[name] = slider_rect
    is_active = app.hovered_ui_element == name or app.active_slider == name
    glColor3f(0.1, 0.1, 0.1);
    glRectf(slider_rect.left, slider_rect.top, slider_rect.right, slider_rect.bottom)
    normalized_val = (value - min_val) / (max_val - min_val)
    fill_w = w * normalized_val;
    fill_rect = pygame.Rect(x, y - 25, fill_w, 20)
    glColor3fv(app.colors['accent_hover'] if is_active else app.colors['accent'])
    glRectf(fill_rect.left, fill_rect.top, fill_rect.right, fill_rect.bottom)

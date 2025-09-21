import pygame
from OpenGL.GL import *
import time
import math


def render_text(app, x, y, text, font, color=None):
    """The low-level function to render text to the OpenGL screen."""
    if color is None: color = app.colors['text']
    text_surface = font.render(text, True, color)
    text_data = pygame.image.tostring(text_surface, "RGBA", True)
    glRasterPos2d(x, y)
    glDrawPixels(text_surface.get_width(), text_surface.get_height(), GL_RGBA, GL_UNSIGNED_BYTE, text_data)


def draw_button(app, rect, text, is_hovered, is_active):
    """Draws a button widget."""
    color = app.colors['accent_hover'] if is_hovered else app.colors['accent']
    glColor3fv(color)
    glRectf(rect.left, rect.top, rect.right, rect.bottom)

    text_surf = app.font_m.render(text, True, app.colors['text'])
    text_x = rect.centerx - text_surf.get_width() / 2
    text_y = rect.centery - text_surf.get_height() / 2
    render_text(app, text_x, text_y, text, app.font_m)


def draw_slider(app, rect, label, value, min_val, max_val, is_active):
    """Draws a slider widget with its text label positioned above the bar."""
    text_y_pos = rect.top + 20
    render_text(app, rect.x, text_y_pos, f"{label}: {value:.2f}", app.font_m)

    # --- The rest of the function remains the same ---
    # Draw background track
    glColor3f(0.1, 0.1, 0.1)
    glRectf(rect.left, rect.top, rect.right, rect.bottom)

    # Draw fill bar
    normalized_val = (value - min_val) / (max_val - min_val)
    fill_width = rect.width * normalized_val
    fill_rect = pygame.Rect(rect.left, rect.top, fill_width, rect.height)
    color = app.colors['accent_hover'] if is_active else app.colors['accent']
    glColor3fv(color)
    glRectf(fill_rect.left, fill_rect.top, fill_rect.right, fill_rect.bottom)


def draw_panels(app):
    """Draws the main background panels for the UI."""
    panel_width = 260
    panel_x = app.display[0] - panel_width

    # Right-hand panel
    glColor4fv(app.colors['panel'])
    glRectf(panel_x, 0, app.display[0], app.display[1])

    # Bottom help bar
    help_bar_height = 40
    glColor4fv(app.colors['panel'])
    glRectf(0, 0, panel_x, help_bar_height)
    help_text = "[L-DRAG] Rotate | [R-DRAG] Pan | [WHEEL] Zoom | [SPACE] Pause | [R] Reset"
    render_text(app, app.ui_padding, 12, help_text, app.font_m, app.colors['text_dim'])


def draw_info_panel(app):
    """Draws the non-interactive info text on the control panel."""
    panel_width = 260
    panel_x = app.display[0] - panel_width
    p = 15  # padding
    y = app.display[1] - 380  # Starting y-position for the info panel

    render_text(app, panel_x + p, y, "Info", app.font_l);
    y -= 40
    info = [
        f"FPS: {app.clock.get_fps():.1f}", f"Time: {time.time() - app.start_time:.1f}s", "",
        "Camera Position:",
        f"  X: {app.camera.translation[0]:.2f}", f"  Y: {app.camera.translation[1]:.2f}",
        f"  Z: {app.camera.translation[2]:.2f}", "",
        "Camera Rotation:",
        f"  Pitch: {app.camera.rotation[0]:.1f}\N{DEGREE SIGN}", f"  Yaw: {app.camera.rotation[1]:.1f}\N{DEGREE SIGN}",
    ]
    for line in info:
        render_text(app, panel_x + p, y, line, app.font_m, app.colors['text_dim']);
        y -= 28


def draw_checkbox(app, rect, label, is_checked, is_hovered):
    """Draws a checkbox widget."""
    # The box part of the checkbox is smaller than the full rect
    box_rect = pygame.Rect(rect.left, rect.top, rect.height, rect.height)

    color = app.colors['accent_hover'] if is_hovered else app.colors['accent']
    glColor3fv(color)
    glRectf(box_rect.left, box_rect.top, box_rect.right, box_rect.bottom)

    # Draw an inner square if the box is checked
    if is_checked:
        glColor3f(0.9, 0.9, 0.9)  # A bright, almost white color
        glRectf(box_rect.left + 4, box_rect.top + 4, box_rect.right - 4, box_rect.bottom - 4)

    # Draw the label text next to the box
    render_text(app, rect.left + rect.height + 8, rect.top + 2, label, app.font_m)


def draw_label(app, rect, text, font, align):
    """Draws a static text label, handling alignment."""
    text_surf = font.render(text, True, app.colors['text_dim'])

    if align == 'left':
        text_x = rect.left
    elif align == 'center':
        text_x = rect.centerx - text_surf.get_width() / 2
    elif align == 'right':
        text_x = rect.right - text_surf.get_width()
    else:
        text_x = rect.left

    text_y = rect.centery - text_surf.get_height() / 2
    render_text(app, text_x, text_y, text, font, app.colors['text_dim'])


def draw_text_input(app, rect, text, is_focused, cursor_pos, cursor_visible):
    """Draws a text input box."""
    # Draw background
    bg_color = (0.1, 0.1, 0.1)
    glColor3fv(bg_color)
    glRectf(rect.left, rect.top, rect.right, rect.bottom)

    # Draw border, highlighted if focused
    border_color = app.colors['accent'] if is_focused else (0.3, 0.3, 0.3)
    glColor3fv(border_color)
    glLineWidth(2.0 if is_focused else 1.0)
    glBegin(GL_LINE_LOOP)
    glVertex2f(rect.left, rect.top);
    glVertex2f(rect.right, rect.top)
    glVertex2f(rect.right, rect.bottom);
    glVertex2f(rect.left, rect.bottom)
    glEnd()
    glLineWidth(1.0)

    # Draw text content
    padding = 5
    text_surf = app.font_m.render(text, True, app.colors['text'])
    render_text(app, rect.left + padding, rect.centery - text_surf.get_height() / 2, text, app.font_m)

    # Draw cursor
    if cursor_visible:
        # Calculate cursor x position
        sub_text_surf = app.font_m.render(text[:cursor_pos], True, app.colors['text'])
        cursor_x = rect.left + padding + sub_text_surf.get_width()
        glColor3fv(app.colors['text'])
        glRectf(cursor_x, rect.bottom + 2, cursor_x + 1, rect.top - 2)


def draw_toggle_switch(app, rect, is_on, is_hovered):
    """Draws an on/off toggle switch."""
    # Draw track
    track_color = app.colors['accent'] if is_on else (0.2, 0.2, 0.2)
    glColor3fv(track_color)
    glRectf(rect.left, rect.top, rect.right, rect.bottom)

    # Draw handle
    handle_color = (0.9, 0.9, 0.9) if is_hovered else (0.7, 0.7, 0.7)
    glColor3fv(handle_color)
    handle_rad = (rect.height / 2) - 2
    if is_on:
        handle_x = rect.right - rect.height / 2
    else:
        handle_x = rect.left + rect.height / 2

    handle_y = rect.centery

    glBegin(GL_POLYGON)
    for i in range(20):
        angle = i * (2 * math.pi / 20)
        glVertex2f(handle_x + math.cos(angle) * handle_rad, handle_y + math.sin(angle) * handle_rad)
    glEnd()


def draw_progress_bar(app, rect, value, min_val, max_val):
    """Draws a simple progress bar."""
    # Background track
    glColor3f(0.15, 0.15, 0.15)
    glRectf(rect.left, rect.top, rect.right, rect.bottom)

    # Filled portion
    ratio = (value - min_val) / float(max_val - min_val)
    fill_width = rect.width * max(0.0, min(1.0, ratio))
    glColor3fv(app.colors['accent'])
    glRectf(rect.left, rect.top, rect.left + fill_width, rect.bottom)

    # Border
    glColor3f(0.4, 0.4, 0.4)
    glLineWidth(1.5)
    glBegin(GL_LINE_LOOP)
    glVertex2f(rect.left, rect.top)
    glVertex2f(rect.right, rect.top)
    glVertex2f(rect.right, rect.bottom)
    glVertex2f(rect.left, rect.bottom)
    glEnd()
    glLineWidth(1.0)

    # Percentage text
    pct = 100 * ratio
    render_text(app, rect.centerx - 15, rect.centery - 8, f"{pct:.0f}%", app.font_m)


def draw_dropdown(app, rect, options, selected_index, is_open):
    """Draws a dropdown menu."""
    # Draw main box
    glColor3f(0.1, 0.1, 0.1)
    glRectf(rect.left, rect.top, rect.right, rect.bottom)

    # Border
    glColor3fv(app.colors['accent'])
    glLineWidth(1.5)
    glBegin(GL_LINE_LOOP)
    glVertex2f(rect.left, rect.top)
    glVertex2f(rect.right, rect.top)
    glVertex2f(rect.right, rect.bottom)
    glVertex2f(rect.left, rect.bottom)
    glEnd()
    glLineWidth(1.0)

    # Current selection text
    selected_text = options[selected_index] if options else ""
    render_text(app, rect.left + 8, rect.centery - 8, selected_text, app.font_m)

    # Draw dropdown arrow
    arrow_x = rect.right - 15
    arrow_y = rect.centery
    glColor3fv(app.colors['text'])
    glBegin(GL_TRIANGLES)
    glVertex2f(arrow_x - 5, arrow_y - 3)
    glVertex2f(arrow_x + 5, arrow_y - 3)
    glVertex2f(arrow_x, arrow_y + 4)
    glEnd()

    # Expanded options if open
    if is_open:
        for i, option in enumerate(options):
            option_rect = pygame.Rect(rect.x, rect.y + (i + 1) * rect.height, rect.width, rect.height)
            glColor3f(0.08, 0.08, 0.08)
            glRectf(option_rect.left, option_rect.top, option_rect.right, option_rect.bottom)
            glColor3fv(app.colors['text'])
            render_text(app, option_rect.left + 8, option_rect.centery - 8, option, app.font_m)

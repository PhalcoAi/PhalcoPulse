# File: phalcopulse/ui/widgets.py
import pygame
from . import drawing


class Widget:
    """Base class for all UI widgets."""

    def __init__(self, rect):
        self.rect = pygame.Rect(rect)
        self.is_hovered = False
        self.is_active = False

    def handle_event(self, event, mouse_pos):
        """Process a single Pygame event."""
        if self.rect.collidepoint(mouse_pos):
            self.is_hovered = True
        else:
            self.is_hovered = False

    def draw(self, app):
        """Draw the widget."""
        pass


class Button(Widget):
    """A clickable button that triggers a callback function."""

    def __init__(self, rect, text, callback):
        super().__init__(rect)
        self.text = text
        self.callback = callback

    def handle_event(self, event, mouse_pos):
        super().handle_event(event, mouse_pos)
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1 and self.is_hovered:
            self.is_active = True

        if event.type == pygame.MOUSEBUTTONUP and event.button == 1 and self.is_hovered and self.is_active:
            if self.callback:
                self.callback()  # Trigger the callback function
            self.is_active = False

        if not self.is_hovered:
            self.is_active = False

    def draw(self, app):
        drawing.draw_button(app, self.rect, self.text, self.is_hovered, self.is_active)


class Slider(Widget):
    """A slider that controls a value and triggers a callback."""

    def __init__(self, rect, label, min_val, max_val, initial_val, callback):
        super().__init__(rect)
        self.label = label
        self.min_val = min_val
        self.max_val = max_val
        self.value = initial_val
        self.callback = callback

    def handle_event(self, event, mouse_pos):
        super().handle_event(event, mouse_pos)
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1 and self.is_hovered:
            self.is_active = True

        if event.type == pygame.MOUSEBUTTONUP and event.button == 1:
            self.is_active = False

        if self.is_active and event.type == pygame.MOUSEMOTION:
            # Update value based on mouse position
            relative_x = mouse_pos[0] - self.rect.x
            ratio = max(0, min(1, relative_x / self.rect.width))
            self.value = self.min_val + ratio * (self.max_val - self.min_val)
            if self.callback:
                self.callback(self.value)  # Trigger callback with the new value

    def draw(self, app):
        drawing.draw_slider(app, self.rect, self.label, self.value, self.min_val, self.max_val,
                            self.is_active or self.is_hovered)


class Checkbox(Widget):
    """A checkbox that represents a boolean state and triggers a callback."""

    def __init__(self, rect, label, is_checked, callback):
        super().__init__(rect)
        self.label = label
        self.checked = is_checked
        self.callback = callback

    def handle_event(self, event, mouse_pos):
        super().handle_event(event, mouse_pos)
        # We use MOUSEBUTTONUP for checkboxes for a more natural feel
        if event.type == pygame.MOUSEBUTTONUP and event.button == 1 and self.is_hovered:
            self.checked = not self.checked  # Toggle the state
            if self.callback:
                self.callback(self.checked)  # Trigger callback with the new state

    def draw(self, app):
        drawing.draw_checkbox(app, self.rect, self.label, self.checked, self.is_hovered)


class Label(Widget):
    """A non-interactive widget for displaying static text."""

    def __init__(self, rect, text, font_size='medium', align='left'):
        super().__init__(rect)
        self.text = text
        self.font_size = font_size
        self.align = align

    def draw(self, app):
        font = app.font_l if self.font_size == 'large' else app.font_m
        drawing.draw_label(app, self.rect, self.text, font, self.align)


class TextInput(Widget):
    """A field for user text input."""

    def __init__(self, rect, initial_text="", max_length=50, callback=None):
        super().__init__(rect)
        self.text = initial_text
        self.max_length = max_length
        self.callback = callback  # Called when Enter is pressed
        self.is_focused = False
        self.cursor_pos = len(initial_text)
        self.cursor_timer = 0
        self.cursor_visible = False

    def handle_event(self, event, mouse_pos):
        super().handle_event(event, mouse_pos)

        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            self.is_focused = self.is_hovered

        if not self.is_focused:
            return

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_BACKSPACE:
                if self.cursor_pos > 0:
                    self.text = self.text[:self.cursor_pos - 1] + self.text[self.cursor_pos:]
                    self.cursor_pos -= 1
            elif event.key == pygame.K_DELETE:
                self.text = self.text[:self.cursor_pos] + self.text[self.cursor_pos + 1:]
            elif event.key == pygame.K_LEFT:
                self.cursor_pos = max(0, self.cursor_pos - 1)
            elif event.key == pygame.K_RIGHT:
                self.cursor_pos = min(len(self.text), self.cursor_pos + 1)
            elif event.key == pygame.K_HOME:
                self.cursor_pos = 0
            elif event.key == pygame.K_END:
                self.cursor_pos = len(self.text)
            elif event.key == pygame.K_RETURN or event.key == pygame.K_KP_ENTER:
                if self.callback:
                    self.callback(self.text)
                self.is_focused = False

        elif event.type == pygame.TEXTINPUT:
            if len(self.text) < self.max_length:
                self.text = self.text[:self.cursor_pos] + event.text + self.text[self.cursor_pos:]
                self.cursor_pos += len(event.text)

    def draw(self, app):
        # Update cursor blink state
        if self.is_focused:
            self.cursor_timer += app.clock.get_time()
            if self.cursor_timer >= 500:  # Blink every 500ms
                self.cursor_timer %= 500
                self.cursor_visible = not self.cursor_visible
        else:
            self.cursor_visible = False

        drawing.draw_text_input(app, self.rect, self.text, self.is_focused, self.cursor_pos, self.cursor_visible)


class ToggleSwitch(Widget):
    """A modern on/off toggle switch."""

    def __init__(self, rect, is_on, callback):
        # A toggle's rect should be roughly 2:1 width to height
        super().__init__(rect)
        self.is_on = is_on
        self.callback = callback

    def handle_event(self, event, mouse_pos):
        super().handle_event(event, mouse_pos)
        if event.type == pygame.MOUSEBUTTONUP and event.button == 1 and self.is_hovered:
            self.is_on = not self.is_on
            if self.callback:
                self.callback(self.is_on)

    def draw(self, app):
        drawing.draw_toggle_switch(app, self.rect, self.is_on, self.is_hovered)


class ProgressBar(Widget):
    """A simple progress bar widget."""

    def __init__(self, rect, min_val=0, max_val=100, initial_val=0):
        super().__init__(rect)
        self.min_val = min_val
        self.max_val = max_val
        self.value = initial_val

    def set_value(self, new_val):
        self.value = max(self.min_val, min(self.max_val, new_val))

    def draw(self, app):
        drawing.draw_progress_bar(app, self.rect, self.value, self.min_val, self.max_val)


class Dropdown(Widget):
    """A dropdown menu for selecting from multiple options."""

    def __init__(self, rect, options, initial_index=0, callback=None):
        super().__init__(rect)
        self.options = options
        self.selected_index = initial_index
        self.is_open = False
        self.callback = callback

    def handle_event(self, event, mouse_pos):
        super().handle_event(event, mouse_pos)

        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if self.is_hovered:
                self.is_open = not self.is_open
            elif self.is_open:
                # Check if clicked on one of the expanded options
                for i, option in enumerate(self.options):
                    option_rect = pygame.Rect(self.rect.x, self.rect.y + (i + 1) * self.rect.height,
                                              self.rect.width, self.rect.height)
                    if option_rect.collidepoint(mouse_pos):
                        self.selected_index = i
                        self.is_open = False
                        if self.callback:
                            self.callback(option)
                        break
                else:
                    self.is_open = False

    def draw(self, app):
        drawing.draw_dropdown(app, self.rect, self.options, self.selected_index, self.is_open)

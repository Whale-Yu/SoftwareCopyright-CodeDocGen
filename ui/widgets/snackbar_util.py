# -*- coding: utf-8 -*-
import flet as ft


def show_snackbar(
    page: ft.Page,
    message: str,
    is_error: bool = False,
    bgcolor=None,
    color=None,
    behavior: ft.SnackBarBehavior | None = None,
    dismiss_direction: ft.DismissDirection | None = None,
    show_close_icon: bool = False,
    close_icon_color=None,
    action: str | ft.SnackBarAction | None = None,
    duration: ft.DurationValue = ft.Duration(milliseconds=4000),
    margin: ft.MarginValue | None = None,
    padding: ft.PaddingValue | None = None,
    width: float | None = None,
    elevation: float | None = None,
    shape: ft.OutlinedBorder | None = None,
    clip_behavior: ft.ClipBehavior = ft.ClipBehavior.HARD_EDGE,
    action_overflow_threshold: float | None = 0.25,
    persist: bool | None = None,
    on_action=None,
    on_visible=None,
    on_dismiss=None,
):
    if bgcolor is None:
        bgcolor = ft.Colors.RED_100 if is_error else ft.Colors.GREEN_100
    if color is None:
        color = ft.Colors.RED_800 if is_error else ft.Colors.GREEN_800

    snack = ft.SnackBar(
        content=ft.Text(message, color=color),
        bgcolor=bgcolor,
        behavior=behavior,
        dismiss_direction=dismiss_direction,
        show_close_icon=show_close_icon,
        close_icon_color=close_icon_color,
        action=action,
        duration=duration,
        margin=margin,
        padding=padding,
        width=width,
        elevation=elevation,
        shape=shape,
        clip_behavior=clip_behavior,
        action_overflow_threshold=action_overflow_threshold,
        persist=persist,
        on_action=on_action,
        on_visible=on_visible,
        on_dismiss=on_dismiss,
    )
    page.show_dialog(snack)

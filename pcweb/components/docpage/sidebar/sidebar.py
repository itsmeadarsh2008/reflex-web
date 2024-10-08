"""Logic for the sidebar component."""

from __future__ import annotations

import reflex as rx
from pcweb import styles
from pcweb.components.docpage.navbar.state import NavbarState
from pcweb.route import Route
from .state import SidebarState, SidebarItem

from .sidebar_items.learn import learn, frontend, backend, hosting
from .sidebar_items.component_lib import (
    get_component_link,
    component_lib,
    graphing_libs,
    other_libs,
)
from .sidebar_items.reference import api_reference, tutorials
from .sidebar_items.recipes import recipes
from pcweb.styles.colors import c_color
from pcweb.styles.fonts import small
from pcweb.styles.shadows import shadows


heading_style2 = {
    "background_color": rx.color("accent", 3),
    "border_radius": "0.5em",
    "width": "100%",
    "padding_left": "0.5em",
    "padding_right": "0.5em",
}


def sidebar_link(*children, **props):
    """Create a sidebar link that closes the sidebar when clicked."""
    on_click = props.pop("on_click", NavbarState.set_sidebar_open(False))
    return rx.link(
        *children,
        on_click=on_click,
        underline="none",
        **props,
    )


def sidebar_leaf(
    item: SidebarItem,
    url: str,
) -> rx.Component:
    """Get the leaf node of the sidebar."""
    item.link = item.link.replace("_", "-")
    if not item.link.endswith("/"):
        item.link += "/"
    if item.outer:
        return sidebar_link(
            rx.flex(
                rx.text(
                    item.names,
                    color=rx.cond(
                        item.link == url,
                        c_color("violet", 9),
                        c_color("slate", 9),
                    ),
                    _hover={
                        "color": c_color("slate", 11),
                        "text_decoration": "none",
                    },
                    transition="color 0.035s ease-out",
                    margin_left="0.5em",
                    margin_top="0.5em",
                    margin_bottom="0.2em",
                    width="100%",
                ),
            ),
            href=item.link,
        )

    return rx.list_item(
        rx.chakra.accordion_item(
            rx.cond(
                item.link == url,
                sidebar_link(
                    rx.flex(
                        rx.flex(
                            rx.text(
                                item.names,
                                color=c_color("violet", 9),
                                style={**small},
                                transition="color 0.035s ease-out",
                            ),
                        ),
                        padding="0px 8px 0px 28px",
                        border_left=f"1.5px solid {c_color('violet', 9)}",
                    ),
                    _hover={"text_decoration": "none"},
                    href=item.link,
                ),
                sidebar_link(
                    rx.flex(
                        rx.text(
                            item.names,
                            color=c_color("slate", 9),
                            _hover={
                                "color": c_color("slate", 11),
                                "text_decoration": "none",
                            },
                            transition="color 0.035s ease-out",
                            style={**small},
                            width="100%",
                        ),
                        padding="0px 8px 0px 28px",
                        border_left=f"1.5px solid {c_color('slate', 4)}",
                        _hover={"border_left": f"1.5px solid {c_color('slate', 8)}"},
                    ),
                    _hover={"text_decoration": "none"},
                    href=item.link,
                ),
            ),
            border="none",
            width="100%",
        ),
        width="100%",
    )


def sidebar_icon(name):
    mappings = {
        "Getting Started": "rocket",
        "Tutorial": "life-buoy",
        "Components": "layers",
        "Pages": "sticky-note",
        "Styling": "palette",
        "Assets": "folder-open-dot",
        "Wrapping React": "atom",
        "Vars": "variable",
        "Events": "arrow-left-right",
        "Substates": "boxes",
        "API Routes": "route",
        "Client Storage": "package-open",
        "Database": "database",
        "Authentication": "lock-keyhole",
        "Utility Methods": "cog",
        "Reflex Deploy": "earth",
        "Self Hosting": "server",
        "Custom Components": "blocks",
    }

    if name in mappings:
        return rx.icon(
            tag=mappings[name],
            size=16,
            margin_right="20px",
        )
    else:
        return rx.fragment()


def sidebar_item_comp(
    item: SidebarItem,
    index: list[int],
    url: str,
):
    return rx.cond(
        len(item.children) == 0,
        sidebar_leaf(item=item, url=url),
        rx.chakra.accordion_item(
            rx.chakra.accordion_button(
                sidebar_icon(item.names),
                rx.text(
                    item.names,
                    style=small,
                ),
                rx.box(
                    flex_grow=1,
                ),
                rx.chakra.accordion_icon(width="16px", height="16px"),
                align_items="center",
                transition="color 0.035s ease-out",
                _hover={
                    "color": c_color("slate", 11),
                },
                style={
                    "&[aria-expanded='true']": {
                        "color": c_color("slate", 11),
                    },
                },
                color=c_color("slate", 9),
                width="100%",
                padding_y="8px",
                padding_left="8px",
                padding_right="0px",
            ),
            rx.chakra.accordion_panel(
                rx.chakra.accordion(
                    rx.unordered_list(
                        *[
                            sidebar_item_comp(item=child, index=index, url=url)
                            for child in item.children
                        ],
                        align_items="flex-start",
                        flex_direction="column",
                        gap="16px",
                        display="flex",
                        margin_left="15px !important",
                        box_shadow=rx.cond(
                            item in other_libs,
                            "none",
                            f"inset 1px 0 0 0 {c_color('slate', 4)}",
                        ),
                        list_style_type="none",
                    ),
                    margin_y="8px",
                    allow_multiple=True,
                    default_index=rx.cond(index, index[1:2], []),
                ),
                padding="0px",
                width="100%",
            ),
            border="none",
            width="100%",
        ),
    )


def calculate_index(sidebar_items, url: str):
    if not isinstance(sidebar_items, list):
        sidebar_items = [sidebar_items]
    if url is None:
        return None
    for item in sidebar_items:
        if not item.link.endswith("/"):
            item.link = item.link + "/"
    if not url.endswith("/"):
        url = url + "/"
    sub = 0
    for i, item in enumerate(sidebar_items):
        if len(item.children) == 0:
            sub += 1
        if item.link == url:
            return [i - sub]
        index = calculate_index(item.children, url)
        if index is not None:
            return [i - sub] + index
    return None


sidebar_items = (
    learn
    + frontend
    + backend
    + hosting
    + component_lib
    + graphing_libs
    + other_libs
    + recipes
    + api_reference
    + tutorials
)
# Flatten the list of sidebar items
flat_items = []

def append_to_items(items):
    for item in items:
        if len(item.children) == 0:
            flat_items.append(item)
        append_to_items(item.children)
append_to_items(sidebar_items)

def get_prev_next(url):
    """Get the previous and next links in the sidebar."""
    url = url.strip("/")
    for i, item in enumerate(flat_items):
        if item.link.strip("/") == url:
            if i == 0:
                return None, flat_items[i + 1]
            elif i == len(flat_items) - 1:
                return flat_items[i - 1], None
            else:
                return flat_items[i - 1], flat_items[i + 1]
    return None, None


def sidebar_category(name: str, url: str, icon: str, index: int):
    return rx.list_item(
        rx.link(
            rx.hstack(
                rx.hstack(
                    rx.box(
                        rx.icon(
                            tag=icon,
                            color=c_color("slate", 9),
                            size=16,
                        ),
                        height="32px",
                        width="32px",
                        padding="8px",
                        border_radius="8px",
                        align_items="center",
                        display="flex",
                        justify_content="center",
                        border=f"1px solid {c_color('slate', 4)}",
                        background_color=c_color("white", 1),
                        box_shadow=shadows["medium"],
                    ),
                    rx.heading(
                        name,
                        color=rx.cond(
                            SidebarState.sidebar_index == index,
                            c_color("slate", 11),
                            c_color("slate", 9),
                        ),
                        as_="h3",
                        style={**small},
                    ),
                    width="100%",
                    justify="start",
                    align_items="center",
                    gap="12px",
                ),
                rx.box(
                    width="7px",
                    height="7px",
                    flex_shrink=0,
                    background_color=c_color("violet", 9),
                    border_radius="50%",
                    visibility=rx.cond(
                        SidebarState.sidebar_index == index,
                        "visible",
                        "hidden",
                    ),
                ),
                _hover={
                    "background_color": c_color("slate", 3),
                },
                background_color=rx.cond(
                    SidebarState.sidebar_index == index,
                    c_color("slate", 3),
                    "transparent",
                ),
                transition="background-color 0.075s ease-out",
                align_items="center",
                justify="start",
                padding="8px 16px 8px 8px",
                justify_content="space-between",
                border_radius="16px",
                align_self="stretch",
                width="100%",
            ),
            on_click=lambda: SidebarState.set_sidebar_index(index),
            width="100%",
            underline="none",
            href=url,
        ),
        width="100%",
    )


def create_sidebar_section(section_title, section_url, items, index, url):
    # Check if the section has any nested sections (Like the Other Libraries Section)
    nested = any(len(child.children) > 0 for item in items for child in item.children)
    # Make sure the index is a list
    index = index.to(list)
    return rx.list_item(
        rx.link(
            rx.heading(
                section_title,
                as_="h5",
                style={
                    "color": c_color("slate", 12),
                    "font-family": "Instrument Sans",
                    "font-size": "14px",
                    "font-style": "normal",
                    "font-weight": "600",
                    "line-height": "20px",
                    "letter-spacing": "-0.21px",
                    "transition": "color 0.035s ease-out",
                    "_hover": {
                        "color": c_color("violet", 9),
                    },
                },
            ),
            underline="none",
            padding_y="12px",
            href=section_url,
        ),
        rx.chakra.accordion(
            *[
                sidebar_item_comp(
                    item=item,
                    index=index if nested else [-1],
                    url=url,
                )
                for item in items
            ],
            allow_multiple=True,
            default_index=index if index is not None else [],
            width="100%",
            padding_left="0em",
            margin_left="0em",
        ),
        margin_left="0em",
        direction="column",
        width="100%",
        flex_direction="column",
        display="flex",
        align_items="left",
    )


@rx.memo
def sidebar_comp(
    url: str,
    learn_index: list[int],
    component_lib_index: list[int],
    frontend_index: list[int],
    backend_index: list[int],
    hosting_index: list[int],
    graphing_libs_index: list[int],
    other_libs_index: list[int],
    api_reference_index: list[int],
    recipes_index: list[int],
    tutorials_index: list[int],
    width: str = "100%",
):

    from pcweb.pages.docs.recipes_overview import overview
    from pcweb.pages.docs.library import library
    from pcweb.pages.docs.custom_components import custom_components
    from pcweb.pages.docs import (
        getting_started,
        state,
        ui,
        hosting as hosting_page,
        datatable_tutorial,
    )
    from pcweb.pages.docs.apiref import pages

    ul_style = {
        "display": "flex",
        "flex_direction": "column",
        "align_items": "flex-start",
    }

    return rx.flex(
        rx.unordered_list(
            sidebar_category(
                "Learn", getting_started.introduction.path, "graduation-cap", 0
            ),
            sidebar_category("Components", library.path, "layout-panel-left", 1),
            sidebar_category("Recipes", overview.path, "scan-text", 2),
            sidebar_category("API Reference", pages[0].path, "book-text", 3),
            style=ul_style,
            margin_left="0px !important",
            list_style_type="none",
            gap="4px",
        ),
        rx.match(
            SidebarState.sidebar_index,
            (
                0,
                rx.unordered_list(
                    create_sidebar_section(
                        "Onboarding",
                        getting_started.introduction.path,
                        learn,
                        learn_index,
                        url,
                    ),
                    create_sidebar_section(
                        "User Interface",
                        ui.overview.path,
                        frontend,
                        frontend_index,
                        url,
                    ),
                    create_sidebar_section(
                        "State", state.overview.path, backend, backend_index, url
                    ),
                    create_sidebar_section(
                        "Hosting",
                        hosting_page.deploy_quick_start.path,
                        hosting,
                        hosting_index,
                        url,
                    ),
                    style=ul_style,
                    margin_left="0px !important",
                    list_style_type="none",
                    padding="0px 16px 0px 8px",
                    gap="24px",
                ),
            ),
            (
                1,
                rx.unordered_list(
                    create_sidebar_section(
                        "Core", library.path, component_lib, component_lib_index, url
                    ),
                    create_sidebar_section(
                        "Graphing",
                        library.path,
                        graphing_libs,
                        graphing_libs_index,
                        url,
                    ),
                    create_sidebar_section(
                        "Other Libraries",
                        library.path,
                        other_libs,
                        other_libs_index,
                        url,
                    ),
                    rx.link(
                        rx.vstack(
                            rx.hstack(
                                rx.icon("atom", size=16),
                                rx.heading(
                                    "Custom Components",
                                    as_="h5",
                                    style={
                                        "font-family": "Instrument Sans",
                                        "font-size": "14px",
                                        "font-style": "normal",
                                        "font-weight": "600",
                                        "line-height": "20px",
                                        "letter-spacing": "-0.21px",
                                    },
                                ),
                                align_items="center",
                                gap="12px",
                                color=c_color("slate", 12),
                            ),
                            rx.text(
                                "See what components people have made with Reflex!",
                                style=small,
                                color=c_color("slate", 9),
                            ),
                            gap="8px",
                            padding="8px 16px",
                            border_radius="12px",
                            margin_top="12px",
                            border=f"1px solid {c_color('slate', 5)}",
                            background_color=c_color("slate", 1),
                            _hover={
                                "background_color": c_color("slate", 3),
                            },
                            transition="background-color 0.075s ease-out",
                            box_shadow=shadows["large"],
                        ),
                        underline="none",
                        href=custom_components.path,
                    ),
                    style=ul_style,
                    margin_left="0px !important",
                    list_style_type="none",
                    padding="0px 16px 0px 8px",
                    gap="24px",
                ),
            ),
            (
                2,
                rx.unordered_list(
                    create_sidebar_section(
                        "Recipes", overview.path, recipes, recipes_index, url
                    ),
                    style=ul_style,
                    margin_left="0px !important",
                    list_style_type="none",
                    padding="0px 16px 0px 8px",
                    gap="24px",
                ),
            ),
            (
                3,
                rx.unordered_list(
                    create_sidebar_section(
                        "Reference",
                        pages[0].path,
                        api_reference,
                        api_reference_index,
                        url,
                    ),
                    create_sidebar_section(
                        "Tutorials",
                        datatable_tutorial.simple_table.path,
                        tutorials,
                        tutorials_index,
                        url,
                    ),
                    style=ul_style,
                    margin_left="0px !important",
                    list_style_type="none",
                    padding="0px 16px 0px 8px",
                    gap="24px",
                ),
            ),
        ),
        direction="column",
        align_items="left",
        overflow_y="scroll",
        max_height="90%",
        width=width,
        gap="24px",
        padding=["8px", "8px", "8px", "0px", "0px"],
        padding_bottom="6em !important",
        position="fixed",
        scrollbar_width="none",
        scroll_padding="1em",
        style={
            "&::-webkit-scrollbar-thumb": {
                "background_color": "transparent",
            },
            "&::-webkit-scrollbar": {
                "background_color": "transparent",
            },
        },
    )


def sidebar(url=None, width: str = "100%") -> rx.Component:
    """Render the sidebar."""
    learn_index = calculate_index(learn, url)
    component_lib_index = calculate_index(component_lib, url)
    frontend_index = calculate_index(frontend, url)
    backend_index = calculate_index(backend, url)
    hosting_index = calculate_index(hosting, url)
    graphing_libs_index = calculate_index(graphing_libs, url)
    other_libs_index = calculate_index(other_libs, url)
    api_reference_index = calculate_index(api_reference, url)
    recipes_index = calculate_index(recipes, url)
    tutorials_index = calculate_index(tutorials, url)

    return rx.flex(
        sidebar_comp(
            url=url,
            learn_index=learn_index,
            component_lib_index=component_lib_index,
            frontend_index=frontend_index,
            backend_index=backend_index,
            hosting_index=hosting_index,
            graphing_libs_index=graphing_libs_index,
            other_libs_index=other_libs_index,
            api_reference_index=api_reference_index,
            recipes_index=recipes_index,
            tutorials_index=tutorials_index,
            width=width,
        ),
        width="100%",
        height="100%",
        justify="end",
    )


sb = sidebar(width="100%")

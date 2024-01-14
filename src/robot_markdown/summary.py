"""Helper functions to create a SUMMARY.md file that can be used with the mkdocs literate-nav plugin."""

from textwrap import indent


def create_summary(items: list) -> str:
    """Create a markdown summary for a list of file paths.

    The generated markdown can be used to create a SUMMARY.md file
    for the literate-nav mkdocs-plugin

    Parameters:
        items: A list of paths

    Returns:
        A markdown string.
    """
    summary_dict, _ = _create_dirtree(items)
    return _to_markdown(summary_dict)


def _create_dirtree(item_paths: list, *, path_separator: str = "/") -> tuple:
    result: tuple = ({}, [])
    for path in item_paths:
        current = result
        nodes = path.split(path_separator)[1:]
        last_idx = len(nodes) - 1
        for idx, node in enumerate(nodes):
            childdirs, files = current
            if idx == last_idx:
                files.append(node)
            else:
                if node not in childdirs:
                    childdirs[node] = ({}, [])
                current = childdirs[node]
    return result


def _to_markdown(items_dict: dict, path: str = "") -> str:
    md_list = ""
    for key, value in items_dict.items():
        childdirs, files = value
        if childdirs:
            md_list += f"* {key.replace('_', ' ')}\n"
            md_list += indent(_to_markdown(childdirs, f"{path}{key}/"), "    ")
        elif len(files) == 1:
            md_list += f"* [{key.replace('_', ' ')}]({path}{key}/{files[0]})\n"
        else:
            md_list += f"* {key.replace('_', ' ')}\n"
            for f in files:
                md_list += f"    * [{f.replace('_', ' ')}]({path}{key}/{f})\n"

    return md_list

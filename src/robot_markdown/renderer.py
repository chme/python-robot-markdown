"""Module for converting RobotFramework result XML file (output.xml) to markdown."""

import os

from jinja2 import Environment, PackageLoader, select_autoescape
from robot.api import ExecutionResult


class Renderer:
    """Renderer class responsible for converting RobotFramework result files to markdown."""

    def __init__(self, theme: str = "mkdocs-material") -> None:
        """Creates a new renderer that will the given theme.

        Parameters:
            theme: The theme (Jinja templates) to be used
        """
        self.theme = theme
        self.jinjaEnv = Environment(
            loader=PackageLoader("robot_markdown", f"templates/{theme}"),
            autoescape=select_autoescape(),
            trim_blocks=True,
        )
        self.template = self.jinjaEnv.get_template("testreport.md.jinja")

    def render(self, robot_result_file: str) -> str:
        """Convert a RobotFramework result XML to markdown.

        Read and parse the given file and convert it to markdown using Jinja templates.

        Parameters:
            robot_result_file: A RobotFramework test execution result file.

        Returns:
            A markdown string.
        """
        output_dir = os.path.abspath(os.path.dirname(robot_result_file)) + "/"
        result = ExecutionResult(robot_result_file)
        return self.template.render(robot=result, output_dir=output_dir)

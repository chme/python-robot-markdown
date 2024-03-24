"""Module for converting RobotFramework result XML file (output.xml) to markdown."""

import os

from dotenv import dotenv_values
from jinja2 import Environment, PackageLoader, select_autoescape
from robot.api import ExecutionResult

from robot_markdown.template_util import TemplateUtil


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

    def render(self, robot_result_file: str, env_file: str | None = None) -> str:
        """Convert a RobotFramework result XML to markdown.

        Read and parse the given file and convert it to markdown using Jinja templates.

        Parameters:
            robot_result_file: A RobotFramework test execution result file.
            env_file: Optional .env file.

        Returns:
            A markdown string.
        """
        robot_env = None
        robot_env = dotenv_values(env_file) if env_file else None
        output_dir = os.path.abspath(os.path.dirname(robot_result_file)) + "/"
        result = ExecutionResult(robot_result_file)
        util = TemplateUtil(output_dir)
        return self.template.render(robot=result, robot_env=robot_env, output_dir=output_dir, robot_util=util)

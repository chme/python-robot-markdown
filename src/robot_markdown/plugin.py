"""MkDocs plugin to integrate RobotFramework test reports."""

import os
import tempfile

from mkdocs.config import config_options as c
from mkdocs.config.base import Config
from mkdocs.config.defaults import MkDocsConfig
from mkdocs.plugins import BasePlugin, event_priority
from mkdocs.structure.files import File, Files

from robot_markdown.renderer import Renderer
from robot_markdown.summary import create_summary


class _ReportConfig(Config):
    robot_reports_dir = c.Type(str)
    robot_output_xml = c.Type(str, default="output.xml")
    create_summary_md = c.Type(bool, default=False)
    summary_md_file = c.Type(str, default="SUMMARY.md")
    docs_rel_dir = c.Type(str, default="tests")
    docs_md_file = c.Type(str, default="testreport.md")
    overwrite_cached_files = c.Type(bool, default=False)
    cache_dir = c.Type(str, default="")


class RobotConfig(Config):
    """Data class for mkdocs plugin config."""

    reports = c.ListOfItems(c.SubConfig(_ReportConfig))


class RobotPlugin(BasePlugin[RobotConfig]):
    """mkdocs plugin to integrate RobotFramework test execution results."""

    def on_files(self, files: Files, *, config: MkDocsConfig) -> Files:
        """Handle the on_files event hook."""
        self._cachedirs = []

        renderer = Renderer()
        for report_config in self.config.reports:
            if report_config.cache_dir:
                self._process(renderer, report_config, report_config.cache_dir, files, config)
            else:
                cachedir = tempfile.TemporaryDirectory(prefix="mkdocs_robot_")
                self._cachedirs.append(cachedir)
                self._process(renderer, report_config, cachedir.name, files, config)

        return files

    @event_priority(-100)
    def on_post_build(self, config: MkDocsConfig) -> None:  # noqa: ARG002 (inherited method)
        """Handle the on_post_build event hook."""
        for cachedir in self._cachedirs:
            cachedir.cleanup()

    def _process(
        self,
        renderer: Renderer,
        report_config: _ReportConfig,
        cachedir: str,
        files: Files,
        config: MkDocsConfig,
    ) -> None:
        summary_items = []

        for dirpath, _, filenames in os.walk(report_config.robot_reports_dir):
            if report_config.robot_output_xml not in filenames:
                continue

            rel_dir = dirpath.removeprefix(f"{report_config.robot_reports_dir}/")
            xml_file = f"{dirpath}/{report_config.robot_output_xml}"
            md_file = f"{report_config.docs_rel_dir}/{rel_dir}/{report_config.docs_md_file}"
            overwrite = report_config.overwrite_cached_files

            md_content = renderer.render(xml_file)
            self._write_file(md_content, f"{cachedir}/{md_file}", overwrite=overwrite)

            files.append(
                File(
                    md_file,
                    cachedir,
                    config["site_dir"],
                    config["use_directory_urls"],
                ),
            )
            summary_items.append(md_file)

        if report_config.create_summary_md:
            summary_contents = create_summary(summary_items)
            summary_file = f"{report_config.docs_rel_dir}/{report_config.summary_md_file}"
            self._write_file(summary_contents, f"{cachedir}/{summary_file}", overwrite=True)
            files.append(
                File(
                    summary_file,
                    cachedir,
                    config["site_dir"],
                    config["use_directory_urls"],
                ),
            )

    def _write_file(self, content: str, output_path: str, *, overwrite: bool = False) -> None:
        """Write content to output_path, making sure any parent directories exist."""
        if not overwrite and os.path.isfile(output_path):
            return
        output_dir = os.path.dirname(output_path)
        os.makedirs(output_dir, exist_ok=True)
        with open(output_path, "w") as f:
            f.write(content)

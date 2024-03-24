"""MkDocs plugin to integrate RobotFramework test reports."""

import os
import re
import shutil
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
    copy_files = c.Type(bool, default=False)
    copy_files_include = c.Type(str, default="^.*\\.(txt|json|xml|html|env)$")
    env_file = c.Type(str, default="")


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

            if report_config.copy_files:
                self._copy_report_dir(dirpath, report_config, cachedir, files, config["site_dir"])

            md_file = self._process_report_dir(dirpath, renderer, report_config, cachedir, files, config["site_dir"])
            summary_items.append(md_file)

        if report_config.create_summary_md:
            summary_contents = create_summary(summary_items)
            summary_file = os.path.join(report_config.docs_rel_dir, report_config.summary_md_file)
            self._write_file(summary_contents, os.path.join(cachedir, summary_file), overwrite=True)
            files.append(
                File(
                    summary_file,
                    cachedir,
                    config["site_dir"],
                    use_directory_urls=False,
                ),
            )

    def _process_report_dir(
        self,
        dirpath: str,
        renderer: Renderer,
        report_config: _ReportConfig,
        cachedir: str,
        files: Files,
        site_dir: str,
    ) -> str:
        rel_dir = os.path.relpath(dirpath, report_config.robot_reports_dir)
        xml_file = os.path.join(dirpath, report_config.robot_output_xml)
        rel_md_file = os.path.join(rel_dir, report_config.docs_md_file)
        md_file = os.path.join(report_config.docs_rel_dir, rel_md_file)
        overwrite = report_config.overwrite_cached_files
        env_file = os.path.join(dirpath, report_config.env_file) if report_config.env_file else None

        md_content = renderer.render(xml_file, env_file=env_file)
        self._write_file(md_content, os.path.join(cachedir, md_file), overwrite=overwrite)

        files.append(
            File(
                md_file,
                cachedir,
                site_dir,
                use_directory_urls=False,
            ),
        )

        return "/" + rel_md_file

    def _write_file(self, content: str, output_path: str, *, overwrite: bool = False) -> None:
        """Write content to output_path, making sure any parent directories exist."""
        if not overwrite and os.path.isfile(output_path):
            return
        output_dir = os.path.dirname(output_path)
        os.makedirs(output_dir, exist_ok=True)
        with open(output_path, "w") as f:
            f.write(content)

    def _copy_report_dir(
        self,
        report_dir: str,
        report_config: _ReportConfig,
        cachedir: str,
        files: Files,
        site_dir: str,
    ) -> None:
        filepattern = re.compile(report_config.copy_files_include)
        for dirpath, _, filenames in os.walk(report_dir):
            rel_dir = dirpath.removeprefix(f"{report_config.robot_reports_dir}/")
            for filename in filenames:
                rel_file = f"{report_config.docs_rel_dir}/{rel_dir}/{filename}"
                target_file = f"{cachedir}/{rel_file}"
                source_file = f"{dirpath}/{filename}"
                if not filepattern.match(source_file):
                    continue
                target_dir = os.path.dirname(target_file)
                os.makedirs(target_dir, exist_ok=True)
                shutil.copy(source_file, f"{cachedir}/{rel_file}")
                files.append(
                    File(
                        rel_file,
                        cachedir,
                        site_dir,
                        use_directory_urls=False,
                    ),
                )

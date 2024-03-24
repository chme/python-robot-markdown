"""Helper classes and function for the Jinja template."""

from robot.result.model import Keyword, Message, TestCase


class TemplateUtil:
    """Helper class for the Jinja template."""

    def __init__(self, output_dir: str) -> None:
        """Creates a new util instance.

        Parameters:
            output_dir: The original output directory of the Robot tests
        """
        self.output_dir = output_dir

    def get_log_messages(self, kw: Keyword | TestCase) -> list[Message]:
        """Returns all log messages of a keyword or a test case and all its children.

        Parameters:
            kw: Either a Keyword or a Testcase

        Retunrs:
            List of messages
        """
        if hasattr(kw, "type") and kw.type == Keyword.MESSAGE:
            if kw.html:
                kw.message = kw.message.replace(f"file://{self.output_dir}", "")
            return [kw]
        if not hasattr(kw, "body"):
            return []

        messages: list[Message] = []
        for item in kw.body:
            messages.extend(self.get_log_messages(item))

        return messages

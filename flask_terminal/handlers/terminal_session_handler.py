import os
import pty
import select
from flask_terminal.config.logger_config import configure_logger

logging = configure_logger('terminal_session_handler')

class TerminalSessionHandler:
    def __init__(self):
        self.master_fd, self.slave_fd = None, None

    def start_session(self):
        """Starts a new terminal session."""
        logging.info("Starting a new terminal session...")
        try:
            self.master_fd, self.slave_fd = pty.openpty()
            subprocess_pid = os.fork()
            if subprocess_pid == 0:
                # In child
                os.setsid()
                os.dup2(self.slave_fd, 0)  # stdin
                os.dup2(self.slave_fd, 1)  # stdout
                os.dup2(self.slave_fd, 2)  # stderr
                os.close(self.master_fd)
                os.execv('/bin/sh', ['/bin/sh'])
            else:
                # In parent
                os.close(self.slave_fd)
                logging.info(f"Started terminal session with PID: {subprocess_pid}")
        except Exception as e:
            logging.error(f"Error starting terminal session: {e}", exc_info=True)

    def execute_command(self, command):
        """Executes a command in the terminal session."""
        logging.info(f"Executing command: {command}")
        try:
            if self.master_fd is not None:
                os.write(self.master_fd, command.encode() + b'\n')
                logging.info(f"Executed command: {command}")
        except Exception as e:
            logging.error(f"Error executing command: {e}", exc_info=True)

    def capture_output(self):
        """Captures the output from the terminal session."""
        logging.info("Capturing output from the terminal session...")
        output = b''
        try:
            if self.master_fd is not None:
                ready, _, _ = select.select([self.master_fd], [], [], 0.1)
                if ready:
                    output = os.read(self.master_fd, 1024)
                    logging.info(f"Captured output: {output.decode()}")
        except Exception as e:
            logging.error(f"Error capturing output: {e}", exc_info=True)
        return output.decode()

    def close_session(self):
        """Closes the terminal session."""
        logging.info("Closing the terminal session...")
        try:
            if self.master_fd is not None:
                os.close(self.master_fd)
                logging.info("Terminal session closed.")
        except Exception as e:
            logging.error(f"Error closing terminal session: {e}", exc_info=True)
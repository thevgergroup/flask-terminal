from flask import Blueprint, jsonify, render_template, request, current_app, session, redirect
from flask_terminal.handlers.terminal_session_handler import TerminalSessionHandler

terminal_blueprint = Blueprint('terminal_blueprint', __name__ , 
                                template_folder='templates', 
                                static_folder='static')

session_handler = TerminalSessionHandler()


@terminal_blueprint.route('/init')
def init_terminal_session():
    """
    Initializes a terminal session.
    Creates a new pseudo-terminal and starts a shell process.

    Returns:
        A JSON response with a success message if the session is initialized successfully,
        or an error message if an exception occurs.
    """
    current_app.logger.info("Attempting to initialize terminal session...")
    try:
        # Initialization logic here
        session_handler.start_session()
        current_app.logger.info("Terminal session initialized successfully.")
        return jsonify(message="Initializing terminal session..."), 200
    except Exception as e:
        current_app.logger.error(f"Error initializing terminal session: {e}", exc_info=True)
        return jsonify(error="An error occurred while initializing the terminal session"), 500


# TODO: Handle escaped carriage returns and newlines in command input
@terminal_blueprint.route('/execute', methods=['POST'])
def execute_command():
    """
    Executes a command in the terminal session.
    Takes a single line command from the request body and writes it to the master file descriptor.

    Returns:
        A JSON response with a success message if the command is executed successfully,
        or an error message if an exception occurs.
    """
    current_app.logger.info("Attempting to execute command...")
    try:
        command = request.json['command']
        session_handler.execute_command(command)
        current_app.logger.info(f"Command executed: {command}")
        return jsonify(message="Command executed."), 200
    except Exception as e:
        current_app.logger.error(f"Error executing command: {e}", exc_info=True)
        return jsonify(error="An error occurred while executing the command"), 500

@terminal_blueprint.route('/poll')
def poll_output():
    """
    Polls for the output of the executed command in the terminal session.

    Returns:
        A JSON response with the output of the command if available,
        or an error message if an exception occurs.
    """
    current_app.logger.info("Attempting to poll for command output...")
    try:
        output = session_handler.capture_output()
        if output:
            current_app.logger.info(f"Command output: {output}")
        return jsonify(output=output), 200
    except Exception as e:
        current_app.logger.error(f"Error polling for command output: {e}", exc_info=True)
        return jsonify(error="An error occurred while polling for command output"), 500

@terminal_blueprint.route('/stop')
def close_terminal_session():
    """
    Closes the terminal session.

    Returns:
        A JSON response with a success message if the session is closed successfully,
        or an error message if an exception occurs.
    """
    current_app.logger.info("Attempting to close terminal session...")
    try:
        session_handler.close_session()
        current_app.logger.info("Terminal session closed successfully.")
        return jsonify(message="Closing terminal session..."), 200
    except Exception as e:
        current_app.logger.error(f"Error closing terminal session: {e}", exc_info=True)
        return jsonify(error="An error occurred while closing the terminal session"), 500


@terminal_blueprint.route('/')
def terminal():
    """
    Renders the terminal interface.

    Returns:
        The rendered template for the terminal interface if successful,
        or an error message if an exception occurs.
    """
    current_app.logger.info("Accessing the terminal interface...")
    try:
        return render_template('flask-terminal/terminal.html'), 200
    except Exception as e:
        current_app.logger.error(f"Error accessing the terminal interface: {e}", exc_info=True)
        return jsonify(error="An error occurred while accessing the terminal interface"), 500
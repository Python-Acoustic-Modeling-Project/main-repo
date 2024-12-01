# Include libraries
import tkinter as tk
from controller import Controller
from view import View
from model import Model

# Main function
def main():
    """
    Entry point for the SPIDAM Audio Analysis Tool.
    Initializes the model, view, and controller before starting the application.
    """

    # Initialize the MVC components
    model = Model()
    controller = Controller(model)
    view = View(controller)

    # Set the view in the controller
    controller.set_view(view)

# Execute program
if __name__ == "__main__":
    main()

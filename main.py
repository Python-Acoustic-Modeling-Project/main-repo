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

    # Creates main application window
    root = tk.Tk()
    root.title("SPIDAM Audio Analysis Tool")

    # Initialize the MVC components
    model = Model()
    controller = Controller(root, model)
    view = View(root, controller)

    # Set the view in the controller
    controller.set_view(view)

    # Run mainloop to start the application
    root.mainloop()

# Execute program
if __name__ == "__main__":
    main()

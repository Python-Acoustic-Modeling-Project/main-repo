# Include libraries
import tkinter as tk
from controller import Controller
from view import View
from model import Model

# Main function
def main():
    """
    Entry point for the audio analysis application.
    Intializes the model, view, and controller.
    """

    # Create the main application window
    root = tk.Tk()
    root.minsize(1000,800)
    root.title("SPIDAM Audio Analysis Tool")

    # Initialize the MVC components
    model = Model()
    controller = Controller(root, model)
    view = View(root, controller)

    # Set the view in the controller
    controller.set_view(view)

    # Start the application
    root.mainloop()

# Execute program
if __name__ == "__main__":

    # Run main function
    main()

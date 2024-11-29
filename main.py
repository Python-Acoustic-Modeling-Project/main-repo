# Include libraries
from tkinter import Tk
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
    root = Tk()
    root.title("SPIDAM Audio Analysis Tool")

    # Initialize the MVC components
    model = Model()
    controller = Controller(model)
    view = View(root, controller)

    # Start the application
    root.mainloop()

# Execute program
if __name__ == "__main__":

    # Run main function
    main()

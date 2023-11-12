import pygubu

# Load the UI file and create the builder
builder: pygubu.Builder = pygubu.Builder()
builder.add_from_file("src/ui/play_action.ui")

def build(network, users):
    pass
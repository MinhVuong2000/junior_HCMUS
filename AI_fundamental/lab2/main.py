
from Solver import Solver



def is_file_path_selected(file_path):
    return file_path is not None and file_path != ""


def get_file_contents(file_path):
    """Return a string containing the file contents of the file located at the
    specified file path """
    with open(file_path, encoding="utf-8") as f:
        file_contents = f.read()

    return file_contents


class Editor():

    def __init__(self, filename_input,filename_output):

        self.filename_input = filename_input
        self.filename_output = filename_output
        

    def run_query(self,rules_text,query_text, choice):
        """Interpret the entered rules and query and display the results in 
        filename_output """

        f = open(self.filename_output,'w')
        
        # Create a new solver so we can try to query for solutions.
        try:
            solver = Solver(rules_text)
        except Exception as e:
            self.handle_exception("Error processing prolog rules.", f, str(e))
            return

        # Attempt to find the solutions and handle any exceptions gracefully
        try:
            if (choice==1):
                solutions = solver.forward_chaining(query_text)
            else:
                print('back')
                solutions = solver.backward_chaining(query_text)
        except Exception as e:
            self.handle_exception("Error processing prolog query.", f, str(e))
            return

        # If our query returns a boolean, we simply display a 'Yes' or a 'No'
        # depending on its value
        if isinstance(solutions, bool):
            f.write("Yes." if solutions else "No.")

        # Our solver returned a map, so we display the variable name to value mappings
        elif isinstance(solutions, dict):
            f.write(
                "\n".join(
                    "{} = {}"
                    # If our solution is a list contining one item, we show that
                    # item, otherwise we display the entire list
                    .format(variable, value[0] if len(value) == 1 else value)
                    for variable, value in solutions.items()
                ),
            )
        else:

            # We know we have no matching solutions in this instance so we provide
            # relevant feedback
            f.write("No solutions found.")

        f.close()

    def handle_exception(self, error_message, output, exception=""):
        """Handle the exception by printing an error message as well as exception in
        our solution text editor / display """
        output.write( error_message + "\n")
        output.write(str(exception) + "\n")
        

    def input_from_file(self):
        rules_text = ""
        query_text = ""
        with open(self.filename_input,'r') as f:
            line = f.readline()
            print(line)
            if (line=="1\n"):
                choice=1
            else: choice=2
            for line in f:
                line = line.strip()
                if (line.startswith('?-')):
                    query_text+=line[2:]
                else: rules_text+=line
            f.close()
        return rules_text,query_text, choice

        




if __name__ == "__main__":

     editor = Editor("input.txt","output.txt")
     rules_text,query_text, choice = editor.input_from_file()
     editor.run_query(rules_text,query_text, choice)

    # # Don't allow users to re-size the editor
    # root.resizable(width=FALSE, height=FALSE)

    # root.mainloop()


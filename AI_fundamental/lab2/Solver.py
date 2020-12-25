from interpreter import Database, Variable, TRUE, Rule, Parser
from collections import defaultdict


class Solver(object):
    def __init__(self, rules_text):
        """Parse the rules text and initialize the database we plan to use to query
        our rules."""
        rules = Parser(rules_text).parse_rules()
        self.database = Database(rules)


    def forward_chaining(self,query_text):
        query = Parser(query_text).parse_query()
        query_rule = Rule(query, TRUE())
        
        rule = self.database.rules
        matching_query_terms1=[]
        for item in rule:
            if (not isinstance(item.tail,TRUE)):
                matching_query_terms1.append(item.head)
        for item in matching_query_terms1:
            add_KB = [it for it in self.database.query(item)]
            #print(add_KB)
            for term in add_KB:
                term = Rule(term, TRUE())
                #print(term)
                if term not in rule:
                    rule.append(term)

        self.database = Database(rule)

        query_variable_map = {}
        variables_in_query = False
        for argument in query.arguments:
            if isinstance(argument, Variable):
                variables_in_query = True
                query_variable_map[argument.name] = argument

        if not variables_in_query:
            if (query_rule in self.database.rules):
                return True
            else: return False
        else:
            solutions_map = defaultdict(list)
            same_query = [i for i in self.database.query(query)]
            for matching in same_query:
                    variable_match = query.match_variable_bindings(matching)

                    print(variable_match)
                    for variable_name, variable in query_variable_map.items():
                        if variable_match.get(variable) not in solutions_map:
                            solutions_map[variable_name].append(variable_match.get(variable))
            
            return solutions_map



    def backward_chaining(self, query_text):
        """Parse the query text and use our database rules to search for matching
        query solutions. """

        query = Parser(query_text).parse_query()
        query_variable_map = {}
        variables_in_query = False

        # Find any variables within the query and return a map containing the
        # variable name to actual Prolog variable mapping we can later use to query
        # our database.
        for argument in query.arguments:
            if isinstance(argument, Variable):
                variables_in_query = True
                query_variable_map[argument.name] = argument
                
        # Return a generator which iterates over the terms matching our query
        matching_query_terms = [item for item in self.database.query(query)]
        if matching_query_terms:
            if query_variable_map:

                # If our query has variables and we have matching query terms/items,
                # we iterate over the query items and our list of query variables and
                # construct a map containing the matching variable names and their
                # values
                solutions_map = defaultdict(list)
                for matching_query_term in matching_query_terms:
                    matching_variable_bindings = query.match_variable_bindings(
                        matching_query_term
                    )
                    print(matching_variable_bindings)
                    # Itarate over the query variables and bind them to the matched
                    # database bindings
                    for variable_name, variable in query_variable_map.items():
                        
                        solutions_map[variable_name].append(
                            matching_variable_bindings.get(variable)
                        )

                return solutions_map

            else:
                # If we have matching query items / terms but no variables in our
                # query, we simply return true to indicate that our query did match
                # our goal. Otherwise, we return None
                
                return True if not variables_in_query else None
        else:
            # If we have no variables in our query, it means our goal had no matches,
            # so we return False. Otherwise simply return None to show no variable
            # bindings were found.
            
            return False if not variables_in_query else None



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
        output.write(error_message + "\n")
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

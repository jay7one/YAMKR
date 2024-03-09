import os
import re

class EnumState:
    def __init__(self):
        self.inside_enum = False

def camel_to_snake(name):
    """
    Convert camelCase to snake_case
    """
    s1 = re.sub('(.)([A-Z][a-z]+)', r'\1_\2', name)
    return re.sub('([a-z0-9])([A-Z])', r'\1_\2', s1).lower()

def find_camelcase_variables_in_files(extensions):
    camelcase_variables = set()
    declared_classes_enums = set()
    enum_state = EnumState()

    # Regular expression to match camel case variables without digits and not starting with 'tk'
    camelcase_pattern = re.compile(r'\b(?![\d_])(?!tk)[A-Z][a-zA-Z0-9]*\b')

    root_dir = os.getcwd()

    for dirpath, _, filenames in os.walk(root_dir):
        for filename in filenames:
            if filename.endswith(extensions):
                filepath = os.path.join(dirpath, filename)
                with open(filepath, 'r', encoding='utf-8') as file:
                    for line in file:
                        # Remove comments
                        line = re.sub(r'#.*', '', line)

                        # Update enum state
                        if 'enum' in line:
                            enum_state.inside_enum = True
                        elif '}' in line and enum_state.inside_enum:
                            enum_state.inside_enum = False

                        # If not inside enum, find camel case variables
                        if not enum_state.inside_enum:
                            # Remove content within quotes
                            line = re.sub(r'".*?"', '', line)
                            line = re.sub(r"'.*?'", '', line)
                            matches = camelcase_pattern.findall(line)
                            for match in matches:
                                # If it's a class or enum name, exclude it
                                if match in declared_classes_enums:
                                    continue
                                # Exclude words prefixed with 'tk' and all uppercase words
                                if not match.startswith('tk') and not match.isupper():
                                    camelcase_variables.add(match)

    return camelcase_variables

def write_variables_to_file(variables, output_file):
    with open(output_file, 'w', encoding='utf-8') as file:
        for variable in variables:
            snake_case = camel_to_snake(variable)
            file.write(f"{variable}\t{snake_case}\n")

if __name__ == "__main__":
    extensions = ('.tcl', '.py')
    output_file = "camelcase_variables.txt"

    camelcase_variables = find_camelcase_variables_in_files(extensions)
    write_variables_to_file(camelcase_variables, output_file)

    print(f"Found {len(camelcase_variables)} unique camelcase variables containing lowercase letters. Stored in {output_file}")

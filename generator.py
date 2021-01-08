"""Build static HTML site from directory of HTML templates and plain files."""
import json
import sys
import shutil
import os
import jinja2


def generate_misc():
    """Templated static website generator."""
    # Reads data for index and about page out of misc_config.json
    with open('configs/misc_config.json') as json_file:
        json_data = json.load(json_file)
        print("loaded misc_config.json")

    out_path = "html/"

    # Creates output directory if necessary
    try:
        if not os.path.exists(out_path):
            os.makedirs(out_path)
            print("created " + out_path + " directory")
    except OSError:
        print("Error managing directories")
        sys.exit(1)

    try:
        # Fetch template with name specified
        template_env = jinja2.Environment(
            loader=jinja2.FileSystemLoader("templates"),
            autoescape=jinja2.select_autoescape(['html', 'xml']),
        )
        print("loaded jinja env")
    except jinja2.TemplateError as err:
        print("Template Error setting up loader")
        print(err)
        sys.exit(1)

    # do templating and write file out
    for page in json_data:
        try:
            template = template_env.get_template(page['template'])
            output = template.render(page['context'])
            print("templated", page['title'] + ".html")
        except jinja2.TemplateError:
            print("Template Error getting and rendering")
            sys.exit(1)

        try:
            write_path = os.path.join(out_path, page['title'] + ".html")
            outfile = open(write_path, "w")
            outfile.write(output)
            outfile.close()
            print("wrote", page['title'] + ".html")
        except IOError:
            print("Error writing file out")
            sys.exit(1)

def main():
    """Top level command line interface."""
    generate_misc()


if __name__ == "__main__":
    main()

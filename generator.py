"""Build static HTML site from directory of HTML templates and plain files."""
import json
import sys
import shutil
import os
import jinja2


def generate(group):
    """Templated static website generator."""
    # Reads data for index and about page out of misc_config.json
    with open('configs/' + group + '_config.json') as json_file:
        json_data = json.load(json_file)
        print("loaded " + group + "_config.json")

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
            out_path = os.path.join("html/", page['out_path'])
            if not os.path.exists(out_path):
                os.makedirs(out_path)
                print("created " + out_path + " directory")
            file_path = os.path.join(out_path, page['title'] + ".html")
            outfile = open(file_path, "w")
            outfile.write(output)
            outfile.close()
            print("wrote", file_path)

        except IOError or OSError:
            print("Error writing file out")
            sys.exit(1)
    print()
    print("DONE WRITING " + group)
    print()

def main():
    """Top level command line interface."""
    group = input("Input group name to generate: (misc, survey, galaxy, field) ")
    if group == 'all':
        generate("misc")
        generate("survey")
        generate("galaxy")
        generate("field")
        print('ALL GENERATING COMPLETE')
        print()
    else:
        generate(group)


if __name__ == "__main__":
    main()

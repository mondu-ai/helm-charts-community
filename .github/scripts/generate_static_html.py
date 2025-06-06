#!/usr/bin/env python3

import yaml
import os

# Define file paths
yaml_file_path = 'public/index.yaml'
template_html_path = 'index.html'  # Assuming this script is run from the repository root
output_html_path = 'public/index.html'
placeholder_comment = '<!-- Chart list will be populated here by the build script -->'

def generate_chart_html(data):
    """Generates HTML list for charts from parsed YAML data."""
    if not data or 'entries' not in data:
        print("No 'entries' found in YAML data or data is empty.")
        return "<p>No chart entries found in index.yaml.</p>"

    entries = data['entries']
    if not entries:
        return "<p>No charts listed in 'entries'.</p>"

    html_parts = ['<ul class="chart-list">']
    for chart_name, versions in sorted(entries.items()):
        html_parts.append(f'  <li><h2>{chart_name}</h2>')
        if versions:
            html_parts.append('    <ul>')
            for version_details in sorted(versions, key=lambda x: x.get('version'), reverse=True):
                version = version_details.get('version', 'N/A')
                description = version_details.get('description', '')
                appVersion = version_details.get('appVersion', '')

                display_text = f"Version: {version}"
                if appVersion:
                    display_text += f" (App: {appVersion})"
                if description:
                    display_text += f" - <em>{description}</em>"
                html_parts.append(f'      <li>{display_text}</li>')
            html_parts.append('    </ul>')
        else:
            html_parts.append('    <p>No versions listed for this chart.</p>')
        html_parts.append('  </li>')
    html_parts.append('</ul>')
    return '\n'.join(html_parts)

def main():
    print(f"Starting static HTML generation: {template_html_path} + {yaml_file_path} -> {output_html_path}")

    # 1. Read index.yaml
    try:
        with open(yaml_file_path, 'r', encoding='utf-8') as f:
            yaml_data = yaml.safe_load(f)
    except FileNotFoundError:
        print(f"Error: YAML file not found at {yaml_file_path}")
        # Create a minimal public/index.html indicating the issue
        try:
            with open(template_html_path, 'r', encoding='utf-8') as tpl_f:
                template_html = tpl_f.read()
            error_message_html = "<p><strong>Error: Chart index (index.yaml) not found. Cannot display charts.</strong></p>"
            output_html = template_html.replace(placeholder_comment, error_message_html)
            os.makedirs(os.path.dirname(output_html_path), exist_ok=True)
            with open(output_html_path, 'w', encoding='utf-8') as out_f:
                out_f.write(output_html)
            print(f"Wrote minimal HTML to {output_html_path} indicating missing YAML.")
        except Exception as e_tpl:
            print(f"Additionally, could not process template HTML: {e_tpl}")
        return # Exit if YAML is missing
    except yaml.YAMLError as e:
        print(f"Error parsing YAML file: {e}")
        # Similar error handling for YAML parse error
        try:
            with open(template_html_path, 'r', encoding='utf-8') as tpl_f:
                template_html = tpl_f.read()
            error_message_html = f"<p><strong>Error: Could not parse chart index (index.yaml). Details: {e}</strong></p>"
            output_html = template_html.replace(placeholder_comment, error_message_html)
            os.makedirs(os.path.dirname(output_html_path), exist_ok=True)
            with open(output_html_path, 'w', encoding='utf-8') as out_f:
                out_f.write(output_html)
            print(f"Wrote minimal HTML to {output_html_path} indicating YAML parsing error.")
        except Exception as e_tpl:
            print(f"Additionally, could not process template HTML: {e_tpl}")
        return # Exit on YAML parse error

    # 2. Generate HTML for charts
    print("Generating HTML content for charts...")
    charts_html = generate_chart_html(yaml_data)

    # 3. Read the template index.html
    try:
        with open(template_html_path, 'r', encoding='utf-8') as f:
            template_html = f.read()
    except FileNotFoundError:
        print(f"Error: Template HTML file not found at {template_html_path}")
        # If template is missing, we can't really proceed to create a useful public/index.html
        # However, the script's primary job is to process index.yaml, so this is a critical error.
        return

    # 4. Inject generated HTML into the template
    if placeholder_comment in template_html:
        output_html = template_html.replace(placeholder_comment, charts_html)
        print(f"Successfully injected chart HTML into template using placeholder.")
    else:
        # Fallback or error if placeholder is missing.
        # For now, let's try to append to a known div if it exists, or just log an error.
        container_div_end_tag = '</div>' # from <div id="chart-list-container">
        container_div_full_tag = '<div id="chart-list-container">'

        # Try to find the specific container
        container_start_index = template_html.find(container_div_full_tag)
        if container_start_index != -1:
            # Find where this div ends
            end_tag_index = template_html.find(container_div_end_tag, container_start_index + len(container_div_full_tag))
            if end_tag_index != -1:
                output_html = template_html[:end_tag_index] + charts_html + template_html[end_tag_index:]
                print("Warning: Placeholder comment not found. Appended chart HTML inside the 'chart-list-container' div.")
            else: # No end tag for the container div
                output_html = template_html + charts_html # Append at the end as a last resort
                print("Error: Placeholder comment not found and could not properly locate end of 'chart-list-container' div. Appended to end of file.")
        else: # Container div itself not found
            output_html = template_html + charts_html # Append at the end as a last resort
            print(f"Error: Placeholder comment '{placeholder_comment}' not found in template. Appended chart HTML to the end of the template as a fallback.")


    # 5. Write the output HTML
    try:
        os.makedirs(os.path.dirname(output_html_path), exist_ok=True) # Ensure 'public/' directory exists
        with open(output_html_path, 'w', encoding='utf-8') as f:
            f.write(output_html)
        print(f"Successfully generated and wrote static HTML to {output_html_path}")
    except IOError as e:
        print(f"Error writing output HTML file: {e}")

if __name__ == '__main__':
    main()

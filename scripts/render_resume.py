import argparse
import json
import os
import sys
import subprocess
import urllib.request
from jinja2 import Environment, FileSystemLoader, select_autoescape
from markupsafe import Markup
import re
try:
    from weasyprint import HTML
except ImportError:
    HTML = None

def load_json(path_or_url):
    """Load JSON from a local file or URL."""
    if path_or_url.startswith('http://') or path_or_url.startswith('https://'):
        with urllib.request.urlopen(path_or_url) as response:
            return json.loads(response.read().decode('utf-8'))
    else:
        with open(path_or_url, 'r') as f:
            return json.load(f)

def render_resume(json_path, output_path, template_dir='templates', template_name='resume.html', extra_context=None):
    """Render the resume HTML."""
    # Load data
    try:
        data = load_json(json_path)
        if extra_context:
            data.update(extra_context)
    except Exception as e:
        print(f"Error loading JSON: {e}", file=sys.stderr)
        sys.exit(1)

    # Setup Jinja2 environment
    env = Environment(
        loader=FileSystemLoader(template_dir),
        autoescape=select_autoescape(['html', 'xml'])
    )

    def format_date(value):
        if not value:
            return value
        try:
            from datetime import datetime
            date_obj = datetime.strptime(value, '%Y-%m-%d')
            return date_obj.strftime('%B %Y')
        except ValueError:
            return value

    env.filters['format_date'] = format_date

    def markdown_bold(value):
        """Convert **text** to <b>text</b>."""
        if isinstance(value, str):
            # Replace **text** with <b>text</b>
            bolded = re.sub(r'\*\*(.*?)\*\*', r'<b>\1</b>', value)
            return Markup(bolded)
        return value

    env.filters['markdown_bold'] = markdown_bold

    try:
        template = env.get_template(template_name)
    except Exception as e:
        print(f"Error loading template: {e}", file=sys.stderr)
        sys.exit(1)

    # Render
    try:
        html_output = template.render(**data)
    except Exception as e:
        print(f"Error rendering template: {e}", file=sys.stderr)
        sys.exit(1)

    # Write output
    if output_path:
        with open(output_path, 'w') as f:
            f.write(html_output)
        print(f"Resume rendered to {output_path}")
    else:
        print(html_output)

    return html_output

def main():
    parser = argparse.ArgumentParser(description='Render resume HTML from JSON.')
    parser.add_argument('json_file', help='Path or URL to the resume JSON file')
    parser.add_argument('-o', '--output', help='Output HTML file path', default='resume.html')
    parser.add_argument('--template-dir', help='Directory containing templates', default='templates')
    parser.add_argument('--pdf', help='Output PDF file path')
    parser.add_argument('--rtf', help='Output RTF file path')

    args = parser.parse_args()

    # Regular render for HTML and PDF
    html_content = render_resume(args.json_file, args.output, args.template_dir)

    if args.pdf:
        if HTML:
            print(f"Generating PDF to {args.pdf}...")
            # Use base_url="." to resolve relative paths in CSS/images if any
            HTML(string=html_content, base_url=".").write_pdf(args.pdf)
            print(f"PDF generated at {args.pdf}")
        else:
            print("Error: weasyprint module not found. Please install it to generate PDF.", file=sys.stderr)
            sys.exit(1)

    if args.rtf:
        print(f"Generating RTF to {args.rtf}...")
        try:
            # Generate temporary HTML specifically for RTF conversion with 'rtf' format context
            # This allows the template to render differently (e.g. extra spacing) for RTF
            rtf_html_path = args.output + '.rtf_temp.html'
            render_resume(args.json_file, rtf_html_path, args.template_dir, extra_context={'format': 'rtf'})
            
            subprocess.run(
                ['pandoc', rtf_html_path, '-o', args.rtf, '-s', '-V', 'title='],
                check=True,
                capture_output=True
            )
            # Cleanup temp file
            if os.path.exists(rtf_html_path):
                os.remove(rtf_html_path)
                
            print(f"RTF generated at {args.rtf}")
        except subprocess.CalledProcessError as e:
            print(f"Error generating RTF: {e.stderr.decode()}", file=sys.stderr)
            sys.exit(1)
        except FileNotFoundError:
            print("Error: pandoc not found. Please install pandoc to generate RTF.", file=sys.stderr)
            sys.exit(1)

if __name__ == '__main__':
    main()

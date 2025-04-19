# import argparse
# import os
# import sys
# from pathlib import Path
# import markdown # For Markdown conversion
# import re # For natural sorting
# from jinja2 import Environment, FileSystemLoader, select_autoescape # For templating

# # --- Constants for Formatting ---
# SEPARATOR_LINE = "-" * 70
# HEADER_LINE = "=" * 70

# # --- Natural Sort Helper ---
# def natural_sort_key(s):
#     """Key function for natural sorting."""
#     return [int(text) if text.isdigit() else text.lower()
#             for text in re.split('([0-9]+)', str(s))]

# # --- Conversion and Index Generation Function ---
# def convert_md_to_html(input_folder_path: Path, output_folder_path: Path, template_env: Environment):
#     """
#     Converts Markdown files to HTML using Jinja2 templates and creates an index.
#     Includes enhanced console logging.

#     Args:
#         input_folder_path (Path): Path to the folder containing .md files.
#         output_folder_path (Path): Path to the folder where HTML files will be saved.
#         template_env (Environment): Jinja2 environment pre-configured with template path.
#     """
#     # Note: Input/Output paths already printed in main()
#     print(f"Processing target folder: '{output_folder_path.name}'")

#     # --- Create Output Directory (Log only if action taken or error) ---
#     output_created = False
#     if not output_folder_path.exists():
#         try:
#             output_folder_path.mkdir(parents=True, exist_ok=True)
#             print(f"  - Created output directory: {output_folder_path}")
#             output_created = True
#         except OSError as e:
#             print(f"  ❌ Error creating output directory {output_folder_path}: {e}", file=sys.stderr)
#             # Decide if we should exit or try to continue
#             # For now, let's exit as conversion will likely fail.
#             sys.exit(1)
#     # else: # Optional: Log if directory already exists
#     #     print(f"  - Output directory exists: {output_folder_path}")


#     # Find all Markdown files
#     md_files = list(input_folder_path.glob('*.md'))

#     if not md_files:
#         print("  - No Markdown (.md) files found. Nothing to convert.")
#         return # Nothing to do

#     print(f"  - Found {len(md_files)} Markdown file(s).")

#     # --- Load Jinja2 Templates ---
#     try:
#         chapter_template = template_env.get_template("chapter.html")
#         index_template = template_env.get_template("index.html")
#         print("  - Loaded Jinja2 templates (chapter.html, index.html).")
#     except Exception as e:
#         print(f"  ❌ Error loading Jinja2 templates: {e}", file=sys.stderr)
#         print("     Ensure templates exist in the specified templates directory.", file=sys.stderr)
#         sys.exit(1)

#     # --- Process each Markdown file ---
#     print(f"  - Converting chapters...")
#     generated_files_info = []
#     converted_count = 0
#     errors_count = 0

#     # Optional: Add a simple progress indicator for many files
#     # print("    Progress: ", end='', flush=True)

#     for md_file_path in md_files:
#         try:
#             md_content = md_file_path.read_text(encoding='utf-8')
#             html_fragment = markdown.markdown(
#                 md_content, extensions=['fenced_code', 'tables', 'footnotes', 'md_in_html', 'attr_list', 'toc']
#             )
#             file_title = md_file_path.stem.replace('-', ' ').replace('_', ' ').title()
#             html_filename = md_file_path.stem + ".html"
#             html_file_path = output_folder_path / html_filename

#             full_html = chapter_template.render(title=file_title, content=html_fragment)
#             html_file_path.write_text(full_html, encoding='utf-8')
#             converted_count += 1
#             generated_files_info.append({'filename': html_filename, 'title': file_title})
#             # Optional: Progress indicator
#             # print(".", end='', flush=True)

#         except Exception as e:
#             print(f"\n    ❌ Error converting file '{md_file_path.name}': {e}", file=sys.stderr) # Newline for visibility
#             errors_count += 1

#     # print() # Newline after progress dots if using them

#     # --- Chapter Conversion Summary ---
#     print(f"    > Converted: {converted_count}")
#     if errors_count > 0:
#         print(f"    > Errors:    {errors_count} ❌")
#     else:
#          print(f"    > Errors:    {errors_count} ✔️")


#     # --- Generate index.html ---
#     if generated_files_info:
#         print(f"  - Generating index page...")
#         generated_files_info.sort(key=lambda x: natural_sort_key(x['filename']))

#         # Determine index title (just use the folder name)
#         index_title = output_folder_path.name.replace('-', ' ').replace('_', ' ').title() # Removed " - Contents"

#         # --- Render index HTML using Jinja2 template ---
#         try:
#             index_html_content = index_template.render(
#                 title=index_title,       # Pass the simplified title
#                 chapters=generated_files_info
#             )
#             index_file_path = output_folder_path / "index.html"
#             index_file_path.write_text(index_html_content, encoding='utf-8')
#             print(f"    > Index file created: {index_file_path.name} ✔️") # Just show filename
#         except Exception as e:
#             print(f"    ❌ Error creating index.html: {e}", file=sys.stderr)
#             # Decide if this error should increment the main error count or be separate

#     elif converted_count > 0:
#          print("  - Skipping index page generation (no chapters successfully converted).")
#     # else: (No MD files found case already handled)


# # --- Path Derivation Function (No changes needed) ---
# def derive_output_path(input_path: Path, output_base_dir_name: str = "website") -> Path:
#     """Derives the output path based on the input path structure."""
#     try:
#         parent_dir = input_path.parent
#         if not parent_dir: raise ValueError("Input path structure invalid: cannot get parent directory.")
#         folder_name = parent_dir.name
#         grandparent_dir = parent_dir.parent
#         if not grandparent_dir: raise ValueError("Input path structure invalid: cannot get grandparent directory.")
#         great_grandparent_dir = grandparent_dir.parent
#         if not great_grandparent_dir: raise ValueError("Input path structure invalid: cannot get great-grandparent directory.")
#         output_base_path = great_grandparent_dir / output_base_dir_name
#         final_output_path = output_base_path / folder_name
#         return final_output_path
#     except AttributeError:
#          raise ValueError(f"Could not determine structure from input path: {input_path}. Path might be too shallow or structure unexpected.")
#     except Exception as e:
#         raise ValueError(f"Error deriving output path from {input_path}: {e}")


# # --- Main Execution Block ---
# def main():
#     """
#     Parses arguments, sets up Jinja2 environment, and initiates conversion.
#     Includes enhanced console logging.
#     """
#     parser = argparse.ArgumentParser(
#         description="Convert Markdown files using Jinja2 templates, link CSS, and create an index.",
#         formatter_class=argparse.RawDescriptionHelpFormatter # Keep description formatting
#     )
#     parser.add_argument("input_folder", help="Path to folder containing Markdown files (e.g., 'markdown/Topic/output').")
#     parser.add_argument("--output-base", default="website", help="Base directory name for output (default: 'website').")
#     parser.add_argument("--templates-dir", default="website/assets/templates", help="Path to Jinja2 templates directory.")

#     args = parser.parse_args()

#     # --- Start Banner ---
#     print(HEADER_LINE)
#     print("      Markdown to HTML Conversion Script")
#     print(HEADER_LINE)

#     # --- Setup Jinja2 Environment (Log less unless error) ---
#     template_folder_path = Path(args.templates_dir)
#     if not template_folder_path.is_dir():
#         print(f"❌ Error: Templates directory not found: {template_folder_path.resolve()}", file=sys.stderr)
#         sys.exit(1)
#     try:
#         env = Environment(
#             loader=FileSystemLoader(template_folder_path),
#             autoescape=select_autoescape(['html', 'xml'])
#         )
#     except Exception as e:
#          print(f"❌ Error initializing Jinja2 environment: {e}", file=sys.stderr)
#          sys.exit(1)

#     # --- Resolve Input/Output Paths (Log clearly) ---
#     try:
#         input_path = Path(args.input_folder).resolve(strict=True)
#     except FileNotFoundError:
#          print(f"❌ Error: Input directory not found: {args.input_folder}", file=sys.stderr)
#          sys.exit(1)
#     except Exception as e:
#         print(f"❌ Error resolving input path '{args.input_folder}': {e}", file=sys.stderr)
#         sys.exit(1)

#     try:
#         output_path = derive_output_path(input_path, args.output_base)
#     except ValueError as e:
#         print(f"❌ Error deriving output path: {e}", file=sys.stderr)
#         print("   Please ensure input path follows structure '.../base_dir/Folder_Name/input_subdir'", file=sys.stderr)
#         sys.exit(1)

#     # --- Print Configuration ---
#     print(f"Input Directory : {input_path}")
#     print(f"Output Directory: {output_path}")
#     print(f"Templates Path  : {template_folder_path.resolve()}") # Show resolved path
#     print(SEPARATOR_LINE)


#     # --- Run Conversion ---
#     convert_md_to_html(input_path, output_path, env)


#     # --- End Banner ---
#     print(SEPARATOR_LINE)
#     print("Processing complete.")
#     print(HEADER_LINE)


# # --- Script Entry Point ---
# if __name__ == "__main__":
#     # Reminder: pip install Jinja2 markdown
#     main()


import argparse
import os
import sys
from pathlib import Path
import markdown # For Markdown conversion
import re # For natural sorting
from jinja2 import Environment, FileSystemLoader, select_autoescape # For templating

# --- Constants for Formatting ---
SEPARATOR_LINE = "-" * 70
HEADER_LINE = "=" * 70
SUB_HEADER_LINE = "~" * 70

# --- Natural Sort Helper ---
def natural_sort_key(s):
    """Key function for natural sorting."""
    return [int(text) if text.isdigit() else text.lower()
            for text in re.split('([0-9]+)', str(s))]

# --- Conversion and Index Generation Function ---
def convert_md_to_html(input_folder_path: Path, output_folder_path: Path, template_env: Environment):
    """
    Converts Markdown files to HTML using Jinja2 templates and creates an index.
    Includes enhanced console logging.

    Args:
        input_folder_path (Path): Path to the folder containing .md files (e.g., 'markdown/Book-Title/output').
        output_folder_path (Path): Path to the folder where HTML files will be saved (e.g., 'website/Book-Title').
        template_env (Environment): Jinja2 environment pre-configured with template path.
    """
    # Note: Overall Input/Output base paths printed in main()
    print(f"Processing Source : '{input_folder_path}'")
    print(f"Target Destination: '{output_folder_path}'")

    # --- Create Output Directory (Log only if action taken or error) ---
    output_created = False
    if not output_folder_path.exists():
        try:
            output_folder_path.mkdir(parents=True, exist_ok=True)
            print(f"  - Created output directory: {output_folder_path}")
            output_created = True
        except OSError as e:
            print(f"  ❌ Error creating output directory {output_folder_path}: {e}", file=sys.stderr)
            # For this book, we cannot continue. Log and return to process next book.
            return False # Indicate failure for this book
    # else: # Optional: Log if directory already exists
    #     print(f"  - Output directory exists: {output_folder_path}")

    # Find all Markdown files in the specific input subfolder
    md_files = list(input_folder_path.glob('*.md'))

    if not md_files:
        print("  - No Markdown (.md) files found in this source folder. Skipping conversion.")
        # Still return True because the *process* didn't fail, there was just nothing to do.
        # An index might still be generated if other books had content.
        return True

    print(f"  - Found {len(md_files)} Markdown file(s).")

    # --- Load Jinja2 Templates (Already loaded in main, passed via env) ---
    try:
        chapter_template = template_env.get_template("chapter.html")
        index_template = template_env.get_template("index.html")
        # print("  - Using loaded Jinja2 templates (chapter.html, index.html).") # Less verbose
    except Exception as e:
        print(f"  ❌ Internal Error: Could not get templates from environment: {e}", file=sys.stderr)
        # This is a more fundamental error, likely stop processing
        return False # Indicate failure

    # --- Process each Markdown file ---
    print(f"  - Converting chapters...")
    generated_files_info = []
    converted_count = 0
    errors_count = 0

    # Optional: Add a simple progress indicator for many files
    # print("    Progress: ", end='', flush=True)

    for md_file_path in sorted(md_files, key=natural_sort_key): # Sort files naturally
        try:
            md_content = md_file_path.read_text(encoding='utf-8')
            # Generate HTML fragment with extensions
            html_fragment = markdown.markdown(
                md_content, extensions=['fenced_code', 'tables', 'footnotes', 'md_in_html', 'attr_list', 'toc']
            )
            # Determine title and filename
            file_title = md_file_path.stem.replace('-', ' ').replace('_', ' ').title()
            html_filename = md_file_path.stem + ".html"
            html_file_path = output_folder_path / html_filename

            # Render full HTML using the chapter template
            full_html = chapter_template.render(
                title=file_title,
                content=html_fragment,
                # Add relative path to CSS if needed by template
                # css_path=os.path.relpath(Path("website/assets/css/style.css"), output_folder_path) # Example
            )
            html_file_path.write_text(full_html, encoding='utf-8')
            converted_count += 1
            generated_files_info.append({'filename': html_filename, 'title': file_title})
            # Optional: Progress indicator
            # print(".", end='', flush=True)

        except Exception as e:
            print(f"\n    ❌ Error converting file '{md_file_path.name}': {e}", file=sys.stderr) # Newline for visibility
            errors_count += 1

    # print() # Newline after progress dots if using them

    # --- Chapter Conversion Summary ---
    print(f"    > Converted: {converted_count}")
    if errors_count > 0:
        print(f"    > Errors:    {errors_count} ❌")
    else:
         print(f"    > Errors:    {errors_count} ✔️")


    # --- Generate index.html for this book ---
    if generated_files_info:
        print(f"  - Generating index page for this book...")
        # Files are already sorted by filename during processing loop and natural sort key applied
        # generated_files_info.sort(key=lambda x: natural_sort_key(x['filename'])) # Should be sorted already

        # Determine index title (use the book's folder name)
        index_title = output_folder_path.name.replace('-', ' ').replace('_', ' ').title()

        # --- Render index HTML using Jinja2 template ---
        try:
            index_html_content = index_template.render(
                title=index_title,       # Pass the book title
                chapters=generated_files_info
                # Add relative path to CSS if needed by template
                # css_path=os.path.relpath(Path("website/assets/css/style.css"), output_folder_path) # Example
            )
            index_file_path = output_folder_path / "index.html"
            index_file_path.write_text(index_html_content, encoding='utf-8')
            print(f"    > Index file created: {index_file_path.name} ✔️") # Just show filename
        except Exception as e:
            print(f"    ❌ Error creating index.html for this book: {e}", file=sys.stderr)
            errors_count += 1 # Count index generation error as part of book processing errors

    elif converted_count > 0 and errors_count == 0:
         # This case shouldn't happen if generated_files_info is populated correctly
         print("  - Warning: Chapters converted but no info available for index generation.")
    elif converted_count == 0 and errors_count > 0:
         print("  - Skipping index page generation due to conversion errors.")
    # else: (No MD files found case already handled)

    return errors_count == 0 # Return True if successful (no errors), False otherwise


# --- Path Derivation Function (No changes needed, assumes input is the subfolder like 'markdown/Book/output') ---
def derive_output_path(input_path: Path, output_base_dir_name: str = "website") -> Path:
    """
    Derives the output path based on the input path structure.
    Expects input_path like '.../parent_dir/Book-Folder-Name/input_subdir'.
    Returns '.../parent_dir.parent / output_base_dir_name / Book-Folder-Name'.
    """
    try:
        # input_path is like ".../markdown/Book-Name/output"
        book_folder_path = input_path.parent # ".../markdown/Book-Name"
        if not book_folder_path: raise ValueError("Input path structure invalid: cannot get parent directory (book folder).")

        book_folder_name = book_folder_path.name # "Book-Name"

        markdown_base_path = book_folder_path.parent # ".../markdown"
        if not markdown_base_path: raise ValueError("Input path structure invalid: cannot get grandparent directory (markdown base).")

        project_root_path = markdown_base_path.parent # "..." (Root containing markdown, website, etc.)
        if not project_root_path: raise ValueError("Input path structure invalid: cannot get great-grandparent directory (project root).")

        output_base_path = project_root_path / output_base_dir_name # ".../website"
        final_output_path = output_base_path / book_folder_name # ".../website/Book-Name"
        return final_output_path
    except AttributeError as e:
         raise ValueError(f"Could not determine structure from input path: {input_path}. Path might be too shallow or structure unexpected. {e}")
    except Exception as e:
        raise ValueError(f"Error deriving output path from {input_path}: {e}")


# --- Main Execution Block ---
def main():
    """
    Finds book folders within 'markdown', sets up Jinja2, and initiates conversion for each book.
    """
    parser = argparse.ArgumentParser(
        description="Convert Markdown files from subfolders within 'markdown' to HTML in corresponding 'website' subfolders.",
        formatter_class=argparse.RawDescriptionHelpFormatter # Keep description formatting
    )
    # Removed input_folder argument
    parser.add_argument("--markdown-dir", default="markdown", help="Base directory containing book folders (default: 'markdown').")
    parser.add_argument("--input-subdir", default="output", help="Subdirectory within each book folder containing .md files (default: 'output').")
    parser.add_argument("--output-base", default="website", help="Base directory name for output website (default: 'website').")
    parser.add_argument("--templates-dir", default="website/assets/templates", help="Path to Jinja2 templates directory.")

    args = parser.parse_args()

    # --- Start Banner ---
    print(HEADER_LINE)
    print("      Bulk Markdown to HTML Conversion Script")
    print(HEADER_LINE)

    # --- Define Base Paths ---
    markdown_base_path = Path(args.markdown_dir).resolve()
    templates_path = Path(args.templates_dir).resolve()
    output_base_name = args.output_base
    input_subdir_name = args.input_subdir

    # --- Validate Base Paths ---
    if not markdown_base_path.is_dir():
        print(f"❌ Error: Base Markdown directory not found: {markdown_base_path}", file=sys.stderr)
        sys.exit(1)
    if not templates_path.is_dir():
        print(f"❌ Error: Templates directory not found: {templates_path}", file=sys.stderr)
        sys.exit(1)

    # --- Setup Jinja2 Environment (Once) ---
    try:
        env = Environment(
            loader=FileSystemLoader(templates_path),
            autoescape=select_autoescape(['html', 'xml'])
        )
        print(f"Jinja2 Environment loaded from: {templates_path}")
    except Exception as e:
         print(f"❌ Error initializing Jinja2 environment: {e}", file=sys.stderr)
         sys.exit(1)

    # --- Print Configuration ---
    print(f"Markdown Source Base: {markdown_base_path}")
    print(f"Input Subdirectory  : '{input_subdir_name}' (within each book folder)")
    print(f"Website Output Base : '{output_base_name}' (relative to project root)")
    print(SEPARATOR_LINE)

    # --- Find and Process Book Folders ---
    books_processed = 0
    books_failed = 0

    # Sort book folders alphabetically for consistent processing order
    book_folders = sorted([item for item in markdown_base_path.iterdir() if item.is_dir()], key=lambda p: p.name)

    if not book_folders:
        print(f"No book subdirectories found in '{markdown_base_path}'. Nothing to process.")
        print(HEADER_LINE)
        sys.exit(0)

    print(f"Found {len(book_folders)} potential book folder(s). Processing...")
    print(SEPARATOR_LINE)

    for book_folder_path in book_folders:
        book_name = book_folder_path.name
        print(f"Processing Book: '{book_name}'")
        print(SUB_HEADER_LINE)

        input_path = book_folder_path / input_subdir_name

        # Check if the specific input subdirectory exists
        if not input_path.is_dir():
            print(f"  - Skipping: Input subdirectory '{input_subdir_name}' not found in '{book_folder_path}'.")
            print(SUB_HEADER_LINE)
            print() # Add space before next book
            continue # Move to the next book folder

        # Derive the output path for this specific book
        try:
            output_path = derive_output_path(input_path, output_base_name)
        except ValueError as e:
            print(f"  ❌ Error deriving output path for '{book_name}': {e}", file=sys.stderr)
            print("     Skipping this book.")
            print(SUB_HEADER_LINE)
            print() # Add space before next book
            books_failed += 1
            continue # Move to the next book folder

        # --- Run Conversion for this book ---
        success = convert_md_to_html(input_path, output_path, env)

        if success:
            books_processed += 1
            print(f"  > Book '{book_name}' processed successfully.")
        else:
            books_failed += 1
            print(f"  ❌ Book '{book_name}' processing encountered errors.")

        print(SUB_HEADER_LINE)
        print() # Add space before next book


    # --- End Summary ---
    print(HEADER_LINE)
    print("Processing Summary:")
    print(f"  - Books Attempted : {len(book_folders)}")
    print(f"  - Books Processed : {books_processed}")
    print(f"  - Books Failed    : {books_failed}")
    if books_failed > 0:
        print("  (Check logs above for specific errors)")
    print("Processing complete.")
    print(HEADER_LINE)


# --- Script Entry Point ---
if __name__ == "__main__":
    # Reminder: pip install Jinja2 markdown Markdown-TOC # (Ensure 'Markdown-TOC' or similar if needed by 'toc')
    main()
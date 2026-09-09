import os
import shutil

import frappe


SYSTEM_FOLDERS = ("Home", "Home/Attachments")


def get_folder_path(file_doc):
    """Return grouping key: attached_to_name if present, else custom folder name, else '' (root)."""
    if file_doc.attached_to_name:
        return file_doc.attached_to_name

    folder = file_doc.folder
    if folder in SYSTEM_FOLDERS or not folder:
        return ""

    return folder.split("/")[-1]


def sanitize(name):
    return "".join(c for c in name if c not in '\\/:*?"<>|').strip()


def get_unique_path(target_path):
    """If target_path already exists, append (1), (2), ... before the extension."""
    if not os.path.exists(target_path):
        return target_path

    folder, file_name = os.path.split(target_path)
    name, ext = os.path.splitext(file_name)

    counter = 1
    while True:
        new_path = os.path.join(folder, f"{name} ({counter}){ext}")
        if not os.path.exists(new_path):
            return new_path
        counter += 1


@frappe.whitelist()
def zip_files(files):
    if isinstance(files, str):
        files = frappe.parse_json(files)

    temp_dir = frappe.get_site_path("private", "files", f"zip_tmp_{frappe.generate_hash(length=8)}")
    os.makedirs(temp_dir, exist_ok=True)

    try:
        for _file in files:
            if isinstance(_file, str):
                _file = frappe.get_doc("File", _file)

            if _file.doctype != "File" or _file.is_folder:
                continue

            if not _file.has_permission("read"):
                continue

            folder_name = sanitize(get_folder_path(_file))
            target_dir = os.path.join(temp_dir, folder_name) if folder_name else temp_dir
            os.makedirs(target_dir, exist_ok=True)

            target_path = os.path.join(target_dir, _file.file_name)
            target_path = get_unique_path(target_path)

            with open(target_path, "wb") as f:
                f.write(_file.get_content())

        zip_path_base = frappe.get_site_path("private", "files", f"files_{frappe.generate_hash(length=6)}")
        zip_path = shutil.make_archive(zip_path_base, "zip", temp_dir)

        with open(zip_path, "rb") as f:
            zip_content = f.read()

        frappe.response["filename"] = os.path.basename(zip_path)
        frappe.response["filecontent"] = zip_content
        frappe.response["type"] = "download"

        os.remove(zip_path)

    finally:
        shutil.rmtree(temp_dir, ignore_errors=True)
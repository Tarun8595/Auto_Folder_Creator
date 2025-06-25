import os
import streamlit as st

def create_from_ascii_tree(file_content, folder_name, save_location):
    lines = file_content.split('\n')
    root_path = os.path.join(save_location, folder_name)
    os.makedirs(root_path, exist_ok=True)

    stack = [root_path]
    prev_indent = 0

    for line in lines:
        line = line.rstrip()
        if not line.strip():
            continue

        stripped = line.lstrip('│├─└ ')
        indent = len(line) - len(stripped)

        while indent < prev_indent:
            stack.pop()
            prev_indent -= 4

        current_path = os.path.join(stack[-1], stripped.strip())

        if ' or ' in stripped:
            filenames = [name.strip() for name in stripped.split(' or ')]
            for fname in filenames:
                open(os.path.join(stack[-1], fname), 'a').close()
        elif '.' in stripped:
            open(current_path, 'a').close()
        else:
            os.makedirs(current_path, exist_ok=True)
            stack.append(current_path)
            prev_indent = indent

    return root_path

st.title("📁 Tarun Auto Folder Creator")

uploaded_file = st.file_uploader("Upload your ASCII Tree `.txt` file", type=['txt'])
folder_name = st.text_input("Enter parent folder name (e.g., ProjectX)")
save_location = st.text_input("Enter full path to save (e.g., C:/Users/YourName/Desktop)")

st.caption("⚠️ Due to browser security, folder browsing is not allowed. Please copy-paste the path manually.")

if st.button("Create Folder Structure"):
    if uploaded_file and folder_name and save_location:
        try:
            content = uploaded_file.read().decode("utf-8")
            result_path = create_from_ascii_tree(content, folder_name, save_location)
            st.success(f"✅ Folder structure created at: `{result_path}`")
        except Exception as e:
            st.error(f"❌ Error: {e}")
    else:
        st.warning("⚠️ Please fill all fields and upload a valid .txt file.")

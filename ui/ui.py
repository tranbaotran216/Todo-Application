import gradio as gr
from api_client import get_todo, add_todo, update_todo, delete_todo

def parse_todos():
    raw = get_todo()
    lines = raw.strip().split("\n")
    rows, values = [], []

    for line in lines: 
        if not line.strip():
            continue

        parts = line.split(" (done=")
        id_task = parts[0].strip()
        id_, task = id_task.split(":", 1)
        id_ = int (id_.strip())
        task = task.strip()

        done = parts[1].replace(")", "").strip().lower() == "true"
        label = f"{id_}: {task}"
        rows.append((label, done))

        if done:
            values.append(label)

    return rows, values

def refresh():
    rows, values = parse_todos()
    choices = [r[0] for r in rows]
    return gr.update(choices= choices, value= values)

def handle_add(task):
    if not task.strip():
        return "Task cannot be empty!"
    add_todo(task)
    return f"Added {task}"

def handle_update(selected):
    rows, _ = parse_todos()
    for label, done in rows:
        id_, task = label.split(":", 1)
        id_ = int(id_.strip())
        task = task.strip()
        should_done = label in selected
        if should_done != done:
            update_todo(id_, task, should_done)
    return f"Updated!"

def handle_delete(i):
    for s in i:
        id_, _ = s.split(":", 1)
        delete_todo(int(id_.strip()))
    return "Deleted!"

with gr.Blocks() as demo:
    gr.Markdown("Todo App")

    with gr.Row():
        new_task = gr.Textbox(placeholder="new task...", label="Add")
        add_btn = gr.Button("Add")

    checklist = gr.CheckboxGroup(label="Tasks")
    status = gr.Markdown("")

    add_btn.click(handle_add, inputs=new_task, outputs=status).then(
        refresh, outputs=checklist
    )

    new_task.submit(handle_add, inputs=new_task, outputs=status).then(
        refresh, outputs=checklist
    )

    delete_btn = gr.Button("Delete selected?")
    delete_btn.click(handle_delete, inputs= checklist, outputs=status).then(
        refresh, outputs=checklist
    )

    checklist.change(handle_update, inputs=checklist, ouputs=status).then(
        refresh, outputs=checklist
    )

    demo.load(refresh, outputs=checklist)

demo.launch()
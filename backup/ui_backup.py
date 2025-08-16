import gradio as gr
from api_client import get_todo,add_todo,update_todo, delete_todo

def build_ui():
    with gr.Blocks() as demo:
        gr.Markdown("Todo application")

        #add new task
        with gr.Row():
            new_task= gr.Textbox(placeholder="New task...", label="Add a task")
            add_btn = gr.Button("Add")

        todo_list = gr.CheckboxGroup(label="Todo list", choices=[])

        # status_box = gr.Textbox(label="Status", interactive=False)
        status_msg = gr.Markdown("")

        #load todos
        def refresh_and_show():
            raw = get_todo() # return string
            lines = raw.strip().split("\n")
            labels = []
            checked = []
            for line in lines:
                if not line.strip():
                    continue
                parts = line.split(" (done=")
                label = parts[0].strip()
                done = parts[1].replace(")", "").strip().lower() == "true"
                labels.append(label)
                if done:
                    checked.append(label)
            return gr.update(choices=labels, value=checked)

        with gr.Row():
            to_id_delete=gr.Number(label="todo id")
            delete_btn = gr.Button("Delete")

    
        #handle functions
        def handle_add(t):
            if not t.strip():
                return "Task cannot be empty!", refresh_and_show()
            status = add_todo(t)
            return f"{status}", refresh_and_show()

        def handle_toggle(selected):
            raw = get_todo()
            lines = raw.strip().split("\n")
            labels = []
            for line in lines:
                if not line.strip():
                    continue
                parts = line.split(" (done=")
                label = parts[0].strip()
                labels.append(label)

                id_, task = label.split(":", 1)
                id_ = int(id_.strip())
                task = task.strip()
                done = label in selected
                update_todo(id_, task, done)
            return gr.update(choices=labels, value= selected)
        
        def handle_delete(i):
            try:
                status = delete_todo(int(i))
                return f"{status}", refresh_and_show()
            except Exception as e:
                return f"Error: {str(e)}", refresh_and_show()
            
        #handle buttons
        add_btn.click(
            fn=handle_add,
            inputs= new_task,
            outputs=[status_msg, todo_list]
        )

        new_task.submit(
            fn=handle_add,
            inputs= new_task,
            outputs=[status_msg, todo_list]
        )
        
        todo_list.change(
            fn=handle_toggle,
            inputs=todo_list,
            outputs=todo_list

        )

        delete_btn.click(
            fn=handle_delete,
            inputs=to_id_delete, 
            outputs=[status_msg, todo_list]
        )
        #load todoapp when running app
        demo.load(refresh_and_show, outputs=todo_list)

    return demo

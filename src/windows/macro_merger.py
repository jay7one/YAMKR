import tkinter as tk
from page.PyMouseMacro import MacroMerge
from macros.macro_event import MacroEvent, EventType

class MacroMerger():

    def __init__(self, root) -> None:

        self.macro_merge_tl = tk.Toplevel(root)
        self.macro_merge = MacroMerge(self.macro_merge_tl)
        self.macro_merge_tl.resizable(0,0)

        self.macro_merge.btn_mm_clear.configure(command=self.btn_mm_cmd_clear)
        self.macro_merge.btn_mm_remove.configure(command=self.btn_mm_cmd_remove)
        self.macro_merge.btn_mm_add.configure(command=self.btn_mm_cmd_add)
        self.macro_merge.btn_mm_ok.configure(command=self.btn_mm_cmd_ok)
        self.macro_merge.btn_mm_cancel.configure(command=self.btn_mm_cmd_cancel)
        self.macro_merge.btn_mm_add_delay.configure(command=self.btn_mm_cmd_add_delay)

        val_num_cmd = self.macro_merge.entry_mm_delay.register(self.validate_number)
        self.macro_merge.entry_mm_delay.config(validate="key", validatecommand=(val_num_cmd, '%P'))

        self.macro_merge.slbox_mm_left.bind("<<ListboxSelect>>", self.select_left_callback)
        self.macro_merge.slbox_mm_right.bind("<<ListboxSelect>>", self.select_right_callback)

        self.right_selection = None
        self.left_selection = None
        self.results = None

    def show(self, macro_list:list[str], selected_macro:str):
        self.results = None
        self.clear_slbox('R')
        self.clear_slbox('L')

        macro_list = [macro for macro in macro_list if macro != selected_macro]

        for i, m in enumerate(macro_list):
            self.macro_merge.slbox_mm_left.insert(i,m)

        self.setup_buttons()
        self.macro_merge_tl.wait_window()
        return self.results

    def set_bt_state(self, button:tk.Button, enabled:bool):
        button.config(state='normal' if enabled else 'disabled')
    def bt_enable(self,button:tk.Button): self.set_bt_state(button,True)
    def bt_disable(self,button:tk.Button): self.set_bt_state(button,False)

    def validate_number(self,P) -> bool:
        #print(f"Validate {P=}")
        p_str = str(P)
        return_val = p_str == '' or str.isdigit(p_str)
        self.set_bt_state( self.macro_merge.btn_mm_add_delay, p_str != '')
        return return_val

    def set_delay_add_bt(self):
        self.set_bt_state(self.macro_merge.btn_mm_add_delay, self.macro_merge.entry_mm_delay.get() != "")

    def setup_buttons(self):
        # Enable diable buttons depending on left or right side selected
        self.bt_disable(self.macro_merge.btn_mm_add)
        self.bt_disable(self.macro_merge.btn_mm_remove)

        self.set_delay_add_bt()

        if self.left_selection is not None:
            self.bt_enable(self.macro_merge.btn_mm_add)
        if self.right_selection is not None:
            self.bt_enable(self.macro_merge.btn_mm_remove)

    def btn_mm_cmd_clear(self): self.clear_slbox('R')

    def clear_slbox(self, box_str):
        if box_str == 'L':
            self.macro_merge.slbox_mm_left.delete(0,tk.END)
            self.left_selection = None
        else:
            self.macro_merge.slbox_mm_right.delete(0,tk.END)
            self.right_selection = None

    def btn_mm_cmd_remove(self):
        if self.right_selection is None: return
        listbox = self.macro_merge.slbox_mm_right
        selection = listbox.curselection()
        if selection:
            listbox.delete(selection)

    def btn_mm_cmd_add(self):
        if self.left_selection is None: return
        self.macro_merge.slbox_mm_right.insert(tk.END, self.left_selection)

    def btn_mm_cmd_ok(self):
        self.results = self.build_event_array(self.macro_merge.slbox_mm_right)
        #self.macro_merge_tl.withdraw()
        self.macro_merge_tl.destroy()


    def build_event_array(self,listbox:tk.Listbox):
        events = []
        for string in [listbox.get(i) for i in range(listbox.index(tk.END))]:
            if string.startswith("Delay:"):
                tokens = string.split(" ")
                try:
                    delay_ms = int(tokens[1])  # Convert delay string to integer
                    events.append(MacroEvent(EventType.DELAY, delay_ms))
                except ValueError:
                    print(f"Invalid delay value: {tokens[1]}")
            else:
                macro_name = string
                events.append(MacroEvent(EventType.SUB_MACRO, macro_name))

        return events

    def get_results(self):  return self.results

    def btn_mm_cmd_cancel(self):
        self.results = None
        self.macro_merge_tl.withdraw()

    def btn_mm_cmd_add_delay(self):
        ms_str = self.macro_merge.entry_mm_delay.get()
        if ms_str == "": return
        self.macro_merge.slbox_mm_right.insert(tk.END, f"Delay: {ms_str} ms")


    def slbox_item_selected(self,event):
        selection = event.widget.curselection()
        if not selection: return None
        index = selection[0]
        return event.widget.get(index)

    def select_left_callback(self,event):
        self.left_selection = self.slbox_item_selected(event)
        self.setup_buttons()

    def select_right_callback(self,event):
        self.right_selection = self.slbox_item_selected(event)
        self.setup_buttons()

def main():
    '''Main entry point for the application.'''
    root = tk.Tk()
    root.protocol( 'WM_DELETE_WINDOW' , root.destroy)

    macro_merger = MacroMerger(root)
    macro_merger.show(["ABC", 'abc123', 'xyz', 'zyg'], 'xyz')

    root.mainloop()

    for e in macro_merger.get_results():
        print(f"Evt: {e}")

if __name__ == '__main__':
    main()

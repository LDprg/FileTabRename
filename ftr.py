import sublime
import sublime_plugin
import os
import os.path
import functools

class FileTabRenameCommand(sublime_plugin.WindowCommand):
    def run(self, group, index):
        window = self.window

        aview = window.active_view()
        bview = window.views_in_group(group)[index]

        aname = aview.file_name() if aview.file_name() else aview.name()
        bname = bview.file_name() if bview.file_name() else bview.name()

        view = aview if window.get_view_index(aview) == (group, index)  else bview
        filename = aname if window.get_view_index(aview) == (group, index)  else bname

#        sublime.message_dialog(filename)
#        filename = self.view.file_name()
        branch, leaf = os.path.split(filename) 

        if not os.access(filename, os.W_OK):
            sublime.error_message(leaf + " is read-only")

        panel = view.window().show_input_panel("New Name:", leaf, functools.partial(self.on_done, filename, branch, view), None, None)

        name, ext = os.path.splitext(leaf)
        panel.sel().clear()
        panel.sel().add(sublime.Region(0, len(name)))


    def on_done(self, old, branch, view, leaf):
            new = os.path.join(branch, leaf)

            try:
                if len(leaf) is 0:
                    sublime.error_message("No filename given")
                    return;

                if os.path.exists(new) and old.lower() != new.lower():
                    sublime.error_message(new + " already exists")
                    return;

                os.rename(old, new)

                v = view.window().find_open_file(old)
                if v:
                    v.retarget(new)
            except Exception as e :
                sublime.status_message("Unable to rename: " + str(e))


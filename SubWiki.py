# coding: utf-8
import sublime, sublime_plugin, os, re
#[[郑海波]]
class MarkdownWikiLinkCommand(sublime_plugin.TextCommand):
    def run(self, edit):        
        #find our current directory
        directory = os.path.split(self.view.file_name())[0]
        #find our current window
        window = self.view.window()
        slash = "\\" if sublime.platform() == "windows" else "/"
        #find the cursor
        location = self.view.sel()[0]
        
        #find the word under the cursor @view.word u和 view.extract_scope都是返回scope
        #后者由tmLanguage定义。 
        word = self.view.substr(self.view.word(location.a)).replace("*", "")
        scope = self.view.substr(self.view.extract_scope(location.a)).replace("*", "")

        
        if "link.external.html.markdown.markdownwiki" in self.view.scope_name(location.a):
                sublime.status_message("try to open " + scope)
                sublime.active_window().run_command('open_url', {"url": scope})
        elif "link.internal.html.markdown.markdownwiki" in self.view.scope_name(location.a):
            #okay, we're good. Keep on keepin' on.        
            
            #compile the full file name and path.

            new_file = directory+slash+word+".wiki"
            #debug section: uncomment to write to the console
            # print "Location: %d" % location.a
            # print "Selected word is '%s'" % word 是·
            # print "Full file path: %s" % new_file
            # print "Selected word scope is '%s'" % self.view.scope_name(location.a)
            # if internalLink in self.view.scope_name(location.a):
            #     print "this is an internal link"
            #end debug section

            if os.path.exists(new_file):
                #open the already-created page.
                new_view = window.open_file(new_file)
            else:
                #Create a new file and slap in the default text.
                new_view = window.new_file()
                new_view.set_encoding('utf-8')
                new_edit = new_view.begin_edit()
                default_text = "#{0}\nWrite about {0} here.".format(word.encode('utf-8'))
                new_view.insert(new_edit,0,default_text.decode("utf-8"))            
                new_view.end_edit(new_edit)
                new_view.set_name("%s.mwiki" % word)
                new_view.set_syntax_file("Packages/User/MarkdownWiki/MarkdownWiki.tmLanguage")
        else:
            sublime.status_message("Can only open WikiWords, email addresses or web addresses.")

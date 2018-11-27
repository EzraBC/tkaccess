# tkaccess
A wrapper for tkinter that makes the interpreter-level gui design process easier

Allows for things like:

    from mytk import root
    r = root()
    r.make.frame('main').grid()
    r.frame_.main.make.label('name', text='Name').grid()
    r.frame_.main.make.entry('name').grid(row=0, column=1)
    name_value = r.frame_.main.entry.name.get()
    
Here I use frame_ to avoid name conflicts with the tkinter.Tk.frame method. Any tkinter widget object can be made or found via any of these equivalent ways:

    r['make']['frame'](name, *args, **kwargs)
    r.make.frame(name, *args, **kwargs)
    r['_make'].FRaMe_(name, *args, **kwargs)
    
widget wrappers and makers are case-insensitive, can be gotten via attribute or as a dict key, and are stripped of up to one underscore per side so as to cover all possible naming conflicts.

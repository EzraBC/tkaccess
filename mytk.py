import tkinter as tk

class WidgetGetter:

    def __init__(self, parent, widget_type):
        self.parent = parent
        self.widget_type = widget_type

    def getter(self, name):
        try:
            return WidgetWrapper(self.parent.children[name + '_' + self.widget_type], is_new=False)
        except KeyError:
            raise AttributeError(f"No {self.widget_type} named '{name}'")

    def __getitem__(self, name):
        return self.getter(name)

    def __getattr__(self, name):
        return self.getter(name)

class WidgetWrapper:

    def __init__(self, widget, *args, is_new=True, **kwargs):
        self.widget = widget(*args, **kwargs) if is_new else widget

    def getter(self, get_type, error_type, name):
        try:
            return getattr(self.widget, get_type)(name)
        except error_type as e:
            if name == 'make':
                return WidgetMaker(self)
            try:
                name = name.strip('_').lower()
                test = getattr(tk, name.title())
                return WidgetGetter(self, name)
            except AttributeError:
                raise e

    def __getitem__(self, name):
        return self.getter('__getitem__', tk._tkinter.TclError, name)

    def __getattr__(self, name):
        return self.getter('__getattribute__', AttributeError, name)

def make_named_widget(parent, widget, name, **kwargs):
    kwargs['name'] = name + '_' + widget.__name__.lower()
    return WidgetWrapper(widget, parent, **kwargs)

class WidgetMaker:

    def __init__(self, parent):
        self.parent = parent

    def getter(self, widget_type):
        def make_named_widget(name, **kwargs):
            kwargs['name'] = f'{name}_{widget_type.lower()}'
            return getattr(tk, widget_type.title())(self.parent, **kwargs)
        return make_named_widget
##        return lambda name, **kwargs: make_named_widget(
##            self.parent,
##            getattr(tk, widget_type.title()),
##            name,
##            **kwargs
##        )

    def __getattr__(self, widget_type):
        return self.getter(widget_type)

    def __getitem__(self, widget_type):
        return self.getter(widget_type)

def root(*args, **kwargs):
    return WidgetWrapper(tk.Tk, *args, **kwargs)
                                                        

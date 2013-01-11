
#CallAfter
#set_timeout = wx.CallLater

# Basic events

# References
# https://developer.mozilla.org/en-US/docs/Mozilla_event_reference
# http://wxpython.org/docs/api/wx.Event-class.html

class EventHandler:
    "Generic Event Handler: maps a wx.Event to a gui2py.Event"
    
    def __init__(self, name, binding, kind):
        self.name = name                # name (type), i.e.: "click"
        self.binding = binding          # wx.Event object
        self.kind = kind                # Event class
    
    def __call__(self, action):
        "Create the actual handler (binded and called by wxPython)"
        # default handler will call the user action with the event instance
        return lambda wx_event: action(self.kind(name=self.name, 
                                                 wx_event=wx_event))
        

class Event:
    "Generic Event Object: holds actual event data (created by EventHandler)"
    
    def __init__(self, name="", wx_event=None):
        self.wx_event = wx_event
        # retrieve wxPython event properties:
        wx_obj = self.wx_event.GetEventObject()
        self.target = wx_obj.reference if wx_obj else None
        self.timestamp = wx_event.GetTimestamp()
        self.name = name                  # name (type), i.e.: "click"

    def prevent_default(self, cancel=True):
        self.wx_event.Skip(not cancel)

    def stop_propagation(self):
        self.wx_event.StopPropagation()


class UIEvent(Event):
    "General -window- related events (detail can hold additional data)"   
    names = ["load", "resize", "scroll", "paint", "unload"]

    def __init__(self, detail=None, wx_event=None):
        Event.__init__(self, wx_event)
        self.detail = detail

    def prevent_default(self):
        if self.name == 'unload':
            if self.wx_event.CanVeto():
                self.wx_event.Veto()
            else:
                raise RuntimeError("Cannot Veto!")
        else:
            Event.prevent_default(self)     # call default implementation


class FocusEvent(Event):
    "Focus related events"
    
    names = ["focus", "blur"]


class FormEvent(Event):
    "Form HTML-like events "
    
    names = ["select", "change", "reset", "submit", "invalid"]
    

class MouseEvent(Event):
    "Mouse related events"
    
    names = ["click", "dblclick", "mousedown", "mousemove",
            "mouseout", "mouseover", "mouseup", "scroll"]

    def __init__(self, wx_event=None):
        Event.__init__(self, wx_event)
        self.screen_x = screen_x
        self.screen_y = screen_y
        self.client_x = client_x
        self.client_y = client_y
        self.ctrl_key = ctrl_key
        self.shift_key = shift_key
        self.alt_key = alt_key
        self.meta_key = meta_key
        self.button = button        # 0: left, 1: center, 2: right


class KeyboardEvent(Event):
    
    names = "onkeypress", "onkeydown", "onkeyup",
    
    def __init__(self, wx_event=None):
        Event.__init__(self, wx_event)
        self.ctrl_key = ctrl_key
        self.shift_key = shift_key
        self.alt_key = alt_key
        self.meta_key = meta_key
        self.key = key              # virtual key code value
        self.char = char            # Unicode character associated

        
class TimingEvent(Event):
    "Time interval events"   
    names = ["idle", "timer"]

    def __init__(self, interval=None, wx_event=None):
        Event.__init__(self, wx_event)
        self.interval = interval

    def request_more(self):
        pass        #wx.RequestMore(needMore=True)


WIDGET_EVENTS = MouseEvent, FocusEvent, TimingEvent

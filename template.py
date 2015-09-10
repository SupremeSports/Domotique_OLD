from flask.ext.socketio import SocketIO, emit

# context is a global used for rendering the templates
context = {}
buttons = []
context["buttons"] = buttons

button_script_update = """
socket.on('{0}_status', function(data)
{{   
    $('#flip_{0}').val(data.state).slider('refresh');
}});
"""

button_script_send = """
$('#flip_{0}').change( function(data)
{{
    socket.emit('{0}', {{state: $('#flip_{0}').val()}});
}});
"""

button_html = """
<form>
    <label for="flip_{0}">{1}:</label>
    <select name="flip_{0}" id="flip_{0}" data-role="slider" data-track-theme="b" data-theme="b">
        <option value="off">Off</option>
        <option value="on">On</option>
    </select>
</form>
"""

class Button():
    def __init__(self, ID, label, pin=None):
        buttons.append(self)
        self.ID = ID
        self.label = label
        self.update = button_script_update.format(ID)
        self.send = button_script_send.format(ID)
        self.html = button_html.format(ID, label)

    def event(self, data):
        state = data["state"]
        if state=="on":
            print self.ID + " ON"
        else:
            print self.ID + " OFF"
        emit(self.ID + "_status", {"state": state}, broadcast=True)
        
    def __repr__(self):
        return self.ID

    def __str__(self):
        return self.label    

footer_chrome = """
<div data-role="footer" data-position="fixed" data-tap-toggle="false">
    <div data-role="navbar">
        <ul>
            <li class="mytab"><a href="#accueil" data-role="tab" data-icon="grid">Accueil</a></li>
            <li class="mytab"><a href="#maison" data-role="tab" data-icon="grid">Maison</a></li>
            <li class="mytab"><a href="#garage" data-role="tab" data-icon="grid">Garage</a></li>
            <li class="mytab"><a href="#piscine" data-role="tab" data-icon="grid">Piscine</a></li>
            <li class="mytab"><a href="#autres" data-role="tab" data-icon="grid">Autres</a></li>
        </ul>
    </div>
</div>
"""

footer = """
<div data-role="footer" data-position="fixed">
    <div data-role="navbar">
        <ul>
            <li class="mytab"><a href="#accueil" data-role="tab" data-icon="grid">Accueil</a></li>
            <li class="mytab"><a href="#maison" data-role="tab" data-icon="grid">Maison</a></li>
            <li class="mytab"><a href="#garage" data-role="tab" data-icon="grid">Garage</a></li>
            <li class="mytab"><a href="#piscine" data-role="tab" data-icon="grid">Piscine</a></li>
            <li class="mytab"><a href="#autres" data-role="tab" data-icon="grid">Autres</a></li>
        </ul>
    </div>
</div>
"""

def ChromeBrowser():
    context["footer"] = footer_chrome

def OtherBrowsers():
    context["footer"] = footer


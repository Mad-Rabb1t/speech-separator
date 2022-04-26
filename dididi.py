import base64
import os
from urllib.parse import quote as urlquote

from flask import Flask, send_from_directory
from dash import Dash, dcc, html
from dash import dcc
from dash import html
from pydub import AudioSegment
from dash.dependencies import Input, Output

UPLOAD_DIRECTORY = "/project/app_uploaded_files"

if not os.path.exists(UPLOAD_DIRECTORY):
    os.makedirs(UPLOAD_DIRECTORY)

# Normally, Dash creates its own Flask server internally. By creating our own,
# we can create a route for downloading files directly:
server = Flask(__name__)
app = Dash(server=server)

app.layout = html.Div(
    [
        html.Div(
            [
        html.Img(src='assets/Soundwave.png', style={"height": "210px",
                                                    "objectFit": "contain",
                                                    'objectPosition': 'center',
                                                    'width': '100%'
                                                    }),
        html.H1("Split My Bullshit", style={"color": "white", 'fontSize': '36px', 'fontWeight': 'bold', 'textAlign': 'center'}),
        dcc.Upload(
            id="upload-data",
            children=html.Div(
                ["Drag and drop or click to select a file to upload."], style={"color": "white"}
            ),
            className="card",
            style={
                #"width": "100%",
                "height": "60px",
                "lineHeight": "60px",
                "borderWidth": "1px",
                # "borderStyle": "dashed",
                "borderRadius": "5px",
                "textAlign": "center",
                "margin": "10px",
                # "background-color": "#151515"
            },
            multiple=True,
        ),
        html.Ul(id="file-list"),
                html.Div([
                    html.H2('If you just want to try out ready sammples', style={'color': 'white', 'fontSize': '24px', 'textAlign': 'center', 'marginButton': '16px'}),
                    html.Div([
                        html.Button("Sample 1", style={'color': 'white', 'background': 'transparent',
                                                       'border': 'none', 'padding': '16px 8px'}),

                    ], style={'display': 'flex', 'flexDirection': 'column', 'gap': '12px'}
                    )
                ])
            ],
        style={"maxWidth": "700px", 'minWidth': '500px', 'display': 'flex', 'padding': '100px 0', 'gap': '24px', 'flexDirection': 'column'})
    ],
    style={"display": "flex",
           "justifyContent": "center",
           #"alignItems": "center",
           "minHeight": "100vh",
           'padding': '100px 0'
           }
)


def save_file(name, content):
    """Decode and store a file uploaded with Plotly Dash."""
    data = content.encode("utf8").split(b";base64,")[1]
    with open(os.path.join(UPLOAD_DIRECTORY, name), "wb") as fp:
        fp.write(base64.decodebytes(data))


def overlay_files(name1, name2):
    sound1 = AudioSegment.from_file("assets/sample.wav")
    sound2 = AudioSegment.from_file("assets/ksks.wav")
    overlay = sound1.overlay(sound2, position=0)
    name = "miksik.wav"
    overlay.export("assets/" + "miksik.wav", format="wav")
    return name


@app.callback(
    Output("file-list", "children"),
    [Input("upload-data", "filename"), Input("upload-data", "contents")],
)
def update_output(uploaded_filenames, uploaded_file_contents):
    """Save uploaded files and regenerate the file list."""

    if uploaded_filenames is not None and uploaded_file_contents is not None:
        html.Audio(id="player", src="assets/" + uploaded_filenames[0], controls=True, style={
            "width": "100%"}),
        html.Audio(id="player", src="assets/" + uploaded_filenames[1], controls=True, style={
            "width": "100%"}),
        name1 = overlay_files("assets/" + uploaded_filenames[0], "assets/" + uploaded_filenames[1])
        return html.Div([
            html.H2("First source", style={"color": "white"}),
            html.Audio(id="player", src="assets/" + uploaded_filenames[0], controls=True, style={
                "width": "100%"}),
            html.H2("Second source", style={"color": "white"}),
            html.Audio(id="player", src="assets/" + uploaded_filenames[1], controls=True, style={
                "width": "100%"}),
            html.H2("Mixed file", style={"color": "white"}),
            html.Audio(id="player", src="assets/" + name1, controls=True, style={
                "width": "100%"})
        ], style={'display': 'flex', 'flexDirection': 'column', 'gap': '16px'}),


if __name__ == "__main__":
    app.run_server(debug=True, port=8888)

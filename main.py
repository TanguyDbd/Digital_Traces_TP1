from flask import Flask, request
import logging

app = Flask(__name__)

logging.basicConfig(level=logging.DEBUG)

prefix_google = """
 <!-- Google tag (gtag.js) -->
<script async
src="https://www.googletagmanager.com/gtag/js?id=G-GV4KJPM75M"></script>
<script>
 window.dataLayer = window.dataLayer || [];
 function gtag(){dataLayer.push(arguments);}
 gtag('js', new Date());
 gtag('config', 'G-GV4KJPM75M');
</script>
 """

@app.route("/")
def hello_world():
    return prefix_google + "Hello World main page"

@app.route("/logger", methods=['GET', 'POST'])
def log():
    # Print a message in Python
    log_msg = "Vous êtes bien connectés à la page des logs"
    app.logger.info(log_msg)

    if request.method == 'POST':
        # Récupérer le texte entré dans la boîte de texte
        text_from_textbox = request.form['textbox']

        # Print a message in the browser console with the text from the text box
        browser_log = f"""
        <script>
            console.log('Console du web browser : Vous êtes bien connectés à la page des logs');
            console.log('Texte de la boîte de texte : {text_from_textbox}');
        </script>
        """
    else:
        # Print a message in the browser console
        browser_log = """
        <script>
            console.log('Console du web browser : Vous êtes bien connectés à la page des logs');
        </script>
        """

    # Formulaire HTML avec une boîte de texte and a button
    form = """
    <form method="POST">
        <label for="textbox">Text Box :</label><br>
        <input type="text" id="textbox" name="textbox"><br><br>
        <input type="submit" value="Soumettre">
        <button type="button" onclick="makeGoogleRequest()">Faire une requête Google</button>
    </form>
    """

    # JavaScript function to make the Google request
    google_request_script = """
    <script>
        function makeGoogleRequest() {
            fetch("https://www.google.com/")
                .then(response => response.text())
                .then(data => console.log("Google Response:", data))
                .catch(error => console.error("Error making Google request:", error));
        }
    </script>
    """

    return log_msg + browser_log + form + google_request_script

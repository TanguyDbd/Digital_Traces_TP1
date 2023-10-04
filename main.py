from flask import Flask

app = Flask(__name__)

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

@app.route("/logger")
def log():
    # Print a message in Python
    log_msg = "Vous êtes bien connectés à la page des logs"
    app.logger.info(log_msg)

    # Print a message in the browser console
    browser_log = """
    <script>
        console.log('Console du web browser : Vous êtes bien connectés à la page des logs');
    </script>
    """
    # The printed msg in python
    print(log_msg)

    return log_msg + browser_log
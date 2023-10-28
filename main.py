from flask import Flask, request, render_template
from io import BytesIO
import base64
import logging
import requests
import os
import numpy as np
import timelog
from google.analytics.data_v1beta import BetaAnalyticsDataClient
from google.analytics.data_v1beta.types import RunReportRequest
from pytrends.request import TrendReq
from matplotlib import pyplot as plt

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

# Main page of our web application
@app.route("/")
def hello_world():
    return prefix_google + "Main page of Tanguy's web Application for Data Traces labs" + """
    <form method="GET" action="/logger">
        <input type="submit" value="Go to the logger page">
    </form>
    <form method="GET" action="/google-request">
        <input type="submit" value="Go to the Google Analytics Requests page">
    </form>
    <form method="GET" action="/trend-chart">
        <input type="submit" value="Go to google trends data">
    </form>
    <form method="GET" action="/timerlog_experiment">
        <input type="submit" value="Go to the timerlog experiment">
    </form>
    """


# TP2 Test the python logger part
@app.route("/logger", methods=['GET', 'POST'])
def log():
    # Print a message in Python
    log_msg = "Vous êtes bien connectés à la page des logs"
    app.logger.info(log_msg)

    if request.method == 'POST':
        # Retreive the message in the textbox
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

    # HTML form with a textbox and a button
    form = """
    <form method="POST">
        <label for="textbox">Text Box :</label><br>
        <input type="text" id="textbox" name="textbox"><br><br>
        <input type="submit" value="Soumettre">
    </form>
    """
    return log_msg + browser_log + form

# TP2 Manipulate cookies part
@app.route('/google-request', methods=['GET'])
def google_request():
    # Render a form with a button to make the Google request
    return """
    <form method="GET" action="/perform-google-request">
        <input type="submit" value="Display Google Analytics Dashboard of this App">
    </form>
    <form method="GET" action="/perform-google-request-cookies">
        <input type="submit" value="Check Google Analytics Request Cookies">
    </form>
    """

# TP2 Manipulate cookies part
@app.route('/perform-google-request', methods=['GET'])
def perform_google_request():
    # Question 2.
    google_url = "https://www.google.com/"
    # Quenstion 4.
    google_analytics_url = "https://analytics.google.com/analytics/web/?pli=1#/p407459024/reports/intelligenthome"
    
    try:
        response = requests.get(google_analytics_url)
        response.raise_for_status()  # Raise an exception for HTTP errors

        return response.text
    except requests.exceptions.RequestException as e:
        return f"Error making Google Analytics request: {str(e)}"

# TP2 Manipulate cookies part
@app.route('/perform-google-request-cookies', methods=['GET'])
def perform_google_request_cookies():
    # Question 2.
    google_url = "https://www.google.com/"
    # Question 4.
    google_analytics_url = "https://analytics.google.com/analytics/web/?pli=1#/p407459024/reports/intelligenthome"
    
    try:
        response = requests.get(google_analytics_url)
        response.raise_for_status()  # Raise an exception for HTTP errors

        # Retrieve cookies of the response
        cookies = response.cookies

        # Send cookies to the template for display
        return render_template('cookies.html', cookies=cookies)
    except requests.exceptions.RequestException as e:
        return f"Error making Google Analytics Cookies request: {str(e)}"

# TP2 Request with oauth part (but not with oauth)
@app.route('/fetch-google-analytics-data', methods=['GET'])
def fetch_google_analytics_data():

    os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = 'data-traces-lab2-6ea184d3105e.json'
    PROPERTY_GA4_ID = '407459024'
    starting_date = "28daysAgo"
    ending_date = "yesterday"

    client = BetaAnalyticsDataClient()
    
    # Function that return the request from the google analytics API
    def get_visitor_count(client, property_id):
        request = RunReportRequest(
            property=f"properties/{property_id}",
            date_ranges=[{"start_date": starting_date, "end_date": ending_date}],
            metrics=[{"name": "activeUsers"}]
        )
        response = client.run_report(request)
        return response

    # Get the active visitor count using the function
    response = get_visitor_count(client, PROPERTY_GA4_ID)

    # Display the number of active visitors
    if response and response.row_count > 0:
        metric_value = response.rows[0].metric_values[0].value
    else:
        metric_value = "N/A"  # Handle the case where there is no data

    return f'Number of active visitors : {metric_value}'



# TP3 Google trend part
@app.route('/trend-chart')
def chart_data():
    pytrends = TrendReq(hl='en-US', tz=360)
    keywords = ["basketball", "handball"]
    pytrends.build_payload(keywords, timeframe='2023-01-01 2023-10-20')
    data = pytrends.interest_over_time()

    # Plot the trends
    plt.figure(figsize=(10, 4))
    plt.plot(data.index, data['basketball'], label='Basketball')
    plt.plot(data.index, data['handball'], label='Handball')
    plt.xlabel('Date')
    plt.ylabel('Number of searchs')
    plt.title('Google Trends Data on basketball and handball comparison')
    plt.legend()

    # Convert the plot for embedding in a web page
    buffer = BytesIO()
    plt.savefig(buffer, format='png')
    plt.close()
    buffer.seek(0)
    plot_data = base64.b64encode(buffer.read()).decode()

    return render_template('chart.html', plot_data=plot_data)

# TP3 Timer log part
@app.route('/timerlog_experiment', methods=['GET'])
def word_count_experiment():

    with open('shakespeare.txt', 'r') as file:
        text = file.read()

    # Create lists to store execution times and results
    exec_times_dict = []
    exec_times_counter = []

    # Run 100 times
    for _ in range(100):
        result_dict, exec_time_dict = timelog.count_dict(text)
        result_counter, exec_time_counter = timelog.count_counter(text)

        exec_times_dict.append((result_dict, exec_time_dict))
        exec_times_counter.append((result_counter, exec_time_counter))

    # Extract execution times from results
    exec_times_dict = [exec_time for _, exec_time in exec_times_dict]
    exec_times_counter = [exec_time for _, exec_time in exec_times_counter]

    # Compute mean and variance for each case
    mean_dict = np.mean(exec_times_dict)
    var_dict = np.var(exec_times_dict)
    mean_counter = np.mean(exec_times_counter)
    var_counter = np.var(exec_times_counter)

    # Create a boxplot
    data = [exec_times_dict, exec_times_counter]
    labels = ['Using Dictionary\nMean: {:.2f}\nVariance: {:.2f}'.format(mean_dict, var_dict),
            'Using Counter\nMean: {:.2f}\nVariance: {:.2f}'.format(mean_counter, var_counter)]

    plt.boxplot(data, labels=labels)
    plt.ylabel('Execution Time in sec')
    plt.title('Execution Time Distributions')
    plt.grid(True)

    # Convert the plot for embedding in a web page
    buffer = BytesIO()
    plt.savefig(buffer, format='png')
    plt.close()
    buffer.seek(0)
    plot_data = base64.b64encode(buffer.read()).decode()

    return render_template('word_count_result.html', plot_data=plot_data)


if __name__ == '__main__':
    app.run(debug=True)
# from datetime import datetime as dt
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import blockbuster
import date
import download_calendar
import loadshedding
import music
import news
import quotes
import twitter
import weather


#TODO: Add blockbuster
#TODO: add calendar events
#TODO: add music
#TODO: add news
#TODO: add twitter trends



# Function to construct the email body
def construct_email_body(day, blockbuster_data, calendar_data, loadshedding_data, music_data, news_data, quote, weather_data):
    # Extract upcoming and now_showing movies from blockbuster_data
    upcoming_movies, now_showing = blockbuster_data

    # Generate HTML for calendar events
    events_html = ''.join(
        f"<li>{event['summary']} from <b>{event['start']['dateTime'].split('T')[1][:5]}</b> to <b>{event['end']['dateTime'].split('T')[1][:5]}</b></li>"
        for event in calendar_data if any(attendee['email'] == v['email'] for attendee in event.get('attendees', []))
    ) if calendar_data else "You're not an attendee on any school events today."

    # Generate HTML for loadshedding
    loadshedding_html = (
        f"<li>There'll likely be loadshedding between {loadshedding_data[0]}</li>"
        if loadshedding_data else "It looks like there'll be no loadshedding. But that may change."
    )

    # Generate rain warning
    rain_warning = "<em>Don't forget to bring an umbrella today</em><br><br>" if rain else ""

    # Generate HTML for upcoming movies
    upcoming_movies_html = """
    <table width="100%" cellpadding="0" cellspacing="0" border="0" style='
        background-color: #f9f9f9;
        padding: 20px;
        border-radius: 10px;
        font-family: Arial, sans-serif;
    '>
        <tr>
    """

   # Centered heading for upcoming movies
    upcoming_movies_html = '''<h3 style="text-align: center;">Upcoming Movies You May Be Interested In:</h3><br>'''

    # Start the table for the grid of movies
    upcoming_movies_html += """
    <table width="100%" cellpadding="0" cellspacing="0" border="0" style='
        background-color: #f9f9f9;
        padding: 20px;
        border-radius: 10px;
        font-family: Arial, sans-serif;
    '>
        <tr>
    """

    # Iterate through the movies and create a grid of 4 columns
    for index, movie in enumerate(upcoming_movies.values()):
        if index % 4 == 0 and index != 0:
            # Start a new row after every 4 movies
            upcoming_movies_html += """
        </tr>
        <tr>
            """

        upcoming_movies_html += f"""
            <td width="25%" valign="top" style='
                padding: 10px;
                text-align: center;
            '>
                <div style='
                    background-color: #ffffff;
                    border: 1px solid #ddd;
                    border-radius: 8px;
                    padding: 15px;
                    box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
                '>
                    <img src='{movie['thumbnail']}' alt='{movie['title']}' style='
                        width: 100%;
                        border-radius: 8px;
                    '>
                    <h3 style='
                        margin: 10px 0;
                        font-size: 18px;
                        color: #333;
                        text-align: center;
                    '>{movie['title']}</h3>
                    <p style='
                        margin: 5px 0;
                        font-size: 14px;
                        color: #555;
                    '>{movie['overview']}</p>
                    <p style='
                        margin: 5px 0;
                        font-size: 14px;
                        color: #555;
                    '><strong>Release Date:</strong> {movie['release_date']}</p>
                    <p style='
                        margin: 5px 0;
                        font-size: 14px;
                        color: #555;
                    '><strong>Main Genre:</strong> {movie['main_genre']}</p>
                    <p style='
                        margin: 5px 0;
                        font-size: 14px;
                        color: #555;
                    '><strong>Secondary Genre:</strong> {movie['secondary_genre']}</p>
                </div>
            </td>
        """

    # Add empty cells if the last row has fewer than 4 movies
    remaining_cells = (4 - (len(upcoming_movies) % 4)) % 4
    for _ in range(remaining_cells):
        upcoming_movies_html += "<td width='25%'></td>"

    upcoming_movies_html += """
        </tr>
    </table>
    """

    # Centered heading for currently showing movies
    showing_movies_html = '''<h3 style="text-align: center;">Movies Currently Showing You may be interested in:</h3><br>'''

    # Start the table for the grid of movies
    showing_movies_html += """
    <table width="100%" cellpadding="0" cellspacing="0" border="0" style='
        background-color: #f9f9f9;
        padding: 20px;
        border-radius: 10px;
        font-family: Arial, sans-serif;
    '>
        <tr>
    """

    # Iterate through the movies and create a grid of 4 columns
    for index, movie in enumerate(now_showing.values()):
        if index % 4 == 0 and index != 0:
            # Start a new row after every 4 movies
            showing_movies_html += """
        </tr>
        <tr>
            """

        showing_movies_html += f"""
            <td width="25%" valign="top" style='
                padding: 10px;
                text-align: center;
            '>
                <div style='
                    background-color: #ffffff;
                    border: 1px solid #ddd;
                    border-radius: 8px;
                    padding: 15px;
                    box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
                '>
                    <img src='{movie['thumbnail']}' alt='{movie['title']}' style='
                        width: 100%;
                        border-radius: 8px;
                    '>
                    <h3 style='
                        margin: 10px 0;
                        font-size: 18px;
                        color: #333;
                        text-align: center;
                    '>{movie['title']}</h3>
                    <p style='
                        margin: 5px 0;
                        font-size: 14px;
                        color: #555;
                    '>{movie['overview']}</p>
                    <p style='
                        margin: 5px 0;
                        font-size: 14px;
                        color: #555;
                    '><strong>Release Date:</strong> {movie['release_date']}</p>
                    <p style='
                        margin: 5px 0;
                        font-size: 14px;
                        color: #555;
                    '><strong>Main Genre:</strong> {movie['main_genre']}</p>
                    <p style='
                        margin: 5px 0;
                        font-size: 14px;
                        color: #555;
                    '><strong>Secondary Genre:</strong> {movie['secondary_genre']}</p>
                </div>
            </td>
        """

    # Add empty cells if the last row has fewer than 4 movies
    remaining_cells = (4 - (len(now_showing) % 4)) % 4
    for _ in range(remaining_cells):
        showing_movies_html += "<td width='25%'></td>"

    showing_movies_html += """
        </tr>
    </table>
    """

    if day == "Sunday":
        entertainment = upcoming_movies_html
    elif day == "Monday":
        entertainment = music_data
    elif day == "Wednsesday":
        entertainment = showing_movies_html
    

    # Construct the full email body
    return f"""
    <html>
    <body>
        <p>Hi Phumelela, <br><br>
            <b>Here's your daily update:</b><br>
            
            <b>Here's how your day is looking: </b><br>
            <ul>
                <li>{morning_weather}</li>
                <li>{afternoon_weather}</li>
                <li>{evening_weather}</li>
            </ul>
            {rain_warning}
            <b>Your calendar: </b><br>
            <ul>{events_html}</ul>
            <b>Loadshedding: </b><br>
            <ul>{loadshedding_html}</ul>
            <em>{quote[0]}</em><br>
            <b> - {quote[1]}</b><br><br>

            <hr>
            {entertainment}

            <hr>
            
        </p>
    </body>
    </html>
    """

# Function to send email
def send_email(to_email, from_email, password, subject, body):
    message = MIMEMultipart()
    message["From"] = from_email
    message["To"] = to_email
    message["Subject"] = subject
    message.attach(MIMEText(body, "html"))

    with smtplib.SMTP("smtp.gmail.com", 587) as connection:
        connection.starttls()
        connection.login(user=from_email, password=password)
        connection.sendmail(from_addr=from_email, to_addrs=to_email, msg=message.as_string())

if __name__ == "__main__":
    # today_index, day = get_today_details()
    full_date = date.get_today_date()[0]
    day = date.get_today_date()[1]
    int_day = date.get_today_date()[2]
    print("Today is", day)
    
    if int_day < 8:
        from_email = 'social.phumelela@gmail.com'
        to_email = 'social.phumelela@gmail.com'
        password = "mdzg lvry nuzb jgka"
        subject = f"{day}'s Daily Update"

        blockbuster_data = blockbuster.get_upcoming_movies(full_date, date.get_future_date(38)), blockbuster.now_showing()
        calendar_data = download_calendar.get_events()
        # print("Calendar data:", calendar_data)
        loadshedding_data = loadshedding.all_affected_hours()
        # print("Loadshedding data:", loadshedding_data)
        music_data = music.get_music_data()
        print("Music data:", music_data)
        news_data = news.get_news_data()
        print("News data:", news_data)
        quote = quotes.get_quote()
        print("Quote:", quote)

    
        morning_weather = weather.hourly_weather(6)[0]
        afternoon_weather = weather.hourly_weather(12)[0]
        evening_weather = weather.hourly_weather(16)[0]
        rain = weather.hourly_weather(16)[1]

        weather_data = [morning_weather, afternoon_weather, evening_weather]
        print("Weather data:", weather_data)

        body = construct_email_body(day, blockbuster_data, calendar_data, loadshedding_data, music_data, news_data, quote, weather_data)
       
        send_email(to_email, from_email, password, subject, body)
        print("Email sent successfully")

        "__pycache__"
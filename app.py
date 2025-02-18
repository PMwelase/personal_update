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
import spotify2
import twitter
import weather

#TODO: add twitter trends



def generate_events_html(calendar_data):
    """Generate HTML for calendar events."""
    if not calendar_data:
        return "You're not an attendee on any school events today."
    
    events_list = []
    for event in calendar_data:
        if any(attendee['email'] == v['email'] for attendee in event.get('attendees', [])):
            start_time = event['start']['dateTime'].split('T')[1][:5]
            end_time = event['end']['dateTime'].split('T')[1][:5]
            events_list.append(
                f"<li>{event['summary']} from <b>{start_time}</b> to <b>{end_time}</b></li>"
            )
    return ''.join(events_list)

def generate_loadshedding_html(loadshedding_data):
    """Generate HTML for loadshedding information."""
    if loadshedding_data:
        return f"<li>There'll likely be loadshedding between {loadshedding_data[0]}</li>"
    return "It looks like there'll be no loadshedding. But that may change."

def generate_movie_grid(movies, title):
    """Generate HTML for a grid of movies."""
    html = f'<h3 style="text-align: center;">{title}</h3><br>'
    html += """
    <table width="100%" cellpadding="0" cellspacing="0" border="0" style='
        background-color: #f9f9f9;
        padding: 20px;
        border-radius: 10px;
        font-family: Arial, sans-serif;
    '>
        <tr>
    """

    for index, movie in enumerate(movies.values()):
        if index % 4 == 0 and index != 0:
            html += "</tr><tr>"
        
        html += generate_movie_card(movie)

    # Fill remaining cells
    remaining_cells = (4 - (len(movies) % 4)) % 4
    html += "<td width='25%'></td>" * remaining_cells
    html += "</tr></table>"
    
    return html

def generate_movie_card(movie):
    """Generate HTML for a single movie card."""
    return f"""
        <td width="25%" valign="top" style='padding: 10px; text-align: center;'>
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
                <h3 style='margin: 10px 0; font-size: 18px; color: #333; text-align: center;'>
                    {movie['title']}
                </h3>
                <p style='margin: 5px 0; font-size: 14px; color: #555;'>{movie['overview']}</p>
                <p style='margin: 5px 0; font-size: 14px; color: #555;'>
                    <strong>Release Date:</strong> {movie['release_date']}
                </p>
                <p style='margin: 5px 0; font-size: 14px; color: #555;'>
                    <strong>Main Genre:</strong> {movie['main_genre']}
                </p>
                <p style='margin: 5px 0; font-size: 14px; color: #555;'>
                    <strong>Secondary Genre:</strong> {movie['secondary_genre']}
                </p>
            </div>
        </td>
    """

def generate_spotify_button(music_data):
    """Generate HTML for Spotify button."""
    spotify_svg = """
    <svg role="img" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg" style="width: 24px; height: 24px; vertical-align: middle;">
        <path d="M12 0C5.4 0 0 5.4 0 12s5.4 12 12 12 12-5.4 12-12S18.6 0 12 0zm5.521 17.34c-.24.359-.66.48-1.021.24-2.82-1.74-6.36-2.101-10.561-1.141-.418.122-.779-.179-.899-.539-.12-.421.18-.78.54-.9 4.56-1.021 8.52-.6 11.64 1.32.42.18.479.659.301 1.02zm1.44-3.3c-.301.42-.841.6-1.262.3-3.239-1.98-8.159-2.58-11.939-1.38-.479.12-1.02-.12-1.14-.6-.12-.48.12-1.021.6-1.141C9.6 9.9 15 10.561 18.72 12.84c.361.181.54.78.241 1.2zm.12-3.36C15.24 8.4 8.82 8.16 5.16 9.301c-.6.179-1.2-.181-1.38-.721-.18-.601.18-1.2.72-1.381 4.26-1.26 11.28-1.02 15.721 1.621.539.3.719 1.02.419 1.56-.299.421-1.02.599-1.559.3z" fill="#1DB954"/>
    </svg>
    """
    return f"""
    <div style="text-align: center; margin-top: 20px;">
        <a href="{music_data}" style="
            text-decoration: none;
            background-color: #1DB954;
            color: white;
            padding: 10px 20px;
            border-radius: 25px;
            font-size: 18px;
            display: inline-flex;
            align-items: center;
            gap: 10px;
        ">
            {spotify_svg}
            Listen to the Top Tracks on Spotify
        </a>
    </div>
    """

def get_entertainment_content(day, upcoming_movies, now_showing, music_data):
    """Determine entertainment content based on day."""
    if day == "Sunday":
        return generate_movie_grid(upcoming_movies, "Upcoming Movies You May Be Interested In:")
    elif day == "Monday":
        return generate_spotify_button(music_data)
    elif day == "Tuesday":
        return generate_movie_grid(now_showing, "Movies Currently Showing You May Be Interested In:")
    else:
        return None

def get_weather_icon(weather_description):
    """Return appropriate weather icon path based on weather description."""
    weather_icons = {
        'clear': 'images/weather-icons/sun.png',
        'sunny': '/weather-icons/sun.png',
        'cloudy': 'images/weather/overcast.png',
        'partly cloudy': '/weather-icons/partly-cloudy.png',
        'rain': '/weather-icons/rain.png',
        'showers': '/weather-icons/rain.png',
        'thunderstorm': '/weather-icons/thunderstorm.png',
        'storm': '/weather-icons/thunderstorm.png',
        'windy': '/weather-icons/wind.png',
        'fog': '/weather-icons/fog.png',
        'snow': '/weather-icons/snow.png',
        'mist': '/weather-icons/mist.png'
    }
    
    # Default to cloudy if no match found
    for key in weather_icons:
        if key in weather_description.lower():
            return weather_icons[key]
    return weather_icons['cloudy']

def generate_weather_card(time_of_day, weather_text):
    """Generate HTML for a single weather card."""
    icon_path = get_weather_icon(weather_text)
    
    return f"""
        <div style="
            flex: 1;
            background-color: white;
            border-radius: 12px;
            padding: 15px;
            margin: 0 10px;
            box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
            text-align: center;
        ">
            <h3 style="
                margin: 0 0 10px 0;
                color: #333;
                font-size: 18px;
            ">{time_of_day}</h3>
            <img src="https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcR0370KTtLvjDIz42atSU4MPPQfIkzAEUu7xQ&s" alt="{weather_text}" style="
                width: 64px;
                height: 64px;
                margin: 10px 0;
            ">
            <p style="
                margin: 10px 0 0 0;
                color: #666;
                font-size: 14px;
            ">{weather_text}</p>
        </div>
    """

def generate_weather_section(morning_weather, afternoon_weather, evening_weather):
    """Generate HTML for all weather cards in a flex container."""
    return f"""
        <div style="
            display: flex;
            justify-content: space-between;
            margin: 20px 0;
            gap: 20px;
        ">
            {generate_weather_card("Morning", morning_weather)}
            {generate_weather_card("Afternoon", afternoon_weather)}
            {generate_weather_card("Evening", evening_weather)}
        </div>
    """

def generate_basic_card(title, content, icon_url=None):
    """Generate HTML for a basic card with optional icon."""
    icon_html = f"""
        <img src="{icon_url}" alt="{title}" style="
            width: 64px;
            height: 64px;
            margin: 10px 0;
        ">
    """ if icon_url else ""
    
    return f"""
        <div style="
            flex: 1;
            background-color: white;
            border-radius: 12px;
            padding: 15px;
            margin: 0 10px;
            box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
            text-align: center;
            min-width: 200px;
        ">
            <h3 style="
                margin: 0 0 10px 0;
                color: #333;
                font-size: 18px;
            ">{title}</h3>
            {icon_html}
            <p style="
                margin: 10px 0 0 0;
                color: #666;
                font-size: 14px;
            ">{content}</p>
        </div>
    """

def generate_card_section(cards, section_title):
    """Generate HTML for a section of cards in a flex container."""
    return f"""
        <div style="margin: 20px 0;">
            <h2 style="color: #333; margin-bottom: 15px;">{section_title}</h2>
            <div style="
                display: flex;
                justify-content: space-between;
                margin: 20px 0;
                gap: 20px;
                overflow-x: auto;
                padding-bottom: 10px;
            ">
                {' '.join(cards)}
            </div>
        </div>
    """

def generate_events_section(calendar_data):
    """Generate HTML for calendar events in card format."""
    if not calendar_data:
        return generate_card_section([generate_basic_card("No Events", "You're not an attendee on any events today.")], "Your Calendar")
    
    event_cards = []
    for event in calendar_data:
        if any(attendee['email'] == v['email'] for attendee in event.get('attendees', [])):
            start_time = event['start']['dateTime'].split('T')[1][:5]
            end_time = event['end']['dateTime'].split('T')[1][:5]
            content = f"{event['summary']}<br><b>{start_time}</b> to <b>{end_time}</b>"
            event_cards.append(generate_basic_card("Event", content))
    
    return generate_card_section(event_cards, "Your Calendar")

def generate_news_section(news_data=None):
    """Generate HTML for news in card format."""
    # Mock data
    mock_news = [
        {
            'title': 'South African markets defy geopolitical tensions with record performance',
            'description': 'Last week, much of the discussion in South Africa, both in the media and private conversations, revolved around the actions of the Trump administration against the country.'
        },
        {
            'title': 'The hottest AI models, what they do, and how to use them',
            'description': 'AI models are being cranked out at a dizzying pace, by everyone from Big Tech companies like Google to startups like OpenAI and Anthropic. Keeping track of the latest ones can be overwhelming. '
        },
        {
            'title': 'The economic ripples of maritime disruption: Understanding the global impact of geopolitical struggles',
            'description': 'The forces of geopolitical tension—spanning territorial disputes, political instability, and military conflicts—have significantly shaped the trajectory of global history. '
        }
    ]
    
    news_cards = []
    for item in mock_news:  # Using mock_news instead of news_data
        content = f"<b>{item['title']}</b><br>{item['description'][:100]}..."
        news_cards.append(generate_basic_card("News", content))
    
    return generate_card_section(news_cards, "Latest News")

def construct_email_body(day, blockbuster_data, calendar_data, loadshedding_data, music_data, news_data, quote, weather_data):
    """Construct the complete email body with card-based sections."""
    upcoming_movies, now_showing = blockbuster_data
    rain_warning = "<em>Don't forget to bring an umbrella today</em><br><br>" if rain else ""
    
    entertainment = get_entertainment_content(day, upcoming_movies, now_showing, music_data)
    events_section = generate_events_section(calendar_data)
    news_section = generate_news_section(news_data)
    weather_html = generate_weather_section(morning_weather, afternoon_weather, evening_weather)

    return f"""
    <html>
    <body style="font-family: Arial, sans-serif; max-width: 800px; margin: 0 auto; padding: 20px;">
        <h1 style="color: #333;">Hi Phumelela,</h1>
        <p><b>Here's your daily update:</b></p>
        
        {weather_html}
        {rain_warning}
        {events_section}
        {news_section}
        
        <div style="margin: 20px 0; padding: 20px; background-color: #f5f5f5; border-radius: 12px;">
            <em>{quote[0]}</em><br>
            <b> - {quote[1]}</b>
        </div>

        <hr style="margin: 30px 0;">
        {entertainment}
        <hr style="margin: 30px 0;">
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
        password = 
        subject = f"{day}'s Daily Update"

        blockbuster_data = blockbuster.get_upcoming_movies(full_date, date.get_future_date(38)), blockbuster.now_showing()
        calendar_data = download_calendar.get_events()
        # print("Calendar data:", calendar_data)
        loadshedding_data = loadshedding.all_affected_hours()
        # print("Loadshedding data:", loadshedding_data)
        music_data = spotify2.main()
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
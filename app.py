from datetime import datetime as dt
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import blockbuster
import download_calendar
import loadshedding
import music
import news
import quotes
import weather


#TODO: Add blockbuster
#TODO: add calendar events
#TODO: add music
#TODO: add news

# Function to get today's details
def get_today_details():
    now = dt.now()
    return now.weekday(), now.strftime("%A")


# Function to construct the email body
def construct_email_body(blockbuster_data, calendar_data, loadshedding_data, music_data, news_data, quote, weather_data):
    events_html = ''.join(
        f"<li>{event['summary']} from <b>{event['start']['dateTime'].split('T')[1][:5]}</b> to <b>{event['end']['dateTime'].split('T')[1][:5]}</b></li>"
        for event in calendar_data if any(attendee['email'] == v['email'] for attendee in event.get('attendees', []))
    ) if calendar_data else "You're not an attendee on any school events today."

    loadshedding_html = (
        f"<li>There'll likely be loadshedding between {loadshedding_data[0]}</li>"
        if loadshedding_data else "It looks like there'll be no loadshedding. But that may change."
    )

    rain_warning = "<em>Don't forget to bring an umbrella today</em><br><br>" if rain else ""

    return f"""
   <html>
    <body>
        <p>Hi Phumelela, <br><br>
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
            Warm Regards,

            <div style="display: flex; align-items: center; margin-top: 0.5rem;">
                <div>
                    <img src="https://avatars.githubusercontent.com/u/23073981?s=280&v=4" alt="WeThinkCode_ Logo" style="width: 80px; height: auto;">
                </div>
                <div style="margin-left: 20px;">
                    <p style="margin: 0; font-size: 14px;">
                        <b>Phumelela Mwelase</b><br>
                        Student<br>
                        WeThinkCode_
                    </p>
                    <tbody><tr><td height="5"></td></tr><tr><td color="#238dfa" height="1" style="width:239px;border-bottom:1px solid rgb(35,141,250);border-left:none;display:block"></td></tr><tr><td height="5"></td></tr></tbody>
                    <p style="margin: 0; font-size: 0.8rem;">
                        <span style="display: flex; align-items: center;">
                            <img src="https://cdn-icons-png.flaticon.com/512/3536/3536505.png" alt="LinkedIn Icon" style="width: 1rem; height: 1rem; margin-right: 5px;">
                            <a href="https://www.linkedin.com/in/phumelelamwelase/" style="color: #000;;">linkedin.com/in/phumelelamwelase</a>
                        </span>
                        <br>
                        <span style="display: flex; align-items: center;">
                            <img src="https://cdn-icons-png.flaticon.com/512/9068/9068642.png" alt="Email Icon" style="width: 1rem; height: 1rem; margin-right: 5px;">
                            <a href="mailto:pmwelase023@student.wethinkcode.co.za" style="color: #000;">pmwelase023student.wethinkcode.co.za</a>
                        </span>
                        <br>
                        <span style="display: flex; align-items: center;">
                            <img src="https://cdn-icons-png.flaticon.com/512/6994/6994770.png" alt="Website Icon" style="width: 1rem; height: 1rem; margin-right: 5px;">
                            <a href="https://wtc-update.onrender.com/" style="color: #000;">wtc-update.onrender.com</a>
                        </span>
                    </p>
                </div>
            </div>
            
            <p>Click <a href="https://wtc-update.onrender.com/unsubscribe" style="color: #000;">here</a> to unsubscribe.</p>
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
    today_index, day = get_today_details()
    print("Today is", day)
    
    if today_index < 8:
        from_email = 'social.phumelela@gmail.com'
        to_email = 'social.phumelela@gmail.com'
        password = "mdzg lvry nuzb jgka"
        subject = f"{day}'s Daily Update"

        blockbuster_data = blockbuster.get_blockbuster_data()
        print("Blockbuster data:", blockbuster_data)
        calendar_data = download_calendar.get_events()
        print("Calendar data:", calendar_data)
        loadshedding_data = loadshedding.all_affected_hours()
        print("Loadshedding data:", loadshedding_data)
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

        body = construct_email_body(blockbuster_data, calendar_data, loadshedding_data, music_data, news_data, quote, weather_data)
       
        send_email(to_email, from_email, password, subject, body)
        print("Email sent successfully")
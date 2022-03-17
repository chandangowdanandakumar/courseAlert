import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from bs4 import BeautifulSoup
import requests
import time

def emailAlert(body):
    account = "ASU Course Alert"
    username = "asucoursealert2022@gmail.com"
    password = "ONE234five#"
    smtp_server = "smtp.gmail.com"
    smtp_port = 587

    message = MIMEMultipart('alternative')
    message['From'] = "asucoursealert2022@gmail.com"
    message['Subject'] = "Course Alert"
    email_body = body + '    '
    message.attach(MIMEText(email_body,'plain'))

    server1 = smtplib.SMTP(smtp_server,smtp_port)
    server1.ehlo()
    server1.starttls()
    server1.login(username,password)
    recepients = ["9153158176@tmomail.net","chandangowdanandakumar@gmail.com","chandangowdanandakumar@outlook.com","cnandak1@asu.edu"]
    for recipient in recepients:
        server1.sendmail(message['From'],recipient, message.as_string())
        pass
    server1.quit()

if __name__ == '__main__':
    classList = [22352]
    for myclass in classList:
        url = 'https://webapp4.asu.edu/catalog/myclasslistresults?t=2221&k='+str(myclass)+'&hon=F&promod=F&e=all&page=1'
        html_text = requests.get(url).text
        soup = BeautifulSoup(html_text, 'lxml')
        seats = soup.find('td', class_='availableSeatsColumnValue')
        currentSeats = int(seats.find_all('span')[0].text)
        totalSeats = int(seats.find_all('span')[2].text)
        i = 7200
        while i > 0:
            html_text = requests.get(url).text
            soup = BeautifulSoup(html_text, 'lxml')
            title = str(int(soup.find('td', class_='classNbrColumnValue').find('a', class_='course-details-link').text))
            seats = soup.find('td', class_='availableSeatsColumnValue')
            if not currentSeats == int(seats.find_all('span')[0].text):
                emailAlert(str(int(seats.find_all('span')[0].text) - currentSeats) + " seats available for " + title)
                currentSeats = int(seats.find_all('span')[0].text)
            elif not totalSeats == int(seats.find_all('span')[2].text):
                emailAlert(str(int(seats.find_all('span')[2].text) - totalSeats) + " seats available for " + title)
                totalSeats = int(seats.find_all('span')[2].text)
            time.sleep(10)
            i -= 1
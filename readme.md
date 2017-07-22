## OpenTable Scheduler

So you've finally decided you want to check out that super popular restaurant and you go to [https://www.opentable.com/](https://www.opentable.com/) to make a reservation, but you find out that it's fully booked for the next while. 😭😭😭

Good thing is though, people are super flaky and flop all the time, so reservations eventually open up (yay!). Use this scheduler to be notified when the next reservation opens up!

## Instructions
### Installation
```
$ git clone git@github.com:iminoso/opentable-scheduler.git
$ cd opentable-scheduler
$ pip install -r requirements.txt
```

### Sendgrid
* Create an account at [sendgrid.com](https://sendgrid.com/). 
* Go to [app.sendgrid.com/settings/api_keys](https://app.sendgrid.com/settings/api_keys) and create an api key

### Configuration
The config file `config.yml` is as shown:
```
EMAIL: '<email to send notifications to>'
SENDGRID_APIKEY: '<send grid api key>'
OPENTABLE_ID: '<open table restaurant id>'
DATETIME: '<date to query reservation search around>'
PEOPLE: '<number of people for reservation>'
DATE_SEARCH_START: '<filter search start date>'
DATE_SEARCH_END: '<filter search end date>'
TIME_SEARCH_START: '<filter earliest time available>'
TIME_SEARCH_END: '<filter latest time available>'
```
Replace the `<...>` fields as follows:


`EMAIL`: The email you want notifications to be sent when a reservation opens up.

`SENDGRID_APIKEY`: The api key you created with your sendgrid account.

`OPENTABLE_ID`: A little bit of "hacking" to find this field. Navigate to the restaurant you want to make the reservation at. Before clicking `Find a Table`, open the chrome debugger by `right click > inspect`. Head to the `Network` tab and now click the `Find a Table` button. Click the `search` link request. The `OPENTABLE_ID` is in the path of the request `https://www.opentable.com/restaurant/profile/<OPENTABLE_ID>/search`.

![id](http://g.recordit.co/yJ452sEcnp.gif)

`DATETIME`: Date to search around in the following format `Year-Month-Day Time`, eg `2017-07-21 19:00`.

`PEOPLE`: Number of people for the booking.

`DATE_SEARCH_START`: The earliest possible date you want for the reservation in the format of `Year-Month-Day`, eg `2017-07-21`.

`DATE_SEARCH_END`: The latest possible date you want for the reservation in the format of `Year-Month-Day`, eg `2017-07-23`.

`TIME_SEARCH_START`: The earliest time of the day you want for your reservation in the format of `Time`, eg `18:00`.

`TIME_SEARCH_END`: The latest time of the day you want for your reservation in the format of `Time`, eg `22:00`.

### Running the scheduler
Run the scheduler as:
```
$ python scheduler.py
```
The scheduler runs every 5 minutes to check if there is a reservation available at your selected restaurant.

### Hosting on Heroku (optional)
An option for hosting the app on a cloud service. 
* Create an account at [heroku.com](https://dashboard.heroku.com/)
* Install the CLI
```
$ brew install heroku
```
* Login using the CLI
```
$ heroku login
Enter your Heroku credentials.
Email: <email to enter>
Password (typing will be hidden):
Authentication successful.
```
* In the directory of this app, create a heroku instance
```
$ heroku create
Creating app... done, ⬢ sleepy-meadow-81798
```
* Deploy the app
```
$ git push heroku master
Initializing repository, done.
updating 'refs/heads/master'
...
```
* Now the app should be running in your created heroku instance
* Check the status of the app by inspecting logs
```
$ heroku logs
```

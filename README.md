Hi  Andrei,   

please find below the TEST CODE TASK -  Python Django Engineer/Remote.

Please complete it as per the Instructions (see below) - Create this Project in your Github repo and
provide a link to me. 

I will submit it to the company for their Review. 

Thank you.


TEST TASK - Python Django Engineer - Remote 
​
Lets we have a django project.
With models:

Rental
 - name

Reservation
  -rental_id
  -checkin(date)
  -checkout(date)


Add the view with the table of Reservations with "previous reservation ID".
Previous reservation is a reservation that is before the current one into same
rental.


Example:
Rental-1
Res-1(2022-01-01, 2022-01-13)
Res-2(2022-01-20, 2022-02-10)
Res-3(2022-02-20, 2022-03-10)

Rental-2
Res-4(2022-01-02, 2022-01-20)
Res-5(2022-01-20, 2022-02-11)


|Rental_name|ID      |Checkin    |Checkout  |Previous reservation, ID|
|rental-1   |Res-1 ID| 2022-01-01|2022-01-13| -                      |
|rental-1   |Res-2 ID| 2022-01-20|2022-02-10| Res-1 ID               |
|rental-1   |Res-3 ID| 2022-02-20|2022-03-10| Res-2 ID               |
|rental-2   |Res-4 ID| 2022-01-02|2022-01-20| -                      |
|rental-2   |Res-5 ID| 2022-01-20|2022-01-11| Res-4 ID               |

Also, add a tests.
Create it into github repo and provide a link to it.


Best regards,
Denisa Molnar

Head Of People & Culture at Global Talents Hub
https://geekrecruiters.zohorecruit.com/jobs/Careers
https://geekrecruiters.com/
https://GlobalTalentsHub.com
https://techrecruitmentacademy.com/support-group48355585
https://careerupgradetools.com/tools-home

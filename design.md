Technology
----------
- Python/Django (Test out Python 3 deployment)
- PostgreSQL
- Kafka / Redis (Realtime notification)

MVP
---
- Anything that refers to sending a message refers to sending a message to an appropriate queue in Kafka
- Listeners will be defined later.

1. ✓ ***Administration-oriented***

    a. **Food Types** What kind of food restrictions do you want to allow? 

        ✓ i. Model: FoodType
            Should only be used to populate a select list of some kind.
            - Name (VarChar / 40)
        ✓ ii. Admin Page (For FoodType)

    b. **Events** Review the connections made by the application

        i. Model: Event
            Information is provided later.
        ii. Admin Page (For Event)

2. ***User-oriented***

    a. **Enroll**
     Give your email, put in some very basic information for the app to help you find a match (Food type)
        
        i. Model: EventProfile
            - Blacklist (ManyToManyField(FoodType))
            - Availability (OneToManyField(Availability))
            - InvitedBy (ForeignKey(Profile))

        ii. /Register page
            - Message NewUser queue on enrollment

        iii. Model: Invitation
            - By (ForeignKey(Profile))
            - To (Varchar(255)) // Email

            - Message InvitedUser on Invitation queue on enrollment

    b. **Passive Mode** 
    Tell it when you are available 
    
        i. Model: Availability
            - From (DateTime)
            - Until (DateTime)
            - IsRecurring (Boolean)
            - RecurringType (Picklist)
                - Weekly
            
        ii. Signal On Create
            - Message Event_(%Week%) for date that you are available if it is the current week.

    c. **Active Mode** 
        Currently only the system can setup an event.
        
        i. Model: Event
            - EventDate (Date)
            - MinAttendees (Integer) - Default to 2.
            - MaxAttendees (Integer) - Default to 3.  
            - Description (Varchar 100) - You should be able to tweet this and a link.
            - Creator (ForeignKey(Profile))
            - AllowEvaluation (Boolean)
            - Status (Picklist(Proposed / Canceled / Awaiting Evaluation / Done))
                - Proposed: Someone created an event
                - Confirmed: The Minimum Possible Attendees are attending
                - Rejected: The event was canceled
                - Awaiting Evaluation: Waiting for the event to be evaluated after it occured
                - Done: Evaluation complete

        ii. Signal On Create
            - Send message to Event_(%Week%) for the event being created.
            - TODO> Are we going to use Redis or Kafka? 
                - We will be using Kafka, with the key being set to event_(week number)
                - 

        iii. Batch job that generates an event if 
            - at least two people with compatibility are available on a day
            - they don't hate each other
            - they haven't had lunch together in the past month
            - Send message to Event_(%Week%) for the event being created.
            - Stored in /management/commands
            
    ~~d. **Lunch Request Approval**~~ (Phase 3; to begin with, you approve all lunch requests.)

     When you get a request, you will be asked to review it and approve it before it is created

        i. Model: TodaysEvent (Shows events you are invited to.)
        ii. /Validate
            - Scroll through all Lunch events and select the one that most fits your interest.
            - Click approve and you can join the event.
            - Approving one auto-rejects a different overlapping event.
        iii. Signal On Approve
            - Send message to Event_Approved for the event that was approved.
            - Send message to Event_Rejected for the event that was rejected.

    ~~e. **Lunch Review** Tell us how Lunch went~~! (Phase 2)
        
        i. Batch to mark Event as Awaiting Evaluation
        ii. Signal On Change
            - Send a message to Event_Evaluate queue
        iii. /Review
            - Add a review of the lunch
            - Did you enjoy your time with the people you went?
        iv. Update Bloom Filter if did not enjoy with person B.
        v. Model (EventEvaluation)
            - Description
            - 
        
        
~~3. ***Microservices***~~ (Phase 3)

    a. Event Proposed Mailer: Get an email when an Event is proposed

        - Uses InvitedUser queue to generate emails

    b. Event Approved Mailer: Get an email when an Event is approved by the minimum number of people necessary.

        - Uses Events_All queue to check for valid events.

    c. Event Evaluate Mailer: Get an evaluation email

        - Uses Event_Evaluate queue to check for valid events.
    
    d. Event Evaluate Mailer: Get an evaluation email

        - Uses Event_Evaluate queue to check for valid events.
        
    e. Contact on-page user on relevent event
        
        - Uses WebSockets + Events_All to create an anonymized list of events that have been approved.  Push these to a user.
        On the webside, if the User is related to the event in question, they can get a notification about it.
    

4. Queues

- NewUser; For any new user created
- InvitedUser; When a user is invited
- Event_(%Week%); When an event is set for a specific week (week 1, week 2, etc..) or when someone is 
interested in attending an event during a particular week.
- Event_Approved; When an event is approved by 2 or more people
- Event_Evaluate; When an event is complete, and you want to get feedback on the event
- Events_All 

    
Avoiding Salacious Rumor through Computer Science
-------------------------------------------------

"They trust me — dumb **cks," - Zuck

If Person A or Person B have a negative experience
- Both will be hashed and put into a [bloom filter](https://en.wikipedia.org/wiki/Bloom_filter) which is used to block
potential pairings.
  
While this can be compromised in a data leak if we are dealing with small amounts of data, we still have plausible 
deniability, which is probably enough.

Potential problems:  Person A is at lunch with 5 people and dislikes one, how do matches work in the future? 


HIPAA Compatibility
-------------------
- LOL
- The “minimum necessary” rule.   We can’t collect extra personal data unless it’s absolutely necessary to perform our services


APIs Necessary
--------------

1. GetInvitation
    POST
    url: /InvitationCode/Create/
    
    If you are a valid user, generate an invitation code and pass it back to you.  Code is saved to DB.

    Success: 
        i. {'invitation_code': 'xxxxxxxxxx'}
        mock: /InvitationCode/Create/Success/
    Failure
        i. Abuse: {'invitation_code': null, 'error_message': 'You are abusing the invitation code system'}
        mock: InvitationCode/Create/Failure/1
        ii. Banned: {'invitation_code': null, 'error_message': 'You cannot give an invitation code'}
        mock: InvitationCode/Create/Failure/2
        iii. Login: {'invitation_code': null, 'error_message': 'You are not logged in'}
        mock: InvitationCode/Create/Failure/3


2. Enrollment
    POST
    url: /Enrollment/Create/
    
    If you have a valid non-expired invitation code, you can create a login, and are then asked to log in.
   

3. Login
    POST
    Must include username and password fields.
    url: /Login/
    
    Return true and create a cookie if valid data is passed.

    Success: 
        i. {"success":true}
        mock: /Login/Success/
    Failure
        i. {"success":false}
        mock: /Login/Failure/
   
4. My Events
    GET
    User must be logged in to retrieve this.  COOKIE is checked server-side.  Only events the user is signed up for are shown.
    
    Success:
    i. {'success': true, 'message': null, 'appointments':[{'date': ..., 'title': ...., 'people': [...names..]}, ...]}

    Failure:
    i. {'success': false, 'message': 'You are not logged in', 'appointments': []}
    ii. {'success': false, 'message': 'You are abusing the system', 'appointments': []}
   
5. Public Events
    GET
    User must be logged in to retrieve this.  COOKIE is checked server-side.
    
    Success:
    i. {'success': true, 'message': null, 'appointments':[{'date': ..., 'title': ...., 'people': [...names..]}, ...]}
    
            // Javascript code below to generate the obj.
            date_fn = (i) => {
                return new Date((new Date()).getTime() + i * 1000 * 60 * 60 * 24)
            }
        
            ret = {'success': true, 'message': null, 'appointments': [
                {'date': date_fn(1), 'title': 'Event 1', 'people': ['Edward', 'Willis']},
                {'date': date_fn(2), 'title': 'Event 2', 'people': ['Willis', 'Debra']},
                {'date': date_fn(3), 'title': 'Event 3', 'people': ['Debra', 'Wilhelmina']},
                {'date': date_fn(4), 'title': 'Event 4', 'people': ['Wilhelmina', 'Thanh', 'David']},
                {'date': date_fn(5), 'title': 'Event 5', 'people': ['Thanh', 'David']},
                {'date': date_fn(6), 'title': 'Event 6', 'people': ['David', 'Lori']},
                {'date': date_fn(7), 'title': 'Event 7', 'people': ['Lori', 'Bobby', 'Charlotte']},
                {'date': date_fn(8), 'title': 'Event 8', 'people': ['Bobby', 'Charlotte']},
             ]}

    Failure:
    i. {'success': false, 'message': 'You are not logged in', 'appointments': []}
    ii. {'success': false, 'message': 'You are abusing the system', 'appointments': []}

6. Valid Locations
    GET
    user must be logged in to retrieve this.  Locations the user can search at.

7. Valid Food Types
    GET
    user must be logged in to retrieve this.  Food types that the user can search for.


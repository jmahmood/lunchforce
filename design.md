Technology
----------
- Python/Django (Test out Python 3 deployment)
- PostgreSQL
- Kafka / Redis (Realtime notification)

MVP
---
- Anything that refers to sending a message refers to sending a message to an appropriate queue in Kafka
- Listeners will be defined later.

1. ***Administration-oriented***

    a. **Food Types** What kind of food restrictions do you want to allow? 

        i. Model: FoodType
            Should only be used to populate a select list of some kind.
            - Name (VarChar / 40)
        ii. Admin Page (For FoodType)

    b. **Connections** Review the connections made by the application

        i. Model: Event
            Should store information about each event
            
            - EventDate (DateTime field)
            - Attendees (ManyToManyField(Profile))
        ii. Admin Page (For FoodType)

2. ***User-oriented***

    a. **Enroll**
     Give your email, put in some very basic information for the app (Food type)
        
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
                - Rejected: The event was canceled
                - Awaiting Evaluation: Waiting for the event to be evaluated after it occured
                - Done: Evaluation complete

        ii. Signal On Create
            - Send message to Event_(%Week%) for the event being created.
            
        iii. Weekly batch job that generates an event if 
            - at least two people with compatibility are available on a day
            - they don't hate each other
            - they haven't had lunch together in the past month
            - Send message to Event_(%Week%) for the event being created.
            
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

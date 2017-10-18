Technology
----------
Python/Django (Test out Python 3 deployment)
PostgreSQL
Kafka / Redis (Realtime notification)

Functionalities
----------

1. Administration

    a. Food Types: What kind of food restrictions do you want to empower? 

        i. Model: FoodType

    b. Connections: Review the connections made by the application

        i. Model: Connection

    c. Rewards: Create a competition to get people onboard! 

        i. Model: LunchCampaign
            - Can we use Force.com for this?  Campaign?
    
2. User
    a. Register: Give your email, put in some very basic information for the app (Food type)
    b. Passive Mode: Tell it when you are available 
    c. Active Mode: Setup an event and tell us how many people you want (and from where?)
    d. Lunch Request Approval: When you get a request, you will be asked to review it and approve it before it is created
    e. Lunch Review: Tell us how Lunch went!

3. Emails
    a. Connection Made: Get an email when a connection is made
        i. Purpose: Add-on integration for emails
        ii. Ease of Use / MVP: Everyone has emails
        
4. Real Time
    a. Messages: Get told when a mail is sent to you / etc..
        i. Purpose: Learn about Kafka / Redis in a real solution
    
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

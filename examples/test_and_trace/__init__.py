"""
This is the top-level package of a distribution.
Imagine there was a setup.py here.

Story
=====

Who: The government
What: Test and Trace whether people have coronavirus
How:
   - Home test
        People will order home test kit if they have symptoms.
        There is a website where people answer questions about
        their personal information. The website also needs to screen people
        whether they are essential workers, whether they have symptoms,
        whether it is too late for them to be tested.
   - Test site
        There is a website for people to register their personal information,
        for them to book an appointment at a test site to be tested.
        The website also needs to screen people whether they are essential
        workers, whether they have symptoms, and whether it is too late for
        them to be tested.
   - Tracking app
        It is mobile application where people download onto their phones.
        The application should track no personal information whatsoever.
        The application should broadcast a random number for identifying itself
        via bluetooth. Other application users in the proximity will then
        store this identifier for 14 days.
        The application will accept self reported test results. When someone
        is tested positive, other app users who have been in the proximity
        in the last 14 days will be notified.
"""

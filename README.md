# Friendable
The no strings attached way to meet new people.

## Inspiration
- Coming into BostonHacks, we were especially intrigued with the mental health and community tracks and how we could deal with these in a world after Covid. Two years of everything being closed and everyone being socially isolated has taken a significant toll on our mental health and has weakened communities. We created Friendable to help people get the ball rolling again socially and help people form new relationships and communities with other local people through shared experiences. Our service helps people take their mind off stressful situations by giving them social outlets in order to help them maintain a healthy mental disposition.

## What it does
- Anyone wanting to use Friendable just needs to navigate to our webapp homepage. They input their phone number and respond with an authentication token that was texted to them for passwordless login, then fill out our patented *Friend Form<sup>TM</sup>*. Using our own custom trained ML models, we cluster people based on how they answer the questionnaire and display the highly customized, unique results. Along with the people, we recommend real time local events and local restaurants that we match to your group based on the questionnaire results. Users can choose to alert the group if they are attending the recommended event. Recommendations also get updated on a weekly basis. If you leave the page, just log back in with your number to see your saved results! This innocent looking project is a technical beast!

## How we built it

### Frontend
 - The frontend was meticulously written in pure HTML/CSS, in order to craft the most visually enticing user experience. The multiple files were linked together with flask, detailed further on.

### Backend
- For the backend we used a combination of Flask and Firebase’s Firestore database. We used flask to interact with the database and process the data. We used Firestore to store all of the data including the users, their answers, the temporary verification codes, groups and activities. 

### Twilio
- Twilio was ultimately used to perform a passwordless login, in which the user would receive a temporary verification code that logs them into an account associated with their phone number. Since no real sensitive data was being collected/kept, we felt that this would be the most convenient solution for the user.

### Google Maps Places/SerpApi
- To retrieve the local destinations we used the Google Cloud Maps Platform, which allowed us to cater the highest rated food destinations to users on a student budget, all within a 2 km radius. We also implemented SerpApi as a way of finding and presenting upcoming/live events occurring at the user’s location. This allows Friendable to propose a truly engaging experience, that is sure to make connections, and take people’s minds off stressful post-Covid life.

### Google Cloud Firebase
- Every user that completes the questionnaire first gets classified into groups by our ML model, which we explain below. Then we save all of the results in our Firebase database until we need to retrieve results. When a user attempts to see their matches, we fetch matching users from Firebase and display their names, as well as their photos to the requesting user. This schema allows us to keep an updated list of active users so that matches can improve and change over time, and we can push rolling updates to users on a weekly basis, including new matches and events.

### Custom ML Clustering Models
- One of the hardest parts of this project was finding a way to properly group users together. To achieve this, we created a custom ML model that clusters users together based on the K-means clustering algorithm. We trained this model on 1500 generated user responses and configured a workflow pipeline that allows us to access this model and group any new user as they utilize our service.

## Challenges we ran into
- One challenge we faced was we had to generate fake data for users to emulate how matching with other users would work. To do this we used random generators and thispersondoesnotexist.com to build complete fake profiles. This also caused a challenge when interrogating the fake data with the real profiles that we created because it meant that we had to be meticulous in the structure of the data and any changes to the structure made would have to be made twice. 

## Accomplishments that we're proud of
- We are proud of having built something that will help students ease into making new friends post pandemic.
- We had never implemented any custom ML models that we trained, so we are very proud we were able to get it working for this project.
- The most valuable aspect of this project is our ability to accurately match people with similar interests. We were able to do so by asking very specific questions that allowed us to precisely categorize people on different personality traits.

## What we learned
- It was my first time using Firestore and although I have used NoSQL databases in the past, it was still a learning experience. After working through the initial pains, the features and ease of use really appealed to me, and I will probably use Firestore again in the future. 

## What's next for Friendable!
- We wanted to implement college club recommendations but because of time constraints had to drop this from the scope of the project.
- We would also like to refine our clustering algorithm and questionnaire to get even more refined and accurate results.
- We also were not able to publicly host this project in the allotted time, which is something that we definitely want to do in the future.



# Midterm Exam 20232
**Course:** IT3090E - Database | **Class:** 149325 | **Date:** 23/4/2024 | **Duration:** 75 min (Closed book)

**Student ID:** ............................... **Student Name:** ...........................................

---

### Question 1: ER Modeling and Relational Schema
Model the following data requirement using an ER model and then transform it into a relational schema:

Bloodhound Coaches runs daily scheduled services all over the country. Customers want to check the schedules and prices online, so a first step is to put the schedule into a database. The company runs services to many towns. Some towns have depots, and some do not. For each depot, we want to record a contact telephone number and street name. All services run between two depots, stopping at a number of stops in between. Each route has a number, and buses will drive that route several times a day. Ticket costs are calculated as a simple sum of prices between each pair of stops visited. However, there may be special prices from time to time, between two specific towns. Children go for half price. Customers want to be able to check the price of any direct journey, and to find out all the route numbers that visit a given stop. The time taken to drive a direct route between two stops is also known. This is assumed to be constant throughout the day.

### Question 2: Functional Dependencies
Given a relation $R(A, B, C, D)$ and a set of functional dependencies $F = \{AB \to D; BC \to C; AC \to B; AC \to CD\}$. Write 4 other functional dependencies that can be derived from $F$ using Armstrong’s axiom system.

### Question 3: Normalization
Given a relation $R(A, B, E, I, J, G, H)$ and a set of functional dependencies $F = \{AB \to E; AG \to J; BE \to I; E \to G; GI \to H\}$:
a. Find a candidate key of $R$.
b. Normalize to Third Normal Form (3NF).

### Question 4: Relational Algebra and SQL
Given the Blood Bank Database schema (Primary keys in **bold**, Foreign keys in *italic*):

*   **Blood_Type** (*blood_type_ID*, name, description)
*   **Donor** (*donor_ID*, *blood_type_ID*, name, date_of_birth, contact_number, city)
*   **Donation** (*d_tran_ID*, *donor_ID*, donation_confirmation, health_condition, amount, date)
*   **Hospital** (*hospital_ID*, name, city)
*   **Recipient_Transaction** (*r_trans_ID*, *hospital_ID*, *blood_type_ID*, date)
*   **Recipient_Transaction_Details** (*r_trans_ID*, *d_tran_ID*)

Write queries for the following:
1. List all Donors in “Hanoi” (city).
2. List the hospitals that have received the blood type “Rh+”.
3. List all donors under 20 years old or over 58 years old.
4. List the number of donations per day in July 2023 (suppose that the date is recognized by day) in order of date.
5. List the information about Donors who have not donated blood in the last 3 years.
6. Write the algebraic expression for query 3.
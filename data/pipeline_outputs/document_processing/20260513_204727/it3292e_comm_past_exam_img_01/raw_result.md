# OCR Result: it3292e_comm_past_exam_img_01

Source: `data/sample/community/IT3292E/past_exam/Database - giữa kì cô Trinh.jpg`

## Segment ?

### Content Description for Learning Value

This document is a database management systems midterm exam. The learning value lies in the four distinct categories of database design and querying problems presented:

1.  **ER Modeling and Schema Transformation:** Question 1 provides a real-world scenario (a coach service) requiring the student to perform conceptual database design and map those requirements into a relational schema.
2.  **Functional Dependencies (FDs):** Question 2 tests the application of Armstrong’s Axioms to infer new functional dependencies from a given set ($F$).
3.  **Relational Normalization:** Question 3 requires identifying the candidate key of a relation and decomposing it into Third Normal Form (3NF), a core concept in database integrity.
4.  **Relational Algebra and SQL:** Question 4 provides a sample database schema (a Blood Bank) and asks for specific queries. This tests the ability to navigate relationships between entities (e.g., matching donors to donations and hospitals) and perform filtering, aggregation, and set operations.

---

### OCR Text Extraction

Midterm Exam 20232
IT3090E - Database Class: 149325 Date: 23/4/2024 Duration: 75 min (Closed book)
Student ID: ...............................Student Name: ........................................... 1

**Question 1:** Modeling the following data requirement using ER model and then transforming it into relational schema
Bloodhound Coaches runs daily scheduled services all over the country. Customers want to check the schedules and prices online, so a first step is to put the schedule into a database.
The company runs services to many towns. Some towns have depots, and some do not. For each depot we want to record a contact telephone number and street name. All services run between two depots, stopping at a number of stops in between. Each route has a number, and buses will drive that route several times a day. Ticket costs are calculated as a simple sum of prices between each pair of stops visited.
However, there may be special prices from time to time, between two specific towns. Children go for half price. Customers want to be able to check the price of any direct journey, and to find out all the route numbers that visit a given stop.
The time taken to drive a direct route between two stops is also known. This is assumed to be constant throughout the day.

**Question 2:** A relation R(ABCD) and a set of functional dependency F = {AB→D; BC→C; AC→B; AC→CD}. Write 4 other functional dependencies that can be derived from F using the Armstrong’s axiom system.

**Question 3:** A relation R(ABEIJGH), and a set of functional dependency F ={AB→E; AG→J; BE→I; E→G; GI→H},
a. Find a candidate key of R
b. Normalize to third normal form.

**Question 4:** Given the Blood Bank Database schema:
Blood_Type (blood_type_ID, name, description)
Donor (donor_ID, blood_type_ID, name, date_of_birth, contact_number, city)
Donation (d_tran_ID, donor_ID, donation_confirmation, health_condition, amount, date)
Hospital (hospital_ID, name, city)
Recipient_Transaction (r_trans_ID, hospital_ID, blood_type_ID, date)
Recipient_Transaction_Details (r_trans_ID, d_tran_ID)
Attributes in bold are primary keys, Attributes in italic are foreign key references to the attributes of the same name which are primary keys in another relation

Write queries for
1. List all Donor in “Hanoi” (city)
2. List the hospital that have received the blood’s type “Rh+”
3. List all donors under 20 years old or over 58 years old.
4. List the number of donations per day in July 2023 (suppose that the date is recognized by day) in order of date.
5. List the information about Donors who do not donate the blood in the 3 last years
6. Write the algebraic expression for query 3

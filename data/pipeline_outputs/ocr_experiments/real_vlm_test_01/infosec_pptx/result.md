# OCR Result: infosec_pptx

Source: `src/experiments/document_processing/test_data/SoICT - 4010E IntroInfoSec - C6- VanNK -extra.pptx`

## Segment 1

Identity Authentication
With extra material for further reading, indicated by symbol *

## Segment 2

Info-Sec 2023
2
Authentication
Basics
Passwords
Challenge-Response
Biometrics
Location
Multiple Methods

## Segment 3

Info-Sec 2023
3
Basics
Authentication: binding of identity to subject
Identity is that of external entity (my identity, Van, etc.)
Subject is computer entity (process, etc.)
Note: 
message authentication is a different topic and already mentioned in the applications of hash functions

## Segment 4

4
Establishing Identity
One or more of the following
What entity knows (eg. password)
What entity has (eg. Identity card, smart card)
What entity is (eg. fingerprints, retinal characteristics)
Where entity is (eg. In front of a particular terminal)

## Segment 5

Info-Sec 2023
5
Authentication System
We need a formal definition, rather abstract view, of an AS 
A 5-tuple (A, C, F, L, S)
A – a set: information that proves identity
C – a set: information stored on computer and used to validate authentication information
F: a set of complementation functions; f : A → C
To compute complement information from identity information
L: authentication functions that prove identity
S: functions enabling entity to create, alter information in A or C

## Segment 6

Info-Sec 2023
6
Example
Password system, with passwords stored on line in clear text
A set of strings making up passwords
C = A
F singleton set of identity function { I }
L single equality test function { eq }
S function to set/change password

## Segment 7

Info-Sec 2023
7
Passwords
Sequence of characters
Examples: 10 digits, a string of letters, etc.
Generated randomly, by user, by computer with user input
Sequence of words
Examples: pass-phrases
Algorithms
Examples: challenge-response, one-time passwords

## Segment 8

Info-Sec 2023
8
Storage
Store as cleartext
If password file compromised, all passwords revealed
Encipher file
Need to have decipherment, encipherment keys in memory
Reduces to previous problem 🡺 need something else
Solution: Instead store one-way hash of password
Got the file, attacker must still guess passwords or invert the hash values

## Segment 9

Info-Sec 2023
9
Example: Unix
By definition, a 5-tuple (A, C, F, L, S)
A – a set: information that proves identity
A = { strings of 8 chars or less }
C – a set: information stored on computer and used to validate authentication information
C = {hash values of password}
F: a set of complementation functions; f : A → C
F = { versions of modified DES }
L: authentication functions that prove identity
L = { login, su, … }
S: functions enabling entity to create, alter information in A or C
S = { passwd, nispasswd, passwd+, … }

## Segment 10

Info-Sec 2023
10
Example: Unix
By definition, a 5-tuple (A, C, F, L, S)
A – a set: information that proves identity
A = { strings of 8 chars or less }
C – a set: information stored on computer and used to validate authentication information
C = {hash values of password}
F: a set of complementation functions; f : A → C
F = { versions of modified DES }
L: authentication functions that prove identity
L = { login, su, … }
S: functions enabling entity to create, alter information in A or C
S = { passwd, nispasswd, passwd+, … }

## Segment 11

Info-Sec 2023
11
Attacking passwords
Goal: find a ∈ A such that:
For some f ∈ F, f(a) = c ∈ C 
c is associated with entity
Two ways to determine whether a meets these requirements:
By trying computing f(a) for a set of a values until succeed
By trying calling I(a) until succeed (I(a) returns true)

## Segment 12

Info-Sec 2023
12
Preventing Attacks
How to prevent this:
Hide at least one of a, f, or c 
Prevents obvious attack from above
Example: UNIX/Linux shadow password files
Hides the c’s
Block access to all l ∈ L or result of l(a)
Prevents attacker from knowing if guess succeeded
Example: preventing any logins to an account from a network
Prevents knowing results of l (or accessing l)

## Segment 13

Info-Sec 2023
13
Dictionary Attacks
Trial-and-error from a list of potential passwords
Off-line: know f and c’s, and repeatedly try different guesses g ∈ A until the list is done or passwords guessed
Examples: crack, john-the-ripper
On-line: have access to functions in L and try guesses g until some l(g) succeeds
Examples: trying to log in by guessing a password

## Segment 14

Info-Sec 2023
14
Success probability over a time period
Anderson’s formula:
P probability of guessing a password in specified period of time
G number of guesses tested in 1 time unit
T number of time units
N number of possible passwords (|A|)
Then P ≥ TG/N

## Segment 15

Info-Sec 2023
15
Example
Goal
Passwords drawn from a 96-char alphabet
Can test 104 guesses per second
Probability of a success to be 0.5 over a 365 day period
What is minimum password length?
Solution
N ≥ TG/P = (365×24×60×60)×104/0.5 = 6.31×1011
Choose s such that Σsj=0 96j ≥ N
So s ≥ 6, meaning passwords must be at least 6 chars long

## Segment 16

Exercise
X = number defined by last 2 digits of your student ID; Y = X mod 4
Assume that H is a cryptographic hash function with output size (Y+2)*16 bits. Assume that Scorpion-i (i=1-9) is a specifically designed line of hardware chips for computing H, where Scorpion-i can create 10i * 1000 hash values a second (e.g. Scorpion-2 can do 100,000 hashes/sec). This product line is the best, fastest and affordable, in the market, priced at ii/2 *$1000 (e.g $2000 for i=2, $16000 for i=4). 

An authentication system requires its users to pick their passwords of length exactly 6 from an alphabet of size N=(X mod 50)+ 40. Using H, this system maintains the hash values of the passwords of all the users. An enemy, who has gained access to this hashed password file, aims to launch an off-line attack to break the password of an important user. Using the Scorpion chips, how much the enemy has to spend in order to finish within a month with success probability (6+Y)*10%?
16

## Segment 17

Info-Sec 2023
17
On password selection
Random selection
Any password from A equally likely to be selected
Pronounceable passwords
User selection of passwords

## Segment 18

Info-Sec 2023
18
Pronounceable Passwords
Generate phonemes randomly
Phoneme is unit of sound, eg. cv, vc, cvc, vcv
Examples: helgoret, juttelon are; przbqxdfl, zxrptglfn are not
Problem: too few
Solution: key crunching
Run long key through hash function and convert to printable sequence
Use this sequence as password

## Segment 19

Info-Sec 2023
19
User Selection
Problem: people pick easy to guess passwords
Based on account names, user names, computer names, place names
Dictionary words (also reversed, odd capitalizations, control characters, “elite-speak”, conjugations or declensions, swear words, Torah/Bible/Koran/… words)
Too short, digits only, letters only
License plates, acronyms, social security numbers
Personal characteristics or foibles (pet names, nicknames, job characteristics, etc.

## Segment 20

Info-Sec 2023
20
Picking Good Passwords
“LlMm*2^Ap”
Names of members of 2 families
“OoHeO/FSK”
Second letter of each word of length 4 or more in third line of third verse of Star-Spangled Banner, followed by “/”, followed by author’s initials 
What’s good here may be bad there
“DMC/MHmh” bad at Dartmouth (“Dartmouth Medical Center/Mary Hitchcock memorial hospital”), ok here
Why are these now bad passwords? ☹

## Segment 21

Info-Sec 2023
21
Proactive Password Checking
Analyze proposed password for “goodness”
Always invoked
Can detect, reject bad passwords for an appropriate definition of “bad”
Discriminate on per-user, per-site basis
Needs to do pattern matching  on words
Needs to execute subprograms and use results
Spell checker, for example
Easy to set up and integrate into password selection system

## Segment 22

Info-Sec 2023
22
Salting
Goal: slow dictionary attacks
Method: perturb hash function so that:
Parameter controls which hash function is used
Parameter differs for each password
So given n password hashes, and therefore n salts, need to hash guess n

## Segment 23

Info-Sec 2023
23
Examples
Vanilla UNIX method
Use DES to encipher 0 message with password as key; iterate 25 times
Perturb E table in DES in one of 4096 ways
12 bit salt flips entries 1–11 with entries 25–36
Alternate methods
Use salt as first part of input to hash function

## Segment 24

Info-Sec 2023
24
Unix actually is …
UNIX system standard hash function
Hashes password into 11 char string using one of 4096 hash functions
As authentication system:
A = { strings of 8 chars or less }
C = { 2 char hash id || 11 char hash }
F = { 4096 versions of modified DES }
L = { login, su, … }
S = { passwd, nispasswd, passwd+, … }

## Segment 25

Exercise
Assume that H is a cryptographic hash function with output size (Y+2)*16 bits. Assume that Scorpion-i (i=1-9) is a specifically designed line of hardware chips for computing H, where Scorpion-i can create 10i * 1000 hash values a second, priced at ii/2 *$1000.
1. An authentication system requires its users to pick their passwords of length exactly 6 from an alphabet of size N=(X mod 50)+ 40. Using H, this system maintains the hash values of the passwords of all the users. An enemy, who has gained access to this hashed password file, aims to launch an off-line attack to break the password of an important user. Using the Scorpion chips, how much the enemy has to spend in order to finish within a month with success probability (6+Y)*10%?
2. The owner decides to enhance the above password system by using salt so that the enemy will need to spend at least 10 times the above mentioned amount of money to achieve the same goal. How many salt bits he/she need to use to achieve this purpose ?
25

## Segment 26

Part 2 ⎯ Access Control                                                                                                  26
Password Cracking: Do the Math*
* Further reading
Assumptions:
Pwds are 8 chars, 128 choices per character
Then 1288 = 256 possible passwords
There is a password file with 210 pwds
Attacker has dictionary of 220 common pwds
Probability 1/4 that password is in dictionary
Work is measured by number of hashes

## Segment 27

Part 2 ⎯ Access Control                                                                                                  27
Salt with slow hash *
Hash password with salt
Choose random salt s and compute 
			y = h(password, s) 
	and store (s,y) in the password file
Note that the salt s is not secret
Analogous to IV 
Still easy to verify salted password
But lots more work for Hacker
Why?

## Segment 28

Part 2 ⎯ Access Control                                                                                                  28
Password Cracking: Case I *
Attack 1 specific password without using a dictionary
E.g., administrator’s password
Must try 256/2 = 255 on average
Like exhaustive key search
Does salt help in this case?

## Segment 29

Part 2 ⎯ Access Control                                                                                                  29
Password Cracking: Case II *
Attack 1 specific password with dictionary
With salt
Expected work: 1/4 (219) + 3/4 (255) ≈ 254.6
In practice, try all pwds in dictionary…
…then work is at most 220 and probability of success is 1/4 
What if no salt is used?
One-time work to compute dictionary: 220
Expected work is of same order as above
But with precomputed dictionary hashes, the  “in practice” attack is essentially free…

## Segment 30

Part 2 ⎯ Access Control                                                                                                  30
Password Cracking: Case III *
Any of 1024 pwds in file, without dictionary
Assume all 210 passwords are distinct 
Need 255 comparisons before expect to find pwd
If no salt is used
Each computed hash yields 210 comparisons
So expected work (hashes) is 255/210 = 245
If salt is used
Expected work is 255 
Each comparison requires a hash computation

## Segment 31

Part 2 ⎯ Access Control                                                                                                  31
Password Cracking: Case IV *
Any of 1024 pwds in file, with dictionary
Prob. one or more pwd in dict.: 1 – (3/4)1024 ≈ 1
So, we ignore case where no pwd is in dictionary
If salt is used, expected work less than 222
See book, or slide notes for details
Work ≈ size of dictionary / P(pwd in dictionary)
What if no salt is used? 
If dictionary hashes not precomputed, work is about 219/210 = 29

## Segment 32

Info-Sec 2023
32
Guessing Through L
Cannot prevent these
Otherwise, legitimate users cannot log in
Make them slow
Backoff
Disconnection
Disabling
Be very careful with administrative accounts!
Jailing
Allow in, but restrict activities

## Segment 33

Info-Sec 2023
33
Password Aging
Force users to change passwords after some time has expired
How do you force users not to re-use passwords?
Record previous passwords
Block changes for a period of time
Give users time to think of good passwords
Don’t force them to change before they can log in
Warn them of expiration days in advance

## Segment 34

Info-Sec 2023
34
Challenge-Response
User, system share a secret function f (in practice, f is a
	known function with unknown parameters, such as a
	cryptographic key)
user
system
request to authenticate
user
system
random message r
(the challenge)
user
system
f(r)
(the response)

## Segment 35

Info-Sec 2023
35
Pass Algorithms
Challenge-response with the function f itself a secret
Challenge is a random string of characters 
Response is some function of that string 
Usually used in conjunction with fixed, reusable password

## Segment 35

### Slide Image
## Image Description:

The image shows a login form. It has fields for "username" and "password". Below these is a CAPTCHA challenge, displaying two distorted words: "asbury" and "law".  There's a text box to enter the CAPTCHA text, and a "login" button at the bottom. The CAPTCHA is powered by reCAPTCHA, with its logo visible. The form has a light blue header with the title "login".

---

## Markdown Notes:

### Login Form Analysis

*   **Purpose:** User authentication - allows access to a system/account.
*   **Fields:**
    *   Username: Text input for user identification.
    *   Password: Text input (masked) for authentication.
*   **Security:**
    *   **CAPTCHA:** Used to differentiate between human users and bots.
        *   Words displayed: "asbury" and "law" (distorted).
        *   Powered by reCAPTCHA.
*   **Action:**
    *   "Login" button: Submits the form for authentication.
*   **UI Elements:**
    *   Light blue header with "login" title.
    *   Standard text input boxes.
    *   Button for submission.
*   **Potential Considerations:**
    *   Password security (encryption, hashing).
    *   CAPTCHA accessibility (audio alternative).
    *   Error handling (invalid credentials, CAPTCHA failure).
    *   Form validation (required fields).

## Segment 36

Info-Sec 2023
36
One-Time Passwords
Password that can be used exactly once
After use, it is immediately invalidated
Challenge-response mechanism
Challenge is number of authentications; response is password for that particular number
Problems
Synchronization of user, system
Generation of good random passwords
Password distribution problem

## Segment 37

Info-Sec 2023
37
S/Key
One-time password scheme based on idea of Lamport
h one-way hash function (MD5 or SHA-1, for example)
User chooses initial seed k
System calculates:
h(k) = k1, h(k1) = k2, …, h(kn–1) = kn
Passwords are reverse order:
p1 = kn, p2 = kn–1, …, pn–1 = k2, pn = k1

## Segment 38

Info-Sec 2023
38
S/Key Protocol
System stores maximum number of authentications n, number
of next authentication i, last correctly supplied password pi–1.
System computes h(pi) = h(kn–i+1) = kn–i+2 = pi–1. If match with
what is stored, system replaces pi–1 with pi and increments i.

## Segment 39

Info-Sec 2023
39
C-R and Dictionary Attacks
Same as for fixed passwords
Attacker knows challenge r and response f(r); if f encryption function, can try different keys
May only need to know form of response; attacker can tell if guess correct by looking to see if deciphered object is of right form
Example: Kerberos Version 4 used DES, but keys had 20 bits of randomness; Purdue attackers guessed keys quickly because deciphered tickets had a fixed set of bits in some locations

## Segment 40

Info-Sec 2023
40
Encrypted Key Exchange *
Defeats off-line dictionary attacks
Idea: random challenges enciphered, so attacker cannot verify correct decipherment of challenge
Assume Alice, Bob share secret password s
In what follows, Alice needs to generate a random public key p and a corresponding private key q
Also, k is a randomly generated session key, and RA and RB are random challenges

## Segment 41

Info-Sec 2023
41
EKE Protocol *
Now Alice, Bob share a randomly generated
secret session key k

## Segment 42

Part 2 ⎯ Access Control                                                                                                  42
Something You Have
Something in your possession
Examples include following…
Car key
Laptop computer (or MAC address)
Password generator (next)
ATM card, smartcard, etc.

## Segment 43

Info-Sec 2023
43
Hardware Support
Token-based authentication
Used to compute response to challenge
May encipher or hash challenge
May require PIN from user
Object user possesses to authenticate, e.g.
memory card (magnetic stripe)
smartcard
Temporally-based
Every minute (or so) different number shown
Computer knows what number to expect when
User enters number and fixed password

## Segment 44

Memory Card
store but do not process data
magnetic stripe card, e.g. bank card
electronic memory card
used alone for physical access (e.g., hotel rooms)
some with password/PIN (e.g., ATMs)
Drawbacks of memory cards include:
need special reader
loss of token issues
user dissatisfaction (OK for ATM, not OK for computer access)

## Segment 45

Smartcard
credit-card like 
has own processor, memory, I/O ports
ROM, EEPROM, RAM memory
executes protocol to authenticate with reader/computer
static: similar to memory cards
dynamic: passwords created every minute; entered manually by user or electronically
challenge-response: computer creates a random number; smart card provides its hash (similar to PK)
also have USB dongles

## Segment 45

### Slide Image
## Markdown Notes: Smartcard Dimensions & Chip Layout

Here's a breakdown of the slide image in markdown format:

**Title:** Smartcard Dimensions

**Key Information:**

*   **Dimensions:**
    *   Width: 85.6 mm
    *   Height: 54 mm
*   **Standard:** Conforms to ISO standard 7816-2
*   **Chip Embedding:** The smartcard chip is embedded *within* the plastic card body and is not visible externally.

**Typical Chip Layout (Internal):**

*   **RAM:** Random Access Memory
*   **EEPROM:** Electrically Erasable Programmable Read-Only Memory (for storage)
*   **CPU:** Central Processing Unit (the "brain" of the card)
*   **Crypto Coprocessor:** Dedicated hardware for cryptographic operations (encryption, decryption, digital signatures, etc.)

**Notes:**

*   These dimensions are standard for most smartcards (credit cards, ID cards, SIM cards, etc.).
*   The chip's internal components work together to securely store and process data.
*   The crypto coprocessor is crucial for security applications.
*   The diagram shows a simplified representation of the chip layout. Actual chip designs can vary.

## Segment 46

Electronic identity cards *
An important application of smart cards
A national e-identity (eID)
Serves the same purpose as other national ID cards (e.g., a driver’s licence)
Can provide stronger proof of identity
A German card
Personal data, Document number, Card access number (six digit random number), Machine readable zone (MRZ): the password
Uses: ePass (government use), eID (general use), eSign (can have private key and certificate)

## Segment 47

User authentication with eID *

## Segment 48

Part 2 ⎯ Access Control                                                                                                  48
Something You Are
Biometric
“You are your key” ⎯ Schneier
Are
Know
Have
Examples
Fingerprint
Handwritten signature
Facial recognition
Speech recognition
Gait (walking) recognition
“Digital doggie” (odor recognition)
Many more!

## Segment 49

Part 2 ⎯ Access Control                                                                                                  49
Why Biometrics?
May be better than passwords
But, cheap and reliable biometrics needed
Today, an active area of research
Biometrics are used in security today
Thumbprint mouse
Palm print for secure entry
Fingerprint to unlock car door, etc.
But biometrics not really that popular
Has not lived up to its promise/hype (yet?)

## Segment 50

Info-Sec 2023
50
Biometrics: core idea
Automated measurement of biological, behavioral features that identify a person
Fingerprints: optical or electrical techniques
Maps fingerprint into a graph, then compares with database
Measurements imprecise, so approximate matching algorithms used
Voices: speaker verification or recognition
Verification: uses statistical techniques to test hypothesis that speaker is who is claimed (speaker dependent)
Recognition: checks content of answers (speaker independent)

## Segment 51

Part 2 ⎯ Access Control                                                                                                  51
Fingerprint: Enrollment
Capture image of fingerprint
Enhance image
Identify “points”

## Segment 52

Part 2 ⎯ Access Control                                                                                                  52
Fingerprint: Recognition
Extracted points are compared with information stored in a database
Is it a statistical match?
Aside: Do identical twins’ fingerprints differ?

## Segment 53

Info-Sec 2023
53
Other Characteristics
Can use several other characteristics
Eyes: patterns in irises unique
Measure patterns, determine if differences are random; or correlate images using statistical tests
Faces: image, or specific characteristics like distance from nose to chin
Lighting, view of face, other noise can hinder this
Keystroke dynamics: believed to be unique
Keystroke intervals, pressure, duration of stroke, where key is struck
Statistical tests used

## Segment 54

Authenticate user based on one of their physical characteristics:
facial
fingerprint
hand geometry
retina pattern
iris
signature
voice
Biometric authentication

## Segment 54

### Slide Image
Here's a description of the slide image and its conversion to markdown notes:

**Image Description:**

The slide presents a 2x2 scatter plot illustrating the relationship between the cost and accuracy of various biometric characteristics used in user authentication schemes. 

*   **X-axis:** Represents Accuracy (increasing from left to right).
*   **Y-axis:** Represents Cost (increasing from bottom to top).
*   **Data Points:** Several biometric methods are plotted on the graph, positioned based on their relative cost and accuracy:
    *   **Low Accuracy, Low Cost:** Voice, Face, Signature, Hand
    *   **High Accuracy, High Cost:** Iris
    *   **Medium Accuracy, Medium Cost:** Finger, Retina

The slide is titled "Figure 3.6 Cost versus accuracy of various biometric characteristics in user authentication schemes."

---

**Markdown Notes:**

```markdown
## Biometric Authentication: Cost vs. Accuracy

**Key Concept:**  There's a trade-off between the cost of implementing a biometric system and its accuracy.

**Graph Overview:**
*   X-axis: Accuracy (Low to High)
*   Y-axis: Cost (Low to High)

**Biometric Methods & Positioning:**

*   **Low Cost, Low Accuracy:**
    *   Voice Recognition
    *   Facial Recognition
    *   Signature Verification
    *   Hand Geometry
*   **Medium Cost, Medium Accuracy:**
    *   Fingerprint Scanning (Finger)
    *   Retinal Scanning (Retina)
*   **High Cost, High Accuracy:**
    *   Iris Scanning (Iris)

**Implications:**

*   Choosing a biometric method requires balancing security needs with budget constraints.
*   Higher accuracy generally comes at a higher cost (hardware, software, maintenance).
*   Less expensive methods may be suitable for lower-security applications.
```

**Note:**  The markdown is formatted for readability and to highlight the key takeaways from the slide.  You can adjust the formatting (e.g., using bullet points, numbered lists, or different headings) to suit your specific needs.

## Segment 55

Operation of a biometricsystem
Verification is analogous to user login via a smart card and a PIN

Identification is biometric info but no IDs; system compares with stored templates

## Segment 55

### Slide Image
Okay, here's a markdown representation of the information presented in the image, broken down into notes.

---

## Generic Biometric System

**Overview:** The image illustrates a generic biometric system and its three main stages: Enrollment, Verification, and Identification.  The system aims to create an association between a user and their unique biometric characteristics.

### 1. Enrollment (a)

*   **Process:**  Initial setup where the system learns a user's biometric data.
*   **Steps:**
    1.  **User Interface:** User interacts (e.g., enters name/PIN and presents biometric data - fingerprint in this example).
    2.  **Biometric Sensor:** Captures the biometric data (fingerprint scan).
    3.  **Feature Extractor:**  Analyzes the biometric data and extracts unique features.
    4.  **Database:** Stores the extracted features as a "template".
*   **Outcome:** Creates a user profile linked to their biometric template.

### 2. Verification (b)

*   **Process:**  Confirms if the user is who they claim to be. (1:1 matching)
*   **Steps:**
    1.  **User Interface:** User claims an identity (e.g., enters name/PIN) and presents biometric data.
    2.  **Biometric Sensor:** Captures the biometric data.
    3.  **Feature Extractor:** Extracts features from the presented biometric data.
    4.  **Feature Matcher:** Compares the extracted features to the *single* template stored for the claimed identity.
    5.  **Output:** Returns a "true" (match) or "false" (no match) result.
*   **Key Point:** Requires the user to identify themselves *first* (e.g., with a username/PIN).

### 3. Identification (c)

*   **Process:**  Determines *who* the user is. (1:N matching)
*   **Steps:**
    1.  **User Interface:** User presents biometric data without claiming an identity.
    2.  **Biometric Sensor:** Captures the biometric data.
    3.  **Feature Extractor:** Extracts features from the presented biometric data.
    4.  **Feature Matcher:** Compares the extracted features to *all* templates stored in the database (N templates).
    5.  **Output:** Returns the user's identity if a match is found, or "user unidentified" if no match is found.
*   **Key Point:** Does *not* require the user to claim an identity beforehand.  The system attempts to find a match within its database.

**Database:**

*   Stores biometric templates.
*   The number of templates varies depending on the system and the number of enrolled users.

**Caption Summary:**

*   Enrollment creates the association between user and biometric characteristics.
*   Authentication can be either verifying a claimed user or identifying an unknown user.

---

I hope this markdown representation is helpful!  Let me know if you'd like any part of it expanded or clarified.

## Segment 56

Biometric Accuracy *
Palm print The system generates a matching score (a number) that quantifies similarity between the input and the stored template
Concerns: sensor noise and detection inaccuracy
Problems of false match/false non-match
* Further reading (Stallings textbook)

## Segment 56

### Slide Image
Here's a description of the slide image, followed by a markdown conversion of the key information into notes:

**Image Description:**

The image is a graph illustrating the probability density functions of matching scores for a biometric system, comparing a genuine user and an imposter.  The x-axis represents the "Matching Score (s)", and the y-axis represents the "Probability Density Function".

Two bell-shaped curves are displayed:

*   **Imposter Profile (left):**  A curve representing the distribution of matching scores when an imposter attempts to gain access.  It's centered around a lower matching score ("average matching value of imposter").
*   **Genuine User Profile (right):** A curve representing the distribution of matching scores when a genuine user attempts to gain access. It's centered around a higher matching score ("average matching value of genuine user").

A vertical dashed line labeled "decision threshold (t)" separates the two curves.  The area under the curve to the *right* of the threshold is considered a "match".

The image highlights two types of errors:

*   **False Non-Match Possible:** The area under the genuine user profile curve to the *left* of the threshold. This represents a genuine user being incorrectly rejected.
*   **False Match Possible:** The area under the imposter profile curve to the *right* of the threshold. This represents an imposter being incorrectly accepted.

The area where the two curves overlap (shaded blue) represents the region where the system is most vulnerable to errors.

**Markdown Notes:**

```markdown
## Biometric Matching Score Distributions

**Concept:**  Biometric systems compare a presented feature to a reference feature, reducing the comparison to a single numeric "Matching Score".

**Key Components:**

*   **Matching Score (s):**  A numerical value representing the similarity between the presented and reference biometric data.
*   **Probability Density Function:**  Shows the likelihood of obtaining a particular matching score.
*   **Imposter Profile:** Distribution of matching scores when an unauthorized user attempts access.  Typically centered around *lower* scores.
*   **Genuine User Profile:** Distribution of matching scores when an authorized user attempts access. Typically centered around *higher* scores.
*   **Decision Threshold (t):**  A pre-defined value used to determine whether a match is declared.  If `s > t`, a match is accepted.

**Error Types:**

*   **False Non-Match (Type I Error):**  Genuine user is incorrectly rejected.  Occurs when the matching score falls *below* the threshold.
*   **False Match (Type II Error):** Imposter is incorrectly accepted. Occurs when the matching score falls *above* the threshold.

**Trade-off:**

*   Adjusting the decision threshold impacts the rates of false matches and false non-matches.  Lowering the threshold reduces false non-matches but increases false matches, and vice-versa.
```

**Important Considerations:**

*   The goal of a biometric system is to minimize both types of errors.
*   The optimal decision threshold depends on the specific application and the relative costs of false matches vs. false non-matches.
*   The curves shown are idealized representations; real-world distributions can be more complex.

## Segment 57

Biometric Accuracy *
Can plot characteristic curve (2,000,000 comparisons)
Pick threshold balancing error rates

## Segment 57

### Slide Image
Here's a description of the slide image and its conversion to markdown notes:

**Image Description:**

The image is a graph displaying Receiver Operating Characteristic (ROC) curves for five different biometric identification systems: Face, Fingerprint, Voice, Hand Geometry, and Iris.  The x-axis represents the "False Match Rate" (FMR), and the y-axis represents the "False Non-Match Rate" (FNMR).  The graph uses a logarithmic scale for both axes to better visualize the performance differences, especially at low error rates. Each biometric system is represented by a different line style and marker.  The curves generally trend downwards from top-left to bottom-right, indicating that as the FMR decreases, the FNMR increases, and vice-versa.  The Iris system demonstrates the best performance, with the lowest FMR and FNMR values.  The Voice system generally has the worst performance.

**Markdown Notes:**

```markdown
## Biometric System Performance - ROC Curves

**Overview:**

*   This graph shows the performance of five biometric systems using Receiver Operating Characteristic (ROC) curves.
*   ROC curves plot False Match Rate (FMR) vs. False Non-Match Rate (FNMR).
*   Logarithmic scale used on both axes to highlight differences at low error rates.

**Biometric Systems Compared:**

*   **Face:** (Dark Blue Circles) - Moderate performance, curves down but not as steeply as Iris or Fingerprint.
*   **Fingerprint:** (Light Blue Open Circles) - Good performance, generally better than Face and Hand Geometry.
*   **Voice:** (Green Squares) - Poorest performance, consistently higher FMR and FNMR.
*   **Hand Geometry:** (Black Diamonds) - Moderate performance, better than Voice but not as good as Fingerprint.
*   **Iris:** (Dark Blue Diamonds) - Best performance, lowest FMR and FNMR across the range.

**Key Observations:**

*   **Trade-off:**  There's an inherent trade-off between FMR and FNMR. Lowering one generally increases the other.
*   **Iris is Superior:** Iris recognition consistently outperforms other methods in terms of accuracy.
*   **Voice is Least Reliable:** Voice recognition is the least reliable, with higher error rates.
*   **System Selection:** The choice of biometric system depends on the specific application and the acceptable levels of FMR and FNMR.

**Source:**

*   Figure 3.10 from [MANS01] (as indicated in the image caption)
```

**Explanation of the Markdown:**

*   **Headers:**  Used to organize the notes.
*   **Bullet Points:**  Used for listing key information.
*   **Bold Text:**  Used to emphasize important terms and system names.
*   **Color/Marker Association:** I've included the color and marker used in the graph to help associate the notes with the visual representation.
*   **Observations:**  Summarizes the main takeaways from the graph.
*   **Source:**  Includes the source information from the image caption.

## Segment 58

Info-Sec 2023
58
Cautions
These can be fooled!
Assumes biometric device accurate in the environment it is being used in!
Transmission of data to validator is tamperproof, correct

## Segment 59

Part 2 ⎯ Access Control                                                                                                  59
Biometrics: The Bottom Line
Biometrics are hard to forge
But attacker could
Steal Alice’s thumb
Photocopy Bob’s fingerprint, eye, etc.
Subvert software, database, “trusted path” …
And how to revoke a “broken” biometric?
Biometrics are not foolproof
Biometric use is relatively limited today
That should change in the (near?) future

## Segment 60

Info-Sec 2023
60
Location – Just a brief
If you know where user is, validate identity by seeing if person is where the user is
Requires special-purpose hardware to locate user
GPS (global positioning system) device gives location signature of entity
Host uses LSS (location signature sensor) to get signature for entity

## Segment 61

Info-Sec 2023
61
Multiple Methods
Example: “where you are” also requires entity to have LSS and GPS, so also “what you have”
Can assign different methods to different tasks
As users perform more and more sensitive tasks, must authenticate in more and more ways (presumably, more stringently) File describes authentication required
Also includes controls on access (time of day, etc.), resources, and requests to change passwords

Pluggable Authentication Modules

## Segment 62

Info-Sec 2023
62
PAM
Idea: when program needs to authenticate, it checks central repository for methods to use
Library call: pam_authenticate
Accesses file with name of program in /etc/pam_d
Modules do authentication checking
sufficient: succeed if module succeeds
required: fail if module fails, but all required modules executed before reporting failure
requisite: like required, but don’t check all modules
optional: invoke only if all previous modules fail

## Segment 63

Info-Sec 2023
63
Example PAM File
auth	sufficient	/usr/lib/pam_ftp.so
auth	required	/usr/lib/pam_unix_auth.so use_first_pass
auth	required	/usr/lib/pam_listfile.so onerr=succeed \ 				item=user sense=deny file=/etc/ftpusers
For ftp:
If user “anonymous”, return okay; if not, set PAM_AUTHTOK to password, PAM_RUSER to name, and fail
Now check that password in PAM_AUTHTOK belongs to that of user in PAM_RUSER; if not, fail
Now see if user in PAM_RUSER named in /etc/ftpusers; if so, fail; if error or not found, succeed

## Segment 64

Extended Material *Kerberos authentication protocol
Material sources: History & some general info from Wiki;
Details on Kerberos versions 4&5 from Stallings Text and slides

## Segment 65

Info-Sec 2023
65
Kerberos
A computer network authentication protocol
which allows nodes communicating over a non-secure network to prove their identity to one another in a secure manner. 
aimed primarily at a client-server model, and it provides mutual authentication -- both the user and the server verify each other's identity. Messages are protected against eaves dropping & replay attacks.
Kerberos builds on SKC and requires a trusted third party, and optionally may use public-key cryptography during certain phases of authentication.

## Segment 66

Sep 2009
Information Security by Van K Nguyen Hanoi University of Technology
66
Kerberos
History [Wiki]
named after the character Kerberos (or Cerberus), the ferocious three-headed guard dog of Hades (from Greek mythology) 
MIT developed Kerberos in 1988 to protect network services provided by Project Athena. 
1st  version was primarily designed by Steve Miller and Clifford Neuman based on the earlier  Needham–Schroeder symmetric-key protocol. Ver 1 - 3 were experimental, internal.
Kerberos version 4, the first public version, was released on January 24, 1989.
Neuman and John Kohl published v5 in 1993 with the intention of overcoming existing limitations and security problems. Version 5 appeared as RFC 1510, which was then made obsolete by RFC 4120 in 2005. In 2005, the Internet Engineering Task Force (IETF) Kerberos working group updated specifications.

## Segment 67

Sep 2009
Information Security by Van K Nguyen Hanoi University of Technology
67
Idea
Ticket
Issuer vouches for identity of requester of service
Identifies sender
Key Distribution Center (KDC) combines two severs: 
Authentication Server, AS  (Also, Kerberos server)
Ticket Granting Server, TGS
User u authenticates to AS
Obtains ticket Tu,TGS for ticket granting service (TGS)
User u wants to use service s:
User sends authenticator Au, ticket Tu,TGS to TGS asking for ticket for service
TGS sends ticket Tu,s to user
User sends Au, Tu,s to server as request to use s

## Segment 68

Kerberos v4 Overview
a basic third-party authentication scheme
have an Authentication Server (AS) 
users initially negotiate with AS to identify self 
AS provides a non-corruptible authentication credential (ticket granting ticket TGT) 
have a Ticket Granting server (TGS)
users subsequently request access to other services from TGS on basis of users TGT
using a complex protocol using DES

## Segment 69

Kerberos 4 Overview

## Segment 69

### Slide Image
Okay, here's a description of the slide image, followed by a conversion to Markdown notes.

**Image Description:**

The image is a diagram illustrating the overview of the Kerberos authentication protocol. It depicts a user at a workstation interacting with three main components: the Authentication Server (AS), the Ticket-Granting Server (TGS), and a service server (represented as a server rack).  Arrows show the flow of messages and requests between these components.  The diagram is numbered 1-6, outlining the steps in the Kerberos process.  There are also annotations indicating how often certain steps occur (e.g., "once per user logon session", "once per type of service", "once per service session").  A database icon is shown next to the Authentication Server.

**Markdown Notes:**

```markdown
## Kerberos Overview

**Core Components:**

*   **Authentication Server (AS):**  Initial authentication point.  Uses a database to verify user credentials.
*   **Ticket-Granting Server (TGS):** Issues tickets for accessing specific services.
*   **Service Server:**  The actual service the user wants to access (e.g., file server, database server).
*   **Workstation/Client:** The user's computer.

**Process Flow:**

1.  **User Logon & Service Request:** User logs onto workstation and requests a service.
2.  **AS Authentication:**
    *   AS verifies user's access rights in its database.
    *   Creates a Ticket-Granting Ticket (TGT) and a session key.
    *   Encrypts TGT and session key using a key derived from the user's password.
    *   Sends TGT and session key to the workstation.
3.  **Workstation Decryption & TGS Request:**
    *   Workstation prompts user for password to decrypt the incoming message.
    *   Workstation sends a request to the TGS for a service ticket, including:
        *   TGT
        *   Authenticator (containing user's name, network address, and timestamp)
        *   Session Key
4.  **TGS Ticket Issuance:**
    *   TGS decrypts the TGT and verifies the request.
    *   Creates a service ticket for the requested server.
    *   Sends the service ticket and a new session key to the workstation.
5.  **Service Request:** Workstation sends the service ticket and authenticator to the service server.
6.  **Service Access:**
    *   Service server verifies the ticket and authenticator.
    *   Grants access to the service.
    *   (Optional) If mutual authentication is required, the server returns an authenticator.

**Frequency of Steps:**

*   Steps 1-2: Once per user logon session.
*   Steps 3-4: Once per type of service requested.
*   Steps 5-6: Once per service session.

**Key Concepts:**

*   **Tickets:** Encrypted credentials used to prove identity.
*   **Session Keys:**  Temporary keys used for secure communication.
*   **Authenticators:**  Time-sensitive proofs of identity.
*   **Encryption:**  Used to protect sensitive information during transmission.
```

**Important Notes about the Markdown:**

*   I've tried to capture the key information from the diagram in a concise and organized manner.
*   The Markdown uses headings, bullet points, and indentation to improve readability.
*   I've added some explanatory notes to clarify the purpose of each component and step.
*   This is a high-level overview; a deeper understanding of Kerberos requires more detailed knowledge of its cryptographic mechanisms.
*   The "Key Concepts" section highlights important terms related to Kerberos.

## Segment 70

Kerberos v4 Dialogue

## Segment 70

### Slide Image
Okay, let's break down the image depicting the Kerberos authentication process and convert it into markdown notes.

**Image Description:**

The image shows a sequence of message exchanges in three parts, illustrating the Kerberos authentication protocol.  Each part represents a distinct phase:

1.  **(a) Authentication Service Exchange:**  The client (C) requests a Ticket-Granting Ticket (TGT) from the Authentication Server (AS).
2.  **(b) Ticket-Granting Service Exchange:** The client (C) uses the TGT to request a service ticket from the Ticket-Granting Server (TGS).
3.  **(c) Client/Server Authentication Exchange:** The client (C) presents the service ticket and an authenticator to the server (V) to gain access to the service.

Each exchange is numbered and shows the messages sent and the encryption used.  The notation `||` represents concatenation of data elements.  `E(K, M)` denotes encryption of message `M` with key `K`.  `ID`, `TS`, `Lifetime`, `AD` represent the ID, Timestamp, Lifetime, and Address of the respective entities.

---

**Markdown Notes: Kerberos Authentication Protocol**

## Kerberos Authentication Protocol

Kerberos is a network authentication protocol that uses secret-key cryptography. It's designed to provide strong authentication for client/server applications.

### 1. Authentication Service Exchange (Obtain TGT)

*   **Goal:** Client (C) obtains a Ticket-Granting Ticket (TGT) from the Authentication Server (AS).
*   **Messages:**
    1.  `C -> AS: IDc || IDtgs || TS1`  (Client to AS: Client ID, TGS ID, Timestamp)
    2.  `AS -> C: E(Kc,tgs, [Kc,tgs || IDtgs || TS2 || Lifetime || TicketTGS])` (AS to Client: Encrypted with Client/TGS shared key. Contains TGS key, TGS ID, Timestamp, Lifetime, and the TGT)
*   **TGT (TicketTGS) Contents:**
    *   `TicketTGS = E(Ktgs, [Kc,tgs || IDc || ADc || IDtgs || TS2 || Lifetime])` (Encrypted with TGS key. Contains Client/TGS key, Client ID, Client Address, TGS ID, Timestamp, Lifetime)

### 2. Ticket-Granting Service Exchange (Obtain Service Ticket)

*   **Goal:** Client (C) obtains a service ticket from the Ticket-Granting Server (TGS).
*   **Messages:**
    1.  `C -> TGS: IDc || TicketTGS || AuthenticatorC` (Client to TGS: Client ID, TGT, Authenticator)
    2.  `TGS -> C: E(Kc,v, [Kc,v || IDv || TS4 || TicketV])` (TGS to Client: Encrypted with Client/Server shared key. Contains Server key, Server ID, Timestamp, and the Service Ticket)
*   **TicketV (Service Ticket) Contents:**
    *   `TicketV = E(Kv, [Kc,v || IDc || ADc || IDv || TS4 || Lifetime])` (Encrypted with Server key. Contains Client/Server key, Client ID, Client Address, Server ID, Timestamp, Lifetime)
*   **AuthenticatorC Contents:**
    *   `AuthenticatorC = E(Kc,tgs, [IDc || ADc || TS3])` (Encrypted with Client/TGS key. Contains Client ID, Client Address, Timestamp)

### 3. Client/Server Authentication Exchange (Obtain Service)

*   **Goal:** Client (C) authenticates to the Server (V) to access the service.
*   **Messages:**
    1.  `C -> V: TicketV || AuthenticatorC` (Client to Server: Service Ticket, Authenticator)
    2.  `V -> C: E(Kc,v, [TS5 + 1])` (Server to Client: Encrypted with Client/Server key. Contains Timestamp + 1.  This confirms the server received the authenticator and is responding.)
*   **TicketV (Service Ticket) Contents (Re-iterated for clarity):**
    *   `TicketV = E(Kv, [Kc,v || IDc || ADc || IDv || TS4 || Lifetime])`
*   **AuthenticatorC Contents (Re-iterated for clarity):**
    *   `AuthenticatorC = E(Kc,tgs, [IDc || ADc || TS3])`

**Key Concepts:**

*   **Encryption:**  Kerberos relies heavily on symmetric-key encryption.
*   **Tickets:**  Tickets are credentials that allow a client to access services without repeatedly providing their password.
*   **Authenticators:**  Authenticators are used to prove that the client is in possession of the ticket and is actively participating in the session.
*   **Timestamps:** Timestamps prevent replay attacks.
*   **Key Distribution Center (KDC):** The AS and TGS together form the KDC.

---

This markdown provides a structured overview of the Kerberos authentication process as depicted in the image.  It breaks down each exchange into its constituent messages and explains the purpose of the key components.  Let me know if you'd like any part of this elaborated further!

## Segment 71

Kerberos Version 5
developed in mid 1990’s
specified as Internet standard RFC 1510
provides improvements over v4
addresses environmental shortcomings
encryption alg, network protocol, byte order, ticket lifetime, authentication forwarding, interrealm auth
and technical deficiencies
double encryption, non-std mode of use, session keys, password attacks

## Segment 72

Kerberos Realms
a Kerberos environment consists of:
a Kerberos server
a number of clients, all registered with server
application servers, sharing keys with server
this is termed a realm
typically a single administrative domain
if have multiple realms, their Kerberos servers must share keys and trust

## Segment 73

Kerberos Realms

## Segment 73

### Slide Image
## Markdown Notes: Kerberos - Request for Service in Another Realm (Figure 14.2)

This diagram illustrates how a client in one Kerberos realm (Realm A) requests a service from a server in another realm (Realm B).

**Key Components:**

* **Client:**  A computer requesting a service. Located in Realm A.
* **Server:** A computer providing a service. Located in Realm B.
* **Realm A:**  Kerberos security domain. Contains:
    * **AS (Authentication Server):** Verifies client identity.
    * **TGS (Ticket Granting Server):** Issues tickets for services.
* **Realm B:** Kerberos security domain. Contains:
    * **AS (Authentication Server):** Verifies client identity.
    * **TGS (Ticket Granting Server):** Issues tickets for services.

**Steps (Numbered on Diagram):**

1. **Client -> Realm A TGS: Request Ticket for Local TGS:** The client requests a ticket to access its *own* realm's Ticket Granting Server (TGS).
2. **Realm A TGS -> Client: Ticket for Local TGS:** The Realm A TGS issues a ticket to the client, allowing it to authenticate with the TGS.
3. **Client -> Realm A TGS: Request Ticket for Remote TGS:** The client uses the ticket from step 2 to request a ticket for the *remote* realm's (Realm B) TGS.  This is a crucial step for cross-realm authentication.
4. **Realm A TGS -> Client: Ticket for Remote TGS:** The Realm A TGS issues a ticket to the client, allowing it to authenticate with the Realm B TGS.
5. **Client -> Realm B TGS: Request Ticket for Remote Server:** The client uses the ticket from step 4 to request a ticket for the specific service on the server in Realm B.
6. **Realm B TGS -> Client: Ticket for Remote Server:** The Realm B TGS issues a ticket to the client, allowing it to authenticate with the server.
7. **Client -> Server: Request Remote Service:** The client uses the ticket from step 6 to request the desired service from the server in Realm B.  The server verifies the ticket.

**Important Considerations:**

* **Trust Relationships:**  This process relies on a pre-established trust relationship between Realm A and Realm B.  The TGS in Realm A must be able to authenticate the TGS in Realm B.
* **Complexity:** Cross-realm authentication is more complex than single-realm authentication.
* **Security:** Kerberos provides strong authentication and protects against replay attacks.

## Segment 74

Protocol
[From Wiki]
Client Authentication to the AS
Client Service Authorization
Client Service Request

## Segment 74

### Slide Image
Okay, here's a description of the slide image, followed by a conversion to Markdown notes.

**Image Description:**

The image illustrates the Kerberos authentication protocol. It depicts a three-way exchange between a Client (C), an Authentication Server (AS), a Ticket-Granting Server (TGS), and a Service Server (SS).  The process is broken down into three phases:

1.  **Client Authentication to the AS:** The client requests authentication from the AS, providing its user ID and the requested service. The AS responds with a Ticket-Granting Ticket (TGT) encrypted with a key shared between the client and the TGS.
2.  **Client Service Authorization:** The client presents the TGT to the TGS, along with a request for a service ticket. The TGS verifies the TGT and issues a service ticket encrypted with a key shared between the client and the service server.
3.  **Client Service Request:** The client presents the service ticket to the service server, along with an authenticator. The service server verifies the ticket and authenticator, granting access to the requested service.

The image also shows the keys used in each exchange: `Kc` (Client-KDC), `KTGS` (KDC-TGS), and `Ks` (Client-Service Server).  The locks represent encryption, and the keys represent the encryption keys used.  Messages are labeled A through H.

---

**Markdown Notes:**

```markdown
## Kerberos Authentication Protocol

**Overview:** A network authentication protocol that uses secret-key cryptography to authenticate a user to multiple services without repeatedly entering credentials.

**Key Players:**

*   **Client (C):** The user or application requesting a service.
*   **Authentication Server (AS):**  Verifies the client's identity and issues a Ticket-Granting Ticket (TGT). Part of the Key Distribution Center (KDC).
*   **Ticket-Granting Server (TGS):** Issues service tickets based on the TGT. Part of the KDC.
*   **Service Server (SS):** Provides the requested service.
*   **Key Distribution Center (KDC):** Contains both the AS and TGS.

**Keys:**

*   `Kc`: Shared secret key between the Client and the KDC.
*   `KTGS`: Shared secret key between the KDC and the TGS.
*   `Ks`: Shared secret key between the Client and the Service Server.

---

### Phase 1: Client Authentication to the AS

1.  **Msg A (Client -> AS):** Client sends a request to the AS containing:
    *   User ID
    *   Requested Service
2.  **Msg B (AS -> Client):** AS responds with:
    *   Ticket-Granting Ticket (TGT) encrypted with `KTGS`.
    *   Session Key (`Kc-TGS`) encrypted with `Kc`.
    *   Client address and validity information.

---

### Phase 2: Client Service Authorization

1.  **Msg C (Client -> TGS):** Client sends a request to the TGS containing:
    *   TGT (obtained in Phase 1)
    *   Service ID
    *   Client address and validity information.
2.  **Msg D (TGS -> Client):** TGS responds with:
    *   Service Ticket encrypted with `Ks`.
    *   Session Key (`Kc-S`) encrypted with `Kc-TGS`.
    *   Client timestamp.
3.  **Msg E (Client -> SS):** Client sends a request to the Service Server containing:
    *   Service Ticket (obtained from TGS)
    *   Authenticator (timestamp encrypted with `Kc-S`)
4.  **Msg F (SS -> Client):** Service Server responds with a challenge.

---

### Phase 3: Client Service Request

1.  **Msg G (Client -> SS):** Client sends the authenticator (timestamp encrypted with `Kc-S`).
2.  **Msg H (SS -> Client):** Service Server grants access to the requested service.

**Security Considerations:**

*   Timestamps prevent replay attacks.
*   Encryption ensures confidentiality and integrity.
*   Tickets have limited validity periods.
```

**Important Notes:**

*   This is a simplified representation of Kerberos.  There are more details and nuances in the actual protocol.
*   The Markdown is formatted for readability. You can adjust the formatting as needed.
*   The image provides a visual aid to understanding the flow of messages and the encryption process.  Refer to the image while reading the notes for better comprehension.

## Segment 75

Kerberos v5 Dialogue

## Segment 75

### Slide Image
Okay, let's break down the image depicting the Kerberos authentication process and convert it into markdown notes.

## Kerberos Authentication Process - Markdown Notes

This outlines the three main phases of Kerberos authentication: Authentication Service Exchange, Ticket-Granting Service Exchange, and Client/Server Authentication Exchange.

---

### 1. Authentication Service Exchange (AS Exchange) - Obtaining a Ticket-Granting Ticket (TGT)

*   **Goal:** Client (C) authenticates to the Authentication Server (AS) and receives a Ticket-Granting Ticket (TGT).
*   **Messages:**
    *   **(1) C → AS:**  `Options || ID_C || Realm_C || ID_TGS || Times || Nonce_1`
        *   `Options`:  Authentication options requested.
        *   `ID_C`: Client's principal name.
        *   `Realm_C`: Client's realm.
        *   `ID_TGS`: Ticket-Granting Service's principal name.
        *   `Times`:  Timestamp.
        *   `Nonce_1`: Random nonce generated by the client.
    *   **(2) AS → C:** `Realm_C || ID_C || Ticket_TGS || E(K_c,tgs, [Times || Nonce_1 || Realm_C || ID_TGS || ID_C])`
        *   `Realm_C`: Client's realm.
        *   `ID_C`: Client's principal name.
        *   `Ticket_TGS`: The Ticket-Granting Ticket.
        *   `E(K_c,tgs, ...)`: Encrypted message using the client's secret key (`K_c,tgs`)
*   **Ticket_TGS Structure:** `E(K_tgs, [Flags || K_c,tgs || Realm_C || ID_C || AD_C || Times])`
    *   `K_tgs`: TGS's secret key.
    *   `Flags`: Ticket flags.
    *   `K_c,tgs`: Session key for communication between the client and TGS.
    *   `Realm_C`: Client's realm.
    *   `ID_C`: Client's principal name.
    *   `AD_C`: Client's addresses (optional).
    *   `Times`: Ticket validity period.

---

### 2. Ticket-Granting Service Exchange (TGS Exchange) - Obtaining a Service-Granting Ticket

*   **Goal:** Client (C) presents the TGT to the Ticket-Granting Service (TGS) and requests a service-granting ticket for a specific server.
*   **Messages:**
    *   **(3) C → TGS:** `Options || ID_C || Times || Nonce_2 || Ticket_TGS || Authenticator_C`
        *   `Options`: Authentication options.
        *   `ID_C`: Client's principal name.
        *   `Times`: Timestamp.
        *   `Nonce_2`: Random nonce generated by the client.
        *   `Ticket_TGS`: The TGT obtained from the AS.
        *   `Authenticator_C`: Proof of possession of the client's key.
    *   **(4) TGS → C:** `Realm_C || ID_C || Ticket_V || E(K_c,v, [Times || Nonce_2 || Realm_C || ID_C])`
        *   `Realm_C`: Client's realm.
        *   `ID_C`: Client's principal name.
        *   `Ticket_V`: The Service-Granting Ticket.
        *   `E(K_c,v, ...)`: Encrypted message using the client's secret key (`K_c,v`)
*   **Ticket_TGS Structure (same as above):** `E(K_tgs, [Flags || K_c,tgs || Realm_C || ID_C || AD_C || Times])`
*   **Ticket_V Structure:** `E(K_v, [Flags || K_c,v || Realm_C || ID_C || AD_C || Times])`
    *   `K_v`: Server's secret key.
    *   `Flags`: Ticket flags.
    *   `K_c,v`: Session key for communication between the client and server.
    *   `Realm_C`: Client's realm.
    *   `ID_C`: Client's principal name.
    *   `AD_C`: Client's addresses (optional).
    *   `Times`: Ticket validity period.
*   **Authenticator_C Structure:** `E(K_c,tgs, [ID_C || Realm_C || TS_1])`
    *   `K_c,tgs`: Session key from TGT.
    *   `ID_C`: Client's principal name.
    *   `Realm_C`: Client's realm.
    *   `TS_1`: Timestamp.

---

### 3. Client/Server Authentication Exchange - Obtaining Service

*   **Goal:** Client (C) authenticates to the Server (V) using the service-granting ticket.
*   **Messages:**
    *   **(5) C → V:** `Options || Ticket_V || Authenticator_C`
        *   `Options`: Authentication options.
        *   `Ticket_V`: The Service-Granting Ticket obtained from the TGS.
        *   `Authenticator_C`: Proof of possession of the client's key.
    *   **(6) V → C:** `E(K_c,v, [TS_2 || Subkey || Seq#])`
        *   `E(K_c,v, ...)`: Encrypted message using the session key (`K_c,v`).
        *   `TS_2`: Timestamp.
        *   `Subkey`: Subsession key (optional).
        *   `Seq#`: Sequence number.
*   **Ticket_V Structure (same as above):** `E(K_v, [Flags || K_c,v || Realm_C || ID_C || AD_C || Times])`
*   **Authenticator_C Structure:** `E(K_c,v, [ID_C || Realm_C || TS_1 || Subkey || Seq#])`
    *   `K_c,v`: Session key from Ticket_V.
    *   `ID_C`: Client's principal name.
    *   `Realm_C`: Client's realm.
    *   `TS_1`: Timestamp.
    *   `Subkey`: Subsession key (optional).
    *   `Seq#`: Sequence number.

---

**Key Concepts:**

*   **Encryption:**  Kerberos relies heavily on symmetric-key encryption.
*   **Tickets:**  Tickets are credentials that allow a client to prove its identity to a service.
*   **Authenticators:**  Authenticators are used to prove that the client possesses the key associated with a ticket.
*   **Timestamps & Nonces:** Used to prevent replay attacks.
*   **Session Keys:**  Temporary keys established for secure communication.
*   **Realms:**  Administrative domains within Kerberos.

---

This markdown provides a detailed breakdown of the Kerberos authentication process as depicted in the image.  It should be a useful reference for understanding the flow of messages and the purpose of each component.  Let me know if you'd like any part of this elaborated further!

## Segment 76

Federated Identity Management
use of common identity management scheme
across multiple enterprises & numerous applications 
supporting many thousands, even millions of users 
principal elements are:
authentication, authorization, accounting, provisioning, workflow automation, delegated administration, password synchronization, self-service password reset, federation
Kerberos contains many of these elements

## Segment 77

Identity Management

## Segment 77

### Slide Image
Here's a description of the slide image and its conversion to markdown notes:

**Image Description:**

The image depicts a "Generic Identity Management Architecture" as a diagram. It shows the interaction between several components:

*   **Principals:** Represented by oval shapes, these are the entities (users, systems) that need to be identified and authenticated. They provide attributes.
*   **Attribute Service:** Two instances of this component are shown, receiving attributes from the Principals and providing them to Administrators.
*   **Administrators:** Represented by rounded rectangles, they receive attributes from the Attribute Service.
*   **Identity Provider:** A central teal-colored box containing four sub-components:
    *   Identity Control Interface
    *   Principal Authentication
    *   Attribute Locator
    *   Identifier Translation
*   **Data Consumers:** Represented by rounded rectangles, they request attribute data and receive identifiers/attribute references from the Identity Provider.

Arrows indicate the flow of information and interactions between these components. The diagram illustrates how principals authenticate, provide attributes, and how data consumers obtain information about them through the Identity Provider and Attribute Services.

---

**Markdown Notes:**

```markdown
## Generic Identity Management Architecture

**Overview:** This diagram illustrates a common architecture for managing digital identities.

**Key Components:**

*   **Principals:**
    *   Entities needing identification (users, systems).
    *   Provide attributes about themselves.
    *   Authenticate and manage their identity elements.
*   **Attribute Service:**
    *   Receives attributes from Principals.
    *   Provides attributes to Administrators.
*   **Administrators:**
    *   Receive attributes from the Attribute Service.
*   **Identity Provider (IdP):**  Central component for identity management.
    *   **Sub-Components:**
        *   *Identity Control Interface:*  Manages access control policies.
        *   *Principal Authentication:* Verifies the identity of Principals.
        *   *Attribute Locator:*  Finds relevant attributes.
        *   *Identifier Translation:*  Maps identifiers between different systems.
*   **Data Consumers:**
    *   Request attribute data.
    *   Receive identifiers and attribute references from the IdP.

**Data Flow:**

1.  Principals provide attributes to the Attribute Service.
2.  Administrators receive attributes from the Attribute Service.
3.  Data Consumers request information from the Identity Provider.
4.  Identity Provider provides identifiers and attribute references to Data Consumers.

**Purpose:**  Facilitates secure and reliable identity management, enabling access control and data sharing.
```

**Note:**  I've tried to capture the essence of the diagram in a structured markdown format.  You can adjust the level of detail and organization to suit your specific needs.

## Segment 78

Identity Federation

## Segment 78

### Slide Image
## Slide Description:

The image depicts a diagram illustrating a typical flow for identity and access management, likely using a protocol like SAML or OAuth. It shows four key components: a **User** with a computer, an **Identity Provider** (source domain) server, an **Administrator** with a computer, and a **Service Provider** (destination domain) server.  Arrows indicate the flow of information between these components.  Numbered callouts explain each step in the process.

## Markdown Notes:

### Identity & Access Management Flow

**Components:**

*   **User:** Initiates access request.
*   **Identity Provider (IdP):**  Authenticates the user and provides identity information. (Source Domain)
*   **Administrator:** Manages user attributes and roles.
*   **Service Provider (SP):**  Hosts the resource the user wants to access. (Destination Domain)

**Flow:**

1.  **Authentication Request:** User's browser/application initiates an authentication dialogue with the Identity Provider. User provides identity information.
2.  **Attribute Provisioning:** Administrator provides attributes (e.g., roles) associated with the user's identity to the Identity Provider.
3.  **Identity & Attribute Request:** Service Provider requests identity information, authentication data, and attributes from the Identity Provider.
4.  **Access Grant/Denial:** Service Provider establishes a session with the user and enforces access control based on the user's identity and attributes.

**Key Concepts:**

*   **Source Domain:** Where the user's identity is managed (IdP).
*   **Destination Domain:** Where the resource is located (SP).
*   **Attributes:**  Information about the user (e.g., role, department) used for access control.
*   **Trust Relationship:**  The IdP and SP must have a pre-established trust relationship.

## Segment 79

Standards Used
Security Assertion Markup Language (SAML)
XML-based language for exchange of security information between online business partners
part of OASIS (Organization for the Advancement of Structured Information Standards) standards for federated identity management
e.g. WS-Federation for browser-based federation
need a few mature industry standards

## Segment 80

Federated Identity Examples

## Segment 80

### Slide Image
Here's a description of the slide image and its conversion to markdown notes:

**Image Description:**

The image depicts three different scenarios of Federated Identity.  Each scenario is represented by a diagram showing the flow of authentication and data between different web applications and user stores.  The title of the image is "Figure 22.6 Federated Identity Scenarios".

*   **(a) Federation based on account linking:**  An end-user authenticates with `Workplace.com` (employee portal). This portal links to health benefits.  The user's information (Name, ID) is shared with `Health.com`. Both `Workplace.com` and `Health.com` have their own user stores containing the same user data.
*   **(b) Federation based on roles:** An end-user authenticates with `Workplace.com` (employee portal) which links to parts supplier.  The user's information (Name, ID, Dept) is shared with `PartsSupplier.com`. `PartsSupplier.com` displays different content ("Welcome Joe", Technical docs, Troubleshooting") based on the user's role (Engineer, Purchaser) which is stored in the `User store` of `PartsSupplier.com`.
*   **(c) Chained Web Services:** An end-user authenticates with `Workplace.com` (Procurement application). This application sends a SOAP message to `PinSupplies.com` (Purchasing Web service). `PinSupplies.com` then sends another SOAP message to `E-Ship.com` (Shipping Web service).

---

**Markdown Notes:**

```markdown
## Federated Identity Scenarios (Figure 22.6)

This slide illustrates three different approaches to Federated Identity.

### 1. Federation based on Account Linking

*   **Scenario:** Sharing user account information between applications.
*   **Flow:**
    1.  End-user authenticates with `Workplace.com` (employee portal).
    2.  `Workplace.com` shares user data (Name, ID) with `Health.com`.
    3.  Both `Workplace.com` and `Health.com` maintain their own user stores with the same user information.
*   **Use Case:**  Providing access to benefits or other services based on existing employee accounts.

### 2. Federation based on Roles

*   **Scenario:**  Sharing user roles to control access and content.
*   **Flow:**
    1.  End-user authenticates with `Workplace.com` (employee portal).
    2.  `Workplace.com` shares user data (Name, ID, Dept) with `PartsSupplier.com`.
    3.  `PartsSupplier.com` uses the user's role (Engineer, Purchaser) to determine what content to display.
    4.  `PartsSupplier.com` maintains a user store with role information.
*   **Use Case:**  Providing role-based access to different features or information within a partner application.

### 3. Chained Web Services

*   **Scenario:**  Passing authentication context between web services.
*   **Flow:**
    1.  End-user authenticates with `Workplace.com` (Procurement application).
    2.  `Workplace.com` sends a SOAP message to `PinSupplies.com` (Purchasing Web service).
    3.  `PinSupplies.com` sends a SOAP message to `E-Ship.com` (Shipping Web service).
*   **Use Case:** Automating processes across multiple services while maintaining user context.
```

**Key takeaways from the image:**

*   Federated Identity allows users to access multiple applications with a single set of credentials.
*   Different federation approaches can be used depending on the specific requirements.
*   Account linking focuses on sharing user data.
*   Role-based federation focuses on sharing user roles.
*   Chained web services focus on passing authentication context between services.

## Segment 81

FIM vs. SSO
SSO: Single Sign-On
Allows users to access multiple web applications at once, using just one set of credentials. 
Beyond the workforce, companies can utilize SSO to help customers access various sections of one account. 
FIM 
As a tool, SSO fits within the broader model of FIM.
The key difference between SSO and FIM is while SSO is designed to authenticate a single credential across various systems within one organization, federated identity management systems offer single access to a number of applications across various enterprises.

## Segment 82

Extended Material *Biometrics
Slides borrowed from Mark Stamp’s web
https://www.cs.sjsu.edu/~stamp/infosec/powerpoint/

## Segment 83

Part 2 ⎯ Access Control                                                                                                  83
Something You Are
Biometric
“You are your key” ⎯ Schneier
Are
Know
Have
Examples
Fingerprint
Handwritten signature
Facial recognition
Speech recognition
Gait (walking) recognition
“Digital doggie” (odor recognition)
Many more!

## Segment 84

Part 2 ⎯ Access Control                                                                                                  84
Ideal Biometric
Universal ⎯ applies to (almost) everyone
In reality, no biometric applies to everyone
Distinguishing ⎯ distinguish with certainty
In reality, cannot hope for 100% certainty
Permanent ⎯ physical characteristic being measured never changes
In reality, OK if it to remains valid for long time
Collectable ⎯ easy to collect required data 
Depends on whether subjects are cooperative
Also, safe, user-friendly, and ???

## Segment 85

Part 2 ⎯ Access Control                                                                                                  85
Identification vs Authentication
Identification ⎯ Who goes there?
Compare one-to-many
Example: FBI fingerprint database
Authentication ⎯ Are you who you say you are?
Compare one-to-one
Example: Thumbprint mouse
Identification problem is more difficult
More “random” matches since more comparisons
We are (mostly) interested in authentication

## Segment 86

Part 2 ⎯ Access Control                                                                                                  86
Enrollment vs Recognition
Enrollment phase
Subject’s biometric info put into database
Must carefully measure the required info
OK if slow and repeated measurement needed
Must be very precise
May be a weak point in real-world use
Recognition phase
Biometric detection, when used in practice
Must be quick and simple
But must be reasonably accurate

## Segment 87

Part 2 ⎯ Access Control                                                                                                  87
Cooperative Subjects?
Authentication ⎯ cooperative subjects
Identification ⎯ uncooperative subjects
For example, facial recognition
Used in Las Vegas casinos to detect known cheaters (also, terrorists in airports, etc.)
Often, less than ideal enrollment conditions
Subject will try to confuse recognition phase
Cooperative subject makes it much easier
We are focused on authentication
So, we can assume subjects are cooperative

## Segment 88

Part 2 ⎯ Access Control                                                                                                  88
Biometric Errors
Fraud rate versus insult rate
Fraud ⎯ Trudy mis-authenticated as Alice
Insult ⎯ Alice not authenticated as Alice
For any biometric, can decrease fraud or insult, but other one will increase
For example
99% voiceprint match ⇒ low fraud, high insult
30% voiceprint match ⇒ high fraud, low insult
Equal error rate: rate where fraud == insult
A way to compare different biometrics

## Segment 89

Part 2 ⎯ Access Control                                                                                                  89
Fingerprint History
1823 ⎯ Professor Johannes Evangelist Purkinje discussed 9 fingerprint patterns 
1856 ⎯ Sir William Hershel used fingerprint (in India) on contracts
1880 ⎯ Dr. Henry Faulds article in Nature about fingerprints for ID
1883 ⎯ Mark Twain’s Life on the Mississippi (murderer ID’ed by fingerprint)

## Segment 90

Part 2 ⎯ Access Control                                                                                                  90
Fingerprint History
1888 ⎯ Sir Francis Galton developed classification system
His system  of “minutia” can be used today
Also verified that fingerprints do not change
Some countries require fixed number of “points” (minutia) to match in criminal cases
In Britain, at least 15 points 
In US, no fixed number of points

## Segment 91

Part 2 ⎯ Access Control                                                                                                  91
Fingerprint Comparison
Loop (double)
Whorl
Arch
Examples of loops, whorls, and arches
Minutia extracted from these features

## Segment 91

### Slide Image
Here's a description of the image and its conversion to markdown notes:

**Image Description:**

The image is a close-up, black and white photograph of a fingerprint. The fingerprint pattern is a clear **whorl** pattern, characterized by circular or spiral ridges. The ridges and valleys are distinctly visible, showing the unique details of the fingerprint. There are some areas of light reflection or slight imperfections in the image, but the overall pattern is well-defined.

---

**Markdown Notes:**

## Fingerprints - Whorl Pattern

*   **What are fingerprints?** Unique patterns of ridges and valleys on the surface of fingertips.
*   **Why are they unique?** Formed during fetal development, influenced by genetic and environmental factors.
*   **Main Fingerprint Patterns:**
    *   **Loops:** Ridges enter and exit on the same side.
    *   **Whorls:** Circular or spiral patterns. (As seen in the image)
    *   **Arches:** Ridges enter on one side and exit on the other, forming a wave-like pattern.
*   **Whorl Characteristics:**
    *   Circular or spiral shape.
    *   Often have a central point.
    *   Can be plain whorls, central pocket loop whorls, double loop whorls, or accidental whorls.
*   **Uses of Fingerprints:**
    *   Identification (forensics, security)
    *   Personal identification
    *   Criminal investigations
*   **Minutiae:**  The specific points where ridges end or split, used for detailed fingerprint analysis. (Not visible in this image, but important to note)

---

**Note:** This markdown provides a basic overview.  You could expand on any of these points with more detail depending on the context of the slide.

## Segment 91

### Slide Image
Here's a description of the image and its conversion to markdown notes:

**Image Description:**

The image is a close-up, black and white photograph of a fingerprint. The dominant feature is a clear, circular whorl pattern in the center.  Ridges and valleys of the fingerprint radiate outwards from this central whorl. The ridges are dark, and the valleys are light, creating a high-contrast image. The overall impression is a detailed and textured representation of a fingerprint.

---

**Markdown Notes:**

```markdown
## Fingerprint Analysis - Whorl Pattern

**Image:** Close-up of a fingerprint showing a whorl pattern.

**Key Features:**

*   **Whorl:**  Circular or spiral pattern.  This is the dominant pattern in the image.
*   **Ridges:** Dark lines representing the raised portions of the skin.
*   **Valleys:** Light spaces between the ridges.
*   **Core:** The central point of the whorl.
*   **High Contrast:**  Clear distinction between ridges and valleys.

**Whorl Pattern Characteristics:**

*   One or more complete circuits.
*   Can be spiral, circular, or oval in shape.
*   Relatively common pattern type (approximately 30-35% of fingerprints).

**Significance:**

*   Unique to each individual.
*   Used for identification and forensic science.
*   Pattern type is a primary classification characteristic.
```

**Note:**  This markdown provides a basic overview.  More detailed notes could include information about minutiae (ridge endings, bifurcations), delta points, and the different types of whorls (plain, central pocket loop, double loop, accidental).

## Segment 91

### Slide Image
Here's a description of the slide image and its conversion to markdown notes:

**Image Description:**

The image is a close-up, black and white photograph of a fingerprint. The fingerprint exhibits a clear **arch pattern**. The ridges run from one side of the print to the other, forming a wave-like shape with a rising arch in the center. There are no deltas or cores visible in this section of the print. The ridges are generally consistent in thickness and spacing, though some minor distortions are present.

---

**Markdown Notes:**

## Fingerprint Analysis - Arch Pattern

*   **Pattern Type:** Arch
*   **Characteristics:**
    *   Ridges enter on one side and exit on the other.
    *   Form a wave-like or rising arch shape.
    *   No deltas present.
    *   No cores present.
*   **Ridge Flow:** Consistent, generally parallel ridges.
*   **Rarity:** Least common fingerprint pattern (approx. 5% of population).
*   **Subcategories:** (Not visible in this image, but worth noting)
    *   Plain Arch
    *   Tented Arch

**Note:** This is a partial fingerprint. A full analysis would require examining the entire print for deltas, cores, and minutiae points.

## Segment 92

Part 2 ⎯ Access Control                                                                                                  92
Fingerprint: Enrollment
Capture image of fingerprint
Enhance image
Identify “points”

## Segment 93

Part 2 ⎯ Access Control                                                                                                  93
Fingerprint: Recognition
Extracted points are compared with information stored in a database
Is it a statistical match?
Aside: Do identical twins’ fingerprints differ?

## Segment 94

Part 2 ⎯ Access Control                                                                                                  94
Hand Geometry
A popular biometric
Measures shape of hand
Width of hand, fingers
Length of fingers, etc.
Human hands not so unique
Hand geometry sufficient for many situations
OK for authentication
Not useful for ID problem

## Segment 95

Part 2 ⎯ Access Control                                                                                                  95
Hand Geometry
Advantages
Quick ⎯ 1 minute for enrollment,           5 seconds for recognition
Hands are symmetric ⎯ so what?
Disadvantages
Cannot use on very young or very old
Relatively high equal error rate

## Segment 96

Part 2 ⎯ Access Control                                                                                                  96
Iris Patterns
Iris pattern development is “chaotic”
Little or no genetic influence
Even for identical twins, uncorrelated
Pattern is stable through lifetime

## Segment 96

### Slide Image
Here's a description of the slide image and its conversion to markdown notes:

**Image Description:**

The image is a close-up, cross-sectional view of a human eye. It shows the outer structures of the eye, including the sclera (white part), the iris (colored part), and the pupil (black center). The cornea (clear front covering) is also visible.  Labels are present pointing to specific parts:

*   **S:** Sclera
*   **I:** Iris
*   **C:** Cornea
*   **L:** (Likely) Lens - though partially obscured.

**Markdown Notes:**

```markdown
## Anatomy of the Human Eye - External Structures

**Overview:** This diagram illustrates the key external components of the human eye.

**Labeled Structures:**

*   **Sclera:**
    *   The white outer layer of the eye.
    *   Provides protection and shape.
*   **Iris:**
    *   The colored part of the eye.
    *   Controls the amount of light entering the eye by adjusting the size of the pupil.
*   **Cornea:**
    *   The clear, dome-shaped front surface of the eye.
    *   Helps to focus light.
*   **Lens:**
    *   Located behind the iris.
    *   Further focuses light onto the retina. (Partially visible in the image)

**Function:** These structures work together to allow us to see by focusing light and protecting the delicate internal parts of the eye.
```

**Additional Notes (Optional):**

*   You could add more detail about the function of each structure.
*   You could include information about common eye conditions affecting these parts.
*   You could add a section on how light travels through the eye.

## Segment 96

### Slide Image
Here's a description of the image and its conversion to markdown notes:

**Image Description:**

The image is a very close-up, detailed view of a human eye, specifically the iris. The iris is a striking blue color with intricate patterns of radial lines emanating from the central pupil. There are variations in the blue tone, with some areas appearing lighter and others darker, creating a textured look.  The pupil is a deep, solid black and perfectly circular. The surrounding sclera (white of the eye) is visible at the edges, showing a slight pinkish hue. The overall impression is one of incredible detail and complexity.

---

**Markdown Notes:**

## Human Iris - Detailed View

*   **Subject:** Close-up of a human eye, focusing on the iris.
*   **Color:** Predominantly blue, with variations in shade.
*   **Patterns:**
    *   Radial lines extending from the pupil.
    *   Complex, textured appearance.
*   **Pupil:**
    *   Deep black.
    *   Perfectly circular.
*   **Sclera:** Visible at edges, slightly pinkish.
*   **Overall Impression:** High level of detail, intricate structure.
*   **Possible Topics:**
    *   Anatomy of the eye
    *   Iris recognition
    *   Color variation in eyes
    *   Microscopic detail in biological structures.

---

I hope this is helpful! Let me know if you'd like me to refine the notes further or focus on a specific aspect of the image.

## Segment 96

### Slide Image
Here's a description of the image and its conversion to markdown notes:

**Image Description:**

The image is a close-up of a human eye. The eye appears to be slightly bloodshot, particularly in the sclera (white part of the eye) towards the corners. The iris is a mottled brown color with visible texture. A bright reflection is visible on the cornea. The skin around the eye shows some wrinkles and texture, suggesting the subject may be older. There's a slight drooping of the upper eyelid.

**Markdown Notes:**

```markdown
## Eye Examination Notes

**Date:** [Insert Date]
**Patient:** [Insert Patient Name/ID]

**Observation:** Close-up view of the right eye (assumed).

**Findings:**

*   **Sclera:** Mildly congested/bloodshot, particularly nasally and temporally.
*   **Iris:** Brown, mottled appearance with visible texture.
*   **Cornea:** Clear, with a bright specular reflection present.
*   **Eyelids:** Slight ptosis (drooping) of the upper eyelid. Skin around the eye shows signs of aging (wrinkles).
*   **Pupil:** Round, reactive to light (assumed, not directly visible in image).

**Possible Considerations:**

*   Conjunctival irritation (cause to be determined).
*   Normal age-related changes to the skin around the eye.
*   Assess for any pain, redness, or discharge reported by the patient.

**Next Steps:**

*   Full ophthalmic examination recommended.
*   Assess visual acuity.
*   Check intraocular pressure.
*   Evaluate for any other signs or symptoms.
```

**Important Considerations:**

*   This is based *solely* on the image. A proper diagnosis requires a full medical examination and patient history.
*   I've made some assumptions (e.g., right eye, pupil reactivity) that would need to be confirmed.
*   The "Possible Considerations" and "Next Steps" sections are suggestions for a medical professional.

## Segment 97

Part 2 ⎯ Access Control                                                                                                  97
Iris Recognition: History
1936 ⎯ suggested by ophthalmologist
1980s ⎯ James Bond film(s)
1986 ⎯ first patent appeared
1994 ⎯ John Daugman patents new-and-improved technique
Patents owned by Iridian Technologies

## Segment 98

Part 2 ⎯ Access Control                                                                                                  98
Iris Scan
Scanner locates iris
Take b/w photo
Use polar coordinates…
2-D wavelet transform
Get 256 byte iris code

## Segment 98

### Slide Image
Here's a description of the slide image and its conversion to markdown notes:

**Image Description:**

The image is a grayscale spectrogram-like plot. It appears to represent a two-dimensional array of data, likely representing signal intensity or frequency over time. 

*   **Axes:** The vertical axis is labeled with numerical values ranging from approximately 10 to 70. The horizontal axis is labeled with numerical values ranging from approximately 0 to 800.
*   **Intensity:** The intensity of the grayscale varies across the plot. Darker areas represent lower values, while lighter areas represent higher values.
*   **Pattern:** The plot exhibits a complex, textured pattern. There are vertical streaks and bands of varying intensity. The pattern seems to change over the horizontal axis, suggesting a dynamic process.  There's a general trend of increasing intensity (lighter shades) towards the right side of the plot.
*   **Overall Impression:** The image looks like a visualization of some kind of signal processing data, potentially audio, radar, or other time-series data.

**Markdown Notes:**

```markdown
## Spectrogram-like Plot Analysis

**Overview:**

*   Grayscale plot representing data intensity over two dimensions.
*   Likely a visualization of signal data (e.g., audio, radar, time-series).

**Axes:**

*   **Vertical Axis:** Values from ~10 to ~70 (units unclear).  Potentially frequency or a similar parameter.
*   **Horizontal Axis:** Values from ~0 to ~800 (units unclear).  Likely represents time or a similar sequential parameter.

**Intensity & Pattern:**

*   Darker shades = lower values.
*   Lighter shades = higher values.
*   Complex, textured pattern with vertical streaks and bands.
*   Intensity generally *increases* towards the right side of the plot.
*   Dynamic pattern suggests a changing signal over time.

**Possible Interpretations:**

*   Could be a spectrogram of an audio signal.
*   Could represent radar data showing signal returns.
*   Could be a visualization of a time-series with varying frequency components.

**Further Investigation:**

*   Determine the units of the axes.
*   Understand the data source and what the plot represents.
*   Analyze the specific patterns to identify key features or events.
```

**Important Considerations:**

*   Without context, it's difficult to definitively say what the plot represents. The markdown notes provide possible interpretations.
*   The units of the axes are unknown and would be crucial for a complete analysis.
*   The specific application of this plot would require additional information.

## Segment 98

### Slide Image
Here's a description of the slide image and its conversion to markdown notes:

**Image Description:**

The image shows a 3D surface plot, likely representing a function of two variables.  The plot has the following characteristics:

*   **Shape:** The surface has a central peak around x=20, y=20, reaching a maximum value of approximately 0.5.  It then dips down to negative values on either side, forming two "valleys" or depressions.
*   **Axes:** The x and y axes both range from 0 to 60. The z-axis (vertical) ranges from -0.5 to 1.
*   **Grid:** The surface is represented by a grid of lines, showing the function's behavior across the x-y plane.
*   **Appearance:** The plot is rendered in grayscale, with lines creating the surface.

**Markdown Notes:**

```markdown
## 3D Surface Plot Analysis

*   **Visualization:** Represents a function of two variables (f(x, y)).
*   **Domain:**  x ∈ [0, 60], y ∈ [0, 60]
*   **Range:** z ∈ [-0.5, 1]
*   **Key Features:**
    *   **Maximum:**  A prominent peak around (x=20, y=20) with a value of approximately z=0.5.
    *   **Minima/Valleys:** Two depressions/valleys on either side of the peak, with negative z-values.
    *   **Symmetry:** Appears to have some degree of symmetry around x=20 and y=20.
*   **Possible Function Type:**  Could represent a saddle point or a function with local maxima and minima.  Further analysis (equation) would be needed to determine the exact function.
*   **Potential Applications:**  This type of plot is used in various fields like:
    *   Optimization (finding maxima/minima)
    *   Data visualization
    *   Modeling physical phenomena
```

**Additional Notes (if context is known):**

If you have any context about *what* this function represents (e.g., a cost function, a probability distribution, a physical surface), you could add that to the markdown notes for more specific analysis.

## Segment 98

### Slide Image
Here's a description of the image and its conversion to markdown notes:

**Image Description:**

The image shows a close-up, thermal-like view of a human eye. The eye is centered in the frame, with the surrounding skin of the eyelid and face visible. The iris and pupil are clearly visible, appearing darker and more defined.  A bright reflection is visible in the pupil.  A cyan (blue-green) circle is drawn around the entire eye, and a smaller cyan crosshair is positioned directly over the pupil. The image has a color gradient, with warmer colors (yellow, orange, red) around the eye and cooler colors elsewhere.  The image also has coordinate axes along the sides, indicating pixel locations.

**Markdown Notes:**

```markdown
## Eye Image Analysis

**Image Overview:**

*   Close-up view of a human eye.
*   Appears to be a thermal or infrared-like image (color gradient suggests temperature differences).
*   Clear visibility of iris, pupil, and surrounding eyelid/facial skin.

**Key Features:**

*   **Pupil:** Darkest part of the eye, with a bright reflection.
*   **Iris:**  Visible surrounding the pupil.
*   **Eye Outline:**  Highlighted by a cyan circle.
*   **Pupil Center:** Marked with a cyan crosshair.
*   **Color Gradient:** Warmer colors (red, orange, yellow) around the eye, cooler elsewhere.
*   **Coordinate System:**  Axes present, indicating pixel locations.

**Possible Applications/Context:**

*   Biometric identification (iris scanning).
*   Eye tracking.
*   Medical imaging/diagnosis.
*   Image processing/computer vision research.
```

**Note:**  The "thermal-like" description is based on the color gradient. Without more information, it's difficult to definitively say if it's a true thermal image.

## Segment 98

### Slide Image
Here's a description of the slide image and its conversion to markdown notes:

**Image Description:**

The image shows a 3D surface plot. The plot appears to represent a function of two variables (x and y). 

*   **Axes:** The x and y axes range from 0 to 60. The z-axis (vertical) ranges from -1 to 1.
*   **Surface:** The surface has a complex shape with multiple peaks and valleys. There's a prominent central peak around x=30, y=30.  There are two smaller, darker depressions or valleys on either side of the central peak. The surface generally slopes downwards away from the central peak in all directions.
*   **Plot Type:** The plot is a wireframe surface plot, meaning it shows the structure of the surface using lines rather than filled areas.

**Markdown Notes:**

```markdown
## 3D Surface Plot Analysis

**Overview:**

*   Represents a function of two variables, f(x, y).
*   Wireframe surface plot.

**Axes Ranges:**

*   x-axis: 0 - 60
*   y-axis: 0 - 60
*   z-axis: -1 to 1

**Key Features:**

*   **Central Peak:**  Prominent peak located approximately at (30, 30).  Indicates a local maximum.
*   **Valleys/Depressions:** Two darker, lower areas (valleys) flanking the central peak.  Suggest local minima.
*   **General Trend:** Surface slopes downwards from the central peak in all directions.
*   **Complexity:** The surface is not simple; it has multiple features suggesting a complex function.

**Possible Interpretations (without knowing the function):**

*   Could represent a wave-like pattern with interference.
*   Might model a physical surface with varying heights.
*   Could be a visualization of a mathematical function with multiple critical points.
```

**Note:**  Without knowing the actual function being plotted, the "Possible Interpretations" section is speculative.  If you have more context about the slide, I can refine these notes further.

## Segment 98

### Slide Image
Here's a description of the slide image and its conversion to markdown notes:

**Image Description:**

The image shows a line graph. The x-axis ranges from 0 to 1200, and the y-axis ranges from -0.1 to 0.3. The graph displays a fluctuating line, starting with relatively high amplitude peaks and valleys in the range of 0-200 on the x-axis.  As the x-axis value increases, the amplitude of the fluctuations generally decreases.  Around the x-axis value of 600, the line crosses and stays near the zero line.  The fluctuations continue, but with a much smaller amplitude, until the end of the graph at x=1200. The line appears to be somewhat noisy.

**Markdown Notes:**

```markdown
## Graph Analysis

*   **Type:** Line graph
*   **X-axis:** 0 - 1200 (units not specified)
*   **Y-axis:** -0.1 to 0.3 (units not specified)
*   **Trend:**
    *   Initial high-amplitude fluctuations (0-200 x-axis).
    *   Decreasing amplitude as x increases.
    *   Line crosses and remains near zero around x=600.
    *   Low-amplitude fluctuations continue to x=1200.
*   **Characteristics:**
    *   Noisy signal.
    *   Fluctuations become less pronounced over time.
*   **Possible Interpretations (without context):**
    *   Decaying signal.
    *   Signal with decreasing energy.
    *   A process stabilizing over time.
```

**Note:**  Without knowing the context of the slide (what the x and y axes represent), the interpretations are general.  More specific notes could be added if the context were known.

## Segment 98

### Slide Image
Here's a description of the slide image and its conversion to markdown notes:

**Image Description:**

The image shows a woman using an ATM (Automated Teller Machine). She is inserting a card into the card reader slot of the ATM. The ATM is a grey color and appears to be located indoors, likely in a bank or a public space. The woman has blonde hair and is wearing a white shirt and a black jacket with a blue collar. The focus is on the interaction between the person and the machine.

**Markdown Notes:**

```markdown
## ATM Usage

* **Visual:** Woman using an ATM to insert a card.
* **Key Elements:**
    * ATM machine (grey)
    * Card reader slot
    * User inserting card
* **Context:**
    * Likely a bank or public location.
    * Represents a common financial transaction.
* **Possible Discussion Points:**
    * Security concerns with ATMs (skimming, fraud)
    * Convenience of ATMs
    * Accessibility of ATMs
    * ATM fees
```

**Possible Uses for these notes:**

*   As a starting point for a presentation on financial security.
*   As a visual aid for a lesson on banking.
*   As a prompt for a discussion about the role of technology in finance.

## Segment 99

Part 2 ⎯ Access Control                                                                                                  99
Measuring Iris Similarity
Based on Hamming distance
Define d(x,y) to be
# of non-match bits / # of bits compared
d(0010,0101) = 3/4 and d(101111,101001) = 1/3
Compute d(x,y) on 2048-bit iris code
Perfect match is d(x,y) = 0
For same iris, expected distance is 0.08
At random, expect distance of 0.50
Accept iris scan as match if distance < 0.32

## Segment 100

Part 2 ⎯ Access Control                                                                                                  100
Iris Scan Error Rate
distance
distance
Fraud rate
== equal error rate

## Segment 100

### Slide Image
Here's a description of the slide image and its conversion to markdown notes:

**Image Description:**

The image shows two histograms representing the distribution of scores from a comparison task.  The x-axis likely represents a similarity or confidence score (ranging from 0.0 to 1.0). The y-axis represents the frequency or count of occurrences of each score.

*   **Left Histogram ("same"):** This histogram is wider and more spread out, peaking around 0.11. It represents the distribution of scores when the items being compared were the *same*.  The standard deviation is 0.065.
*   **Right Histogram ("different"):** This histogram is narrower and more concentrated, peaking around 0.458. It represents the distribution of scores when the items being compared were *different*. The standard deviation is 0.0197.
*   **d' Value:** The image also displays a d' value of 7.3.  This is a measure of sensitivity or discriminability – how well the two distributions are separated. A higher d' indicates better separation.
*   **Sample Size:** The image notes that the data is based on 2.3 million comparisons.

**Markdown Notes:**

```markdown
## Comparison Task Results

**Overview:**
Histograms showing the distribution of scores from a comparison task (2.3 million comparisons).  The task involved determining if two items were the "same" or "different".

**Distributions:**

*   **"Same" Condition:**
    *   Mean: 0.110
    *   Standard Deviation: 0.065
    *   Distribution: Wider, more spread out.
*   **"Different" Condition:**
    *   Mean: 0.458
    *   Standard Deviation: 0.0197
    *   Distribution: Narrower, more concentrated.

**Key Metric:**

*   **d' (Discriminability):** 7.3
    *   Indicates a very strong ability to distinguish between "same" and "different" conditions.  High separation between the distributions.

**Interpretation:**
The results suggest a clear and reliable ability to differentiate between identical and non-identical items. The large sample size lends confidence to these findings.
```

**Key improvements in the markdown notes:**

*   **Clear headings and structure:**  Makes the information easy to scan and understand.
*   **Bullet points:**  Organize the data for each condition.
*   **Interpretation:** Adds a brief summary of what the results mean.
*   **Emphasis:** Uses bolding to highlight important terms and values.
*   **Context:** Provides a brief description of the task.

## Segment 100

### Slide Image
Here's a description of the image and its conversion to markdown notes:

**Image Description:**

The image depicts a five-pointed star. The star is colored with alternating sections of purple and orange. The orange sections have a dotted pattern within them. The star has a black outline. The background is white.

**Markdown Notes:**

```markdown
## Star Image Analysis

* **Shape:** Five-pointed star
* **Colors:**
    * Purple
    * Orange
* **Pattern:** Orange sections have a dotted/stippled pattern.
* **Outline:** Black outline defining the star's shape.
* **Background:** White
* **Possible Uses:**  Could represent a decorative element, a symbol of achievement, or a visual aid for geometry/shape recognition.
```

## Segment 100

### Slide Image
Here's a description of the image and its conversion to markdown notes:

**Image Description:**

The image depicts a five-pointed star. The star is colored with alternating sections of purple and a speckled orange/coral color. The star has a black outline. The background is white. The star appears to be a 3D representation, with shading suggesting depth.

**Markdown Notes:**

```markdown
## Star Image Analysis

* **Shape:** Five-pointed star
* **Color:**
    * Alternating sections of:
        * Purple
        * Speckled Orange/Coral
* **Outline:** Black
* **Background:** White
* **Representation:** Appears 3D with shading.
* **Possible Uses:**  Could represent achievement, decoration, or a celestial object.
```

**Additional Notes (depending on context):**

*   If this is part of a design lesson, you could add notes about color contrast, shape symmetry, and the use of outlines.
*   If it's related to geometry, you could discuss the angles and lines that make up the star.
*   If it's part of a presentation, you could add a title and a brief explanation of its relevance.

## Segment 101

Part 2 ⎯ Access Control                                                                                                  101
Attack on Iris Scan
Good photo of eye can be scanned
Attacker could use photo of eye
Afghan woman was authenticated by iris scan of old photo
Story can be found here
To prevent attack, scanner could use light to be sure it is a “live” iris

## Segment 102

Part 2 ⎯ Access Control                                                                                                  102
Equal Error Rate Comparison
Equal error rate (EER): fraud == insult rate
Fingerprint biometrics used in practice have EER ranging from about 10-3 to as high as 5%
Hand geometry has EER of about 10-3
In theory, iris scan has EER of about 10-6
Enrollment phase may be critical to accuracy
Most biometrics much worse than fingerprint!
Biometrics useful for authentication…
…but for identification, not so impressive today

## Segment 103

Part 2 ⎯ Access Control                                                                                                  103
Biometrics: The Bottom Line
Biometrics are hard to forge
But attacker could
Steal Alice’s thumb
Photocopy Bob’s fingerprint, eye, etc.
Subvert software, database, “trusted path” …
And how to revoke a “broken” biometric?
Biometrics are not foolproof
Biometric use is relatively limited today
That should change in the (near?) future

## Segment 104

http://pc.vietica.com/van.nguyen/InfoSec-VietNhat/InfoSec.htm

## Segment 104

### Slide Image
Here's a markdown conversion of the slide image's content:

## Slide Notes: SOICT - Thank You

**Visual:**

*   Image of a modern, multi-story building (likely the SOICT building).  The architecture is angular and features a lot of windows.
*   A red vertical bar on the left side of the slide.

**Text:**

*   **Logo:** SOICT 25th Anniversary Logo (includes Vietnamese text and the English "SOICT")
    *   "SOICT" stands for School of Information and Communication Technology.
    *   "VIỆN CÔNG NGHỆ THÔNG TIN VÀ TRUYỀN THÔNG" (Vietnamese translation of the school name)
*   **Main Text:** "Thank you for your attentions!" (in white text on the red bar)
*   **Website:** soict.hust.edu.vn/
*   **Facebook:** fb.com/groups/soict

**Key Takeaways:**

*   This is a closing slide for a presentation given by or about the School of Information and Communication Technology (SOICT) at Hanoi University of Science and Technology (HUST).
*   The slide celebrates the school's 25th anniversary.
*   Provides contact information for further engagement.

---

Let me know if you'd like me to elaborate on any aspect of this breakdown!

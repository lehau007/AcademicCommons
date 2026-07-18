[NORMALIZATION_ERROR] Normalization failed twice (Error code: 413 - {'error': {'message': 'Request too large for model `openai/gpt-oss-120b` in organization `org_01kkedd9pnejqr8cfvvrfp64h7` service tier `on_demand` on tokens per minute (TPM): Limit 8000, Requested 18841, please reduce your message size and try again. Need more tokens? Upgrade to Dev Tier today at https://console.groq.com/settings/billing', 'type': 'tokens', 'code': 'rate_limit_exceeded'}})

Identity Authentication
With extra material for further reading, indicated by symbol *

Info-Sec 2023
2
Authentication
Basics
Passwords
Challenge-Response
Biometrics
Location
Multiple Methods

Info-Sec 2023
3
Basics
Authentication: binding of identity to subject
Identity is that of external entity (my identity, Van, etc.)
Subject is computer entity (process, etc.)
Note: 
message authentication is a different topic and already mentioned in the applications of hash functions

4
Establishing Identity
One or more of the following
What entity knows (eg. password)
What entity has (eg. Identity card, smart card)
What entity is (eg. fingerprints, retinal characteristics)
Where entity is (eg. In front of a particular terminal)

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

Info-Sec 2023
6
Example
Password system, with passwords stored on line in clear text
A set of strings making up passwords
C = A
F singleton set of identity function { I }
L single equality test function { eq }
S function to set/change password

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

Info-Sec 2023
11
Attacking passwords
Goal: find a ∈ A such that:
For some f ∈ F, f(a) = c ∈ C 
c is associated with entity
Two ways to determine whether a meets these requirements:
By trying computing f(a) for a set of a values until succeed
By trying calling I(a) until succeed (I(a) returns true)

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

Info-Sec 2023
13
Dictionary Attacks
Trial-and-error from a list of potential passwords
Off-line: know f and c’s, and repeatedly try different guesses g ∈ A until the list is done or passwords guessed
Examples: crack, john-the-ripper
On-line: have access to functions in L and try guesses g until some l(g) succeeds
Examples: trying to log in by guessing a password

Info-Sec 2023
14
Success probability over a time period
Anderson’s formula:
P probability of guessing a password in specified period of time
G number of guesses tested in 1 time unit
T number of time units
N number of possible passwords (|A|)
Then P ≥ TG/N

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

Exercise
X = number defined by last 2 digits of your student ID; Y = X mod 4
Assume that H is a cryptographic hash function with output size (Y+2)*16 bits. Assume that Scorpion-i (i=1-9) is a specifically designed line of hardware chips for computing H, where Scorpion-i can create 10i * 1000 hash values a second (e.g. Scorpion-2 can do 100,000 hashes/sec). This product line is the best, fastest and affordable, in the market, priced at ii/2 *$1000 (e.g $2000 for i=2, $16000 for i=4). 

An authentication system requires its users to pick their passwords of length exactly 6 from an alphabet of size N=(X mod 50)+ 40. Using H, this system maintains the hash values of the passwords of all the users. An enemy, who has gained access to this hashed password file, aims to launch an off-line attack to break the password of an important user. Using the Scorpion chips, how much the enemy has to spend in order to finish within a month with success probability (6+Y)*10%?
16

Info-Sec 2023
17
On password selection
Random selection
Any password from A equally likely to be selected
Pronounceable passwords
User selection of passwords

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

Info-Sec 2023
19
User Selection
Problem: people pick easy to guess passwords
Based on account names, user names, computer names, place names
Dictionary words (also reversed, odd capitalizations, control characters, “elite-speak”, conjugations or declensions, swear words, Torah/Bible/Koran/… words)
Too short, digits only, letters only
License plates, acronyms, social security numbers
Personal characteristics or foibles (pet names, nicknames, job characteristics, etc.

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

Info-Sec 2023
22
Salting
Goal: slow dictionary attacks
Method: perturb hash function so that:
Parameter controls which hash function is used
Parameter differs for each password
So given n password hashes, and therefore n salts, need to hash guess n

Info-Sec 2023
23
Examples
Vanilla UNIX method
Use DES to encipher 0 message with password as key; iterate 25 times
Perturb E table in DES in one of 4096 ways
12 bit salt flips entries 1–11 with entries 25–36
Alternate methods
Use salt as first part of input to hash function

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

Exercise
Assume that H is a cryptographic hash function with output size (Y+2)*16 bits. Assume that Scorpion-i (i=1-9) is a specifically designed line of hardware chips for computing H, where Scorpion-i can create 10i * 1000 hash values a second, priced at ii/2 *$1000.
1. An authentication system requires its users to pick their passwords of length exactly 6 from an alphabet of size N=(X mod 50)+ 40. Using H, this system maintains the hash values of the passwords of all the users. An enemy, who has gained access to this hashed password file, aims to launch an off-line attack to break the password of an important user. Using the Scorpion chips, how much the enemy has to spend in order to finish within a month with success probability (6+Y)*10%?
2. The owner decides to enhance the above password system by using salt so that the enemy will need to spend at least 10 times the above mentioned amount of money to achieve the same goal. How many salt bits he/she need to use to achieve this purpose ?
25

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

Part 2 ⎯ Access Control                                                                                                  28
Password Cracking: Case I *
Attack 1 specific password without using a dictionary
E.g., administrator’s password
Must try 256/2 = 255 on average
Like exhaustive key search
Does salt help in this case?

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

Info-Sec 2023
35
Pass Algorithms
Challenge-response with the function f itself a secret
Challenge is a random string of characters 
Response is some function of that string 
Usually used in conjunction with fixed, reusable password


### Slide Image
This image illustrates a standard web authentication form incorporating a CAPTCHA (Completely Automated Public Turing test to tell Computers and Humans Apart) challenge.

Key elements include:

*   **Authentication Fields:** The form requires a "username" and "password," which are standard inputs for verifying user identity.
*   **CAPTCHA Mechanism:** A ReCAPTCHA widget is used to prevent automated software (bots) from submitting the form.
    *   **Challenge:** The user must read two distorted words ("asbury" and "law") and enter them into a text field.
    *   **Accessibility and Utility Tools:** The widget includes interactive buttons for users to:
        *   Refresh the CAPTCHA image (the circular arrow icon).
        *   Access an audio version of the challenge (the speaker icon).
        *   Access help or instructions (the question mark icon).
*   **Form Submission:** A "login" button is provided to process the data entered across all fields.


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

Info-Sec 2023
38
S/Key Protocol
System stores maximum number of authentications n, number
of next authentication i, last correctly supplied password pi–1.
System computes h(pi) = h(kn–i+1) = kn–i+2 = pi–1. If match with
what is stored, system replaces pi–1 with pi and increments i.

Info-Sec 2023
39
C-R and Dictionary Attacks
Same as for fixed passwords
Attacker knows challenge r and response f(r); if f encryption function, can try different keys
May only need to know form of response; attacker can tell if guess correct by looking to see if deciphered object is of right form
Example: Kerberos Version 4 used DES, but keys had 20 bits of randomness; Purdue attackers guessed keys quickly because deciphered tickets had a fixed set of bits in some locations

Info-Sec 2023
40
Encrypted Key Exchange *
Defeats off-line dictionary attacks
Idea: random challenges enciphered, so attacker cannot verify correct decipherment of challenge
Assume Alice, Bob share secret password s
In what follows, Alice needs to generate a random public key p and a corresponding private key q
Also, k is a randomly generated session key, and RA and RB are random challenges

Info-Sec 2023
41
EKE Protocol *
Now Alice, Bob share a randomly generated
secret session key k

Part 2 ⎯ Access Control                                                                                                  42
Something You Have
Something in your possession
Examples include following…
Car key
Laptop computer (or MAC address)
Password generator (next)
ATM card, smartcard, etc.

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

Smartcard
credit-card like 
has own processor, memory, I/O ports
ROM, EEPROM, RAM memory
executes protocol to authenticate with reader/computer
static: similar to memory cards
dynamic: passwords created every minute; entered manually by user or electronically
challenge-response: computer creates a random number; smart card provides its hash (similar to PK)
also have USB dongles


### Slide Image

{
  "nodes": [
    { "id": "1", "label": "Smartcard" },
    { "id": "2", "label": "Smartcard Chip" },
    { "id": "3", "label": "Typical chip layout" },
    { "id": "4", "label": "RAM" },
    { "id": "5", "label": "EEPROM" },
    { "id": "6", "label": "ROM" },
    { "id": "7", "label": "CPU" },
    { "id": "8", "label": "Crypto coprocessor" }
  ],
  "edges": [
    { "source": "2", "target": "1", "relationship": "embedded in" },
    { "source": "3", "target": "2", "relationship": "magnified view of" },
    { "source": "4", "target": "3", "relationship": "component of" },
    { "source": "5", "target": "3", "relationship": "component of" },
    { "source": "6", "target": "3", "relationship": "component of" },
    { "source": "7", "target": "3", "relationship": "component of" },
    { "source": "8", "target": "3", "relationship": "component of" }
  ],
  "directed": true
}



Electronic identity cards *
An important application of smart cards
A national e-identity (eID)
Serves the same purpose as other national ID cards (e.g., a driver’s licence)
Can provide stronger proof of identity
A German card
Personal data, Document number, Card access number (six digit random number), Machine readable zone (MRZ): the password
Uses: ePass (government use), eID (general use), eSign (can have private key and certificate)

User authentication with eID *

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

Part 2 ⎯ Access Control                                                                                                  51
Fingerprint: Enrollment
Capture image of fingerprint
Enhance image
Identify “points”

Part 2 ⎯ Access Control                                                                                                  52
Fingerprint: Recognition
Extracted points are compared with information stored in a database
Is it a statistical match?
Aside: Do identical twins’ fingerprints differ?

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

Authenticate user based on one of their physical characteristics:
facial
fingerprint
hand geometry
retina pattern
iris
signature
voice
Biometric authentication


### Slide Image
The provided image is a scatter plot representing various biometric characteristics mapped against two axes: "Cost" and "Accuracy". In a graph-theoretic sense, this is not a network (graph with edges); rather, it is a set of isolated nodes representing data points on a 2D plane.

As there are no explicit edges connecting the nodes, the edge list is empty.


{
  "graph": {
    "nodes": [
      { "id": "Hand", "label": "Hand" },
      { "id": "Signature", "label": "Signature" },
      { "id": "Face", "label": "Face" },
      { "id": "Voice", "label": "Voice" },
      { "id": "Retina", "label": "Retina" },
      { "id": "Finger", "label": "Finger" },
      { "id": "Iris", "label": "Iris" }
    ],
    "edges": [],
    "directed": false,
    "description": "Scatter plot of biometric characteristics. No explicit edges or directed relationships are defined between the nodes."
  }
}



Operation of a biometricsystem
Verification is analogous to user login via a smart card and a PIN

Identification is biometric info but no IDs; system compares with stored templates


### Slide Image

{
  "graph": {
    "nodes": [
      { "id": "1", "label": "User interface (Name (PIN))" },
      { "id": "2", "label": "Biometric sensor" },
      { "id": "3", "label": "Feature extractor" },
      { "id": "4", "label": "Database" },
      { "id": "5", "label": "Feature matcher" },
      { "id": "6", "label": "Output (true/false or identity)" }
    ],
    "edges": [
      { "source": "1", "target": "2", "directed": true },
      { "source": "2", "target": "3", "directed": true },
      { "source": "3", "target": "4", "directed": true, "context": "Enrollment" },
      { "source": "1", "target": "4", "directed": true },
      { "source": "3", "target": "5", "directed": true, "context": "Verification/Identification" },
      { "source": "4", "target": "5", "directed": true, "context": "Verification/Identification" },
      { "source": "5", "target": "6", "directed": true }
    ]
  }
}



Biometric Accuracy *
Palm print The system generates a matching score (a number) that quantifies similarity between the input and the stored template
Concerns: sensor noise and detection inaccuracy
Problems of false match/false non-match
* Further reading (Stallings textbook)


### Slide Image

{
  "nodes": [
    { "id": 1, "label": "Probability density function" },
    { "id": 2, "label": "imposter profile" },
    { "id": 3, "label": "decision threshold (t)" },
    { "id": 4, "label": "profile of genuine user" },
    { "id": 5, "label": "false nonmatch possible" },
    { "id": 6, "label": "false match possible" },
    { "id": 7, "label": "average matching value of imposter" },
    { "id": 8, "label": "average matching value of genuine user" },
    { "id": 9, "label": "Matching score (s)" }
  ],
  "edges": [
    { "from": 2, "to": 7, "directed": true },
    { "from": 4, "to": 8, "directed": true },
    { "from": 5, "to": 7, "directed": true },
    { "from": 6, "to": 8, "directed": true }
  ]
}



Biometric Accuracy *
Can plot characteristic curve (2,000,000 comparisons)
Pick threshold balancing error rates


### Slide Image
The provided image is a line graph representing biometric performance data, not a network or a structured graph with interconnected nodes in a topological sense. However, if we interpret the legend labels as nodes and the shared context of the chart as a relationship, we can structure this information in JSON format as requested:


{
  "graph_type": "Data Visualization / Multi-line Chart",
  "nodes": [
    { "id": "Face", "label": "Face", "style": "solid blue line with filled circles" },
    { "id": "Fingerprint", "label": "Fingerprint", "style": "solid blue line with open circles" },
    { "id": "Voice", "label": "Voice", "style": "solid black line with filled squares" },
    { "id": "Hand", "label": "Hand", "style": "solid black line with open diamonds" },
    { "id": "Iris", "label": "Iris", "style": "isolated filled diamond" }
  ],
  "edges": [],
  "description": "This is a log-log plot showing biometric error rates. There are no edges (connections) between the entities themselves; rather, each entity represents a distinct data series plotted against the axes 'false match rate' and 'false nonmatch rate'. The Iris node is an isolated data point."
}


**Note:** In graph theory terms, this visualization is a collection of independent functional curves rather than a relational graph. Therefore, the "edges" list is empty as the entities do not link to one another; they represent competing variables within the same coordinate system.


Info-Sec 2023
58
Cautions
These can be fooled!
Assumes biometric device accurate in the environment it is being used in!
Transmission of data to validator is tamperproof, correct

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

Info-Sec 2023
60
Location – Just a brief
If you know where user is, validate identity by seeing if person is where the user is
Requires special-purpose hardware to locate user
GPS (global positioning system) device gives location signature of entity
Host uses LSS (location signature sensor) to get signature for entity

Info-Sec 2023
61
Multiple Methods
Example: “where you are” also requires entity to have LSS and GPS, so also “what you have”
Can assign different methods to different tasks
As users perform more and more sensitive tasks, must authenticate in more and more ways (presumably, more stringently) File describes authentication required
Also includes controls on access (time of day, etc.), resources, and requests to change passwords

Pluggable Authentication Modules

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

Extended Material *Kerberos authentication protocol
Material sources: History & some general info from Wiki;
Details on Kerberos versions 4&5 from Stallings Text and slides

Info-Sec 2023
65
Kerberos
A computer network authentication protocol
which allows nodes communicating over a non-secure network to prove their identity to one another in a secure manner. 
aimed primarily at a client-server model, and it provides mutual authentication -- both the user and the server verify each other's identity. Messages are protected against eaves dropping & replay attacks.
Kerberos builds on SKC and requires a trusted third party, and optionally may use public-key cryptography during certain phases of authentication.

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

Kerberos v4 Overview
a basic third-party authentication scheme
have an Authentication Server (AS) 
users initially negotiate with AS to identify self 
AS provides a non-corruptible authentication credential (ticket granting ticket TGT) 
have a Ticket Granting server (TGS)
users subsequently request access to other services from TGS on basis of users TGT
using a complex protocol using DES

Kerberos 4 Overview


### Slide Image

{
  "nodes": [
    { "id": "workstation", "label": "Workstation (User)" },
    { "id": "as", "label": "Authentication Server (AS)" },
    { "id": "tgs", "label": "Ticket-granting Server (TGS)" },
    { "id": "database", "label": "Database" },
    { "id": "server", "label": "Server" }
  ],
  "edges": [
    {
      "source": "workstation",
      "target": "as",
      "label": "request ticket-granting ticket",
      "directed": true
    },
    {
      "source": "as",
      "target": "workstation",
      "label": "ticket + session key",
      "directed": true
    },
    {
      "source": "as",
      "target": "database",
      "label": "verify/retrieve",
      "directed": true
    },
    {
      "source": "database",
      "target": "as",
      "label": "verify/retrieve",
      "directed": true
    },
    {
      "source": "workstation",
      "target": "tgs",
      "label": "request service-granting ticket",
      "directed": true
    },
    {
      "source": "tgs",
      "target": "workstation",
      "label": "ticket + session key",
      "directed": true
    },
    {
      "source": "workstation",
      "target": "server",
      "label": "request service",
      "directed": true
    },
    {
      "source": "server",
      "target": "workstation",
      "label": "provide server authenticator",
      "directed": true
    }
  ]
}



Kerberos v4 Dialogue


### Slide Image
Here is the extraction of the text and formulas from the provided image:

### **Section (a)**
**Explanatory Text:** Authentication Service Exchange to obtain ticket-granting ticket
**Formulas:**
1. $C \to AS: ID_c \parallel ID_{tgs} \parallel TS_1$
2. $AS \to C: E(K_c, [K_{c,tgs} \parallel ID_{tgs} \parallel TS_2 \parallel Lifetime_2 \parallel Ticket_{tgs}])$
   $Ticket_{tgs} = E(K_{tgs}, [K_{c,tgs} \parallel ID_C \parallel AD_C \parallel ID_{tgs} \parallel TS_2 \parallel Lifetime_2])$

---

### **Section (b)**
**Explanatory Text:** Ticket-Granting Service Exchange to obtain service-granting ticket
**Formulas:**
3. $C \to TGS: ID_v \parallel Ticket_{tgs} \parallel Authenticator_c$
4. $TGS \to C: E(K_{c,tgs}, [K_{c,v} \parallel ID_v \parallel TS_4 \parallel Ticket_v])$
   $Ticket_{tgs} = E(K_{tgs}, [K_{c,tgs} \parallel ID_C \parallel AD_C \parallel ID_{tgs} \parallel TS_2 \parallel Lifetime_2])$
   $Ticket_v = E(K_v, [K_{c,v} \parallel ID_C \parallel AD_C \parallel ID_v \parallel TS_4 \parallel Lifetime_4])$
   $Authenticator_c = E(K_{c,tgs}, [ID_C \parallel AD_C \parallel TS_3])$

---

### **Section (c)**
**Explanatory Text:** Client/Server Authentication Exchange to obtain service (for mutual authentication)
**Formulas:**
5. $C \to V: Ticket_v \parallel Authenticator_c$
6. $V \to C: E(K_{c,v}, [TS_5 + 1])$
   $Ticket_v = E(K_v, [K_{c,v} \parallel ID_C \parallel AD_C \parallel ID_v \parallel TS_4 \parallel Lifetime_4])$
   $Authenticator_c = E(K_{c,v}, [ID_C \parallel AD_C \parallel TS_5])$


Kerberos Version 5
developed in mid 1990’s
specified as Internet standard RFC 1510
provides improvements over v4
addresses environmental shortcomings
encryption alg, network protocol, byte order, ticket lifetime, authentication forwarding, interrealm auth
and technical deficiencies
double encryption, non-std mode of use, session keys, password attacks

Kerberos Realms
a Kerberos environment consists of:
a Kerberos server
a number of clients, all registered with server
application servers, sharing keys with server
this is termed a realm
typically a single administrative domain
if have multiple realms, their Kerberos servers must share keys and trust

Kerberos Realms


### Slide Image

{
  "nodes": [
    { "id": "client", "label": "Client" },
    { "id": "realm_a_as", "label": "Realm A: AS" },
    { "id": "realm_a_tgs", "label": "Realm A: TGS" },
    { "id": "realm_b_as", "label": "Realm B: AS" },
    { "id": "realm_b_tgs", "label": "Realm B: TGS" },
    { "id": "server", "label": "Server" }
  ],
  "edges": [
    {
      "source": "client",
      "target": "realm_a_as",
      "label": "1. request ticket for local TGS",
      "directed": true
    },
    {
      "source": "realm_a_as",
      "target": "client",
      "label": "2. ticket for local TGS",
      "directed": true
    },
    {
      "source": "client",
      "target": "realm_a_tgs",
      "label": "3. request ticket for remote TGS",
      "directed": true
    },
    {
      "source": "realm_a_tgs",
      "target": "client",
      "label": "4. ticket for remote TGS",
      "directed": true
    },
    {
      "source": "client",
      "target": "realm_b_tgs",
      "label": "5. request ticket for remote server",
      "directed": true
    },
    {
      "source": "realm_b_tgs",
      "target": "client",
      "label": "6. ticket for remote server",
      "directed": true
    },
    {
      "source": "client",
      "target": "server",
      "label": "7. request remote service",
      "directed": true
    }
  ]
}



Protocol
[From Wiki]
Client Authentication to the AS
Client Service Authorization
Client Service Request


### Slide Image

{
  "nodes": [
    { "id": "client", "label": "Client (C)" },
    { "id": "as", "label": "Authentication Server (AS)" },
    { "id": "tgs", "label": "Ticket-granting Server (TGS)" },
    { "id": "ss", "label": "Service Server (SS)" }
  ],
  "edges": [
    {
      "source": "client",
      "target": "as",
      "label": "User ID + requested service"
    },
    {
      "source": "as",
      "target": "client",
      "label": "Msg A, Msg B (TGT)"
    },
    {
      "source": "client",
      "target": "tgs",
      "label": "Msg C, Msg D"
    },
    {
      "source": "tgs",
      "target": "client",
      "label": "Msg E, Msg F"
    },
    {
      "source": "client",
      "target": "ss",
      "label": "Msg E, Msg G"
    },
    {
      "source": "ss",
      "target": "client",
      "label": "Msg H"
    }
  ],
  "directed": true
}



Kerberos v5 Dialogue


### Slide Image
### Explanatory Text
*   **(a) Authentication Service Exchange to obtain ticket-granting ticket**
*   **(b) Ticket-Granting Service Exchange to obtain service-granting ticket**
*   **(c) Client/Server Authentication Exchange to obtain service**

---

### Formula Text

**(a)**
(1) $\text{C} \rightarrow \text{AS} : \text{Options} \parallel ID_c \parallel \text{Realm}_c \parallel ID_{tgs} \parallel \text{Times} \parallel \text{Nonce}_1$
(2) $\text{AS} \rightarrow \text{C} : \text{Realm}_c \parallel ID_c \parallel \text{Ticket}_{tgs} \parallel \text{E}(K_c, [\text{K}_{c,tgs} \parallel \text{Times} \parallel \text{Nonce}_1 \parallel \text{Realm}_{tgs} \parallel ID_{tgs}])$
$\text{Ticket}_{tgs} = \text{E}(K_{tgs}, [\text{Flags} \parallel K_{c,tgs} \parallel \text{Realm}_c \parallel ID_c \parallel AD_c \parallel \text{Times}])$

**(b)**
(3) $\text{C} \rightarrow \text{TGS} : \text{Options} \parallel ID_v \parallel \text{Times} \parallel \text{Nonce}_2 \parallel \text{Ticket}_{tgs} \parallel \text{Authenticator}_c$
(4) $\text{TGS} \rightarrow \text{C} : \text{Realm}_c \parallel ID_c \parallel \text{Ticket}_v \parallel \text{E}(K_{c,tgs}, [K_{c,v} \parallel \text{Times} \parallel \text{Nonce}_2 \parallel \text{Realm}_v \parallel ID_v])$
$\text{Ticket}_{tgs} = \text{E}(K_{tgs}, [\text{Flags} \parallel K_{c,tgs} \parallel \text{Realm}_c \parallel ID_c \parallel AD_c \parallel \text{Times}])$
$\text{Ticket}_v = \text{E}(K_v, [\text{Flags} \parallel K_{c,v} \parallel \text{Realm}_c \parallel ID_c \parallel AD_c \parallel \text{Times}])$
$\text{Authenticator}_c = \text{E}(K_{c,tgs}, [ID_c \parallel \text{Realm}_c \parallel TS_1])$

**(c)**
(5) $\text{C} \rightarrow \text{V} : \text{Options} \parallel \text{Ticket}_v \parallel \text{Authenticator}_c$
(6) $\text{V} \rightarrow \text{C} : \text{E}_{K_{c,v}} [ TS_2 \parallel \text{Subkey} \parallel \text{Seq\#} ]$
$\text{Ticket}_v = \text{E}(K_v, [\text{Flags} \parallel K_{c,v} \parallel \text{Realm}_c \parallel ID_c \parallel AD_c \parallel \text{Times}])$
$\text{Authenticator}_c = \text{E}(K_{c,v}, [ID_c \parallel \text{Realm}_c \parallel TS_2 \parallel \text{Subkey} \parallel \text{Seq\#}])$


Federated Identity Management
use of common identity management scheme
across multiple enterprises & numerous applications 
supporting many thousands, even millions of users 
principal elements are:
authentication, authorization, accounting, provisioning, workflow automation, delegated administration, password synchronization, self-service password reset, federation
Kerberos contains many of these elements

Identity Management


### Slide Image
### Node Labels

The node labels in the provided image are:

1. **Principal**
2. **Administrator**
3. **Data consumer**
4. **Attribute service**
5. **Identity Provider** (which contains sub-components):
   - **Identity control interface**
     - **Principal authentication**
     - **Identifier translation**
   - **Attribute locator**

### Edge List and Directionality

The edges in the graph, along with their directionality, are as follows:

1. **Principal → Identity Provider**: Principals authenticate, manage their identity elements.
   - **Directionality**: One-way (from Principal to Identity Provider)

2. **Identity Provider → Principal**: (Implicit, not directly shown but inferred as part of the authentication and management process)
   - **Directionality**: One-way (from Identity Provider to Principal, though not directly shown)

3. **Principal → Attribute service**: Principals provide attributes.
   - **Directionality**: One-way (from Principal to Attribute service)

4. **Administrator → Attribute service**: Administrators provide attributes.
   - **Directionality**: One-way (from Administrator to Attribute service)

5. **Attribute service → Data consumer**: Data consumers apply references to obtain attribute data.
   - **Directionality**: One-way (from Attribute service to Data consumer)

6. **Identity Provider → Data consumer**: Data consumers obtain identifiers, attribute references.
   - **Directionality**: One-way (from Identity Provider to Data consumer)

### Structured Graph Representation in JSON


{
  "nodes": [
    {
      "id": "Principal",
      "label": "Principal"
    },
    {
      "id": "Administrator",
      "label": "Administrator"
    },
    {
      "id": "Data consumer",
      "label": "Data consumer"
    },
    {
      "id": "Attribute service",
      "label": "Attribute service"
    },
    {
      "id": "Identity Provider",
      "label": "Identity Provider",
      "subComponents": [
        {
          "id": "Identity control interface",
          "label": "Identity control interface"
        },
        {
          "id": "Principal authentication",
          "label": "Principal authentication"
        },
        {
          "id": "Identifier translation",
          "label": "Identifier translation"
        },
        {
          "id": "Attribute locator",
          "label": "Attribute locator"
        }
      ]
    }
  ],
  "edges": [
    {
      "source": "Principal",
      "target": "Identity Provider",
      "label": "Principals authenticate, manage their identity elements",
      "directionality": "one-way"
    },
    {
      "source": "Principal",
      "target": "Attribute service",
      "label": "Principals provide attributes",
      "directionality": "one-way"
    },
    {
      "source": "Administrator",
      "target": "Attribute service",
      "label": "Administrators provide attributes",
      "directionality": "one-way"
    },
    {
      "source": "Attribute service",
      "target": "Data consumer",
      "label": "Data consumers apply references to obtain attribute data",
      "directionality": "one-way"
    },
    {
      "source": "Identity Provider",
      "target": "Data consumer",
      "label": "Data consumers obtain identifiers, attribute references",
      "directionality": "one-way"
    }
  ]
}


This JSON representation captures the nodes (entities) and edges (relationships) as described in the provided image, along with their directionality and brief descriptions of each relationship.


Identity Federation


### Slide Image
### Graph Representation

The graph consists of the following components:

#### Node Labels
- **User**
- **Identity Provider (source domain)**
- **Administrator**
- **Service Provider (destination domain)**

#### Edge List and Directionality
The edges represent interactions or information exchanges between nodes. The directionality of the edges indicates the flow of information.

1. **User → Identity Provider (source domain)**: The user initiates an authentication dialogue with the identity provider.
2. **Administrator → Identity Provider (source domain)**: The administrator provides attributes associated with an identity to the identity provider.
3. **Identity Provider (source domain) → Service Provider (destination domain)**: The service provider obtains identity information, authentication information, and associated attributes from the identity provider.
4. **Service Provider (destination domain) → User**: The service provider opens a session with the remote user.

#### Structured Graph Representation in JSON


{
  "nodes": [
    {
      "id": "User",
      "label": "User"
    },
    {
      "id": "Identity Provider (source domain)",
      "label": "Identity Provider (source domain)"
    },
    {
      "id": "Administrator",
      "label": "Administrator"
    },
    {
      "id": "Service Provider (destination domain)",
      "label": "Service Provider (destination domain)"
    }
  ],
  "edges": [
    {
      "source": "User",
      "target": "Identity Provider (source domain)",
      "label": "1. Initiates authentication dialogue"
    },
    {
      "source": "Administrator",
      "target": "Identity Provider (source domain)",
      "label": "2. Provides attributes"
    },
    {
      "source": "Identity Provider (source domain)",
      "target": "Service Provider (destination domain)",
      "label": "3. Provides identity and attribute information"
    },
    {
      "source": "Service Provider (destination domain)",
      "target": "User",
      "label": "4. Opens session"
    }
  ]
}


This JSON representation captures the nodes (entities) and edges (interactions) of the graph, providing a structured view of the authentication and authorization process described in the diagram.


Standards Used
Security Assertion Markup Language (SAML)
XML-based language for exchange of security information between online business partners
part of OASIS (Organization for the Advancement of Structured Information Standards) standards for federated identity management
e.g. WS-Federation for browser-based federation
need a few mature industry standards

Federated Identity Examples


### Slide Image
## Step 1: Extract Node Labels

The node labels from the diagrams are:

1. **Initial authentication**
2. **Workplace.com (employee portal)**
   - Links: health benefits etc.
3. **End user (employee)**
4. **Health.com**
5. **User store**
   - Name: ID
   - Role: 
   - Date: 1410
   - Ravi: 1693
6. **Initial authentication**
7. **PartsSupplier.com**
   - Welcome tool
   - Technical doc.
   - Troubleshooting
8. **User store**
   - Name: ID
   - Role: Engineer
   - Ravi: 1693
   - Punch
9. **Workplace.com (procurement application)**
10. **PinSupplies.com**
   - Purchasing
   - Web service
11. **E-ship.com**
    - Shipping
    - Web service

## Step 2: Extract Edge List and Directionality

The edge list with directionality from the diagrams are:

1. **Initial authentication → Workplace.com (employee portal)**
2. **Workplace.com (employee portal) → End user (employee)**
3. **Workplace.com (employee portal) → Health.com**
4. **Health.com → User store**
5. **Initial authentication → Workplace.com (employee portal)**
6. **Workplace.com (employee portal) → PartsSupplier.com**
7. **PartsSupplier.com → User store**
8. **Initial authentication → Workplace.com (procurement application)**
9. **Workplace.com (procurement application) → PinSupplies.com**
10. **PinSupplies.com → E-ship.com**

## Step 3: Structured Graph Representation in JSON

To represent the graph in JSON, we will create a nodes array and an edges array. Each node will have an id (which corresponds to its label) and each edge will have a source and a target, representing the directionality of the edge.


{
  "nodes": [
    {"id": "Initial authentication"},
    {"id": "Workplace.com (employee portal)"},
    {"id": "End user (employee)"},
    {"id": "Health.com"},
    {"id": "User store"},
    {"id": "Initial authentication (2)"},
    {"id": "PartsSupplier.com"},
    {"id": "User store (2)"},
    {"id": "Workplace.com (procurement application)"},
    {"id": "PinSupplies.com"},
    {"id": "E-ship.com"}
  ],
  "edges": [
    {"source": "Initial authentication", "target": "Workplace.com (employee portal)"},
    {"source": "Workplace.com (employee portal)", "target": "End user (employee)"},
    {"source": "Workplace.com (employee portal)", "target": "Health.com"},
    {"source": "Health.com", "target": "User store"},
    {"source": "Initial authentication (2)", "target": "Workplace.com (employee portal)"},
    {"source": "Workplace.com (employee portal)", "target": "PartsSupplier.com"},
    {"source": "PartsSupplier.com", "target": "User store (2)"},
    {"source": "Initial authentication (2)", "target": "Workplace.com (procurement application)"},
    {"source": "Workplace.com (procurement application)", "target": "PinSupplies.com"},
    {"source": "PinSupplies.com", "target": "E-ship.com"}
  ]
}


The final answer is: 

{
  "nodes": [
    {"id": "Initial authentication"},
    {"id": "Workplace.com (employee portal)"},
    {"id": "End user (employee)"},
    {"id": "Health.com"},
    {"id": "User store"},
    {"id": "Initial authentication (2)"},
    {"id": "PartsSupplier.com"},
    {"id": "User store (2)"},
    {"id": "Workplace.com (procurement application)"},
    {"id": "PinSupplies.com"},
    {"id": "E-ship.com"}
  ],
  "edges": [
    {"source": "Initial authentication", "target": "Workplace.com (employee portal)"},
    {"source": "Workplace.com (employee portal)", "target": "End user (employee)"},
    {"source": "Workplace.com (employee portal)", "target": "Health.com"},
    {"source": "Health.com", "target": "User store"},
    {"source": "Initial authentication (2)", "target": "Workplace.com (employee portal)"},
    {"source": "Workplace.com (employee portal)", "target": "PartsSupplier.com"},
    {"source": "PartsSupplier.com", "target": "User store (2)"},
    {"source": "Initial


FIM vs. SSO
SSO: Single Sign-On
Allows users to access multiple web applications at once, using just one set of credentials. 
Beyond the workforce, companies can utilize SSO to help customers access various sections of one account. 
FIM 
As a tool, SSO fits within the broader model of FIM.
The key difference between SSO and FIM is while SSO is designed to authenticate a single credential across various systems within one organization, federated identity management systems offer single access to a number of applications across various enterprises.

Extended Material *Biometrics
Slides borrowed from Mark Stamp’s web
https://www.cs.sjsu.edu/~stamp/infosec/powerpoint/

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

Part 2 ⎯ Access Control                                                                                                  89
Fingerprint History
1823 ⎯ Professor Johannes Evangelist Purkinje discussed 9 fingerprint patterns 
1856 ⎯ Sir William Hershel used fingerprint (in India) on contracts
1880 ⎯ Dr. Henry Faulds article in Nature about fingerprints for ID
1883 ⎯ Mark Twain’s Life on the Mississippi (murderer ID’ed by fingerprint)

Part 2 ⎯ Access Control                                                                                                  90
Fingerprint History
1888 ⎯ Sir Francis Galton developed classification system
His system  of “minutia” can be used today
Also verified that fingerprints do not change
Some countries require fixed number of “points” (minutia) to match in criminal cases
In Britain, at least 15 points 
In US, no fixed number of points

Part 2 ⎯ Access Control                                                                                                  91
Fingerprint Comparison
Loop (double)
Whorl
Arch
Examples of loops, whorls, and arches
Minutia extracted from these features


### Slide Image
This image displays a fingerprint exhibiting a **whorl pattern**, characterized by ridges that form circular or spiral shapes around a central point. 

Key dermatoglyphic features present include:

*   **Core:** The innermost point of the pattern, located in the center of the whorl.
*   **Deltas:** Areas where ridges diverge to form triangular shapes. This specific print shows a delta on the left side, where the ridges split to flow in different directions, which is a defining marker for classifying fingerprint patterns.
*   **Ridges and Valleys:** The high-contrast black lines represent the friction ridges, while the white spaces between them represent the valleys. These ridges are the primary anatomical structures used in biometric identification and forensics.
*   **Minutiae:** Throughout the pattern, specific points of interest are visible, such as ridge endings (where a ridge stops abruptly) and bifurcations (where a single ridge splits into two). These unique characteristics are the basis for fingerprint matching algorithms.



### Slide Image
This image displays a fingerprint featuring a **whorl pattern**, characterized by a central circular core surrounded by concentric ridges. 

Key forensic and biometric features present include:

*   **Core:** The central, innermost point of the pattern, marked by a tight, circular ridge formation.
*   **Deltas:** Two distinct delta points are visible—one on the lower left and one on the lower right. A delta is the point where two ridge flows diverge to form the triangular pattern characteristic of loop and whorl fingerprint classifications.
*   **Ridge Flow:** The ridges form a closed loop system that travels in an oval shape, rotating around the core and terminating or flowing outward toward the deltas.
*   **Pattern Classification:** The presence of a central core with two associated deltas confirms this as a **plain whorl** pattern, a primary classification category in dactyloscopy (the study of fingerprints).



### Slide Image
This image displays a **plain arch** fingerprint pattern. 

Key characteristics for identification include:

*   **Ridge Flow:** The friction ridges enter from one side of the print, rise upward toward the center to form a wave-like or arching shape, and exit on the opposite side.
*   **Absence of Deltas:** Unlike loop or whorl patterns, this configuration lacks a "delta"—the triangular junction where two or more ridge lines diverge. 
*   **Lack of Cores:** There is no "core" or focal point within the pattern where ridges turn back on themselves. 

The structure is defined by its simple, continuous ridge flow that remains uninterrupted by the complexities found in other fingerprint classifications.


Part 2 ⎯ Access Control                                                                                                  92
Fingerprint: Enrollment
Capture image of fingerprint
Enhance image
Identify “points”

Part 2 ⎯ Access Control                                                                                                  93
Fingerprint: Recognition
Extracted points are compared with information stored in a database
Is it a statistical match?
Aside: Do identical twins’ fingerprints differ?

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

Part 2 ⎯ Access Control                                                                                                  95
Hand Geometry
Advantages
Quick ⎯ 1 minute for enrollment,           5 seconds for recognition
Hands are symmetric ⎯ so what?
Disadvantages
Cannot use on very young or very old
Relatively high equal error rate

Part 2 ⎯ Access Control                                                                                                  96
Iris Patterns
Iris pattern development is “chaotic”
Little or no genetic influence
Even for identical twins, uncorrelated
Pattern is stable through lifetime


### Slide Image
The provided image displays a cross-section of an eye, highlighting specific anatomical structures labeled with letters. Based on standard anatomical knowledge of the structures identified in the image:

*   **S** refers to the **Sclera** (the white outer layer of the eye).
*   **I** refers to the **Iris** (the colored part of the eye surrounding the pupil).
*   **C** refers to the **Cornea** (the transparent front part of the eye that covers the iris and pupil).

The relationship between these components is spatial and structural. The Cornea (C) is the outermost layer protecting the front, the Iris (I) is positioned behind the cornea, and the Sclera (S) forms the outer wall of the eyeball, extending from the boundary of the cornea.


{
  "graph": {
    "nodes": [
      { "id": "S", "label": "Sclera" },
      { "id": "I", "label": "Iris" },
      { "id": "C", "label": "Cornea" }
    ],
    "edges": [
      {
        "source": "C",
        "target": "I",
        "relationship": "positioned_anterior_to",
        "directed": true
      },
      {
        "source": "S",
        "target": "C",
        "relationship": "connected_to",
        "directed": false
      },
      {
        "source": "I",
        "target": "S",
        "relationship": "contained_within",
        "directed": true
      }
    ]
  }
}




### Slide Image
The visual element depicts a close-up of a human eye, specifically focusing on the iris. The iris is the colored part of the eye, and in this image, it appears to be blue-gray with a black pupil at its center. Surrounding the iris are white lines and patterns that resemble the unique characteristics of an individual's iris, also known as an "iris scan" or "iris pattern." 

This visual element could contribute to learning about the anatomy of the human eye, specifically the unique features of the iris, or it could be used in the context of biometrics and identification technology that uses iris scanning for security purposes.



### Slide Image
This image shows the anatomy of a human eye, highlighting the following features:

*   **Plica Semilunaris:** Located in the medial canthus (the inner corner of the eye), there is a distinct, pinkish, fleshy mucosal fold. This structure is a vestigial remnant of the nictitating membrane found in other vertebrate species.
*   **Caruncula Lacrimalis:** Situated slightly medial to the plica semilunaris, this is the small, reddish elevation of tissue. It contains sebaceous and sweat glands and is a common site for the accumulation of ocular secretions (often referred to as "sleep").
*   **Sclera:** The visible portion of the white of the eye is shown, containing fine, branching blood vessels (episcleral vessels).
*   **Iris and Pupil:** The image displays a darkly pigmented iris with visible crypts and radial striations. The pupil is centralized. A localized white reflection (corneal light reflex) is visible on the surface of the cornea, indicating the point of light source reflection.
*   **Eyelid Margins:** The image shows the upper and lower eyelids, including the punctum (the opening for tear drainage, visible on the lower eyelid margin near the inner corner) and the presence of eyelashes.


Part 2 ⎯ Access Control                                                                                                  97
Iris Recognition: History
1936 ⎯ suggested by ophthalmologist
1980s ⎯ James Bond film(s)
1986 ⎯ first patent appeared
1994 ⎯ John Daugman patents new-and-improved technique
Patents owned by Iridian Technologies

Part 2 ⎯ Access Control                                                                                                  98
Iris Scan
Scanner locates iris
Take b/w photo
Use polar coordinates…
2-D wavelet transform
Get 256 byte iris code


### Slide Image
The provided image is a grayscale spectrogram representing signal intensity over time and frequency; it does not contain a graphical diagram with nodes and edges. Therefore, it cannot be parsed into a graph representation.


{
  "node_labels": [],
  "edge_list": [],
  "directionality": "N/A",
  "note": "The image provided is a scientific data visualization (spectrogram) and does not contain a node-edge graph structure."
}




### Slide Image
The provided image is a 3D surface plot representing a mathematical function (specifically a 2D Gaussian-like wave or Sinc function) mapped over a grid, rather than a network diagram or graph structure consisting of nodes and edges.

As there are no nodes or directed connections present in the image, a graph representation would be empty.


{
  "nodes": [],
  "edges": [],
  "directed": false,
  "note": "The image is a 3D surface plot of a continuous mathematical function, not a network graph."
}




### Slide Image
The provided image is a single photograph of a human eye with two superimposed cyan circular overlays. There is no graph structure (nodes or edges) present in the image.

If you are interpreting the geometric features as components of a graph, here is the JSON representation based on the visual elements provided:


{
  "graph_type": "undirected",
  "nodes": [
    {
      "id": "pupil_boundary",
      "label": "inner_circle",
      "description": "Cyan circle delineating the pupil boundary"
    },
    {
      "id": "iris_boundary",
      "label": "outer_circle",
      "description": "Cyan circle delineating the iris boundary"
    },
    {
      "id": "pupil_center",
      "label": "crosshair",
      "description": "Cyan crosshair mark indicating the center of the pupil"
    }
  ],
  "edges": [
    {
      "source": "pupil_center",
      "target": "pupil_boundary",
      "relationship": "centered_within"
    },
    {
      "source": "pupil_boundary",
      "target": "iris_boundary",
      "relationship": "concentric"
    }
  ]
}




### Slide Image
The provided image is a 3D surface plot representing a mathematical function (likely a Gabor wavelet or similar oscillatory Gaussian surface), not a graph or network diagram. Consequently, it contains no nodes, edges, or structural connectivity data to extract.


{
  "nodes": [],
  "edges": [],
  "directed": false,
  "description": "The input image is a 3D surface plot and does not represent a network graph structure."
}




### Slide Image
The provided image is a signal processing plot showing amplitude over time (or index). It is **not a network graph**; therefore, it does not contain nodes, edges, or structural connectivity that can be represented as a graph.

The plot displays a time-series or discrete sequence of data points where the x-axis represents index/time (0 to 1200) and the y-axis represents a value (approximately -0.1 to 0.3).

If you are looking for a data representation of the plotted values, it would be a **sequential array** rather than a graph structure.


{
  "graph_type": "none",
  "error": "The image is a time-series plot, not a node-edge graph structure.",
  "data_type": "time-series",
  "axes": {
    "x_axis": "index/time (0 to 1200)",
    "y_axis": "amplitude (-0.1 to 0.3)"
  }
}




### Slide Image
This image demonstrates the process of using a biometric identification device. The key instructional components are:

*   **Device Interaction:** The subject is positioning their hand or a specific identification item directly in front of the optical scanning panel of the biometric terminal.
*   **Alignment:** The proximity of the hand to the sensor highlights the requirement for correct placement to trigger the identification process.
*   **Application:** The equipment represents typical hardware used for secure access control, identity verification, or time-and-attendance logging.


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

Part 2 ⎯ Access Control                                                                                                  100
Iris Scan Error Rate
distance
distance
Fraud rate
== equal error rate


### Slide Image
The provided image is a statistical plot (a histogram showing two distributions) rather than a network or graph structure. Therefore, it does not contain nodes or edges in the context of graph theory.

If you interpret the visual components as a data structure, the representation is as follows:


{
  "graph_type": "none",
  "reasoning": "The image is a statistical histogram comparing two populations ('same' and 'different'). There are no nodes connected by edges, so no graph structure exists.",
  "nodes": [],
  "edges": [],
  "metadata": {
    "labels": ["same", "different"],
    "statistics": {
      "same": {
        "mean": 0.110,
        "stnd.dev": 0.065
      },
      "different": {
        "mean": 0.458,
        "stnd.dev": 0.0197
      },
      "d_prime": 7.3,
      "sample_size": "2.3 million comparisons"
    }
  }
}




### Slide Image
The image depicts a star shape with 5 points. The star has a white center and is divided into sections of black and gray.



### Slide Image
The image depicts a star polygon with 10 points, divided into sections of different colors. The star polygon is composed of 10 triangular sections, with some sections shaded in black and gray, while others remain unshaded.

**Key Features:**

*   **Symmetry:** The star polygon exhibits rotational symmetry.
*   **Sections:** It is divided into 10 triangular sections.
*   **Coloring:** Some sections are shaded in black and gray, while others are unshaded.

**Geometric Properties:**

*   **Angles:** Each internal angle of the star polygon is 36 degrees (360/10).
*   **Triangles:** The star polygon can be divided into 10 isosceles triangles.

**Mathematical Concepts:**

*   **Geometry:** The image illustrates geometric concepts, such as symmetry and angles.
*   **Fractals:** The star polygon can be used to explore fractal geometry and self-similarity.

**Educational Value:**

*   **Geometry Lesson:** This image can be used to teach students about star polygons, symmetry, and geometric properties.
*   **Math Exploration:** It provides a visual representation for exploring mathematical concepts, such as angles, triangles, and fractals.


Part 2 ⎯ Access Control                                                                                                  101
Attack on Iris Scan
Good photo of eye can be scanned
Attacker could use photo of eye
Afghan woman was authenticated by iris scan of old photo
Story can be found here
To prevent attack, scanner could use light to be sure it is a “live” iris

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

http://pc.vietica.com/van.nguyen/InfoSec-VietNhat/InfoSec.htm


### Slide Image
This image identifies the School of Information and Communication Technology (SoICT) at Hanoi University of Science and Technology (HUST).

Key information provided includes:

*   **Institution:** School of Information and Communication Technology (SoICT), Hanoi University of Science and Technology.
*   **Physical Location:** The building depicted is labeled as "B1," indicating it serves as a primary facility for the school.
*   **Digital Contact Points:** 
    *   Official website: scict.hust.edu.vn
    *   Official Facebook community: fb.com/groups/soict
*   **Milestone:** The branding indicates the institution is celebrating its 25th anniversary.

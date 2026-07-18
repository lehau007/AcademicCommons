## Identity Authentication

- With extra material for further reading, indicated by symbol *

---

## Authentication

- The process of verifying the identity of a user, device, or other entity in a computer system, often as a prerequisite to allowing access to resources in a system.

---

## Authentication vs. Authorization

| Authentication | Authorization |
|----------------|--------------|
| Who are you?   | What are you allowed to do? |
| Prove your identity | Prove your right to access |
| Examples: password, biometrics, security token | Examples: file permissions, access control lists, capabilities |

---

## Authentication Factors

- Something you know (password, PIN)
- Something you have (smart card, token)
- Something you are (biometrics)
- Somewhere you are (location)
- Something you do (behavioral biometrics)

---

## Multi-Factor Authentication

- Using more than one authentication factor
- Increases security
- Examples:
  - ATM: card (have) + PIN (know)
  - Online banking: password (know) + SMS code (have)
  - Smartphone unlock: fingerprint (are) + PIN (know)

---

## Passwords

- Most common authentication method
- Weaknesses:
  - Easy to guess or brute-force
  - Users choose weak passwords
  - Susceptible to phishing and keylogging
- Best practices:
  - Use strong, unique passwords
  - Use a password manager
  - Enable multi-factor authentication

---

## Biometrics

- Use physical characteristics to authenticate
- Examples: fingerprint, face recognition, iris scan
- Advantages:
  - Difficult to forge
  - Convenient
- Disadvantages:
  - Privacy concerns
  - False positives/negatives
  - Cannot be changed if compromised

---

## Security Tokens

- Physical devices used to authenticate
- Examples: smart cards, USB tokens, OTP generators
- Advantages:
  - Difficult to duplicate
  - Can be combined with other factors
- Disadvantages:
  - Can be lost or stolen
  - Require additional hardware

---

## Authentication Protocols

- Challenge-response
- Zero-knowledge proofs
- Kerberos
- Public key infrastructure (PKI)
- OAuth, OpenID Connect

---

## Summary

- Authentication is verifying identity
- Multiple factors increase security
- Passwords are common but weak
- Biometrics and tokens offer alternatives
- Protocols enable secure authentication

---

## Further Reading *

- [NIST Digital Identity Guidelines](https://pages.nist.gov/800-63-3/)
- [OWASP Authentication Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/Authentication_Cheat_Sheet.html)
- [RFC 4949: Internet Security Glossary](https://datatracker.ietf.org/doc/html/rfc4949)

## Authentication

- Basics
- Passwords
- Challenge-Response
- Biometrics
- Location
- Multiple Methods

## Basics

- Authentication: binding of identity to subject
- Identity is that of external entity (my identity, Van, etc.)
- Subject is computer entity (process, etc.)

Note:  
message authentication is a different topic and already mentioned in the applications of hash functions

## Establishing Identity

- One or more of the following:
    - What entity knows (eg. password)
    - What entity has (eg. Identity card, smart card)
    - What entity is (eg. fingerprints, retinal characteristics)
    - Where entity is (eg. In front of a particular terminal)

## Authentication System

- We need a formal definition, rather abstract view, of an AS 
- A 5-tuple (A, C, F, L, S)
- A – a set: information that proves identity
- C – a set: information stored on computer and used to validate authentication information
- F: a set of complementation functions; f : A → C
- To compute complement information from identity information
- L: authentication functions that prove identity
- S: functions enabling entity to create, alter information in A or C

## Example

- Password system, with passwords stored on line in clear text
- A set of strings making up passwords
- C = A
- F singleton set of identity function { I }
- L single equality test function { eq }
- S function to set/change password

## Passwords

- Sequence of characters
  - Examples: 10 digits, a string of letters, etc.
  - Generated randomly, by user, by computer with user input
- Sequence of words
  - Examples: pass-phrases
- Algorithms
  - Examples: challenge-response, one-time passwords

## Storage

- Store as cleartext
- If password file compromised, all passwords revealed
- Encipher file
- Need to have decipherment, encipherment keys in memory
- Reduces to previous problem 🡺 need something else
- Solution: Instead store one-way hash of password
- Got the file, attacker must still guess passwords or invert the hash values

## Example: Unix

- By definition, a 5-tuple (A, C, F, L, S)
- A – a set: information that proves identity
  - A = { strings of 8 chars or less }
- C – a set: information stored on computer and used to validate authentication information
  - C = {hash values of password}
- F: a set of complementation functions; f : A → C
  - F = { versions of modified DES }
- L: authentication functions that prove identity
  - L = { login, su, … }
- S: functions enabling entity to create, alter information in A or C
  - S = { passwd, nispasswd, passwd+, … }

## Example: Unix

- By definition, a 5-tuple (A, C, F, L, S)
- A – a set: information that proves identity
    - A = { strings of 8 chars or less }
- C – a set: information stored on computer and used to validate authentication information
    - C = {hash values of password}
- F: a set of complementation functions; f : A → C
    - F = { versions of modified DES }
- L: authentication functions that prove identity
    - L = { login, su, … }
- S: functions enabling entity to create, alter information in A or C
    - S = { passwd, nispasswd, passwd+, … }

## Attacking passwords

- Goal: find a ∈ A such that:
- For some f ∈ F, f(a) = c ∈ C
- c is associated with entity

Two ways to determine whether a meets these requirements:
- By trying computing f(a) for a set of a values until succeed
- By trying calling I(a) until succeed (I(a) returns true)

## Preventing Attacks

- How to prevent this:
    - Hide at least one of a, f, or c 
        - Prevents obvious attack from above
        - Example: UNIX/Linux shadow password files
            - Hides the c’s
    - Block access to all l ∈ L or result of l(a)
        - Prevents attacker from knowing if guess succeeded
        - Example: preventing any logins to an account from a network
            - Prevents knowing results of l (or accessing l)

## Dictionary Attacks

- Trial-and-error from a list of potential passwords
- Off-line: know f and c’s, and repeatedly try different guesses g ∈ A until the list is done or passwords guessed
- Examples: crack, john-the-ripper
- On-line: have access to functions in L and try guesses g until some l(g) succeeds
- Examples: trying to log in by guessing a password

## Success probability over a time period

- Anderson’s formula:
- P = probability of guessing a password in specified period of time
- G = number of guesses tested in 1 time unit
- T = number of time units
- N = number of possible passwords (|A|)
- Then [Formula: P ≥ TG/N]

## Example

- Goal
    - Passwords drawn from a 96-char alphabet
    - Can test 10^4 guesses per second
    - Probability of a success to be 0.5 over a 365 day period
    - What is minimum password length?

- Solution
    - [Formula: N ≥ TG/P] = (365×24×60×60)×10^4/0.5 = 6.31×10^11
    - Choose s such that [Formula: Σsj=0 96j ≥ N]
    - So s ≥ 6, meaning passwords must be at least 6 chars long

## Exercise

- X = number defined by last 2 digits of your student ID; Y = X mod 4
- Assume that H is a cryptographic hash function with output size (Y+2)*16 bits.
- Assume that Scorpion-i (i=1-9) is a specifically designed line of hardware chips for computing H, where Scorpion-i can create 10i * 1000 hash values a second (e.g. Scorpion-2 can do 100,000 hashes/sec).
- This product line is the best, fastest and affordable, in the market, priced at ii/2 *$1000 (e.g $2000 for i=2, $16000 for i=4).
- An authentication system requires its users to pick their passwords of length exactly 6 from an alphabet of size N=(X mod 50)+ 40.
- Using H, this system maintains the hash values of the passwords of all the users.
- An enemy, who has gained access to this hashed password file, aims to launch an off-line attack to break the password of an important user.
- Using the Scorpion chips, how much the enemy has to spend in order to finish within a month with success probability (6+Y)*10%?

## On password selection

- Random selection
- Any password from A equally likely to be selected
- Pronounceable passwords
- User selection of passwords

## Pronounceable Passwords

- Generate phonemes randomly
- Phoneme is unit of sound, eg. cv, vc, cvc, vcv
- Examples: helgoret, juttelon are; przbqxdfl, zxrptglfn are not
- Problem: too few
- Solution: key crunching
  - Run long key through hash function and convert to printable sequence
  - Use this sequence as password

## User Selection

- Problem: people pick easy to guess passwords
- Based on account names, user names, computer names, place names
- Dictionary words (also reversed, odd capitalizations, control characters, “elite-speak”, conjugations or declensions, swear words, Torah/Bible/Koran/… words)
- Too short, digits only, letters only
- License plates, acronyms, social security numbers
- Personal characteristics or foibles (pet names, nicknames, job characteristics, etc.)

## Picking Good Passwords

- “LlMm*2^Ap”
  - Names of members of 2 families
- “OoHeO/FSK”
  - Second letter of each word of length 4 or more in third line of third verse of Star-Spangled Banner, followed by “/”, followed by author’s initials 
- What’s good here may be bad there
  - “DMC/MHmh” bad at Dartmouth (“Dartmouth Medical Center/Mary Hitchcock memorial hospital”), ok here
- Why are these now bad passwords? ☹

## Proactive Password Checking

- Analyze proposed password for “goodness”
- Always invoked
- Can detect, reject bad passwords for an appropriate definition of “bad”
- Discriminate on per-user, per-site basis
- Needs to do pattern matching on words
- Needs to execute subprograms and use results
  - Spell checker, for example
- Easy to set up and integrate into password selection system

## Salting

- Goal: slow dictionary attacks
- Method: perturb hash function so that:
  - Parameter controls which hash function is used
  - Parameter differs for each password
- So given n password hashes, and therefore n salts, need to hash guess n times

## Examples

- Vanilla UNIX method
    - Use DES to encipher 0 message with password as key; iterate 25 times
    - Perturb E table in DES in one of 4096 ways
    - 12 bit salt flips entries 1–11 with entries 25–36
- Alternate methods
    - Use salt as first part of input to hash function

## Unix actually is …

- UNIX system standard hash function
- Hashes password into 11 char string using one of 4096 hash functions

### As authentication system:
- A = { strings of 8 chars or less }
- C = { 2 char hash id || 11 char hash }
- F = { 4096 versions of modified DES }
- L = { login, su, … }
- S = { passwd, nispasswd, passwd+, … }

## Exercise

- Assume that H is a cryptographic hash function with output size (Y+2)*16 bits.
- Assume that Scorpion-i (i=1-9) is a specifically designed line of hardware chips for computing H, where Scorpion-i can create 10i * 1000 hash values a second, priced at ii/2 *$1000.

### 1. An authentication system requires its users to pick their passwords of length exactly 6 from an alphabet of size N=(X mod 50)+ 40. Using H, this system maintains the hash values of the passwords of all the users. An enemy, who has gained access to this hashed password file, aims to launch an off-line attack to break the password of an important user. Using the Scorpion chips, how much the enemy has to spend in order to finish within a month with success probability (6+Y)*10%?

### 2. The owner decides to enhance the above password system by using salt so that the enemy will need to spend at least 10 times the above mentioned amount of money to achieve the same goal. How many salt bits he/she need to use to achieve this purpose ?

## Password Cracking: Do the Math*

- Assumptions:
- Passwords are 8 characters, 128 choices per character
- Then 128^8 = 2^56 possible passwords
- There is a password file with 2^10 passwords
- Attacker has dictionary of 2^20 common passwords
- Probability 1/4 that password is in dictionary
- Work is measured by number of hashes

* Further reading

## Part 2 ⎯ Access Control

- Salt with slow hash *
- Hash password with salt
- Choose random salt s and compute [Formula: y = h(password, s)]
- and store (s,y) in the password file
- Note that the salt s is not secret
- Analogous to IV
- Still easy to verify salted password
- But lots more work for Hacker
- Why?

## Password Cracking: Case I

- Attack 1 specific password without using a dictionary
- E.g., administrator’s password
- Must try [Formula: 2^56/2 = 2^55] on average
- Like exhaustive key search
- Does salt help in this case?

## Password Cracking: Case II *

- Attack 1 specific password with dictionary
- With salt
- Expected work: [Formula: Expected work calculation]
- In practice, try all pwds in dictionary…
- …then work is at most 2^20 and probability of success is 1/4 
- What if no salt is used?
- One-time work to compute dictionary: 2^20
- Expected work is of same order as above
- But with precomputed dictionary hashes, the  “in practice” attack is essentially free…

## Password Cracking: Case III *

- Any of 1024 pwds in file, without dictionary
- Assume all 2^10 passwords are distinct 
- Need 2^5.5 comparisons before expect to find pwd

- If no salt is used
  - Each computed hash yields 2^10 comparisons
  - So expected work (hashes) is 2^5.5/2^10 = 2^4.5

- If salt is used
  - Expected work is 2^5.5 
  - Each comparison requires a hash computation

## Password Cracking: Case IV *

- Any of 1024 pwds in file, with dictionary
- Prob. one or more pwd in dict.: 1 – (3/4)1024 ≈ 1
- So, we ignore case where no pwd is in dictionary
- If salt is used, expected work less than 222
- See book, or slide notes for details
- Work ≈ size of dictionary / P(pwd in dictionary)
- What if no salt is used? 
- If dictionary hashes not precomputed, work is about 219/210 = 29

## Guessing Through L

- Cannot prevent these
- Otherwise, legitimate users cannot log in
- Make them slow
  - Backoff
  - Disconnection
  - Disabling
- Be very careful with administrative accounts!
- Jailing
  - Allow in, but restrict activities

## Password Aging

- Force users to change passwords after some time has expired
- How do you force users not to re-use passwords?
  - Record previous passwords
  - Block changes for a period of time
- Give users time to think of good passwords
  - Don’t force them to change before they can log in
  - Warn them of expiration days in advance

## Challenge-Response

- User, system share a secret function f (in practice, f is a known function with unknown parameters, such as a cryptographic key)
- user
- system
- request to authenticate
- user
- system
- random message r (the challenge)
- user
- system
- f(r) (the response)

## Pass Algorithms

- Challenge-response with the function f itself a secret
- Challenge is a random string of characters 
- Response is some function of that string 
- Usually used in conjunction with fixed, reusable password

---

## Slide Image

This visual element is a **login form** for a website. It contains the following components relevant to learning:

- **Username Field**: A text box where users enter their unique identifier.
- **Password Field**: A text box (with masked input) for entering a secret password.
- **CAPTCHA**: A security feature to distinguish human users from bots. The user must type the two distorted words shown in the image ("asbury law") into the provided text box.
- **Login Button**: A button to submit the entered credentials and CAPTCHA for authentication.

This form demonstrates a typical authentication process, including the use of CAPTCHA for added security.

## One-Time Passwords

- Password that can be used exactly once
- After use, it is immediately invalidated
- Challenge-response mechanism
  - Challenge is number of authentications; response is password for that particular number
- Problems
  - Synchronization of user, system
  - Generation of good random passwords
  - Password distribution problem

## S/Key

- One-time password scheme based on idea of Lamport
- Uses one-way hash function (MD5 or SHA-1, for example)
- User chooses initial seed k
- System calculates:  
  - h(k) = k1, h(k1) = k2, …, h(kn–1) = kn
- Passwords are reverse order:  
  - p1 = kn, p2 = kn–1, …, pn–1 = k2, pn = k1

## S/Key Protocol

- System stores maximum number of authentications n, number of next authentication i, last correctly supplied password pi–1.
- System computes [Formula: h(pi) = h(kn–i+1) = kn–i+2 = pi–1]. If match with what is stored, system replaces pi–1 with pi and increments i.

## C-R and Dictionary Attacks

- Same as for fixed passwords
- Attacker knows challenge r and response f(r); if f encryption function, can try different keys
- May only need to know form of response; attacker can tell if guess correct by looking to see if deciphered object is of right form
- Example: Kerberos Version 4 used DES, but keys had 20 bits of randomness; Purdue attackers guessed keys quickly because deciphered tickets had a fixed set of bits in some locations

## Encrypted Key Exchange *

- Defeats off-line dictionary attacks
- Idea: random challenges enciphered, so attacker cannot verify correct decipherment of challenge
- Assume Alice, Bob share secret password s
- In what follows, Alice needs to generate a random public key p and a corresponding private key q
- Also, k is a randomly generated session key, and RA and RB are random challenges

## EKE Protocol *

- Now Alice, Bob share a randomly generated secret session key k

## Something You Have

- Something in your possession
- Examples include:
  - Car key
  - Laptop computer (or MAC address)
  - Password generator (next)
  - ATM card, smartcard, etc.

## Hardware Support

- Token-based authentication
- Used to compute response to challenge
- May encipher or hash challenge
- May require PIN from user
- Object user possesses to authenticate, e.g.
    - memory card (magnetic stripe)
    - smartcard
- Temporally-based
    - Every minute (or so) different number shown
    - Computer knows what number to expect when
    - User enters number and fixed password

## Memory Card

- store but do not process data
- magnetic stripe card, e.g. bank card
- electronic memory card
- used alone for physical access (e.g., hotel rooms)
- some with password/PIN (e.g., ATMs)
- Drawbacks of memory cards include:
  - need special reader
  - loss of token issues
  - user dissatisfaction (OK for ATM, not OK for computer access)

## Smartcard

- credit-card like 
- has own processor, memory, I/O ports
- ROM, EEPROM, RAM memory
- executes protocol to authenticate with reader/computer
- static: similar to memory cards
- dynamic: passwords created every minute; entered manually by user or electronically
- challenge-response: computer creates a random number; smart card provides its hash (similar to PK)
- also have USB dongles

## Slide Image

This visual element provides technical information about the physical and internal structure of a smartcard:

- **Smartcard Dimensions**: 
  - The card measures 85.6 mm in width and 54 mm in height.
  - These dimensions conform to ISO standard 7816-2.
- **Chip Location and Layout**:
  - The chip is embedded in the plastic card and is not visible from the outside.
  - The diagram shows a typical chip layout, which includes:
    - **RAM** (Random Access Memory)
    - **EEPROM** (Electrically Erasable Programmable Read-Only Memory)
    - **ROM** (Read-Only Memory)
    - **CPU** (Central Processing Unit)
    - **Crypto coprocessor** (for cryptographic operations)
- **Learning Value**:
  - The image teaches the standardized size of smartcards and the typical components found in their embedded chips, which are essential for understanding how smartcards function in secure transactions and data storage.

## Electronic identity cards

- An important application of smart cards

## A national e-identity (eID)

- Serves the same purpose as other national ID cards (e.g., a driver’s licence)
- Can provide stronger proof of identity

## A German card

- Personal data
- Document number
- Card access number (six digit random number)
- Machine readable zone (MRZ): the password
- Uses: ePass (government use), eID (general use), eSign (can have private key and certificate)

## User authentication with eID *

- eID is a digital identity card issued by the government
- eID can be used for authentication and digital signing
- eID is based on PKI (Public Key Infrastructure)
- eID is used for authentication in many e-services
- eID is used for digital signing in many e-services
- eID is used for encryption in many e-services
- eID is used for authentication in many e-services
- eID is used for digital signing in many e-services
- eID is used for encryption in many e-services

## Something You Are

- Biometric
- “You are your key” ⎯ Schneier
- Are
- Know
- Have

### Examples

- Fingerprint
- Handwritten signature
- Facial recognition
- Speech recognition
- Gait (walking) recognition
- “Digital doggie” (odor recognition)
- Many more!

## Why Biometrics?

- May be better than passwords
- But, cheap and reliable biometrics needed
- Today, an active area of research
- Biometrics are used in security today
    - Thumbprint mouse
    - Palm print for secure entry
    - Fingerprint to unlock car door, etc.
- But biometrics not really that popular
- Has not lived up to its promise/hype (yet?)

## Biometrics: core idea

- Automated measurement of biological, behavioral features that identify a person
- Fingerprints: optical or electrical techniques
    - Maps fingerprint into a graph, then compares with database
    - Measurements imprecise, so approximate matching algorithms used
- Voices: speaker verification or recognition
    - Verification: uses statistical techniques to test hypothesis that speaker is who is claimed (speaker dependent)
    - Recognition: checks content of answers (speaker independent)

## Fingerprint: Enrollment

- Capture image of fingerprint
- Enhance image
- Identify “points”

## Fingerprint: Recognition

- Extracted points are compared with information stored in a database
- Is it a statistical match?
- Aside: Do identical twins’ fingerprints differ?

## Other Characteristics

- Can use several other characteristics

- Eyes: patterns in irises unique
  - Measure patterns, determine if differences are random; or correlate images using statistical tests

- Faces: image, or specific characteristics like distance from nose to chin
  - Lighting, view of face, other noise can hinder this

- Keystroke dynamics: believed to be unique
  - Keystroke intervals, pressure, duration of stroke, where key is struck
  - Statistical tests used

## Biometric authentication

- Authenticate user based on one of their physical characteristics:
  - facial
  - fingerprint
  - hand geometry
  - retina pattern
  - iris
  - signature
  - voice

## Cost vs. Accuracy of Biometric Characteristics

This visual element is a two-dimensional graph that compares the cost and accuracy of various biometric characteristics used in user authentication schemes. The x-axis represents accuracy, while the y-axis represents cost. The biometric characteristics included in the graph are:

- Hand
- Signature
- Face
- Voice
- Retina
- Finger
- Iris

The position of each characteristic on the graph indicates its relative cost and accuracy. For example, "Iris" is positioned in the upper right corner, indicating that it is both high in cost and high in accuracy. "Voice" is positioned in the lower left corner, indicating that it is both low in cost and low in accuracy. The other characteristics fall somewhere in between these two extremes. This graph provides a visual representation of the trade-offs between cost and accuracy for different biometric authentication methods.

## Operation of a biometric system

- Verification is analogous to user login via a smart card and a PIN
- Identification is biometric info but no IDs; system compares with stored templates

## Slide Image

Here is the structured graph representation in JSON format, extracted from the diagram:

```json
{
  "nodes": [
    "User interface",
    "Biometric sensor",
    "Feature extractor",
    "Database",
    "Feature matcher"
  ],
  "edges": [
    {"from": "User interface", "to": "Biometric sensor", "direction": "->"},
    {"from": "Biometric sensor", "to": "Feature extractor", "direction": "->"},
    {"from": "Feature extractor", "to": "Database", "direction": "->", "context": "Enrollment"},
    {"from": "Feature extractor", "to": "Feature matcher", "direction": "->", "context": "Verification/Identification"},
    {"from": "Database", "to": "Feature matcher", "direction": "->", "context": "Verification/Identification"},
    {"from": "Feature matcher", "to": "User interface", "direction": "->", "context": "Verification"},
    {"from": "Feature matcher", "to": "User interface", "direction": "->", "context": "Identification"}
  ],
  "contexts": {
    "Enrollment": [
      "User interface -> Biometric sensor -> Feature extractor -> Database"
    ],
    "Verification": [
      "User interface -> Biometric sensor -> Feature extractor -> Feature matcher -> User interface",
      "Database -> Feature matcher"
    ],
    "Identification": [
      "User interface -> Biometric sensor -> Feature extractor -> Feature matcher -> User interface",
      "Database -> Feature matcher"
    ]
  }
}
```

## Explanation

- **Nodes**: All unique components in the diagrams.
- **Edges**: All possible connections, with directionality and context (enrollment, verification, identification).
- **Contexts**: Each process flow as a sequence of nodes.

## Biometric Accuracy

- Palm print: The system generates a matching score (a number) that quantifies similarity between the input and the stored template
- Concerns: sensor noise and detection inaccuracy
- Problems of false match/false non-match
- Further reading (Stallings textbook)

## Biometric Matching and Decision Threshold

- The visual element is a graph that illustrates the concept of **biometric matching** and the **decision threshold** used to distinguish between imposters and genuine users in a biometric system.
- **X-axis (Matching score, s):** Represents the matching score between a presented biometric feature and a reference feature.
- **Y-axis (Probability density function):** Represents the probability density of the matching scores.
- **Imposter profile:** The left bell curve represents the distribution of matching scores for imposters (unauthorized users). The average matching value of imposters is labeled.
- **Genuine user profile:** The right bell curve represents the distribution of matching scores for genuine users (authorized users). The average matching value of genuine users is labeled.
- **Decision threshold (t):** The vertical dashed line represents the threshold value. If a matching score is greater than this threshold, access is granted (match declared).
- **False nonmatch:** The blue-shaded area under the genuine user curve to the left of the threshold represents the probability of a genuine user being incorrectly rejected (false nonmatch).
- **False match:** The gray-shaded area under the imposter curve to the right of the threshold represents the probability of an imposter being incorrectly accepted (false match).
- **Learning value:** This diagram helps explain the trade-off between false matches and false nonmatches in biometric systems and the role of the decision threshold in balancing security and usability.

## Biometric Accuracy

- Can plot characteristic curve (2,000,000 comparisons)
- Pick threshold balancing error rates

## Slide Image

This visual element is a graph comparing the performance of five biometric measurement systems: Face, Fingerprint, Voice, Hand, and Iris. The graph uses a log-log scale to plot the false nonmatch rate (y-axis) against the false match rate (x-axis).

Key learning points from the graph:

- **Axes**: The x-axis represents the false match rate (the probability that an impostor is incorrectly accepted), and the y-axis represents the false nonmatch rate (the probability that a legitimate user is incorrectly rejected). Both axes use a logarithmic scale.
- **Curves**: Each biometric system is represented by a different curve or line, showing the trade-off between false match and false nonmatch rates for that system.
- **Performance**: Systems with curves closer to the bottom left corner (low false match and low false nonmatch rates) are more accurate. The Iris system (diamond) performs best, followed by Fingerprint (circle), Hand (white diamond), Voice (black square), and Face (blue circle).
- **Interpretation**: The graph allows for a direct comparison of the accuracy and reliability of different biometric systems, highlighting the strengths and weaknesses of each.

This graph is valuable for understanding the effectiveness of various biometric authentication methods and for making informed decisions about which system to use in different security contexts.

## Cautions

- These can be fooled!
- Assumes biometric device accurate in the environment it is being used in!
- Transmission of data to validator is tamperproof, correct

## Biometrics: The Bottom Line

- Biometrics are hard to forge
- But attacker could:
  - Steal Alice’s thumb
  - Photocopy Bob’s fingerprint, eye, etc.
  - Subvert software, database, “trusted path” …
  - And how to revoke a “broken” biometric?
- Biometrics are not foolproof
- Biometric use is relatively limited today
- That should change in the (near?) future

## Location – Just a brief

- If you know where user is, validate identity by seeing if person is where the user is
- Requires special-purpose hardware to locate user
- GPS (global positioning system) device gives location signature of entity
- Host uses LSS (location signature sensor) to get signature for entity

## Multiple Methods

- Example: “where you are” also requires entity to have LSS and GPS, so also “what you have”
- Can assign different methods to different tasks
- As users perform more and more sensitive tasks, must authenticate in more and more ways (presumably, more stringently)
- File describes authentication required
- Also includes controls on access (time of day, etc.), resources, and requests to change passwords

## Pluggable Authentication Modules

- [Content missing from provided text]

## PAM

- Idea: when program needs to authenticate, it checks central repository for methods to use
- Library call: pam_authenticate
- Accesses file with name of program in /etc/pam_d
- Modules do authentication checking
- sufficient: succeed if module succeeds
- required: fail if module fails, but all required modules executed before reporting failure
- requisite: like required, but don’t check all modules
- optional: invoke only if all previous modules fail

## Example PAM File

- auth	sufficient	/usr/lib/pam_ftp.so
- auth	required	/usr/lib/pam_unix_auth.so use_first_pass
- auth	required	/usr/lib/pam_listfile.so onerr=succeed \ 				item=user sense=deny file=/etc/ftpusers

For ftp:
- If user “anonymous”, return okay; if not, set PAM_AUTHTOK to password, PAM_RUSER to name, and fail
- Now check that password in PAM_AUTHTOK belongs to that of user in PAM_RUSER; if not, fail
- Now see if user in PAM_RUSER named in /etc/ftpusers; if so, fail; if error or not found, succeed

## Extended Material: Kerberos authentication protocol

- Material sources: 
  - History & some general info from Wiki
  - Details on Kerberos versions 4&5 from Stallings Text and slides

## Kerberos

- A computer network authentication protocol which allows nodes communicating over a non-secure network to prove their identity to one another in a secure manner.
- Aimed primarily at a client-server model, and it provides mutual authentication -- both the user and the server verify each other's identity.
- Messages are protected against eavesdropping & replay attacks.
- Kerberos builds on SKC and requires a trusted third party, and optionally may use public-key cryptography during certain phases of authentication.

## Kerberos

- named after the character Kerberos (or Cerberus), the ferocious three-headed guard dog of Hades (from Greek mythology)
- MIT developed Kerberos in 1988 to protect network services provided by Project Athena.
- 1st version was primarily designed by Steve Miller and Clifford Neuman based on the earlier Needham–Schroeder symmetric-key protocol. Ver 1 - 3 were experimental, internal.
- Kerberos version 4, the first public version, was released on January 24, 1989.
- Neuman and John Kohl published v5 in 1993 with the intention of overcoming existing limitations and security problems. Version 5 appeared as RFC 1510, which was then made obsolete by RFC 4120 in 2005. In 2005, the Internet Engineering Task Force (IETF) Kerberos working group updated specifications.

## Idea

- Ticket
- Issuer vouches for identity of requester of service
- Identifies sender
- Key Distribution Center (KDC) combines two servers: 
    - Authentication Server, AS (Also, Kerberos server)
    - Ticket Granting Server, TGS
- User u authenticates to AS
- Obtains ticket Tu,TGS for ticket granting service (TGS)
- User u wants to use service s:
    - User sends authenticator Au, ticket Tu,TGS to TGS asking for ticket for service
    - TGS sends ticket Tu,s to user
    - User sends Au, Tu,s to server as request to use s

## Kerberos v4 Overview

- a basic third-party authentication scheme
- have an Authentication Server (AS)
- users initially negotiate with AS to identify self
- AS provides a non-corruptible authentication credential (ticket granting ticket TGT)
- have a Ticket Granting server (TGS)
- users subsequently request access to other services from TGS on basis of users TGT
- using a complex protocol using DES

## Kerberos 4 Overview

- Kerberos is a network authentication protocol designed to provide secure authentication for users and services in a distributed environment.
- It uses secret-key cryptography to authenticate client-server applications and verify the identities of users and services.
- Kerberos 4 is an earlier version of the protocol, succeeded by Kerberos 5, but its core concepts remain foundational.

## Slide Image: Kerberos Authentication Process

Here is a structured graph representation of the Kerberos authentication process as depicted in the image:

### Node Labels

- User/Workstation
- Authentication Server (AS)
- Ticket-granting Server (TGS)
- Server

### Edge List with Directionality

- User/Workstation → Authentication Server (AS): request ticket-granting ticket
- Authentication Server (AS) → User/Workstation: ticket + session key
- User/Workstation → Ticket-granting Server (TGS): request service-granting ticket
- Ticket-granting Server (TGS) → User/Workstation: ticket + session key
- User/Workstation → Server: request service
- Server → User/Workstation: provide server authenticator

## Kerberos v4 Dialogue

- Let's break down the graph from the image into nodes, edges, and directionality, and then represent it in JSON format.

## Nodes

- C (Client)
- AS (Authentication Service)
- TGS (Ticket-Granting Service)
- V (Service/Server)

## Edge List & Directionality

- C → AS
- AS → C
- C → TGS
- TGS → C
- C → V
- V → C

## JSON Representation

```json
{
  "nodes": [
    {"id": "C", "label": "Client"},
    {"id": "AS", "label": "Authentication Service"},
    {"id": "TGS", "label": "Ticket-Granting Service"},
    {"id": "V", "label": "Service/Server"}
  ],
  "edges": [
    {"source": "C", "target": "AS", "label": "IDc, IDtgs, TS1"},
    {"source": "AS", "target": "C", "label": "EKc,..., Tickettgs"},
    {"source": "C", "target": "TGS", "label": "IDv, Tickettgs, Authenticatorc"},
    {"source": "TGS", "target": "C", "label": "EKc,..., Ticketv"},
    {"source": "C", "target": "V", "label": "Ticketv, Authenticatorc"},
    {"source": "V", "target": "C", "label": "EKc,v"}
  ]
}
```

## Explanation

- Each node represents a principal in the Kerberos authentication protocol.
- Each edge represents a message exchange, with the direction indicating the sender and receiver.
- The `label` for each edge is a summary of the message contents as shown in the image.

Let me know if you want a more detailed breakdown of the message contents or a specific graph format!

## Kerberos Version 5

- Developed in mid 1990’s
- Specified as Internet standard RFC 1510
- Provides improvements over v4
- Addresses environmental shortcomings
  - Encryption alg, network protocol, byte order, ticket lifetime, authentication forwarding, interrealm auth
- And technical deficiencies
  - Double encryption, non-std mode of use, session keys, password attacks

## Kerberos Realms

- A Kerberos environment consists of:
  - a Kerberos server
  - a number of clients, all registered with server
  - application servers, sharing keys with server
- This is termed a realm
- Typically a single administrative domain
- If have multiple realms, their Kerberos servers must share keys and trust

## Kerberos Realms

- Client requests ticket for local TGS from Kerberos_A_AS
- Kerberos_A_AS returns ticket for local TGS to Client
- Client requests ticket for remote TGS from Kerberos_A_TGS
- Kerberos_A_TGS returns ticket for remote TGS to Client
- Client requests ticket for remote server from Kerberos_B_TGS
- Kerberos_B_TGS returns ticket for remote server to Client
- Client requests remote service from Server

### Node Labels

- Client
- Kerberos_A_AS (Kerberos AS in Realm A)
- Kerberos_A_TGS (Kerberos TGS in Realm A)
- Kerberos_B_TGS (Kerberos TGS in Realm B)
- Kerberos_B_AS (Kerberos AS in Realm B)
- Server

### Edge List & Directionality

- Client → Kerberos_A_AS (request ticket for local TGS)
- Kerberos_A_AS → Client (ticket for local TGS)
- Client → Kerberos_A_TGS (request ticket for remote TGS)
- Kerberos_A_TGS → Client (ticket for remote TGS)
- Client → Kerberos_B_TGS (request ticket for remote server)
- Kerberos_B_TGS → Client (ticket for remote server)
- Client → Server (request remote service)

### JSON Representation

```json
{
  "nodes": [
    "Client",
    "Kerberos_A_AS",
    "Kerberos_A_TGS",
    "Kerberos_B_TGS",
    "Kerberos_B_AS",
    "Server"
  ],
  "edges": [
    {"source": "Client", "target": "Kerberos_A_AS", "label": "request ticket for local TGS"},
    {"source": "Kerberos_A_AS", "target": "Client", "label": "ticket for local TGS"},
    {"source": "Client", "target": "Kerberos_A_TGS", "label": "request ticket for remote TGS"},
    {"source": "Kerberos_A_TGS", "target": "Client", "label": "ticket for remote TGS"},
    {"source": "Client", "target": "Kerberos_B_TGS", "label": "request ticket for remote server"},
    {"source": "Kerberos_B_TGS", "target": "Client", "label": "ticket for remote server"},
    {"source": "Client", "target": "Server", "label": "request remote service"}
  ]
}
```

Let me know if you need the realms or Kerberos components (AS, TGS) grouped differently!

## Protocol

- [From Wiki]
- Client Authentication to the AS
- Client Service Authorization
- Client Service Request

---

## Slide Image

Here’s a structured graph representation in JSON, based on the diagram:

---

## Node Labels

- Client (C)
- Authentication Server (AS)
- Ticket-granting Server (TGS)
- Service Server (SS)

---

## Edge List & Directionality

- C → AS (User ID + requested service)
- AS → C (Msg A, Msg B)
- C → TGS (Msg C, Msg D)
- TGS → C (Msg E, Msg F)
- C → SS (Msg E, Msg G)
- SS → C (Msg H)

---

## JSON Representation

```json
{
  "nodes": [
    {"id": "C", "label": "Client"},
    {"id": "AS", "label": "Authentication Server"},
    {"id": "TGS", "label": "Ticket-granting Server"},
    {"id": "SS", "label": "Service Server"}
  ],
  "edges": [
    {"source": "C", "target": "AS", "label": "User ID + requested service"},
    {"source": "AS", "target": "C", "label": "Msg A, Msg B"},
    {"source": "C", "target": "TGS", "label": "Msg C, Msg D"},
    {"source": "TGS", "target": "C", "label": "Msg E, Msg F"},
    {"source": "C", "target": "SS", "label": "Msg E, Msg G"},
    {"source": "SS", "target": "C", "label": "Msg H"}
  ]
}
```

---

## Explanation

- Each node represents a component in the Kerberos authentication protocol.
- Each edge represents a message flow, with directionality indicated by "source" and "target".
- The "label" on each edge describes the message(s) exchanged.

Let me know if you need a more detailed breakdown of each message!

## Kerberos v5 Dialogue

- The following is a structured graph representation in JSON, extracted from the diagram:

```json
{
  "nodes": [
    {"id": "C", "label": "Client"},
    {"id": "AS", "label": "Authentication Service"},
    {"id": "TGS", "label": "Ticket-Granting Service"},
    {"id": "V", "label": "Server"}
  ],
  "edges": [
    {"source": "C", "target": "AS", "label": "Options || ID_c || Realm_c || ID_tgs || Times || Nonce_1", "direction": "C → AS"},
    {"source": "AS", "target": "C", "label": "Realm_c || ID_c || Ticket_tgs || EK_c,tgs[Flags || Realm_c || ID_c || Times || Nonce_1 || Realm_c || ID_tgs]", "direction": "AS → C"},
    {"source": "C", "target": "TGS", "label": "Options || ID_t || Times || Nonce_2 || Ticket_tgs || Authenticator_c", "direction": "C → TGS"},
    {"source": "TGS", "target": "C", "label": "Realm_t || ID_t || Ticket_tgs || EK_c,tgs[Flags || Realm_t || ID_t || Times || Nonce_2 || Realm_t || ID_t]", "direction": "TGS → C"},
    {"source": "C", "target": "V", "label": "Options || Ticket_t || Authenticator_c", "direction": "C → V"},
    {"source": "V", "target": "C", "label": "EK_c,v[TS_2 || Subkey || Seq#]", "direction": "V → C"}
  ]
}
```

## Explanation

- **Nodes**: Represent the entities involved (Client, Authentication Service, Ticket-Granting Service, Server).
- **Edges**: Represent the messages exchanged, with the message content as the label and the directionality indicated.
- The directionality is shown in the "direction" field (e.g., "C → AS" means from Client to Authentication Service).

If you need a different format or more details, let me know!

## Federated Identity Management

- Use of common identity management scheme across multiple enterprises & numerous applications 
- Supporting many thousands, even millions of users 
- Principal elements are:
  - authentication
  - authorization
  - accounting
  - provisioning
  - workflow automation
  - delegated administration
  - password synchronization
  - self-service password reset
  - federation
- Kerberos contains many of these elements

## Identity Management

- Identity management involves several key entities and their interactions.
- The main entities are: Principal, Administrator, Attribute service, Identity Provider, and Data consumer.
- The relationships between these entities are directed, showing the flow of information or actions.

## Slide Image

Here is a structured graph representation in JSON format, extracted from the diagram:

```json
{
  "nodes": [
    "Principal",
    "Administrator",
    "Attribute service",
    "Identity Provider",
    "Data consumer"
  ],
  "edges": [
    {"from": "Principal", "to": "Identity Provider", "label": "authenticate, manage their identity elements"},
    {"from": "Principal", "to": "Attribute service", "label": "provide attributes"},
    {"from": "Administrator", "to": "Attribute service", "label": "provide attributes"},
    {"from": "Attribute service", "to": "Identity Provider", "label": "provide attributes"},
    {"from": "Identity Provider", "to": "Data consumer", "label": "obtain identifiers, attribute references"},
    {"from": "Data consumer", "to": "Attribute service", "label": "apply references to obtain attribute data"}
  ],
  "directionality": "Directed"
}
```

## Explanation

- **Nodes**: The main entities in the diagram.
- **Edges**: The relationships between the entities, with labels describing the interaction.
- **Directionality**: All edges are directed, showing the flow of information or actions.

## Identity Federation

- **Nodes**: User, Identity Provider (source domain), Administrator, Service Provider (destination domain)
- **Edges**: 
  - User → Identity Provider (source domain) (Step 1)
  - Administrator → Identity Provider (source domain) (Step 2)
  - Service Provider (destination domain) → Identity Provider (source domain) (Step 3)
  - Service Provider (destination domain) → User (Step 4)
- **Directionality**: All edges are directed, as indicated by arrows in the diagram.
- **Labels**: Each edge is labeled according to the step number in the diagram.

## Standards Used

- Security Assertion Markup Language (SAML)
- XML-based language for exchange of security information between online business partners
- Part of OASIS (Organization for the Advancement of Structured Information Standards) standards for federated identity management
- e.g. WS-Federation for browser-based federation
- Need a few mature industry standards

## Federated Identity Examples

- Nodes: Each entity or system in the diagram is represented as a node.
- Edges: Each arrow in the diagram is represented as a directed edge, indicating the direction of interaction or authentication flow.
- Directionality: All edges are directed, as indicated by the arrows in the diagram.

### Graph Representation (JSON)

```json
{
  "nodes": [
    "End user (employee)",
    "Workplace.com (employee portal)",
    "User store (Workplace.com)",
    "Health.com",
    "User store (Health.com)",
    "PartsSupplier.com",
    "User store (PartsSupplier.com)",
    "Workplace.com (employee portal, parts supplier)",
    "Workplace.com (Procurement application)",
    "PinSupplies.com (Purchasing Web service)",
    "E-ship.com (Shipping Web service)"
  ],
  "edges": [
    {
      "source": "End user (employee)",
      "target": "Workplace.com (employee portal)",
      "direction": "directed"
    },
    {
      "source": "Workplace.com (employee portal)",
      "target": "User store (Workplace.com)",
      "direction": "directed"
    },
    {
      "source": "Workplace.com (employee portal)",
      "target": "Health.com",
      "direction": "directed"
    },
    {
      "source": "Health.com",
      "target": "User store (Health.com)",
      "direction": "directed"
    },
    {
      "source": "End user (employee)",
      "target": "Workplace.com (employee portal, parts supplier)",
      "direction": "directed"
    },
    {
      "source": "Workplace.com (employee portal, parts supplier)",
      "target": "User store (Workplace.com)",
      "direction": "directed"
    },
    {
      "source": "Workplace.com (employee portal, parts supplier)",
      "target": "PartsSupplier.com",
      "direction": "directed"
    },
    {
      "source": "PartsSupplier.com",
      "target": "User store (PartsSupplier.com)",
      "direction": "directed"
    },
    {
      "source": "Workplace.com (Procurement application)",
      "target": "PinSupplies.com (Purchasing Web service)",
      "direction": "directed"
    },
    {
      "source": "PinSupplies.com (Purchasing Web service)",
      "target": "E-ship.com (Shipping Web service)",
      "direction": "directed"
    }
  ]
}
```

### Explanation

- **Nodes**: Each entity or system in the diagram is represented as a node.
- **Edges**: Each arrow in the diagram is represented as a directed edge, indicating the direction of interaction or authentication flow.
- **Directionality**: All edges are directed, as indicated by the arrows in the diagram.

## FIM vs. SSO

- SSO: Single Sign-On
  - Allows users to access multiple web applications at once, using just one set of credentials.
  - Beyond the workforce, companies can utilize SSO to help customers access various sections of one account.
- FIM
  - As a tool, SSO fits within the broader model of FIM.
  - The key difference between SSO and FIM is while SSO is designed to authenticate a single credential across various systems within one organization, federated identity management systems offer single access to a number of applications across various enterprises.

## Extended Material *Biometrics

- Slides borrowed from Mark Stamp’s web
- https://www.cs.sjsu.edu/~stamp/infosec/powerpoint/

## Biometrics

- Biometrics = “life measurement”
- Use of unique biological characteristics to identify a person
- Examples:
  - Fingerprints
  - Hand geometry
  - Retina
  - Iris
  - Face
  - Voice
  - DNA

## Biometrics

- Used for authentication
- Used for identification
- Used for screening

## Biometric System

- Sensor
- Feature extraction
- Matching
- Decision

## Biometric System

- Enrollment
- Verification
- Identification

## Biometric System

- False match rate (FMR)
- False nonmatch rate (FNMR)
- Equal error rate (EER)
- Failure to enroll (FTE)
- Failure to acquire (FTA)

## Biometric System

- Performance depends on:
  - Population
  - Environment
  - Application

## Biometric System

- Spoofing
- Replay
- Trojan horse
- Hill climbing
- Side channel
- Coercion

## Biometric System

- Privacy
- Ethics
- Law

## Biometric System

- Multimodal
- Multispectral
- Multitemporal

## Biometric System

- Fusion
- Template protection
- Cancelable biometrics
- Homomorphic encryption
- Secure multiparty computation

## Biometric System

- Standards
- Interoperability
- Usability
- Accessibility

## Biometric System

- Research
- Development
- Deployment
- Evaluation

## Biometric System

- Future
- Challenges
- Opportunities

## Something You Are

- Biometric
- “You are your key” ⎯ Schneier
- Are
- Know
- Have

### Examples

- Fingerprint
- Handwritten signature
- Facial recognition
- Speech recognition
- Gait (walking) recognition
- “Digital doggie” (odor recognition)
- Many more!

## Ideal Biometric

- Universal ⎯ applies to (almost) everyone
  - In reality, no biometric applies to everyone
- Distinguishing ⎯ distinguish with certainty
  - In reality, cannot hope for 100% certainty
- Permanent ⎯ physical characteristic being measured never changes
  - In reality, OK if it to remains valid for long time
- Collectable ⎯ easy to collect required data 
  - Depends on whether subjects are cooperative
  - Also, safe, user-friendly, and ???

## Identification vs Authentication

- Identification ⎯ Who goes there?
  - Compare one-to-many
  - Example: FBI fingerprint database
- Authentication ⎯ Are you who you say you are?
  - Compare one-to-one
  - Example: Thumbprint mouse
- Identification problem is more difficult
  - More “random” matches since more comparisons
- We are (mostly) interested in authentication

## Enrollment vs Recognition

- Enrollment phase
  - Subject’s biometric info put into database
  - Must carefully measure the required info
  - OK if slow and repeated measurement needed
  - Must be very precise
  - May be a weak point in real-world use
- Recognition phase
  - Biometric detection, when used in practice
  - Must be quick and simple
  - But must be reasonably accurate

## Cooperative Subjects?

- Authentication ⎯ cooperative subjects
- Identification ⎯ uncooperative subjects
- For example, facial recognition
- Used in Las Vegas casinos to detect known cheaters (also, terrorists in airports, etc.)
- Often, less than ideal enrollment conditions
- Subject will try to confuse recognition phase
- Cooperative subject makes it much easier
- We are focused on authentication
- So, we can assume subjects are cooperative

## Biometric Errors

- Fraud rate versus insult rate
- Fraud ⎯ Trudy mis-authenticated as Alice
- Insult ⎯ Alice not authenticated as Alice
- For any biometric, can decrease fraud or insult, but other one will increase
- For example:
    - 99% voiceprint match ⇒ low fraud, high insult
    - 30% voiceprint match ⇒ high fraud, low insult
- Equal error rate: rate where fraud == insult
- A way to compare different biometrics

## Part 2 ⎯ Access Control

- 89

## Fingerprint History

- 1823 ⎯ Professor Johannes Evangelist Purkinje discussed 9 fingerprint patterns
- 1856 ⎯ Sir William Hershel used fingerprint (in India) on contracts
- 1880 ⎯ Dr. Henry Faulds article in Nature about fingerprints for ID
- 1883 ⎯ Mark Twain’s Life on the Mississippi (murderer ID’ed by fingerprint)

## Fingerprint History

- 1888 ⎯ Sir Francis Galton developed classification system
- His system of “minutia” can be used today
- Also verified that fingerprints do not change
- Some countries require fixed number of “points” (minutia) to match in criminal cases
- In Britain, at least 15 points 
- In US, no fixed number of points

## Fingerprint Comparison

- Loop (double)
- Whorl
- Arch
- Examples of loops, whorls, and arches
- Minutia extracted from these features

## Slide Image

- This image shows a close-up of a fingerprint.
- The fingerprint is made up of ridges and valleys, which form unique patterns.
- These patterns can be used for identification purposes because no two fingerprints are exactly alike.
- The image highlights the loops and whorls that are common in fingerprint patterns.
- Fingerprints are commonly used in forensic science for personal identification.

## Slide Image

- This is a close-up image of a fingerprint.
- The fingerprint is composed of a series of ridges and valleys that form unique patterns.
- The central pattern in this fingerprint is a whorl, which is characterized by circular or spiral ridges.
- The surrounding ridges curve around the central whorl.
- Fingerprints are unique to each individual and are used for identification purposes in forensic science.

## Slide Image

- This is a close-up image of a fingerprint.
- The pattern consists of ridges and valleys, which are unique to each individual.
- Fingerprints are used in forensic science for identification purposes because no two people have the same fingerprint pattern.
- The image shows a loop pattern, which is one of the three main types of fingerprint patterns, the other two being whorls and arches.

## Fingerprint: Enrollment

- Capture image of fingerprint
- Enhance image
- Identify “points”

## Fingerprint: Recognition

- Extracted points are compared with information stored in a database
- Is it a statistical match?
- Aside: Do identical twins’ fingerprints differ?

## Hand Geometry

- A popular biometric
- Measures shape of hand
    - Width of hand, fingers
    - Length of fingers, etc.
- Human hands not so unique
- Hand geometry sufficient for many situations
    - OK for authentication
    - Not useful for ID problem

## Hand Geometry

- Advantages
  - Quick ⎯ 1 minute for enrollment, 5 seconds for recognition
  - Hands are symmetric ⎯ so what?
- Disadvantages
  - Cannot use on very young or very old
  - Relatively high equal error rate

## Iris Patterns

- Iris pattern development is “chaotic”
- Little or no genetic influence
- Even for identical twins, uncorrelated
- Pattern is stable through lifetime

---

## Slide Image: Human Eye Cross-section

This image is a detailed cross-section of the human eye, showing the following labeled anatomical structures:

- **Sclera (S):** The tough, white outer layer of the eyeball.
- **Iris (I):** The colored part of the eye, which controls the size of the pupil.
- **Cornea (C):** The transparent front part of the eye that covers the iris, pupil, and anterior chamber.

These structures are essential for protecting the eye, controlling light entry, and focusing vision.

---

## Slide Image: Close-up of Human Eye

This is a close-up image of a human eye. The black circle in the center is the pupil, which controls the amount of light that enters the eye. The colored area surrounding the pupil is the iris, which contains muscles that adjust the size of the pupil. The iris also determines eye color, which in this case appears to be blue or gray. The white area at the outer edge is the sclera, which provides structure and protection. The detailed patterns in the iris are unique to each individual and are used in biometric identification.

---

## Slide Image: External Anatomy of the Human Eye

This is a close-up image of a human eye. Key anatomical features visible include:

- **Pupil:** The black circular opening in the center of the iris that allows light to enter the eye.
- **Iris:** The colored part of the eye surrounding the pupil, which controls the size of the pupil and thus the amount of light that enters.
- **Sclera:** The white part of the eye, which provides structure and protection.
- **Eyelids:** The upper and lower folds of skin that can close to protect the eye.
- **Eyelashes:** Small hairs on the edge of the eyelids that help protect the eye from debris.
- **Caruncle:** The small, pink, globular nodule at the inner corner of the eye, which contains sweat and oil glands.
- **Blood vessels:** Small red lines visible in the sclera, which supply blood to the eye tissues.

This image can be used to study the external anatomy of the human eye and understand how its structures function together to protect the eye and regulate vision.

## Iris Recognition: History

- 1936 ⎯ suggested by ophthalmologist
- 1980s ⎯ James Bond film(s)
- 1986 ⎯ first patent appeared
- 1994 ⎯ John Daugman patents new-and-improved technique
- Patents owned by Iridian Technologies

## Iris Scan

- Scanner locates iris
- Take b/w photo
- Use polar coordinates…
- 2-D wavelet transform
- Get 256 byte iris code

---

## Slide Image: Spectrogram

This image is a **spectrogram**, which is a visual representation of the spectrum of frequencies in a signal as it varies with time.

**Key learning points:**
- **X-axis:** Represents time (in arbitrary units, likely milliseconds or frames).
- **Y-axis:** Represents frequency (in arbitrary units, likely Hertz or frequency bins).
- **Color intensity:** Represents the amplitude (energy) of the frequencies at a given time. Brighter areas indicate higher amplitude (louder or more energy), while darker areas indicate lower amplitude (softer or less energy).

**Educational value:**
- Spectrograms are used in audio analysis, speech recognition, music analysis, and many other fields to visualize how the frequency content of a signal changes over time.
- They help identify patterns, such as harmonics, formants, or noise, that are not easily seen in the raw waveform.

---

## Slide Image: 3D Wireframe Plot

This is a 3D wireframe plot of a mathematical surface. The axes are labeled with numbers from 0 to 60 on the horizontal axes and from -0.5 to 1 on the vertical axis. The surface has a central peak and dips symmetrically around it, suggesting it is a plot of a function with a single maximum at the center and minima surrounding it. This type of plot is commonly used to visualize mathematical functions of two variables, such as z = f(x, y), and helps in understanding the behavior of the function in three-dimensional space.

---

## Slide Image: Eye Heatmap

This image shows a close-up of a human eye with a heatmap overlay. The heatmap uses a color gradient from yellow (hotter areas) to red (cooler areas) to indicate temperature or intensity values across the eye region.

A blue circle is drawn around the iris, and a crosshair is centered on the pupil. These markings are likely used for eye-tracking or biometric analysis, helping to locate and measure the position and size of the iris and pupil. The axes on the left and bottom indicate pixel coordinates, which are useful for referencing specific locations within the image.

---

## Slide Image: 3D Wireframe Function

This is a 3D wireframe plot of a mathematical function, likely a 2D Gaussian or a similar bell-shaped surface. The axes are labeled with numerical values, with the horizontal axes ranging from 0 to 60 and the vertical axis ranging from -1 to 1. The plot visually represents how the function's value changes over a grid of (x, y) coordinates, with the highest point at the center and values decreasing symmetrically outward. This type of plot is used to illustrate surface topology, function behavior, or data distributions in three dimensions.

---

## Slide Image: Line Plot

This image is a line plot with the following learning-relevant features:

- The x-axis ranges from 0 to 1200.
- The y-axis ranges from -0.1 to 0.3.
- The data appears to be a time series or sequence, with values that decrease in amplitude as the x-value increases.
- The plot shows high variability at the beginning, with spikes that gradually become smaller and less frequent as the sequence progresses.
- There are distinct "blocks" or segments where the amplitude and frequency of the spikes change, suggesting the data may be divided into different regimes or phases.

This pattern is typical of a signal that is being damped or filtered over time, or it could represent a process that is stabilizing or converging. The plot could be used to illustrate concepts such as signal decay, convergence, or the effect of noise reduction in a system.

---

## Slide Image: ATM Use

The image shows a person using an ATM (Automated Teller Machine). The individual is holding a card and appears to be interacting with the machine, possibly entering information or retrieving cash. This visual element is useful for illustrating concepts related to banking, financial transactions, or the use of technology in everyday life.

## Measuring Iris Similarity

- Based on Hamming distance
- Define d(x,y) to be:
  - # of non-match bits / # of bits compared
- d(0010,0101) = 3/4 and d(101111,101001) = 1/3
- Compute d(x,y) on 2048-bit iris code
- Perfect match is d(x,y) = 0
- For same iris, expected distance is 0.08
- At random, expect distance of 0.50
- Accept iris scan as match if distance < 0.32

## Iris Scan Error Rate

- Fraud rate
- Equal error rate

## Histogram of Similarity Scores

This histogram shows the distribution of similarity scores for two types of image comparisons: "same" (images of the same person) and "different" (images of different people). The x-axis represents the similarity score, ranging from 0.0 to 1.0. The y-axis represents the frequency of each score.

Key learning points:

- The "same" distribution (left) has a mean similarity score of 0.110 and a standard deviation of 0.065.
- The "different" distribution (right) has a mean similarity score of 0.458 and a standard deviation of 0.197.
- The two distributions are well separated, with minimal overlap, indicating that the similarity metric is effective at distinguishing between images of the same and different people.
- The d' value of 7.3 quantifies the separation between the two distributions, with higher values indicating better discrimination.
- The analysis is based on 2.3 million comparisons, providing a robust sample size for statistical inference.


## Attack on Iris Scan

- Good photo of eye can be scanned
- Attacker could use photo of eye
- Afghan woman was authenticated by iris scan of old photo
- Story can be found here
- To prevent attack, scanner could use light to be sure it is a “live” iris

## Equal Error Rate Comparison

- Equal error rate (EER): fraud == insult rate
- Fingerprint biometrics used in practice have EER ranging from about 10^-3 to as high as 5%
- Hand geometry has EER of about 10^-3
- In theory, iris scan has EER of about 10^-6
- Enrollment phase may be critical to accuracy
- Most biometrics much worse than fingerprint!
- Biometrics useful for authentication…
- …but for identification, not so impressive today

## Biometrics: The Bottom Line

- Biometrics are hard to forge
- But attacker could:
  - Steal Alice’s thumb
  - Photocopy Bob’s fingerprint, eye, etc.
  - Subvert software, database, “trusted path” …
  - And how to revoke a “broken” biometric?
- Biometrics are not foolproof
- Biometric use is relatively limited today
- That should change in the (near?) future

Certainly! Please provide the text you want to be reformatted as Markdown. I cannot access external links or files. Paste the extracted text here, and I’ll clean it up as requested!
## Identity Authentication
### With extra material for further reading, indicated by symbol *

<!-- No content to normalize, awaiting subsequent text segments -->

## Info-Sec 2023
### 2. Authentication Basics
#### Methods
- Passwords
- Challenge-Response
- Biometrics
- Location
- Multiple Methods

### Info-Sec 2023
#### 3 Basics

Authentication: binding of identity to subject. 
Identity is that of an external entity (my identity, Van, etc.), while the subject is a computer entity (process, etc.).

**Note**: Message authentication is a different topic and has already been mentioned in the applications of hash functions.

## 4. Establishing Identity

Establishing identity involves one or more of the following methods:

* What entity knows (e.g., password)
* What entity has (e.g., identity card, smart card)
* What entity is (e.g., fingerprints, retinal characteristics)
* Where the entity is (e.g., in front of a particular terminal)

## Info-Sec 2023
### Authentication System

We need a formal definition, rather abstract view, of an Authentication System (AS) as a 5-tuple:

* A – a set: information that proves identity
* C – a set: information stored on computer and used to validate authentication information
* F: a set of complementation functions; *f : A → C*, to compute complement information from identity information
* L: authentication functions that prove identity
* S: functions enabling entity to create, alter information in A or C

## Info-Sec 2023
### 6. Example: Password System

### Overview
The example describes a password system with passwords stored online in clear text.

### Components
- **A**: A set of strings making up passwords.
- **C**: Equal to **A**.
- **F**: A singleton set of the identity function { **I** }.
- **L**: A single equality test function { **eq** }.
- **S**: A function to set/change a password.

## Info-Sec 2023
### 7. Passwords

A password is a sequence of characters. Examples include:

* 10 digits
* A string of letters

Passwords can be generated in various ways:
* Randomly
* By a user
* By a computer with user input

Alternatively, a password can be a sequence of words, such as pass-phrases.

There are also different types of password algorithms, including:
* Challenge-response
* One-time passwords

## Info-Sec 2023
### 8. Storage

### Store as Cleartext
Storing passwords as cleartext poses a significant risk. If the password file is compromised, all passwords are revealed.

### Encipher File
A better approach is to encipher the file. However, this requires having both decipherment and encipherment keys in memory. 

This reduces to the previous problem, as there is still a need for something else to secure the keys.

### Solution: One-Way Hash of Password
The solution is to store a one-way hash of the password instead. If an attacker obtains the file, they must still guess the passwords or invert the hash values.

## Info-Sec 2023
### 9. Example: Unix

By definition, a 5-tuple (A, C, F, L, S) is defined as follows:

* A – a set: information that proves identity
  * A = { strings of 8 chars or less }
* C – a set: information stored on computer and used to validate authentication information
  * C = {hash values of password}
* F: a set of complementation functions; f : A → C
  * F = { versions of modified DES }
* L: authentication functions that prove identity
  * L = { login, su, … }
* S: functions enabling entity to create, alter information in A or C
  * S = { passwd, nispasswd, passwd+, … }

## Info-Sec 2023
### 10
#### Example: Unix

By definition, a 5-tuple (A, C, F, L, S)

* A – a set: information that proves identity
  * A = { strings of 8 chars or less }
* C – a set: information stored on computer and used to validate authentication information
  * C = {hash values of password}
* F: a set of complementation functions; f : A → C
  * F = { versions of modified DES }
* L: authentication functions that prove identity
  * L = { login, su, … }
* S: functions enabling entity to create, alter information in A or C
  * S = { passwd, nispasswd, passwd+, … }

## Info-Sec 2023
### 11 - Attacking Passwords

The goal is to find a value $a$ in set $A$ such that:

For some function $f$ in set $F$, $f(a) = c$ in set $C$, 
where $c$ is associated with an entity.

There are two ways to determine whether a given $a$ meets these requirements:

* By trying to compute $f(a)$ for a set of $a$ values until successful
* By trying to call $I(a)$ until successful (i.e., $I(a)$ returns `true`)

## Info-Sec 2023
### 12 Preventing Attacks

To prevent attacks, consider the following measures:

* Hide at least one of $a$, $f$, or $c$ to prevent obvious attacks from above. 
  An example of this approach is UNIX/Linux shadow password files, which hide the $c$'s.

* Block access to all $l \in L$ or the result of $l(a)$ to prevent an attacker from knowing if a guess succeeded. 
  For instance, preventing any logins to an account from a network prevents knowing the results of $l$ (or accessing $l$).

## Info-Sec 2023
### 13 Dictionary Attacks

Dictionary attacks involve trial-and-error attempts using a list of potential passwords.

#### Types of Dictionary Attacks

* **Off-line Dictionary Attacks**: Given $f$ and $c$'s, repeatedly try different guesses $g \in A$ until the list is exhausted or passwords are guessed. 
  Examples: crack, john-the-ripper

* **On-line Dictionary Attacks**: Have access to functions in $L$ and try guesses $g$ until some $l(g)$ succeeds. 
  Examples: trying to log in by guessing a password

## Info-Sec 2023
### Success Probability over a Time Period

Anderson's formula:

* $P$: probability of guessing a password in specified period of time
* $G$: number of guesses tested in 1 time unit
* $T$: number of time units
* $N$: number of possible passwords (|A|)

Then $P \geq \frac{TG}{N}$

## Info-Sec 2023
### Example

#### Goal
Passwords are drawn from a 96-char alphabet. The goal is to find the minimum password length given that:
- The system can test $10^4$ guesses per second.
- The probability of a success over a 365-day period is 0.5.

#### Solution
The number of attempts $N$ over a 365-day period is given by:
$N ≥ \frac{TG}{P}$

where:
- $T = 365 \times 24 \times 60 \times 60$ seconds
- $G = 10^4$ guesses per second
- $P = 0.5$

Substituting the given values:
$N = \frac{(365 \times 24 \times 60 \times 60) \times 10^4}{0.5} = 6.31 \times 10^{11}$

To ensure the password space is greater than or equal to $N$, we choose $s$ such that:
$\sum_{j=0}^{s} 96^j ≥ N$

This implies that $s ≥ 6$, meaning passwords must be at least 6 characters long.

## Exercise

### Definitions
- $X$ = number defined by the last 2 digits of your student ID
- $Y = X \mod 4$
- $H$ is a cryptographic hash function with an output size of $(Y+2) \times 16$ bits.

### Hardware Specifications
The Scorpion-$i$ line of hardware chips (where $i = 1-9$) is designed for computing $H$. Each Scorpion-$i$ can generate $10i \times 1000$ hash values per second. The pricing for each Scorpion-$i$ is $\frac{i^2}{2} \times \$1000$.

### Authentication System Requirements
- Password length: exactly 6 characters
- Alphabet size: $N = (X \mod 50) + 40$

### Objective
An enemy aims to break a password using an off-line attack given access to the hashed password file. The goal is to succeed within a month with a success probability of $(6+Y) \times 10\%$.

### Task
Determine how much the enemy must spend on Scorpion chips to achieve this.

Info-Sec 2023
17
On password selection
Random selection
Any password from A equally likely to be selected
Pronounceable passwords
User selection of passwords

# Info-Sec 2023
## 18 Pronounceable Passwords

Generate phonemes randomly. A phoneme is a unit of sound, e.g., cv, vc, cvc, vcv.

Examples of pronounceable passwords: 
- helgoret
- juttelon

Examples of non-pronounceable passwords: 
- przbqxdfl
- zxrptglfn

The problem with pronounceable passwords is that there are too few. 
The solution is key crunching: 
Run a long key through a hash function and convert it to a printable sequence. 
Use this sequence as the password.

## Info-Sec 2023
### 19 - User Selection

## Problem
People pick easy-to-guess passwords based on:
- Account names
- User names
- Computer names
- Place names

Common password choices include:
- Dictionary words 
  - Reversed
  - Odd capitalizations
  - Control characters
  - “Elite-speak”
  - Conjugations or declensions
  - Swear words
  - Torah/Bible/Koran/… words

Weak passwords also include:
- Too short
- Digits only
- Letters only

Examples of easily guessable passwords:
- License plates
- Acronyms
- Social security numbers
- Personal characteristics or foibles (pet names, nicknames, job characteristics, etc.)

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

## Info-Sec 2023
### 21. Proactive Password Checking

Proactive password checking involves analyzing a proposed password for its "goodness". This process is always invoked and can detect and reject bad passwords based on an appropriate definition of "bad". The analysis can be done on a per-user, per-site basis.

The checking process requires:
- Pattern matching on words
- Execution of subprograms and use of their results
  - Examples include a spell checker

This approach is easy to set up and integrate into a password selection system.

Info-Sec 2023
22
Salting
Goal: slow dictionary attacks
Method: perturb hash function so that:
Parameter controls which hash function is used
Parameter differs for each password
So given n password hashes, and therefore n salts, need to hash guess n

## Info-Sec 2023
### 23

### Examples

#### Vanilla UNIX method
Use DES to encipher a 0 message with a password as the key; iterate 25 times. 
Perturb the E table in DES in one of 4096 ways. 
A 12-bit salt flips entries 1–11 with entries 25–36.

#### Alternate methods
Use the salt as the first part of the input to a hash function.

### Info-Sec 2023
#### 24

Unix actually is based on a standard hash function for UNIX systems. This function hashes a password into an 11-character string using one of 4096 hash functions.

The authentication system components are defined as follows:

- **A**: strings of 8 characters or less
- **C**: 2-character hash ID || 11-character hash
- **F**: 4096 versions of modified DES
- **L**: login, su, …
- **S**: passwd, nispasswd, passwd+, …

Exercise
Assume that H is a cryptographic hash function with output size (Y+2)*16 bits. Assume that Scorpion-i (i=1-9) is a specifically designed line of hardware chips for computing H, where Scorpion-i can create 10i * 1000 hash values a second, priced at ii/2 *$1000.
1. An authentication system requires its users to pick their passwords of length exactly 6 from an alphabet of size N=(X mod 50)+ 40. Using H, this system maintains the hash values of the passwords of all the users. An enemy, who has gained access to this hashed password file, aims to launch an off-line attack to break the password of an important user. Using the Scorpion chips, how much the enemy has to spend in order to finish within a month with success probability (6+Y)*10%?
2. The owner decides to enhance the above password system by using salt so that the enemy will need to spend at least 10 times the above mentioned amount of money to achieve the same goal. How many salt bits he/she need to use to achieve this purpose ?
25

## Part 2 — Access Control
### Password Cracking: Do the Math

#### Assumptions
* Passwords are 8 characters, with 128 choices per character.
* Then, there are $128^8 = 2^{56}$ possible passwords.
* There is a password file with $2^{10}$ passwords.
* The attacker has a dictionary of $2^{20}$ common passwords.
* The probability is $1/4$ that a password is in the dictionary.

#### Work Measurement
Work is measured by the number of hashes.

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

## Part 2 — Access Control
### Password Cracking: Case I 

Attack a specific password without using a dictionary, for example, the administrator's password. This requires trying 256/2 = 255 attempts on average, similar to an exhaustive key search.

Does salt help in this case?

## Part 2 — Access Control
### Password Cracking: Case II

#### Attack on a Specific Password with Dictionary

With salt:
- Expected work: $\frac{1}{4} (2^{19}) + \frac{3}{4} (2^{55}) \approx 2^{54.6}$
- In practice, try all passwords in dictionary… 
- …then work is at most $2^{20}$ and probability of success is $\frac{1}{4}$

#### Without Salt

- One-time work to compute dictionary: $2^{20}$
- Expected work is of the same order as above
- But with precomputed dictionary hashes, the “in practice” attack is essentially free…

## Part 2 — Access Control
### Password Cracking: Case III

Assume all $2^{10}$ passwords are distinct. Any of $2^{10}$ pwds in file, without dictionary.

Need $2^{55}$ comparisons before expecting to find pwd.

#### Without Salt

If no salt is used, each computed hash yields $2^{10}$ comparisons. 
So expected work (hashes) is $\frac{2^{55}}{2^{10}} = 2^{45}$.

#### With Salt

If salt is used, expected work is $2^{55}$. 
Each comparison requires a hash computation.

## Part 2 — Access Control
### Password Cracking: Case IV

Any of 1024 passwords in a file, with dictionary. 
The probability of one or more passwords in the dictionary is $1 – (3/4)^{1024} ≈ 1$. 
So, we ignore the case where no password is in the dictionary.

If a salt is used, the expected work is less than $2^{22}$. 
See the book or slide notes for details. 
The work is approximately $\frac{\text{size of dictionary}}{P(\text{pwd in dictionary})}$.

What if no salt is used? 
If dictionary hashes are not precomputed, the work is about $\frac{2^{19}}{2^{10}} = 2^9$.

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

## Info-Sec 2023
### 33: Password Aging

Force users to change passwords after some time has expired. To prevent password re-use:
- Record previous passwords
- Block changes for a period of time
- Give users time to think of good passwords
- Don’t force them to change before they can log in
- Warn them of expiration days in advance

## Info-Sec 2023
### 34

## Challenge-Response

User and system share a secret function *f* (in practice, *f* is a known function with unknown parameters, such as a cryptographic key).

The challenge-response process is as follows:

- User requests to authenticate
- System sends a random message *r* (the challenge)
- User sends *f(r)* (the response) back to the system. 

This can be represented as:

User → System: request to authenticate
System → User: random message *r* (the challenge)
User → System: *f(r)* (the response)

## Info-Sec 2023
## 35
## Pass Algorithms

Challenge-response with the function f itself a secret. The challenge is a random string of characters. The response is some function of that string. Usually used in conjunction with fixed, reusable password. 

No visual element provided.

## Info-Sec 2023
### One-Time Passwords

One-Time Passwords are passwords that can be used exactly once. After use, they are immediately invalidated. They operate on a challenge-response mechanism, where:

* The challenge is the number of authentications.
* The response is the password for that particular number.

### Problems

The following problems are associated with One-Time Passwords:

* Synchronization of user and system.
* Generation of good random passwords.
* Password distribution problem.

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

## Info-Sec 2023
### 38

## S/Key Protocol

The system stores the maximum number of authentications `n`, the number of the next authentication `i`, and the last correctly supplied password `p_i-1`.

The system computes `h(p_i) = h(k_n-i+1) = k_n-i+2 = p_i-1`. If there is a match with what is stored, the system replaces `p_i-1` with `p_i` and increments `i`.

### Info-Sec 2023
#### 39 - C-R and Dictionary Attacks

Same as for fixed passwords. An attacker knows the challenge $r$ and response $f(r)$. If $f$ is an encryption function, the attacker can try different keys.

The attacker may only need to know the form of the response. They can tell if their guess is correct by checking if the deciphered object is of the right form.

##### Example: Kerberos Version 4

Kerberos Version 4 used DES, but the keys had only 20 bits of randomness. Attackers at Purdue were able to guess the keys quickly because the deciphered tickets had a fixed set of bits in specific locations.

## Info-Sec 2023
### 40 - Encrypted Key Exchange

The Encrypted Key Exchange defeats off-line dictionary attacks. The idea is to use random challenges enciphered, making it impossible for an attacker to verify the correct decipherment of the challenge.

### Overview

Assume Alice and Bob share a secret password $s$. 

### Key Generation

In what follows:
- Alice needs to generate a random public key $p$ and a corresponding private key $q$.
- $k$ is a randomly generated session key.
- $R_A$ and $R_B$ are random challenges.

## Info-Sec 2023
### 41

## EKE Protocol

Now Alice and Bob share a randomly generated secret session key $k$.

## Part 2 — Access Control
### Something You Have

Something in your possession. Examples include:
- Car key
- Laptop computer (or MAC address)
- Password generator
- ATM card, smartcard, etc.

### Info-Sec 2023
#### 43. Hardware Support

## Token-based Authentication

Token-based authentication is used to compute a response to a challenge. 
It may encipher or hash the challenge and may require a PIN from the user. 

The object a user possesses to authenticate includes:
- Memory card (magnetic stripe)
- Smartcard

## Types of Token-based Authentication

### Temporally-based Authentication

In temporally-based authentication, a different number is shown every minute or so. 
The computer knows what number to expect when the user enters the number along with a fixed password.

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

## Smartcard

A smartcard is credit-card like, with its own processor, memory, and I/O ports. It has ROM, EEPROM, and RAM memory. The smartcard executes a protocol to authenticate with a reader or computer.

There are different types of smartcard authentication:

* **Static**: similar to memory cards
* **Dynamic**: passwords are created every minute, either entered manually by the user or electronically
* **Challenge-response**: the computer creates a random number, and the smartcard provides its hash (similar to public key)

Additionally, there are also USB dongles available. 

### Error Message

The following error was encountered while attempting to process a request:
 
[LLM_ERROR] 
All providers failed: 
- Gemini (timed out) 
- Azure 
- Groq (Error code: 429 - 
  {'error': 
    {'message': 
      'Rate limit reached for model `meta-llama/llama-4-scout-17b-16e-instruct` in organization `org_01kkedd9pnejqr8cfvvrfp64h7` service tier `on_demand` on requests per minute (RPM): Limit 30, Used 30, Requested 1. Please try again in 2s. Need more tokens? Upgrade to Dev Tier today at https://console.groq.com/settings/billing', 
     'type': 'requests', 
     'code': 'rate_limit_exceeded'}})

## Electronic Identity Cards

An important application of smart cards is a national e-identity (eID), which serves the same purpose as other national ID cards (e.g., a driver’s licence). However, an eID can provide stronger proof of identity.

### German Card

A German eID card contains:
- Personal data
- Document number
- Card access number (six-digit random number)
- Machine-readable zone (MRZ): the password

### Uses

The card has multiple uses:
- ePass (government use)
- eID (general use)
- eSign (can have private key and certificate)

## User Authentication with eID

(No further text provided)

## Part 2 — Access Control
### Something You Are: Biometric

"You are your key" — Schneier

Biometric access control methods include:

* Are (inherent characteristics)
* Know (knowledge-based)
* Have (object-based)

Examples of biometric methods:
- Fingerprint
- Handwritten signature
- Facial recognition
- Speech recognition
- Gait (walking) recognition
- "Digital doggie" (odor recognition)
- Many more!

## Part 2 — Access Control
### Why Biometrics?

Biometrics may be better than passwords. However, cheap and reliable biometrics are needed. Today, biometrics is an active area of research. 

Biometrics are used in security today, for example:
* Thumbprint mouse
* Palm print for secure entry
* Fingerprint to unlock car doors, etc.

However, biometrics has not really become popular and has not lived up to its promise or hype (yet?).

## Info-Sec 2023
### Biometrics: Core Idea

Automated measurement of biological, behavioral features that identify a person.

### Types of Biometrics

#### Fingerprints
Uses optical or electrical techniques. Maps fingerprint into a graph, then compares with database. Measurements are imprecise, so approximate matching algorithms are used.

#### Voices
There are two types: 
- **Speaker Verification**: uses statistical techniques to test the hypothesis that the speaker is who is claimed (speaker dependent).
- **Speaker Recognition**: checks the content of answers (speaker independent).

## Part 2 — Access Control

### Fingerprint: Enrollment

The process involves the following steps:
- Capture image of fingerprint
- Enhance image
- Identify “points”

## Part 2 — Access Control

### Fingerprint: Recognition

Extracted points are compared with information stored in a database. The question then arises: Is it a statistical match?

### Identical Twins' Fingerprints

Do identical twins' fingerprints differ?

### Info-Sec 2023
#### 53

## Other Characteristics

Several other characteristics can be used for identification. These include:

- **Eyes**: The patterns in irises are unique. Identification involves measuring these patterns and determining if the differences between them are random, or correlating images using statistical tests.

- **Faces**: This can involve analyzing the image of a face or specific characteristics, such as the distance from the nose to the chin. However, factors like lighting, the view of the face, and other noise can hinder this method.

- **Keystroke Dynamics**: Believed to be unique to individuals, keystroke dynamics involve analyzing:
  - Keystroke intervals
  - Pressure
  - Duration of the stroke
  - Where the key is struck

Statistical tests are used in the analysis of these characteristics.

## Biometric Authentication

Authenticate user based on one of their physical characteristics:
* Facial
* Fingerprint
* Hand geometry
* Retina pattern
* Iris
* Signature
* Voice

### Error Log

The following error occurred while processing a request:
 
[LLM_ERROR] All providers failed: Gemini (timed out), Azure, Groq (Error code: 429 - {'error': {'message': 'Rate limit reached for model `meta-llama/llama-4-scout-17b-16e-instruct` in organization `org_01kkedd9pnejqr8cfvvrfp64h7` service tier `on_demand` on requests per minute (RPM): Limit 30, Used 30, Requested 1. Please try again in 2s. Need more tokens? Upgrade to Dev Tier today at https://console.groq.com/settings/billing', 'type': 'requests', 'code': 'rate_limit_exceeded'}}).

## Operation of a Biometric System

Verification is analogous to user login via a smart card and a PIN. 
Identification uses biometric information but no IDs; the system compares it with stored templates.

### Biometric Accuracy
The system generates a matching score (a number) that quantifies similarity between the input and the stored template. Concerns include sensor noise and detection inaccuracy, which can lead to problems of false matches and false non-matches. 
* Further reading (Stallings textbook)

### Extracting Table Information
To accurately extract row labels, column labels, and cell values from a given table or matrix, a sample table must be provided as input.

#### Example Table
| Column A | Column B | Column C
| --- | --- | --- 
| Row 1 | 10 | 20 | 30
| Row 2 | 40 | 50 | 60
| Row 3 | 70 | 80 | 90

#### JSON Representation
```json
{
  "schema_version": "1.0",
  "content_type": "table",
  "row_labels": ["Row 1", "Row 2", "Row 3"],
  "column_labels": ["Column A", "Column B", "Column C"],
  "values": [
    [10, 20, 30],
    [40, 50, 60],
    [70, 80, 90]
  ],
  "notes": "Example table with numeric values."
}
```

### Providing Your Table
There are two ways to provide your table:

1. **Text Representation:** If your table can be described or represented in a simple text format similar to the example above, it can be shared.
2. **CSV Format:** Alternatively, if your table can be represented in CSV (Comma Separated Values) format, that would also work. For example:
```csv
"Column A","Column B","Column C"
"Row 1",10,20,30
"Row 2",40,50,60
"Row 3",70,80,90
```

### Automating Table Extraction with Python
Here's a simple Python script to automate the extraction into a JSON format:

```python
import json

def table_to_json(row_labels, column_labels, table_values):
    data = {
        "schema_version": "1.0",
        "content_type": "table",
        "row_labels": row_labels,
        "column_labels": column_labels,
        "values": table_values,
        "notes": "Automatically converted table."
    }
    return json.dumps(data, indent=2)

# Example usage
row_labels = ["Row 1", "Row 2", "Row 3"]
column_labels = ["Column A", "Column B", "Column C"]
table_values = [[10, 20, 30], [40, 50, 60], [70, 80, 90]]

print(table_to_json(row_labels, column_labels, table_values))
```
This script takes row labels, column labels, and table values as input and outputs a JSON string.

## Biometric Accuracy

### Characteristic Curve and Threshold Selection

The characteristic curve can be plotted with 2,000,000 comparisons. This curve is used to pick a threshold that balances error rates. 

### Note on Visual Elements 

There is no visual element provided.

## Info-Sec 2023
### 58. Cautions

These can be fooled! It assumes the biometric device is accurate in the environment it is being used in. The transmission of data to the validator is tamperproof, correct.

## Part 2 — Access Control
### Biometrics: The Bottom Line

Biometrics are hard to forge. However, an attacker could:
- Steal Alice’s thumb
- Photocopy Bob’s fingerprint, eye, etc.
- Subvert software, database, “trusted path” …

And there's the issue of revoking a “broken” biometric. 
Biometrics are not foolproof. 
Biometric use is relatively limited today. 
That should change in the (near?) future.

## Info-Sec 2023
### 60
#### Location – Just a brief

If you know where a user is, you can validate their identity by verifying if the person is actually where the user claims to be. This method requires special-purpose hardware to locate the user. A GPS (Global Positioning System) device can provide a location signature of an entity. The host uses an LSS (Location Signature Sensor) to obtain the signature for the entity.

# Info-Sec 2023
## 61
## Multiple Methods

Multiple authentication methods can be employed. For example, "where you are" requires an entity to have Location Services (LSS) and GPS, which also implies "what you have". Different methods can be assigned to different tasks.

As users perform more sensitive tasks, they must authenticate in more ways, presumably with increasing stringency. A file describes the required authentication. This includes controls on access, such as time of day, as well as resources and requests to change passwords.

## Pluggable Authentication Modules

### Info-Sec 2023
#### 62 - PAM

The idea behind PAM (Privileged Access Management) is that when a program needs to authenticate, it checks a central repository for methods to use. This is achieved through a library call: `pam_authenticate`.

The configuration for PAM is typically stored in files located in `/etc/pam.d/`, with the file name corresponding to the name of the program.

The authentication process involves modules that perform the actual authentication checking. These modules can be configured with the following control flags:

* **sufficient**: Succeed if the module succeeds.
* **required**: Fail if the module fails, but all required modules must be executed before reporting failure.
* **requisite**: Like required, but don't check all modules.
* **optional**: Invoke only if all previous modules fail.

### Info-Sec 2023
#### 63

##### Example PAM File
```markdown
auth sufficient /usr/lib/pam_ftp.so
auth required /usr/lib/pam_unix_auth.so use_first_pass
auth required /usr/lib/pam_listfile.so onerr=succeed \
  item=user sense=deny file=/etc/ftpusers
```

##### For ftp:

* If user “anonymous”, return okay; if not, set PAM_AUTHTOK to password, PAM_RUSER to name, and fail
* Now check that password in PAM_AUTHTOK belongs to that of user in PAM_RUSER; if not, fail
* Now see if user in PAM_RUSER named in /etc/ftpusers; if so, fail; if error or not found, succeed

## Extended Material: Kerberos Authentication Protocol

### Material Sources
- History and general information from Wiki
- Details on Kerberos versions 4 and 5 from Stallings Text and slides

### Info-Sec 2023
#### 65. Kerberos

Kerberos is a computer network authentication protocol which allows nodes communicating over a non-secure network to prove their identity to one another in a secure manner. It is aimed primarily at a client-server model, and it provides mutual authentication -- both the user and the server verify each other's identity. Messages are protected against eavesdropping and replay attacks. Kerberos builds on Symmetric Key Cryptography (SKC) and requires a trusted third party, and optionally may use public-key cryptography during certain phases of authentication.

## Sep 2009
## Information Security by Van K Nguyen, Hanoi University of Technology
## 66
## Kerberos

### History
Kerberos is named after the character Kerberos (or Cerberus), the ferocious three-headed guard dog of Hades (from Greek mythology). 
MIT developed Kerberos in 1988 to protect network services provided by Project Athena. The first version was primarily designed by Steve Miller and Clifford Neuman, based on the earlier Needham–Schroeder symmetric-key protocol. Versions 1-3 were experimental and internal.

Kerberos version 4, the first public version, was released on January 24, 1989. 
Neuman and John Kohl published version 5 in 1993, with the intention of overcoming existing limitations and security problems. 
Version 5 appeared as RFC 1510, which was then made obsolete by RFC 4120 in 2005. 
In 2005, the Internet Engineering Task Force (IETF) Kerberos working group updated the specifications.

## Information Security
### Sep 2009
### Van K Nguyen
### Hanoi University of Technology
### 67

## Idea

### Ticket
The issuer vouches for the identity of the requester of service. 
It identifies the sender.

### Key Distribution Center (KDC)
The KDC combines two servers: 
- Authentication Server (AS), also known as the Kerberos server
- Ticket Granting Server (TGS)

## Process

### User Authentication and Ticket Granting
1. User \( u \) authenticates to AS.
2. Obtains ticket \( T_{u,TGS} \) for ticket granting service (TGS).

### Service Request
1. User \( u \) wants to use service \( s \):
2. User sends authenticator \( A_u \), ticket \( T_{u,TGS} \) to TGS asking for ticket for service.
3. TGS sends ticket \( T_{u,s} \) to user.
4. User sends \( A_u, T_{u,s} \) to server as request to use \( s \).

## Kerberos v4 Overview

Kerberos v4 is a basic third-party authentication scheme. The scheme involves:

* An Authentication Server (AS) 
* A Ticket Granting Server (TGS)

The process works as follows:

* Users initially negotiate with the AS to identify themselves. 
* The AS provides a non-corruptible authentication credential, known as a Ticket Granting Ticket (TGT). 
* Users subsequently request access to other services from the TGS on the basis of the user's TGT. 
* The protocol used is complex and utilizes DES.

## Kerberos 4 Overview

No content available due to error: 
[LLM_ERROR] All providers failed: Gemini (timed out), Azure, Groq (Error code: 429 - {'error': {'message': 'Rate limit reached for model `meta-llama/llama-4-scout-17b-16e-instruct` in organization `org_01kkedd9pnejqr8cfvvrfp64h7` service tier `on_demand` on requests per minute (RPM): Limit 30, Used 30, Requested 1. Please try again in 2s. Need more tokens? Upgrade to Dev Tier today at https://console.groq.com/settings/billing', 'type': 'requests', 'code': 'rate_limit_exceeded'}}).

## Kerberos v4 Dialogue

### Slide Image
[LLM_ERROR] 
All providers failed: 
- Gemini (timed out)
- Azure
- Groq (Error code: 429 - 
  {'error': {'message': 'Rate limit reached for model `meta-llama/llama-4-scout-17b-16e-instruct` in organization `org_01kkedd9pnejqr8cfvvrfp64h7` service tier `on_demand` on requests per minute (RPM): Limit 30, Used 30, Requested 1. Please try again in 2s. Need more tokens? Upgrade to Dev Tier today at https://console.groq.com/settings/billing', 'type': 'requests', 'code': 'rate_limit_exceeded'}})

## Kerberos Version 5

Developed in the mid-1990s, Kerberos Version 5 was specified as Internet standard RFC 1510. It provides improvements over version 4, addressing both environmental shortcomings and technical deficiencies.

### Improvements

The improvements include:
- Encryption algorithm
- Network protocol
- Byte order
- Ticket lifetime
- Authentication forwarding
- Interrealm authentication

### Addressed Deficiencies

The addressed deficiencies include:
- Double encryption
- Non-standard mode of use
- Session keys
- Password attacks

## Kerberos Realms

A Kerberos environment consists of:
- A Kerberos server
- A number of clients, all registered with the server
- Application servers, sharing keys with the server

This configuration is termed a *realm*, typically a single administrative domain. 
If you have multiple realms, their Kerberos servers must share keys and trust each other.

## Kerberos Realms

No visual element provided.

### Protocol
#### From Wiki
- Client Authentication to the AS
- Client Service Authorization
- Client Service Request

### Representing a Graph in JSON
To provide a structured graph representation in JSON, let's consider a simple example graph. We'll define a directed graph with nodes (also known as vertices) and edges.

#### Example Graph
Suppose we have a graph with the following properties:

* **Nodes (Vertices):** A, B, C, D
* **Edges:** 
  * A -> B (directed from A to B)
  * B -> C (directed from B to C)
  * C -> A (directed from C to A)
  * D -> B (directed from D to B)

### JSON Representations

#### Basic Representation
A common JSON representation for a graph might involve specifying nodes and edges separately. Here is one way to structure it:

```json
{
  "nodes": [
    {"id": "A"},
    {"id": "B"},
    {"id": "C"},
    {"id": "D"}
  ],
  "edges": [
    {"source": "A", "target": "B", "direction": "out"},
    {"source": "B", "target": "C", "direction": "out"},
    {"source": "C", "target": "A", "direction": "out"},
    {"source": "D", "target": "B", "direction": "out"}
  ]
}
```

#### Alternative Representation with Directionality
If you want to explicitly highlight directionality (directed vs. undirected) and possibly add more details like edge weights or labels, you could structure the JSON like this:

```json
{
  "graphType": "directed", // or "undirected"
  "nodes": [
    {"id": "A"},
    {"id": "B"},
    {"id": "C"},
    {"id": "D"}
  ],
  "edges": [
    {"source": "A", "target": "B"},
    {"source": "B", "target": "C"},
    {"source": "C", "target": "A"},
    {"source": "D", "target": "B"}
  ]
}
```

Or, with additional properties for edges:

```json
{
  "graphType": "directed",
  "nodes": [
    {"id": "A"},
    {"id": "B"},
    {"id": "C"},
    {"id": "D"}
  ],
  "edges": [
    {"source": "A", "target": "B", "label": "rel1", "weight": 1.0},
    {"source": "B", "target": "C", "label": "rel2", "weight": 2.0},
    {"source": "C", "target": "A", "label": "rel3", "weight": 3.0},
    {"source": "D", "target": "B", "label": "rel4", "weight": 4.0}
  ]
}
```

### Code to Generate This JSON
If you're working in Python, here's a simple way to construct and output such a graph representation:

```python
import json

class Graph:
    def __init__(self, directed=False):
        self.nodes = []
        self.edges = []
        self.directed = directed

    def add_node(self, id):
        self.nodes.append({"id": id})

    def add_edge(self, source, target, label=None, weight=None):
        edge = {"source": source, "target": target}
        if label:
            edge["label"] = label
        if weight:
            edge["weight"] = weight
        self.edges.append(edge)

    def to_json(self):
        graph_repr = {
            "graphType": "directed" if self.directed else "undirected",
            "nodes": self.nodes,
            "edges": self.edges
        }
        return json.dumps(graph_repr, indent=2)

# Usage
g = Graph(directed=True)
g.add_node("A")
g.add_node("B")
g.add_node("C")
g.add_node("D")
g.add_edge("A", "B")
g.add_edge("B", "C")
g.add_edge("C", "A")
g.add_edge("D", "B")

print(g.to_json())
```

This example constructs a directed graph and outputs its JSON representation. Adjustments can be made based on specific requirements or programming languages.

# Kerberos v5 Dialogue

## Graph Representation in JSON

To provide a structured graph representation in JSON, including node labels, edge lists, and directionality, let's consider a simple example graph. This graph will have 5 nodes and 7 edges. The graph is directed.

### Graph Details

* **Nodes (Vertices):** A, B, C, D, E
* **Edges:**
  * A → B
  * A → C
  * B → D
  * C → B
  * C → E
  * D → E
  * E → B

### JSON Representation

```json
{
  "graph": {
    "nodes": [
      {"id": "A", "label": "Node A"},
      {"id": "B", "label": "Node B"},
      {"id": "C", "label": "Node C"},
      {"id": "D", "label": "Node D"},
      {"id": "E", "label": "Node E"}
    ],
    "edges": [
      {"source": "A", "target": "B", "direction": "out"},
      {"source": "A", "target": "C", "direction": "out"},
      {"source": "B", "target": "D", "direction": "out"},
      {"source": "C", "target": "B", "direction": "out"},
      {"source": "C", "target": "E", "direction": "out"},
      {"source": "D", "target": "E", "direction": "out"},
      {"source": "E", "target": "B", "direction": "out"}
    ],
    "directionality": "directed"
  }
}
```

## Explanation and Usage

* **Nodes:** Each node is represented as a JSON object within the `nodes` array. Each node has an `id` (which could be a unique identifier or a label) and a `label` for readability.
* **Edges:** The `edges` array contains JSON objects representing the edges. Each edge object specifies a `source` node, a `target` node, and the `direction` of the edge. Since this is a directed graph, the direction of each edge is specified as "out" to denote it has a direction from source to target.
* **Directionality:** The `directionality` field within the graph object indicates that this graph is directed. If all edges had a direction and there were no edges from target to source, you could infer directionality from the edges themselves, but including it explicitly can be helpful.

This JSON object can be easily parsed and used in applications that work with graph data structures, such as social network analysis tools, graph databases (e.g., Neo4j), or libraries for graph algorithms in programming languages like Python (NetworkX), JavaScript (Sigma.js, Cytoscape.js), etc.

## Federated Identity Management

The use of a common identity management scheme across multiple enterprises and numerous applications supports many thousands, even millions of users. The principal elements are:

* Authentication
* Authorization
* Accounting
* Provisioning
* Workflow automation
* Delegated administration
* Password synchronization
* Self-service password reset
* Federation

Kerberos contains many of these elements.

## Identity Management

There is no visual element provided. Please share the visual element, and I'll describe its content in a way that focuses on its learning value.

## Identity Federation

There is no visual element provided. Please share the visual element, and I will describe its content, focusing on the information that contributes to learning value.

## Standards Used

The following standards are used:

* Security Assertion Markup Language (SAML): an XML-based language for the exchange of security information between online business partners. SAML is part of OASIS (Organization for the Advancement of Structured Information Standards) standards for federated identity management, which includes standards like WS-Federation for browser-based federation.

To achieve the desired outcome, a few mature industry standards are required.

## Federated Identity Examples

No visual element provided.

### FIM vs. SSO

## Definitions

* **SSO**: Single Sign-On
 Allows users to access multiple web applications at once, using just one set of credentials. 
Beyond the workforce, companies can utilize SSO to help customers access various sections of one account.

## Relationship to FIM

As a tool, SSO fits within the broader model of FIM. 
The key difference between SSO and FIM is while SSO is designed to authenticate a single credential across various systems within one organization, federated identity management systems offer single access to a number of applications across various enterprises.

No change is needed for the provided text as it appears to be a simple header with a reference. However, to adhere strictly to Markdown formatting for headers and links, here is the normalized version:

# Extended Material *Biometrics*
Slides borrowed from [Mark Stamp’s web](https://www.cs.sjsu.edu/~stamp/infosec/powerpoint/)

## Part 2 — Access Control

### Something You Are: Biometric

"You are your key" — Schneier

Biometric access control methods include:

* Are: 
* Know: 
* Have: 

Examples of biometric authentication:

* Fingerprint
* Handwritten signature
* Facial recognition
* Speech recognition
* Gait (walking) recognition
* "Digital doggie" (odor recognition)
* Many more!

## Part 2 — Access Control

### Ideal Biometric

The ideal biometric should have the following characteristics:

* **Universal**: applies to (almost) everyone
* **Distinguishing**: distinguish with certainty
* **Permanent**: physical characteristic being measured never changes

However, in reality:

* No biometric applies to everyone
* Cannot hope for 100% certainty
* It is acceptable if the characteristic remains valid for a long time

### Collectability

* **Collectable**: easy to collect required data
* Collectability depends on whether subjects are cooperative
* Additionally, the biometric should be safe, user-friendly, and other unspecified characteristics.

## Part 2 — Access Control
### Identification vs Authentication

Identification is the process of determining "Who goes there?" It involves comparing a given input to a large set of known identities, which is a one-to-many comparison. An example of identification is an FBI fingerprint database.

Authentication, on the other hand, verifies if a user "Are you who you say you are?" This process involves a one-to-one comparison, such as a thumbprint mouse.

The identification problem is more difficult because it involves more comparisons, leading to a higher chance of "random" matches. However, we are mostly interested in authentication.

## Part 2 — Access Control
### Enrollment vs Recognition

The enrollment phase involves putting a subject's biometric information into a database. During this phase, it is crucial to carefully measure the required information. It is acceptable if slow and repeated measurements are needed to ensure precision. However, this process may be a weak point in real-world use.

In contrast, the recognition phase, which involves biometric detection in practical use, requires quick and simple measurements. Nevertheless, it must still be reasonably accurate.

## Part 2 — Access Control

### Cooperative Subjects

We differentiate between authentication for cooperative subjects and identification for uncooperative subjects. 
For example, facial recognition is used in Las Vegas casinos to detect known cheaters, as well as for identifying terrorists in airports. 
Often, less than ideal enrollment conditions are present. 
In such cases, the subject may try to confuse the recognition phase. 

However, when the subject is cooperative, it makes the process much easier. 
Since we are focused on authentication, we can assume that the subjects are cooperative.

## Part 2 — Access Control
### Biometric Errors

The relationship between fraud rate and insult rate can be described as follows:

* **Fraud**: Trudy mis-authenticated as Alice
* **Insult**: Alice not authenticated as Alice

For any biometric, decreasing one will increase the other. 

### Trade-off Between Fraud and Insult Rates

| Match Rate | Fraud Rate | Insult Rate |
| --- | --- | --- |
| 99% | Low | High |
| 30% | High | Low |

The **Equal Error Rate** is the rate at which **fraud == insult**, providing a way to compare different biometrics.

## Part 2 — Access Control

### Fingerprint History

The history of fingerprinting dates back to several key milestones:
- 1823: Professor Johannes Evangelist Purkinje discussed 9 fingerprint patterns.
- 1856: Sir William Hershel used fingerprints (in India) on contracts.
- 1880: Dr. Henry Faulds published an article in Nature about using fingerprints for identification.
- 1883: Mark Twain’s *Life on the Mississippi* featured a story where a murderer was identified by their fingerprint.

## Part 2 — Access Control

### Fingerprint History

In 1888, Sir Francis Galton developed a classification system for fingerprints based on the study of "minutia." His system remains usable today and also verified that fingerprints do not change over time. 

Some countries require a fixed number of matching "points" (minutia) for identification in criminal cases. The requirements vary:
| Country | Minimum Points Required |
| --- | --- |
| Britain | 15 |
| US | No fixed number |

## Part 2 — Access Control
### Fingerprint Comparison

Fingerprint patterns are classified into three main types:
- Loop (double)
- Whorl
- Arch

These patterns are often referred to as examples of loops, whorls, and arches. Minutia are extracted from these features for detailed analysis.

### Note on Visual Elements
There are no visual elements provided for the following slides. If you can share them, I can describe their content, focusing on information that contributes to learning value.

## Part 2 — Access Control

### Fingerprint: Enrollment

The process involves the following steps:
1. Capture image of fingerprint
2. Enhance image
3. Identify “points”

## Part 2 — Access Control

### Fingerprint Recognition

Extracted points are compared with information stored in a database. The question arises: Is it a statistical match?

#### Aside: Identical Twins' Fingerprints

Do identical twins' fingerprints differ?

## Part 2 — Access Control
### Hand Geometry

A popular biometric, hand geometry measures the shape of the hand, including:
- Width of hand
- Width of fingers
- Length of fingers, etc.

However, human hands are not so unique. Therefore, hand geometry is sufficient for many situations and okay for authentication, but not useful for identification (ID) problems.

## Part 2 — Access Control
### Hand Geometry

#### Advantages
* Quick — 1 minute for enrollment, 5 seconds for recognition
* Hands are symmetric — so what?

#### Disadvantages
* Cannot use on very young or very old
* Relatively high equal error rate

## Part 2 — Access Control
### Iris Patterns

Iris pattern development is “chaotic” with little or no genetic influence. Even for identical twins, the patterns are uncorrelated. The pattern is stable through lifetime. 

(No visual elements provided)

## Part 2 — Access Control
### Iris Recognition: History

* 1936: suggested by an ophthalmologist
* 1980s: popularized in James Bond films
* 1986: first patent appeared
* 1994: John Daugman patents a new and improved technique

Patents owned by Iridian Technologies.

## Part 2: Access Control

### Iris Scan

The iris scan process involves the following steps:
- Scanner locates iris
- Take black and white photo
- Use polar coordinates
- 2-D wavelet transform
- Get 256 byte iris code

## Graph Representation in JSON

To provide a structured graph representation in JSON, including node labels, edge lists, and directionality, let's consider a simple example graph.

### Example Graph

- **Nodes**: A, B, C, D, E
- **Edges**:
  - A → B
  - A → C
  - B → D
  - C → E
  - D → E
  - E → B

### JSON Representation

Here's how you could represent this graph in JSON, including node labels, edge lists, and directionality:

```json
{
  "nodes": [
    {"id": "A", "label": "Node A"},
    {"id": "B", "label": "Node B"},
    {"id": "C", "label": "Node C"},
    {"id": "D", "label": "Node D"},
    {"id": "E", "label": "Node E"}
  ],
  "edges": [
    {"source": "A", "target": "B", "direction": "OUT"},
    {"source": "A", "target": "C", "direction": "OUT"},
    {"source": "B", "target": "D", "direction": "OUT"},
    {"source": "C", "target": "E", "direction": "OUT"},
    {"source": "D", "target": "E", "direction": "OUT"},
    {"source": "E", "target": "B", "direction": "OUT"}
  ]
}
```

However, for a more compact and graph-database-like representation:

```json
{
  "nodes": ["A", "B", "C", "D", "E"],
  "edges": [
    {"from": "A", "to": "B"},
    {"from": "A", "to": "C"},
    {"from": "B", "to": "D"},
    {"from": "C", "to": "E"},
    {"from": "D", "to": "E"},
    {"from": "E", "to": "B"}
  ]
}
```

Or, if you want to explicitly denote directionality:

```json
{
  "nodes": ["A", "B", "C", "D", "E"],
  "edges": [
    {"source": "A", "target": "B"},
    {"source": "A", "target": "C"},
    {"source": "B", "target": "D"},
    {"source": "C", "target": "E"},
    {"source": "D", "target": "E"},
    {"source": "E", "target": "B"}
  ]
}
```

### How to Extract This Information

If you're working with an existing graph structure, you could extract this information as follows:

```python
import networkx as nx
import json

# Create a directed graph
G = nx.DiGraph()

# Add nodes
G.add_nodes_from(['A', 'B', 'C', 'D', 'E'])

# Add edges
G.add_edges_from([('A', 'B'), ('A', 'C'), ('B', 'D'), ('C', 'E'), ('D', 'E'), ('E', 'B')])

# Extract nodes and edges
nodes = list(G.nodes)
edges = [{"source": edge[0], "target": edge[1]} for edge in G.edges]

# Create JSON
graph_json = {
    "nodes": nodes,
    "edges": edges
}

print(json.dumps(graph_json, indent=2))
```

## Extracting Surrounding Explanatory Text and Formulas

To accomplish the task of extracting surrounding explanatory text separately from formula text and returning formulas in LaTeX, let's consider a general approach.

### Step 1: Preprocessing

First, you need to preprocess your text. This involves cleaning and possibly tokenizing the text into smaller parts that can be analyzed.

### Step 2: Identifying Formulas

Next, you'll need to identify the parts of the text that are mathematical formulas. This can be challenging because it depends on how the formulas are represented in your text.

### Step 3: Extraction

Once you've identified the formulas, you can extract them.

### Step 4: Conversion and Separation

If the formulas are not already in LaTeX format, you might need to convert them into LaTeX.

### Example Approach in Python

Here's a simple example using Python:

```python
import re

def extract_and_convert(text):
    # Simple example: assuming formulas are enclosed in $...$
    pattern = r'\$(.*?)\$'
    formulas = re.findall(pattern, text)
    explanatory_text = re.sub(pattern, '', text)

    latex_formulas = []
    for formula in formulas:
        latex_formula = f"${formula}$"
        latex_formulas.append(latex_formula)

    return explanatory_text, latex_formulas

# Example usage
text = "The Pythagorean theorem is $a^2 + b^2 = c^2$. This is very useful."
explanatory_text, latex_formulas = extract_and_convert(text)

print("Explanatory Text:")
print(explanatory_text)
print("\nLaTeX Formulas:")
for i, formula in enumerate(latex_formulas):
    print(f"Formula {i+1}: {formula}")
```

## Limitations

- **Complexity of Formulas**: The above example assumes a very simple scenario. Real-world formulas can be much more complex and may require more sophisticated parsing and conversion techniques.
- **Existing LaTeX Commands**: If your input is already in LaTeX, you'll need to handle LaTeX commands and environments specifically.

## Conclusion

The task involves text processing and potentially complex parsing and conversion steps. The specifics can vary greatly depending on your exact requirements and the structure of your input.

## Part 2 — Access Control
### Measuring Iris Similarity

Iris similarity is based on Hamming distance, defined as:

d(x,y) = # of non-match bits / # of bits compared

Examples:
- d(0010,0101) = 3/4
- d(101111,101001) = 1/3

The Hamming distance is computed on a 2048-bit iris code. A perfect match is indicated by d(x,y) = 0. 

For the same iris, the expected distance is 0.08, while a random match is expected to have a distance of 0.50. 

An iris scan is accepted as a match if the distance is less than 0.32.

# Part 2 — Access Control
## Iris Scan Error Rate

* distance
* distance
* Fraud rate
* == equal error rate

## Graph Representation in JSON

To provide a structured graph representation in JSON, including node labels, edge lists, and directionality, let's consider a simple example graph. We'll define a directed graph with nodes (also known as vertices) and edges. The graph will have directionality, meaning the edges have a direction from one node to another.

### Example Graph

* **Nodes**: A, B, C, D, E
* **Edges**:
  - A → B
  - A → C
  - B → D
  - C → E
  - D → E
  - E → B

### JSON Representation

Here's how you could represent this graph in JSON, including node labels, edge lists, and directionality:

```json
{
  "nodes": [
    {"id": "A", "label": "Node A"},
    {"id": "B", "label": "Node B"},
    {"id": "C", "label": "Node C"},
    {"id": "D", "label": "Node D"},
    {"id": "E", "label": "Node E"}
  ],
  "edges": [
    {"source": "A", "target": "B", "direction": "OUT"},
    {"source": "A", "target": "C", "direction": "OUT"},
    {"source": "B", "target": "D", "direction": "OUT"},
    {"source": "C", "target": "E", "direction": "OUT"},
    {"source": "D", "target": "E", "direction": "OUT"},
    {"source": "E", "target": "B", "direction": "OUT"}
  ]
}
```

However, for a more compact and standard representation, especially in graph databases and libraries (like Neo4j, NetworkX), you might see it represented with an adjacency list or directly with nodes and edges without explicit direction labels, assuming an inherent directionality:

```json
{
  "nodes": ["A", "B", "C", "D", "E"],
  "edges": [
    {"from": "A", "to": "B"},
    {"from": "A", "to": "C"},
    {"from": "B", "to": "D"},
    {"from": "C", "to": "E"},
    {"from": "D", "to": "E"},
    {"from": "E", "to": "B"}
  ]
}
```

Or, with more detailed node information and implicit directionality:

```json
{
  "nodes": [
    {"id": "A"},
    {"id": "B"},
    {"id": "C"},
    {"id": "D"},
    {"id": "E"}
  ],
  "edges": [
    {"source": "A", "target": "B"},
    {"source": "A", "target": "C"},
    {"source": "B", "target": "D"},
    {"source": "C", "target": "E"},
    {"source": "D", "target": "E"},
    {"source": "E", "target": "B"}
  ]
}
```

### Code to Generate This JSON

If you're working in Python, here's a simple way to generate such a JSON structure:

```python
import json

class Graph:
    def __init__(self):
        self.nodes = []
        self.edges = []

    def add_node(self, id, label=None):
        self.nodes.append({"id": id, "label": label or f"Node {id}"})

    def add_edge(self, source, target):
        self.edges.append({"source": source, "target": target})

    def to_json(self):
        return json.dumps(self, default=lambda o: o.__dict__, indent=2)

# Usage
graph = Graph()
for char in 'ABCDE':
    graph.add_node(char)

edges = [('A', 'B'), ('A', 'C'), ('B', 'D'), ('C', 'E'), ('D', 'E'), ('E', 'B')]
for edge in edges:
    graph.add_edge(*edge)

print(graph.to_json())
```

Alternatively, you can use the following Python script:

```python
import json

# Example graph data
nodes = ['A', 'B', 'C', 'D', 'E']
edges = [('A', 'B'), ('A', 'C'), ('B', 'D'), ('C', 'E'), ('D', 'E'), ('E', 'B')]

# Convert to JSON friendly format
json_data = {
    "nodes": nodes,
    "edges": [{"from": e[0], "to": e[1]} for e in edges]
}

# Export to JSON
json_string = json.dumps(json_data, indent=2)
print(json_string)
```

Or, define classes for `Node`, `Edge`, and `Graph`, and then use these to construct the graph and print its JSON representation:

```python
import json

class Node:
    def __init__(self, label):
        self.label = label

class Edge:
    def __init__(self, source, target, direction="out"):
        self.source = source
        self.target = target
        self.direction = direction

class Graph:
    def __init__(self, directionality="directed"):
        self.nodes = []
        self.edges = []
        self.directionality = directionality

    def add_node(self, node):
        self.nodes.append({"label": node.label})

    def add_edge(self, edge):
        self.edges.append({"source": edge.source, "target": edge.target, "direction": edge.direction})

    def to_json(self):
        graph_json = {
            "nodes": self.nodes,
            "edges": self.edges,
            "directionality": self.directionality
        }
        return graph_json

# Usage
graph = Graph()

node_a = Node("A")
node_b = Node("B")
node_c = Node("C")
node_d = Node("D")
node_e = Node("E")

graph.add_node(node_a)
graph.add_node(node_b)
graph.add_node(node_c)
graph.add_node(node_d)
graph.add_node(node_e)

edge_ab = Edge("A", "B")
edge_ac = Edge("A", "C")
edge_bd = Edge("B", "D")
edge_ce = Edge("C", "E")
edge_de = Edge("D", "E")
edge_eb = Edge("E", "B")

graph.add_edge(edge_ab)
graph.add_edge(edge_ac)
graph.add_edge(edge_bd)
graph.add_edge(edge_ce)
graph.add_edge(edge_de)
graph.add_edge(edge_eb)

print(json.dumps(graph.to_json(), indent=2))
```

## Part 2 — Access Control
### Attack on Iris Scan

An attacker could use a good photo of an eye to bypass an iris scan. For example, an Afghan woman was authenticated by an iris scan using an old photo. 
The story can be found [here](link). 
To prevent such an attack, a scanner could use light to verify that it is scanning a "live" iris.

## Part 2 — Access Control

### Equal Error Rate Comparison

The equal error rate (EER) is where the fraud rate equals the insult rate. 
Fingerprint biometrics used in practice have EERs ranging from about $10^{-3}$ to as high as 5%. 
Hand geometry has an EER of about $10^{-3}$. 
In theory, iris scan has an EER of about $10^{-6}$. 

The enrollment phase may be critical to accuracy. 
Most biometrics are much worse than fingerprint. 
Biometrics are useful for authentication, but for identification, not so impressive today.

## Part 2 — Access Control
### Biometrics: The Bottom Line

Biometrics are hard to forge. However, an attacker could:
- Steal Alice’s thumb
- Photocopy Bob’s fingerprint, eye, etc.
- Subvert software, database, “trusted path” …

And there's the issue of revoking a “broken” biometric.

Biometrics are not foolproof. 
Biometric use is relatively limited today. 
That should change in the (near?) future.

## Thông Tin Bảo Mật
## InfoSec

## Mục Tiêu
- Đảm bảo tính bảo mật (confidentiality)
- Đảm bảo tính toàn vẹn (integrity)
- Đảm bảo tính sẵn sàng (availability)

## Các Thành Phần Của An Toàn Thông Tin
- **An toàn** (safety): đảm bảo hệ thống hoạt động đúng và an toàn
- **An ninh** (security): bảo vệ hệ thống và dữ liệu khỏi truy cập trái phép

## Các Loại Tấn Công
### Tấn Công Chủ Động (Active Attack)
- Làm thay đổi dữ liệu
- Ví dụ: giả mạo, thêm, xóa dữ liệu

### Tấn Công Bị Động (Passive Attack)
- Không làm thay đổi dữ liệu
- Ví dụ: nghe lén, thu thập thông tin

## Mô Hình Bảo Mật
### Mô Hình OSI 7 Lớp
| Lớp | Chức Năng |
| --- | --- |
| 7 | Application |
| 6 | Presentation |
| 5 | Session |
| 4 | Transport |
| 3 | Network |
| 2 | Data Link |
| 1 | Physical |

## Các Cơ Chế Bảo Mật
### Mã Hóa (Encryption)
- **Mã hóa đối xứng** (symmetric encryption): sử dụng cùng một khóa để mã hóa và giải mã
- **Mã hóa bất đối xứng** (asymmetric encryption): sử dụng một cặp khóa (công khai và riêng tư)

## Công Thức Mã Hóa
- **DES (Data Encryption Standard)**: sử dụng mã hóa đối xứng
- **RSA (Rivest-Shamir-Adleman)**: sử dụng mã hóa bất đối xứng

## Các Kĩ Thuật Mã Hóa
### Kĩ Thuật Mã Hóa Đối Xứng
- **AES (Advanced Encryption Standard)**
- **DES (Data Encryption Standard)**

### Kĩ Thuật Mã Hóa Bất Đối Xứng
- **RSA (Rivest-Shamir-Adleman)**
- **DSA (Digital Signature Algorithm)**
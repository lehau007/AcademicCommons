## Identity Authentication

- With extra material for further reading, indicated by symbol *

## Authentication Basics
- Passwords
- Challenge-Response
- Biometrics
- Location
- Multiple Methods

## Basics
- Authentication: binding of identity to subject
- Identity is that of external entity (my identity, Van, etc.)
- Subject is computer entity (process, etc.)
- Note: 
  - message authentication is a different topic and already mentioned in the applications of hash functions

## Establishing Identity

- What entity knows (e.g. password)
- What entity has (e.g. Identity card, smart card)
- What entity is (e.g. fingerprints, retinal characteristics)
- Where entity is (e.g. In front of a particular terminal)

## Authentication System

We need a formal definition, rather abstract view, of an AS 
A 5-tuple (A, C, F, L, S)
- A – a set: information that proves identity
- C – a set: information stored on computer and used to validate authentication information
- F: a set of complementation functions; f : A → C 
  To compute complement information from identity information
- L: authentication functions that prove identity
- S: functions enabling entity to create, alter information in A or C

## Info-Sec 2023 Example

- Password system, with passwords stored on line in clear text
- A set of strings making up passwords
- C = A
- F: singleton set of identity function { I }
- L: single equality test function { eq }
- S: function to set/change password

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
  - Reduces to previous problem → need something else
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
- Two ways to determine whether a meets these requirements:
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
  - P: probability of guessing a password in specified period of time
  - G: number of guesses tested in 1 time unit
  - T: number of time units
  - N: number of possible passwords (|A|)
- [Formula: probability of guessing a password] P ≥ TG/N

## Example
- Goal: Passwords drawn from a 96-char alphabet
- Can test 10^4 guesses per second
- Probability of a success to be 0.5 over a 365 day period
- What is minimum password length?

## Solution
- Solution: N ≥ TG/P = (365×24×60×60)×10^4/0.5 = 6.31×10^11
- Choose s such that Σs j=0 96j ≥ N
- So s ≥ 6, meaning passwords must be at least 6 chars long

## Exercise
- Assume that X = number defined by last 2 digits of your student ID; Y = X mod 4
- Assume that H is a cryptographic hash function with output size (Y+2)*16 bits.
- Assume that Scorpion-i (i=1-9) is a specifically designed line of hardware chips for computing H, where Scorpion-i can create 10i * 1000 hash values a second.
- This product line is the best, fastest and affordable, in the market, priced at i^2/2 *$1000.

## Authentication System
- An authentication system requires its users to pick their passwords of length exactly 6 from an alphabet of size N=(X mod 50)+ 40.
- Using H, this system maintains the hash values of the passwords of all the users.

## Off-line Attack
- An enemy, who has gained access to this hashed password file, aims to launch an off-line attack to break the password of an important user.
- Using the Scorpion chips, the enemy wants to finish within a month with success probability (6+Y)*10%.

## Cost Calculation
- To calculate the cost, we need to determine the number of hash values the enemy needs to compute: 
  | Success Probability | Value |
  | --- | --- |
  | (6+Y)*10% |  |
- Assuming a month is approximately 2.6*10^6 seconds, and using the Scorpion-i chip which can compute 10i * 1000 hash values per second, 
  the cost will be i^2/2 *$1000. 
- The exact calculation will depend on X and Y. 

## No additional text 
(no additional text to process)

## On password selection
- Random selection
- Any password from A equally likely to be selected
- Pronounceable passwords
- User selection of passwords

## Pronounceable Passwords

- Generate phonemes randomly
- Phoneme is unit of sound, e.g. cv, vc, cvc, vcv
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

- Names of members of 2 families: “LlMm*2^Ap”, “OoHeO/FSK”
- Second letter of each word of length 4 or more in third line of third verse of Star-Spangled Banner, followed by “/”, followed by author’s initials: 
- What’s good here may be bad there: “DMC/MHmh” 
  - bad at Dartmouth (“Dartmouth Medical Center/Mary Hitchcock memorial hospital”), ok here
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

## Unix Authentication System
- UNIX system standard hash function
- Hashes password into 11 char string using one of 4096 hash functions
- As authentication system:
  - A = { strings of 8 chars or less }
  - C = { 2 char hash id || 11 char hash }
  - F = { 4096 versions of modified DES }
  - L = { login, su, … }
  - S = { passwd, nispasswd, passwd+, … }

## Exercise

Assume that H is a cryptographic hash function with output size (Y+2)*16 bits. Assume that Scorpion-i (i=1-9) is a specifically designed line of hardware chips for computing H, where Scorpion-i can create 10i * 1000 hash values a second, priced at ii/2 *$1000.

- An authentication system requires its users to pick their passwords of length exactly 6 from an alphabet of size N=(X mod 50)+ 40.
- Using H, this system maintains the hash values of the passwords of all the users.
- An enemy, who has gained access to this hashed password file, aims to launch an off-line attack to break the password of an important user.
- Using the Scorpion chips, how much the enemy has to spend in order to finish within a month with success probability (6+Y)*10%?

## Enhanced Password System

- The owner decides to enhance the above password system by using salt so that the enemy will need to spend at least 10 times the above mentioned amount of money to achieve the same goal.
- How many salt bits he/she need to use to achieve this purpose?

## Password Cracking: Do the Math

* Further reading
Assumptions:
- Pwds are 8 chars, 128 choices per character
- Then 128^8 = 2^56 possible passwords
- There is a password file with 2^10 pwds
- Attacker has dictionary of 2^20 common pwds
- Probability 1/4 that password is in dictionary
Work is measured by number of hashes

## Part 2 ⎯ Access Control

- Salt with slow hash *
- Hash password with salt
- Choose random salt s and compute 
  y = h(password, s) 
  and store (s,y) in the password file
- Note that the salt s is not secret
- Analogous to IV 
- Still easy to verify salted password
- But lots more work for Hacker
- Why?

## Password Cracking: Case I

- Attack 1 specific password without using a dictionary
- E.g., administrator’s password
- Must try 2^8/2 = 255 on average 
- Like exhaustive key search
- Does salt help in this case?

## Password Cracking: Case II

- Attack 1 specific password with dictionary
  - With salt
    - Expected work: [Formula: 1/4 (2^19) + 3/4 (2^55) ≈ 2^54.6]
    - In practice, try all pwds in dictionary…
    - …then work is at most 2^20 and probability of success is 1/4 
  - What if no salt is used?
    - One-time work to compute dictionary: 2^20
    - Expected work is of same order as above
    - But with precomputed dictionary hashes, the  “in practice” attack is essentially free…

## Password Cracking: Case III

- Assume all 2<sup>10</sup> passwords are distinct 
- Need 2<sup>55</sup> comparisons before expect to find pwd
- If no salt is used
  - Each computed hash yields 2<sup>10</sup> comparisons
  - So expected work (hashes) is 2<sup>55</sup> / 2<sup>10</sup> = 2<sup>45</sup>
- If salt is used
  - Expected work is 2<sup>55</sup> 
  - Each comparison requires a hash computation

## Password Cracking: Case IV

- Any of 1024 pwds in file, with dictionary
- Prob. one or more pwd in dict.: 1 – (3/4)1024 ≈ 1
- So, we ignore case where no pwd is in dictionary
- If salt is used, expected work less than 2^22
- See book, or slide notes for details
- Work ≈ size of dictionary / P(pwd in dictionary)

## What if no salt is used?

- If dictionary hashes not precomputed, work is about 2^19/2^10 = 2^9

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

- User and system share a secret function f (in practice, f is a known function with unknown parameters, such as a cryptographic key)
- The process works as follows:
  - User requests to authenticate
  - System sends a random message r (the challenge)
  - User responds with f(r) (the response) 
  - [Formula: response calculated using challenge and shared secret]

## Pass Algorithms
- Challenge-response with the function f itself a secret
- Challenge is a random string of characters 
- Response is some function of that string 
- Usually used in conjunction with fixed, reusable password

## One-Time Passwords

- Password that can be used exactly once
- After use, it is immediately invalidated
- Challenge-response mechanism
  - Challenge is number of authentications
  - Response is password for that particular number
- Problems
  - Synchronization of user, system
  - Generation of good random passwords
  - Password distribution problem

## S/Key

- One-time password scheme based on idea of Lamport
- h one-way hash function (MD5 or SHA-1, for example)
- User chooses initial seed k
- System calculates:
  - h(k) = k1 
  - h(k1) = k2 
  - … 
  - h(kn–1) = kn
- Passwords are reverse order:
  - p1 = kn 
  - p2 = kn–1 
  - … 
  - pn–1 = k2 
  - pn = k1

## S/Key Protocol

The system stores the maximum number of authentications `n`, the number of the next authentication `i`, and the last correctly supplied password `pi–1`.

The system computes:
- `h(pi) = h(kn–i+1) = kn–i+2 = pi–1`

If the computed value matches what is stored, the system:
- Replaces `pi–1` with `pi`
- Increments `i`

## C-R and Dictionary Attacks

- Same as for fixed passwords
- Attacker knows challenge `r` and response `f(r)`; if `f` encryption function, can try different keys
- May only need to know form of response; attacker can tell if guess correct by looking to see if deciphered object is of right form
- Example: Kerberos Version 4 used DES, but keys had 20 bits of randomness; Purdue attackers guessed keys quickly because deciphered tickets had a fixed set of bits in some locations

## Encrypted Key Exchange 

* Defeats off-line dictionary attacks
* Idea: random challenges enciphered, so attacker cannot verify correct decipherment of challenge
* Assume Alice, Bob share secret password s
* In what follows, Alice needs to generate a random public key p and a corresponding private key q
* Also, k is a randomly generated session key, and RA and RB are random challenges

## EKE Protocol
- Now Alice, Bob share a randomly generated secret session key k

## Access Control
- Something You Have
- Something in your possession
- Examples include following:
  - Car key
  - Laptop computer (or MAC address)
  - Password generator 
  - ATM card, smartcard, etc.

## Hardware Support

- Token-based authentication
  - Used to compute response to challenge
  - May encipher or hash challenge
  - May require PIN from user
- Object user possesses to authenticate, e.g.
  - memory card (magnetic stripe)
  - smartcard

## Temporally-based Authentication

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
- challenge-response: computer creates a random number; smart card provides its hash [Formula: hash function output]
- also have USB dongles

## Electronic identity cards
- An important application of smart cards
- A national e-identity (eID) serves the same purpose as other national ID cards (e.g., a driver’s licence)
- Can provide stronger proof of identity

## A German card
- Personal data
- Document number
- Card access number (six digit random number)
- Machine readable zone (MRZ): the password
- Uses: 
  - ePass (government use)
  - eID (general use)
  - eSign (can have private key and certificate)

## User authentication with eID

- *No content provided.* 

Please provide the rest of the text for me to reformat. I will make sure to follow the guidelines. 

If you provide more text, I can assist you with:

- Converting to Markdown headings
- Formatting bullet points
- Removing standalone page numbers and navigation headers
- Replacing garbled formula characters
- Preserving tables as Markdown tables

Please go ahead and provide the rest of the text.

## Something You Are
Biometric
“You are your key” ⎯ Schneier
- Are
- Know
- Have
- Examples
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

## Biometric Authentication
- Authenticate user based on one of their physical characteristics:
  - facial
  - fingerprint
  - hand geometry
  - retina pattern
  - iris
  - signature
  - voice

## Table Extraction and JSON Formatting
To accurately extract row labels, column labels, and cell values from a given table and return them in a structured JSON format.

## Hypothetical Table Example
| Country     | Population (2020) | GDP (Billion USD) |
|-------------|-------------------|-------------------|
| USA         | 331,449,281       | 22.67             |
| China       | 1,439,323,776     | 16.14             |
| Japan       | 127,171,983       | 5.15              |

## JSON Output Example
```json
{
  "schema_version": "1.0",
  "content_type": "tabular_data",
  "row_labels": ["USA", "China", "Japan"],
  "column_labels": ["Country", "Population (2020)", "GDP (Billion USD)"],
  "values": [
    ["USA", 331449281, 22.67],
    ["China", 1439323776, 16.14],
    ["Japan", 127171983, 5.15]
  ],
  "notes": "Data is representative and used for demonstration purposes."
}
```

## Python Example for HTML Table Extraction
```python
import pandas as pd
import json

def extract_from_html_table(html_table_string):
    try:
        df = pd.read_html(html_table_string)[0]
        data = {
            "schema_version": "1.0",
            "content_type": "tabular_data",
            "row_labels": df.index.tolist(),
            "column_labels": df.columns.tolist(),
            "values": df.values.tolist(),
            "notes": "Extracted from HTML table."
        }
        return data
    except Exception as e:
        return {"error": str(e)}

html_string = """
<table>
  <tr>
    <th>Country</th>
    <th>Population (2020)</th>
    <th>GDP (Billion USD)</th>
  </tr>
  <tr>
    <td>USA</td>
    <td>331,449,281</td>
    <td>22.67</td>
  </tr>
  <tr>
    <td>China</td>
    <td>1,439,323,776</td>
    <td>16.14</td>
  </tr>
  <tr>
    <td>Japan</td>
    <td>127,171,983</td>
    <td>5.15</td>
  </tr>
</table>
"""

data = extract_from_html_table(html_string)
print(json.dumps(data, indent=2))
```
This Python example demonstrates how to extract data from an HTML table. Adjustments would be needed based on the actual source and structure of your table. For direct CSV files, you could use `pd.read_csv()` instead.

## Operation of a Biometric System

- Verification is analogous to user login via a smart card and a PIN
- Identification is biometric info but no IDs; system compares with stored templates

## Biometric Accuracy
- Palm print: The system generates a matching score (a number) that quantifies similarity between the input and the stored template
- Concerns: sensor noise and detection inaccuracy
- Problems of false match/false non-match
- Further reading (Stallings textbook)

## Extracting Table Data
To accurately extract row labels, column labels, and cell values from a given table or matrix, a sample table is needed as input. 

## Example Table
| Country  | GDP (Billions) | Population (Millions) |
|----------|----------------|-----------------------|
| USA      | 22.67           | 331                   |
| China    | 16.14           | 1449                  |
| Japan    | 5.15            | 128                   |

## Example Table Description
- **Row Labels:** Country names (USA, China, Japan)
- **Column Labels:** GDP (Billions), Population (Millions)
- **Cell Values:** The numeric values within the table.

## JSON Output
Given the table, here is how you might represent it in JSON format:
```json
{
  "schema_version": "1.0",
  "content_type": "tabular_data",
  "row_labels": ["USA", "China", "Japan"],
  "column_labels": ["GDP (Billions)", "Population (Millions)"],
  "values": [
    [22.67, 331],
    [16.14, 1449],
    [5.15, 128]
  ],
  "notes": "Economic data for major countries."
}
```

## Achieving This Programmatically
If you were to do this programmatically, you could follow these steps:
- Read the Input Data: Depending on the format of your input data (e.g., CSV, Excel, direct input), choose an appropriate library to read it.
- Identify Row Labels, Column Labels, and Cell Values:
  - Row labels are usually in the first column.
  - Column labels are typically at the top row.
  - Cell values are the numeric or text data within the table.
- Structure the Data: Organize the data into the required JSON schema.

## Python Example
Here's a simple Python example using `pandas` for data manipulation and `json` for handling JSON:
```python
import pandas as pd
import json

# Sample data
data = {
    "Country": ["USA", "China", "Japan"],
    "GDP (Billions)": [22.67, 16.14, 5.15],
    "Population (Millions)": [331, 1449, 128]
}

# Create DataFrame
df = pd.DataFrame(data).set_index('Country')

# Convert to JSON
output = {
    "schema_version": "1.0",
    "content_type": "tabular_data",
    "row_labels": list(df.index),
    "column_labels": list(df.columns),
    "values": df.values.tolist(),
    "notes": "Economic data for major countries."
}

# Pretty print JSON
print(json.dumps(output, indent=2))
```
This example assumes you start with structured data. Adjustments would be needed based on the actual source and structure of your data.

## Biometric Accuracy

- Can plot characteristic curve (2,000,000 comparisons)
- Pick threshold balancing error rates

## Cautions
- These can be fooled!
- Assumes biometric device accurate in the environment it is being used in!
- Transmission of data to validator is tamperproof, correct

## Biometrics: The Bottom Line
- Biometrics are hard to forge
- But attacker could
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

- auth sufficient /usr/lib/pam_ftp.so
- auth required /usr/lib/pam_unix_auth.so use_first_pass
- auth required /usr/lib/pam_listfile.so onerr=succeed \
  item=user sense=deny file=/etc/ftpusers

## PAM FTP Authentication Logic

For ftp:
- If user “anonymous”, return okay; if not, set [Formula: PAM authentication token] to password, [Formula: PAM remote user] to name, and fail
- Now check that password in [Formula: PAM authentication token] belongs to that of user in [Formula: PAM remote user]; if not, fail
- Now see if user in [Formula: PAM remote user] named in /etc/ftpusers; if so, fail; if error or not found, succeed

## Extended Material * Kerberos authentication protocol

- Material sources: History & some general info from Wiki;
- Details on Kerberos versions 4&5 from Stallings Text and slides

## Kerberos
- A computer network authentication protocol which allows nodes communicating over a non-secure network to prove their identity to one another in a secure manner.
- Aimed primarily at a client-server model, and it provides mutual authentication -- both the user and the server verify each other's identity.
- Messages are protected against eavesdropping & replay attacks.
- Kerberos builds on SKC and requires a trusted third party, and optionally may use [Formula: public-key cryptography] during certain phases of authentication.

## Kerberos
- named after the character Kerberos (or Cerberus), the ferocious three-headed guard dog of Hades (from Greek mythology)
- MIT developed Kerberos in 1988 to protect network services provided by Project Athena.
- 1st version was primarily designed by Steve Miller and Clifford Neuman based on the earlier Needham–Schroeder symmetric-key protocol. Ver 1 - 3 were experimental, internal.
- Kerberos version 4, the first public version, was released on January 24, 1989.
- Neuman and John Kohl published v5 in 1993 with the intention of overcoming existing limitations and security problems. Version 5 appeared as RFC 1510, which was then made obsolete by RFC 4120 in 2005. In 2005, the Internet Engineering Task Force (IETF) Kerberos working group updated specifications.

## Idea

- The issuer vouches for the identity of the requester of service
- Identifies sender
- Key Distribution Center (KDC) combines two servers: 
  - Authentication Server, AS (Also, Kerberos server)
  - Ticket Granting Server, TGS

## Kerberos Process

- User `u` authenticates to AS
- Obtains ticket `Tu,TGS` for ticket granting service (TGS)
- User `u` wants to use service `s`:
  - User sends authenticator `Au`, ticket `Tu,TGS` to TGS asking for ticket for service
  - TGS sends ticket `Tu,s` to user
  - User sends `Au`, `Tu,s` to server as request to use `s`

## Kerberos v4 Overview

- a basic third-party authentication scheme
- have an Authentication Server (AS) 
- users initially negotiate with AS to identify self 
- AS provides a non-corruptible authentication credential (ticket granting ticket TGT) 
- have a Ticket Granting server (TGS)
- users subsequently request access to other services from TGS on basis of users TGT
- using a complex protocol using DES

## Kerberos 4 Overview

To provide a structured graph representation in JSON, including node labels, edge lists, and directionality, let's consider a simple example graph. We'll define a directed graph with 5 nodes and 6 edges.

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

However, for a more conventional and compact graph representation in JSON, especially in graph libraries and databases, you might see it represented with an adjacency list or with simpler node and edge definitions:

### Alternative JSON Representation

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

Or, even more succinctly:

### Succinct JSON Representation

```json
{
  "nodes": ["A", "B", "C", "D", "E"],
  "links": [
    ["A", "B"],
    ["A", "C"],
    ["B", "D"],
    ["C", "E"],
    ["D", "E"],
    ["E", "B"]
  ]
}
```

### Directionality

- In all representations above, edges are considered directed, from the source (or `from`) node to the target (or `to`) node.
- If the graph were undirected, you might either:
  1. Not specify directionality.
  2. Ensure that each edge is represented in both directions (e.g., ["A", "B"] and ["B", "A"]).

### Code to Generate

If you were to generate such a graph representation programmatically, you might start with a basic structure like this in Python:

```python
import json

class Graph:
    def __init__(self):
        self.nodes = []
        self.edges = []

    def add_node(self, id, label):
        self.nodes.append({"id": id, "label": label})

    def add_edge(self, source, target):
        self.edges.append({"source": source, "target": target, "direction": "OUT"})

    def to_json(self):
        return json.dumps(self, default=lambda o: o.__dict__, indent=2)

# Example usage
g = Graph()
g.add_node("A", "Node A")
g.add_node("B", "Node B")
# ... add other nodes
g.add_edge("A", "B")
g.add_edge("A", "C")
# ... add other edges

print(g.to_json())
```

This example provides a basic framework. Adjustments might be needed based on the specific requirements or libraries you're working with.

## Kerberos v4 Dialogue

No content on this slide.

## Example Graph

- **Nodes**: A, B, C, D, E
- **Edges**:
  - A → B
  - A → C
  - B → D
  - C → E
  - D → E
  - E → B

## JSON Representation

Here's how you could represent this graph in JSON, including node labels, edge list, and directionality:

| Key | Description |
| --- | --- |
| nodes | An array of node objects, each with an `id` and a `label`. |
| edges | An array of edge objects, each with a `source`, `target`, and `direction`. |
| graphProperties | A simple object to denote if the graph is directed or not. |

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
  ],
  "graphProperties": {
    "directed": true
  }
}
```

## Explanation

- **nodes**: An array of node objects, each with an `id` and a `label`.
- **edges**: An array of edge objects, each with a `source`, `target`, and `direction`. The direction is represented as "OUT" for outgoing edges, but you could adjust this to better fit your needs (e.g., "IN" for incoming, "BOTH" for undirected).
- **graphProperties**: A simple object to denote if the graph is directed or not.

## Python Script to Generate This JSON

```python
import json

def create_graph_json(nodes, edges):
    graph_json = {
        "nodes": [{"id": node, "label": f"Node {node}"} for node in nodes],
        "edges": [{"source": edge[0], "target": edge[1], "direction": "OUT"} for edge in edges],
        "graphProperties": {"directed": True}
    }
    return json.dumps(graph_json, indent=2)

# Define your graph
nodes = ['A', 'B', 'C', 'D', 'E']
edges = [('A', 'B'), ('A', 'C'), ('B', 'D'), ('C', 'E'), ('D', 'E'), ('E', 'B')]

# Generate and print JSON
print(create_graph_json(nodes, edges))
```

This script takes a list of nodes and edges as input and generates a JSON string representing the graph. You can adjust the node and edge definitions to fit your specific use case.

## Kerberos Version 5

- developed in mid 1990’s
- specified as Internet standard RFC 1510
- provides improvements over v4
- addresses environmental shortcomings
  - encryption alg
  - network protocol
  - byte order
  - ticket lifetime
  - authentication forwarding
  - interrealm auth
- and technical deficiencies
  - double encryption
  - non-std mode of use
  - session keys
  - password attacks

## Kerberos Realms

- A Kerberos environment consists of:
  - A Kerberos server
  - A number of clients, all registered with the server
  - Application servers, sharing keys with the server
- This is termed a realm
- Typically a single administrative domain
- If have multiple realms, their Kerberos servers must share keys and trust

## Kerberos Realms

No visual element provided. Please share the visual element, and I'll describe its content in a way that focuses on its learning value.

## Protocol

- Client Authentication to the AS
- Client Service Authorization
- Client Service Request

## Example Graph

Suppose we have a graph with the following properties:

- **Nodes (Vertices):** A, B, C, D
- **Edges:** 
  - A -> B (directed from A to B)
  - B -> C (directed from B to C)
  - C -> A (directed from C to A)
  - D -> B (directed from D to B)

## JSON Representation

A common JSON representation for a graph might involve specifying nodes and edges separately. Here's one way to structure it:

| Key  | Value |
|------|-------|
| nodes | Array of node objects |
| edges | Array of edge objects |

Example:
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

However, for a more detailed and structured representation that includes directionality explicitly in the graph definition, you might use a format like GraphJSON or adopt a more verbose JSON structure. Here's an alternative:

```json
{
  "graph": {
    "nodes": [
      {"id": "A"},
      {"id": "B"},
      {"id": "C"},
      {"id": "D"}
    ],
    "edges": [
      {
        "id": "edge1",
        "source": "A",
        "target": "B",
        "directionality": "directed"
      },
      {
        "id": "edge2",
        "source": "B",
        "target": "C",
        "directionality": "directed"
      },
      {
        "id": "edge3",
        "source": "C",
        "target": "A",
        "directionality": "directed"
      },
      {
        "id": "edge4",
        "source": "D",
        "target": "B",
        "directionality": "directed"
      }
    ],
    "directed": true
  }
}
```

## Directionality

- In the context of graph theory, a **directed graph** (or digraph) is a graph where edges have direction, represented by an ordered pair of vertices.
- The **directionality** of an edge in a directed graph refers to the direction in which the edge traverses.

## Code to Generate This JSON

If you were to generate this JSON programmatically, you might do something like this in Python:

```python
import json

class Graph:
    def __init__(self, directed=True):
        self.nodes = []
        self.edges = []
        self.directed = directed

    def add_node(self, id):
        self.nodes.append({"id": id})

    def add_edge(self, source, target):
        self.edges.append({"source": source, "target": target, "direction": "out"})

    def to_json(self):
        graph_json = {
            "nodes": self.nodes,
            "edges": self.edges
        }
        return json.dumps(graph_json, indent=2)

# Usage
g = Graph()
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

This Python code defines a simple graph data structure and can output a JSON representation of the graph.

## Kerberos v5 Dialogue

No content on this slide.

## Example Graph

To provide a structured graph representation in JSON, including node labels, edge lists, and directionality, let's consider a simple example graph. We'll define a directed graph with 5 nodes and 6 edges.

- **Nodes**: A, B, C, D, E
- **Edges**:
  - A → B
  - A → C
  - B → D
  - C → E
  - D → E
  - E → B

## JSON Representation

Here's how you could represent this graph in JSON, including node labels, edge lists, and directionality:

| Key  | Value |
|------|-------|
| nodes | [     |
|      |   {"id": "A", "label": "Node A"}, |
|      |   {"id": "B", "label": "Node B"}, |
|      |   {"id": "C", "label": "Node C"}, |
|      |   {"id": "D", "label": "Node D"}, |
|      |   {"id": "E", "label": "Node E"}  |
|    ] |
| edges | [     |
|      |   {"source": "A", "target": "B", "direction": "OUT"}, |
|      |   {"source": "A", "target": "C", "direction": "OUT"}, |
|      |   {"source": "B", "target": "D", "direction": "OUT"}, |
|      |   {"source": "C", "target": "E", "direction": "OUT"}, |
|      |   {"source": "D", "target": "E", "direction": "OUT"}, |
|      |   {"source": "E", "target": "B", "direction": "OUT"}  |
|    ] |

However, for a more compact and standard representation, especially when using popular graph libraries or frameworks, you might see variations. For instance, some representations might not explicitly mention directionality if it's implied by the structure (e.g., in a directed graph, every edge has a direction).

## Alternative Compact Representation

| Key  | Value |
|------|-------|
| nodes | ["A", "B", "C", "D", "E"] |
| edges | [     |
|      |   {"from": "A", "to": "B"}, |
|      |   {"from": "A", "to": "C"}, |
|      |   {"from": "B", "to": "D"}, |
|      |   {"from": "C", "to": "E"}, |
|      |   {"from": "D", "to": "E"}, |
|      |   {"from": "E", "to": "B"}  |
|    ] |

Or, if you're working with a format like GraphJSON or similar, which might derive directionality from the edge definition:

| Key  | Value |
|------|-------|
| nodes | [     |
|      |   {"id": "A"}, |
|      |   {"id": "B"}, |
|      |   {"id": "C"}, |
|      |   {"id": "D"}, |
|      |   {"id": "E"}  |
|    ] |
| edges | [     |
|      |   {"id": 1, "source": "A", "target": "B"}, |
|      |   {"id": 2, "source": "A", "target": "C"}, |
|      |   {"id": 3, "source": "B", "target": "D"}, |
|      |   {"id": 4, "source": "C", "target": "E"}, |
|      |   {"id": 5, "source": "D", "target": "E"}, |
|      |   {"id": 6, "source": "E", "target": "B"}  |
|    ] |

The best representation depends on your specific use case, tools, and libraries you're working with.

## Federated Identity Management

- use of common identity management scheme across multiple enterprises & numerous applications
- supporting many thousands, even millions of users
- principal elements are:
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

## Identity Federation

There is no visual element provided. Please share the visual element, and I will describe its content, focusing on the information that contributes to learning value.

## Standards Used

- Security Assertion Markup Language (SAML)
- XML-based language for exchange of security information between online business partners
- Part of OASIS (Organization for the Advancement of Structured Information Standards) standards for federated identity management
- e.g. WS-Federation for browser-based federation
- Need a few mature industry standards

## Federated Identity Examples

To provide a structured graph representation in JSON, including node labels, edge lists, and directionality, let's consider a simple example graph. This graph will have 5 nodes and 7 edges with specific directionality.

### Example Graph Description
- **Nodes**: A, B, C, D, E
- **Edges**:
  - A → B (directed)
  - A → C (directed)
  - B → D (directed)
  - C → E (directed)
  - D → E (directed)
  - E → B (directed)
  - E → A (directed)

### JSON Representation

Here's how you could represent this graph in JSON, including nodes, edges, and their directionality:

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
    {"source": "A", "target": "B", "direction": "OUT"},
    {"source": "A", "target": "C", "direction": "OUT"},
    {"source": "B", "target": "D", "direction": "OUT"},
    {"source": "C", "target": "E", "direction": "OUT"},
    {"source": "D", "target": "E", "direction": "OUT"},
    {"source": "E", "target": "B", "direction": "OUT"},
    {"source": "E", "target": "A", "direction": "OUT"}
  ],
  "graphProperties": {
    "directed": true
  }
}
```

However, a more compact and commonly used format for graph representation, especially in graph databases and libraries (like Neo4j, NetworkX), would focus on the edges for directed graphs since nodes can often be inferred from the edges:

```json
{
  "nodes": ["A", "B", "C", "D", "E"],
  "edges": [
    {"from": "A", "to": "B"},
    {"from": "A", "to": "C"},
    {"from": "B", "to": "D"},
    {"from": "C", "to": "E"},
    {"from": "D", "to": "E"},
    {"from": "E", "to": "B"},
    {"from": "E", "to": "A"}
  ],
  "directed": true
}
```

Or, focusing purely on essential information for a directed graph:

```json
{
  "directed": true,
  "nodes": ["A", "B", "C", "D", "E"],
  "links": [
    {"source": "A", "target": "B"},
    {"source": "A", "target": "C"},
    {"source": "B", "target": "D"},
    {"source": "C", "target": "E"},
    {"source": "D", "target": "E"},
    {"source": "E", "target": "B"},
    {"source": "E", "target": "A"}
  ]
}
```

## How to Extract

If you're extracting this information from a database or another data structure, you would:

- **Query** your data source to get the list of nodes and edges.
- **Iterate** through the edges to understand their directionality.
- **Format** the data into the desired JSON structure.

If you're working with a specific library or framework (like NetworkX in Python), you can use its built-in functions to create a graph, extract its components, and then serialize it into a JSON format. For example:

```python
import networkx as nx
import json

# Create a directed graph
G = nx.DiGraph()

# Add edges
G.add_edges_from([('A', 'B'), ('A', 'C'), ('B', 'D'), ('C', 'E'), ('D', 'E'), ('E', 'B'), ('E', 'A')])

# Serialize
data = {
    "directed": True,
    "nodes": list(G.nodes),
    "links": [{"source": e[0], "target": e[1]} for e in G.edges]
}

print(json.dumps(data, indent=2))
```

This would output a JSON representation similar to those shown above.

## FIM vs. SSO

- SSO: Single Sign-On
  - Allows users to access multiple web applications at once, using just one set of credentials.
  - Beyond the workforce, companies can utilize SSO to help customers access various sections of one account.
- FIM 
  - As a tool, SSO fits within the broader model of FIM.
  - The key difference between SSO and FIM is while SSO is designed to authenticate a single credential across various systems within one organization, federated identity management systems offer single access to a number of applications across various enterprises.

## Extended Material * Biometrics

Extended Material * Biometrics
Slides borrowed from Mark Stamp’s web
https://www.cs.sjsu.edu/~stamp/infosec/powerpoint/

## Something You Are
- Biometric
- “You are your key” ⎯ Schneier
- Categories:
  - Are
  - Know
  - Have
- Examples:
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
- In reality, OK if it remains valid for long time
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
- For example
  - 99% voiceprint match ⇒ low fraud, high insult
  - 30% voiceprint match ⇒ high fraud, low insult
- Equal error rate: rate where fraud == insult
- A way to compare different biometrics

## Fingerprint History
- 1823 — Professor Johannes Evangelist Purkinje discussed 9 fingerprint patterns
- 1856 — Sir William Hershel used fingerprint (in India) on contracts
- 1880 — Dr. Henry Faulds article in Nature about fingerprints for ID
- 1883 — Mark Twain’s Life on the Mississippi (murderer ID’ed by fingerprint)

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
  - Quick — 1 minute for enrollment, 5 seconds for recognition
  - Hands are symmetric — so what?
- Disadvantages
  - Cannot use on very young or very old
  - Relatively high equal error rate

## Iris Patterns
- Iris pattern development is “chaotic”
- Little or no genetic influence
- Even for identical twins, uncorrelated
- Pattern is stable through lifetime

## Iris Recognition: History
- 1936 — suggested by ophthalmologist
- 1980s — James Bond film(s)
- 1986 — first patent appeared
- 1994 — John Daugman patents new-and-improved technique
- Patents owned by Iridian Technologies

## Iris Scan
- Scanner locates iris
- Take b/w photo
- Use polar coordinates…
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
```
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

## Code to Generate JSON
If you were to generate this JSON programmatically, you might do something like:
```python
import json

class Graph:
    def __init__(self):
        self.nodes = []
        self.edges = []

    def add_node(self, id, label=None):
        self.nodes.append({"id": id, "label": label or f"Node {id}"})

    def add_edge(self, source, target):
        self.edges.append({"source": source, "target": target, "direction": "OUT"})

    def to_json(self):
        return json.dumps(self.__dict__, indent=2)

# Usage
graph = Graph()
for char in 'ABCDE':
    graph.add_node(char)

edges = [('A', 'B'), ('A', 'C'), ('B', 'D'), ('C', 'E'), ('D', 'E'), ('E', 'B')]
for source, target in edges:
    graph.add_edge(source, target)

print(graph.to_json())
```

## Another Graph Example
To provide a structured graph representation in JSON, including node labels, edge list, and directionality, let's consider another simple example graph. 

Let's say we have a graph with the following properties:
- **Nodes (Vertices):** A, B, C, D
- **Edges:** 
  - A -> B (directed from A to B)
  - B -> C (directed from B to C)
  - C -> A (directed from C to A)
  - D -> B (directed from D to B)

### JSON Representation
Here's how we can represent this graph in JSON, including node labels, edge list, and directionality:
```
{
  "nodes": [
    {"id": "A"},
    {"id": "B"},
    {"id": "C"},
    {"id": "D"}
  ],
  "edges": [
    {"from": "A", "to": "B"},
    {"from": "B", "to": "C"},
    {"from": "C", "to": "A"},
    {"from": "D", "to": "B"}
  ]
}
```

## Explanation
- **Nodes:** Each node is represented by a unique identifier (`id`). 
- **Edges:** Each edge is defined by a `from` node and a `to` node, which clearly indicates the direction of the edge.

## Code to Generate This JSON
If you're working in Python and want to create this structure programmatically:
```python
class Node:
    def __init__(self, id):
        self.id = id

class Edge:
    def __init__(self, from_node, to_node):
        self.from_node = from_node
        self.to_node = to_node

class Graph:
    def __init__(self):
        self.nodes = []
        self.edges = []

    def add_node(self, node):
        self.nodes.append({"id": node.id})

    def add_edge(self, edge):
        self.edges.append({"from": edge.from_node, "to": edge.to_node})

    def to_json(self):
        graph_repr = {
            "nodes": self.nodes,
            "edges": self.edges
        }
        return graph_repr

# Usage
if __name__ == "__main__":
    graph = Graph()

    node_a = Node("A")
    node_b = Node("B")
    node_c = Node("C")
    node_d = Node("D")

    graph.add_node(node_a)
    graph.add_node(node_b)
    graph.add_node(node_c)
    graph.add_node(node_d)

    edge_ab = Edge("A", "B")
    edge_bc = Edge("B", "C")
    edge_ca = Edge("C", "A")
    edge_db = Edge("D", "B")

    graph.add_edge(edge_ab)
    graph.add_edge(edge_bc)
    graph.add_edge(edge_ca)
    graph.add_edge(edge_db)

    import json
    print(json.dumps(graph.to_json(), indent=2))
```

## Extracting Surrounding Explanatory Text and Formulas
To accomplish the task of extracting surrounding explanatory text separately from formula text and returning formulas in LaTeX, we'll need to follow a step-by-step approach.

## Steps
1. **Input Preparation**: Preparing the input text that contains both explanatory text and formula text.
2. **Formula Identification**: Identifying the parts of the text that are formulas.
3. **LaTeX Conversion**: Converting the identified formula text into LaTeX format.
4. **Text Separation**: Separating the explanatory text from the formula text.

## Example Code
```python
import re

def extract_and_convert_latex(text):
    pattern = r'\(([^\)]+)\)'
    matches = re.findall(pattern, text)

    latex_formulas = [f"${match}$" for match in matches]

    text_without_formulas = re.sub(pattern, '', text)
    text_without_formulas = re.sub(r'\)', '', text_without_formulas)  
    text_without_formulas = re.sub(r'\(', '', text_without_formulas)  

    text_without_formulas = ' '.join(text_without_formulas.split())

    return text_without_formulas, latex_formulas

# Example usage
text = "The equation for the area of a circle is \(A = \pi r^2\), which is a fundamental concept in geometry."
explanatory_text, formulas = extract_and_convert_latex(text)

print("Explanatory Text:")
print(explanatory_text)
print("\nFormulas in LaTeX:")
for formula in formulas:
    print(formula)
```

## Measuring Iris Similarity

- Based on Hamming distance
- Define d(x,y) to be 
  - # of non-match bits / # of bits compared
- Example distances: 
  - d(0010,0101) = 3/4 
  - d(101111,101001) = 1/3
- Compute d(x,y) on 2048-bit iris code
- Perfect match is d(x,y) = 0
- For same iris, expected distance is 0.08
- At random, expect distance of 0.50
- Accept iris scan as match if distance < 0.32

## Iris Scan Error Rate

- distance
- distance
- Fraud rate
- == equal error rate

## Graph Representation in JSON

To provide a structured graph representation in JSON, including node labels, edge lists, and directionality, let's consider a simple example graph. We'll define a directed graph with 5 nodes and 6 edges.

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

| Key  | Value                                                                                           |
|------|-------------------------------------------------------------------------------------------------|
| nodes| [A, B, C, D, E]                                                                                 |
| edges| [\{from: A, to: B\}, {from: A, to: C}, {from: B, to: D}, {from: C, to: E}, {from: D, to: E}, {from: E, to: B}] |

However, a more compact and commonly used format for graph representation, especially in graph databases and algorithms, is the **GraphSON** format or simple adjacency list representations.

### Adjusted JSON Representation

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

### GEXF/GraphML Style JSON

```json
{
  "graph": {
    "nodes": [
      {"id": "A"},
      {"id": "B"},
      {"id": "C"},
      {"id": "D"},
      {"id": "E"}
    ],
    "edges": [
      {"id": "1", "source": "A", "target": "B", "type": "directed"},
      {"id": "2", "source": "A", "target": "C", "type": "directed"},
      {"id": "3", "source": "B", "target": "D", "type": "directed"},
      {"id": "4", "source": "C", "target": "E", "type": "directed"},
      {"id": "5", "source": "D", "target": "E", "type": "directed"},
      {"id": "6", "source": "E", "target": "B", "type": "directed"}
    ]
  }
}
```

### Adjacency List Representation

For directed graphs, an adjacency list is a compact way to represent the graph:

```json
{
  "A": ["B", "C"],
  "B": ["D"],
  "C": ["E"],
  "D": ["E"],
  "E": ["B"]
}
```

## Alternative Graph Representations

### Example Graph

Suppose we have a graph with the following properties:

- **Nodes (Vertices):** A, B, C, D
- **Edges:** 
  - A -> B (directed from A to B)
  - B -> C (directed from B to C)
  - C -> A (directed from C to A)
  - D -> B (directed from D to B)

### JSON Representation

A common JSON representation for a graph might involve specifying nodes and edges separately.

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

### Alternative Representations

Some graph libraries and databases use a different structure, focusing on the relationships and their directionality implicitly.

```json
{
  "nodes": [
    {"id": "A"},
    {"id": "B"},
    {"id": "C"},
    {"id": "D"}
  ],
  "links": [
    {"source": "A", "target": "B"},
    {"source": "B", "target": "C"},
    {"source": "C", "target": "A"},
    {"source": "D", "target": "B"}
  ]
}
```

## Code to Generate JSON

If you're working in Python, here's a simple way to create and manipulate such a graph structure:

```python
import json

class Graph:
    def __init__(self):
        self.nodes = []
        self.edges = []

    def add_node(self, id):
        self.nodes.append({"id": id})

    def add_edge(self, source, target):
        self.edges.append({"source": source, "target": target, "direction": "out"})

    def to_json(self):
        return json.dumps(self, default=lambda o: o.__dict__, indent=2)

# Usage
g = Graph()
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

## Attack on Iris Scan
- Good photo of eye can be scanned
- Attacker could use photo of eye
- Afghan woman was authenticated by iris scan of old photo
- Story can be found here
- To prevent attack, scanner could use light to be sure it is a “live” iris

## Equal Error Rate Comparison

- Equal error rate (EER): fraud == insult rate
- Fingerprint biometrics used in practice have EER ranging from about 10-3 to as high as 5%
- Hand geometry has EER of about 10-3
- In theory, iris scan has EER of about 10-6
- Enrollment phase may be critical to accuracy
- Most biometrics much worse than fingerprint!
- Biometrics useful for authentication…
- …but for identification, not so impressive today

## Biometrics: The Bottom Line
- Biometrics are hard to forge
- But attacker could
  - Steal Alice’s thumb
  - Photocopy Bob’s fingerprint, eye, etc.
  - Subvert software, database, “trusted path” …
- And how to revoke a “broken” biometric?
- Biometrics are not foolproof
- Biometric use is relatively limited today
- That should change in the (near?) future

I'm happy to help you reformat the text as clean Markdown. However, I don't see any text provided. Please paste the text extracted from the lecture slides, and I'll get started on reformatting it for you.


Once you provide the text, I'll:


1. Format the slide titles as ## headings
2. Format bullet points with -
3. Remove standalone page numbers
4. Remove navigation headers repeated across slides
5. Replace garbled or fragmented formula characters with [Formula: brief description]
6. Preserve tables as Markdown tables


Please go ahead and provide the text!
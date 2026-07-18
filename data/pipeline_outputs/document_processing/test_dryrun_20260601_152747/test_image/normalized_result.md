## Error Report

All providers failed: 
- Gemini (timed out)
- Azure
- Groq

The Groq error details are as follows:

### Groq Error Details

* Error code: 429
* Error message: 
  Rate limit reached for model `meta-llama/llama-4-scout-17b-16e-instruct` 
  in organization `org_01kkedd9pnejqr8cfvvrfp64h7` 
  service tier `on_demand` 
  on requests per minute (RPM): 
  * Limit: 30
  * Used: 30
  * Requested: 1
  
  Please try again in 2s. 
  Need more tokens? 
  Upgrade to Dev Tier today at https://console.groq.com/settings/billing

* Error type: requests
* Error code: rate_limit_exceeded
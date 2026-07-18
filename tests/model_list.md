# Available Bedrock Models (tested 2026-06-19)

Endpoint: `https://bedrock-mantle.us-east-1.api.aws/v1`  
Inference type: On-demand | Quota: 100M TPM, 100 RPM

## Test criteria
- **Text OK**: model responds without error
- **Chinese bias**: >20% CJK characters in reply → flagged as biased
- **Vision**: accepts `image_url` in message content

---

## Results

| Model ID | Text | Chinese bias | Vision | Notes |
|---|:---:|:---:|:---:|---|
| `moonshotai.kimi-k2.5` | OK | no | **OK** | Recommended — only model with vision support |
| `zai.glm-5` | OK | no | no | Clean English output |
| `zai.glm-4.7` | OK | no | no | Clean English output |
| `zai.glm-4.7-flash` | OK | no | no | Fastest in group |
| `minimax.minimax-m2.1` | OK | no | no | Responded clearly |
| `minimax.minimax-m2` | empty | no | no | Returned empty text — may need special format |
| `minimax.minimax-m2.5` | empty | no | no | Returned empty text — may need special format |
| `moonshotai.kimi-k2-thinking` | truncated | no | no | Thinking model, output cut short at max_tokens=80 |

---

## Recommendation

- **Default LLM (text tasks)**: `zai.glm-4.7-flash` — fast, reliable, no Chinese bias
- **Vision tasks**: `moonshotai.kimi-k2.5` — only model supporting image input on this account
- **Avoid for now**: `minimax.minimax-m2`, `minimax.minimax-m2.5` (empty responses), `moonshotai.kimi-k2-thinking` (needs higher max_tokens for thinking chain)

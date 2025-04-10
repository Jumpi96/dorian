# Dorian MVP Specification – Developer-Ready

## Overview
**Dorian** is a wardrobe assistant that helps users manage their clothing and get outfit or packing recommendations via a web app. It leverages a hosted LLM to generate structured outfit suggestions based on the user's wardrobe and prompt input. This MVP focuses on a lightweight, flexible experience with room to grow.

---

## Core Features (MVP)

### 1. **User Authentication**
- Sign-in via third-party providers (Google, Apple)
- Multi-user support from the start

### 2. **Wardrobe Management**
- Add clothing items via free-text input (e.g., "brown sweatshirt")
- View list of wardrobe items per user
- No tags, images, or categories in MVP, but structure for future expansion

### 3. **Recommendation Modes (Tabs)**
- **Wear** – Suggest an outfit for an occasion or day
- **Pack** – Suggest a packing list for a trip
- **Buy** – Suggest one item to buy next based on the user’s wardrobe

### 4. **LLM-Powered Recommendations**
- Accepts free-text prompt input with UI hints
- Parses prompt + wardrobe to create structured LLM request
- Returns structured response (e.g., outfit with top, bottom, shoes, etc.)
- Context-aware in pack mode (remembers packed items)

### 5. **Feedback System**
- Users can give ⬆️/⬇️ feedback per recommendation
- Feedback is stored and will influence future recommendations in future versions

### 6. **History View**
- Simple list of past outfit suggestions
- Includes item breakdown and timestamp

### 7. **Soft Rate Limit**
- Maximum of 10 LLM-backed requests per user per day

### 8. **Fallback Handling**
- If wardrobe is too small, display: “Add a few more items to get better recommendations.”

---

## System Architecture

### Web App
- **Frontend**: React + TailwindCSS (hosted on Vercel or Cloudflare Pages)
- **Backend**: AWS Lambda + API Gateway
- **Database**: DynamoDB (fully serverless)
- **LLM API**: Hosted provider (e.g., OpenAI GPT-4 via API)
- **Auth**: AWS Cognito (or Auth0/Clerk.dev if preferred)

---

## DynamoDB Schema

### `users`
```json
{
  "userId": "abc123",
  "email": "user@email.com",
  "createdAt": "2025-04-08"
}
```

### `wardrobeItems`
```json
{
  "userId": "abc123",
  "itemId": "item001",
  "description": "brown sweatshirt"
}
```

### `interactions`
```json
{
  "userId": "abc123",
  "interactionId": "int001",
  "mode": "wear",
  "prompt": "What should I wear tomorrow?",
  "response": {
    "top": "black t-shirt",
    "bottom": "olive chinos",
    "shoes": "white sneakers"
  },
  "timestamp": "2025-04-08T14:00:00Z",
  "feedback": "thumbsUp"
}
```

### `rateLimits`
```json
{
  "userId": "abc123",
  "date": "2025-04-08",
  "requestCount": 7
}
```

---

## API Endpoints

### Auth
- `POST /auth/login` – Sign in via OAuth provider

### Wardrobe
- `POST /wardrobe/add` – Add item
- `GET /wardrobe` – List wardrobe items

### Recommendations
- `POST /recommend/wear`
- `POST /recommend/pack`
- `POST /recommend/buy`

### Feedback
- `POST /feedback` – Submit thumbs up/down

### History
- `GET /history` – List past structured outfits

---

## LLM Prompt Handling
- User input is natural language
- Backend enriches it using UI hints (occasion, weather, etc.)
- Formats structured prompt (e.g., LMQL or JSON outline)
- Response parsed and rendered as structured outfit

### Output Format (Outfit)
```json
{
  "top": "black t-shirt",
  "bottom": "olive chinos",
  "shoes": "white sneakers",
  "outerwear": "grey hoodie",
  "accessories": "black cap"
}
```

---

## Error Handling Strategy
- Validate user input server-side
- Catch LLM API failures gracefully:
  - Show generic error message: “Couldn’t fetch a recommendation. Try again later.”
- Wardrobe checks before recommendations
- Fallback message for too-few items
- Track request errors in logs (CloudWatch)

---

## Testing Plan

### Unit Tests
- Prompt formatter
- API handlers (add item, recommend, rate limit)
- DynamoDB access logic

### Integration Tests
- Full wardrobe → outfit flow
- Rate-limited user path
- Feedback submission and logging

### Manual QA
- Add, view, and remove wardrobe items
- Send all 3 types of prompts
- Test with empty wardrobe
- Login/logout across multiple browsers

---

## Future Enhancements
- Autocomplete on add-item input
- Add photos, tags, and links to wardrobe items
- Smart wardrobe insights ("you don’t have anything for rain")
- Learning from feedback to tailor style
- Re-try recommendations with feedback loops
- Monetization via clothing suggestions and affiliate links

---

## Domain
- App hosted on: `https://dorian.app`

---

## Final Notes
- Start lean, focus on core loop (add item → get outfit)
- Keep structured I/O from day one for future AI improvements
- All LLM-related data is stored for fine-tuning and analytics down the line

Ready to build 🚀


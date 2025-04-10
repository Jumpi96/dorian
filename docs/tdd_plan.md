Below is a comprehensive **blueprint** for building the Dorian MVP step-by-step, then breaking those steps down into **iterative chunks**, then further into **right-sized tasks**. Finally, you’ll find a **series of prompts** that can be used with a code-generation LLM to implement each piece in a **test-driven** manner. Each prompt picks up where the previous one left off, so no code is left orphaned. 

---

# 1. **High-Level Blueprint**

1. **Set Up Project Foundations**
   - Establish repo structure
   - Configure CI/CD (GitHub Actions or similar)
   - Prepare environment for local development

2. **Implement Authentication**
   - Choose OAuth provider (e.g., Google)
   - Integrate sign-in flow
   - Store user records in DynamoDB

3. **Wardrobe Management**
   - Create DynamoDB table for wardrobe items
   - Implement add-item endpoint
   - Implement fetch-items endpoint

4. **LLM Integration**
   - Set up basic API call to a hosted LLM (e.g., GPT-4)
   - Design prompt schema (input + output format)
   - Test the integration with sample requests

5. **Recommendation Endpoints**
   - `/recommend/wear`, `/recommend/pack`, `/recommend/buy`
   - Rate limiting logic (10 requests/day)
   - Fallback for insufficient wardrobe

6. **Feedback System**
   - Store feedback in interactions table
   - Simple thumbs-up/down endpoint

7. **History View**
   - Interactions table queries
   - Display list of past recommendations

8. **Frontend UI**
   - React app with routing for:
     - Authentication
     - Wardrobe (list/add)
     - Recommendation interface
     - History
   - Integrate TailwindCSS

9. **Deployment**
   - Infrastructure as code (e.g., AWS SAM or Serverless Framework)
   - Configure environment variables (LLM API key, etc.)
   - Deploy to AWS Lambda + DynamoDB + S3 (for static hosting) or Vercel

10. **Testing & QA**
    - Write unit tests for backend logic
    - Integration tests for full flow (add wardrobe item → get recommendation)
    - Manual QA for UI

---

# 2. **Break Down into Iterative Chunks**

We’ll group tasks into phases, each with small, testable deliverables that build on each other.

### **Phase 1: Project Setup & Basic Skeleton**

1. **Initialize Repo & CI/CD**
   - Create project structure (frontend + backend folders)
   - Configure GitHub Actions (or similar) to run tests on push

2. **DynamoDB Table Definitions**
   - Create a local or test environment with DynamoDB
   - Write code to provision or connect to `users`, `wardrobeItems`, `interactions`, `rateLimits`

3. **Auth Skeleton**
   - Set up basic OAuth flow (stub code for now)
   - Validate user flow in local dev environment

4. **React App Initialization**
   - Create minimal React app using Create React App (or Vite)
   - Set up basic Tailwind

### **Phase 2: Backend APIs (Wardrobe & Auth)**

1. **User Registration & Login**
   - Implement real OAuth integration
   - Store user in `users` table on first sign-in

2. **Wardrobe Management Endpoints**
   - `POST /wardrobe/add`
   - `GET /wardrobe`

3. **Frontend Wardrobe Integration**
   - Connect React UI to new endpoints
   - Add item form + display items list

### **Phase 3: LLM Integration & Recommendation**

1. **LLM API Setup**
   - Introduce environment variable for LLM API key
   - Create a simple service to call GPT-4 (or similar)

2. **Rate Limiting**
   - Build logic for `rateLimits` table
   - Prevent more than 10 requests per user per day

3. **Recommend Endpoints**
   - `POST /recommend/wear`
   - `POST /recommend/pack`
   - `POST /recommend/buy`
   - Validate that user has enough items, else fallback

4. **Frontend Recommendation UI**
   - Add tabs for wear/pack/buy
   - Add input prompt field + results display

### **Phase 4: Feedback & History**

1. **Feedback Submission**
   - `POST /feedback`
   - Store thumbs-up/down in `interactions` with reference to the recommendation

2. **History Endpoint**
   - `GET /history`
   - Return past interactions (recommendations + feedback)

3. **Frontend Integration for Feedback & History**
   - Display thumbs-up/down on results
   - Show a history page or component listing past interactions

### **Phase 5: Final Integration & Testing**

1. **End-to-End Manual QA**
   - Run through all flows (auth, add items, recommend, feedback, view history)
2. **Automated Tests**
   - Write integration tests for main flows
   - Confirm no major regressions
3. **Deploy**
   - Finalize deployment scripts (AWS or Vercel)
   - Launch MVP

---

# 3. **Further Breakdown of Each Phase into Smaller Steps**

We’ll zoom in again to ensure each step is right-sized for incremental, testable progress.

### **Phase 1: Project Setup & Basic Skeleton**

1. **Initialize Project Structure**
   - `mkdir dorian-mvp` → create `backend/` and `frontend/`
   - Initialize `package.json` or multiple repos as needed
   - Confirm standard Node version is used

2. **Configure CI/CD**
   - Create `.github/workflows/ci.yml`
   - On push/pull_request, run `npm install && npm test`
   - (Stubs for now; we don’t have tests yet)

3. **Set Up DynamoDB Tables** (Local + Scripts)
   - Write a small script (e.g., using AWS SDK) to create tables:
     - `users`
     - `wardrobeItems`
     - `interactions`
     - `rateLimits`
   - Test locally that the tables exist

4. **Auth Skeleton**
   - Create minimal endpoints: `/auth/login`, `/auth/callback`
   - Return a fake user object for now
   - Confirm we can “login” and store a user ID in memory

5. **React + Tailwind Setup**
   - Use `create-react-app` (or Vite)
   - Install and configure Tailwind
   - Test minimal “Hello World” page

### **Phase 2: Backend APIs (Wardrobe & Auth)**

1. **Implement Real OAuth**
   - Use Google or Apple with an OAuth library
   - On success, store user in `users` table with `userId` = sub from OAuth
   - Return JWT or session to client

2. **Add Wardrobe Endpoints**
   - `POST /wardrobe/add` – parse item description, insert into `wardrobeItems`
   - `GET /wardrobe` – fetch user’s items from `wardrobeItems`

3. **Wardrobe UI**
   - React form to add new item
   - Display items in a list
   - Confirm data flows: UI → API → DynamoDB → UI

### **Phase 3: LLM Integration & Recommendation**

1. **LLM API Setup**
   - Create a small function `callLLM(prompt)` that returns structured JSON
   - Use environment variable `LLM_API_KEY`
   - Basic error handling + logging

2. **Rate Limiting Mechanism**
   - Query `rateLimits` table for the user + current date
   - If >= 10, reject request
   - Else increment and proceed

3. **Recommend Endpoints**
   - `POST /recommend/wear`
     - Check rate limit
     - Query wardrobe items
     - Format prompt
     - Call LLM
     - Parse structured response
     - Save to `interactions`
   - Same pattern for `pack` and `buy`, with slight differences in prompt formatting

4. **Recommendation UI**
   - Create 3 tabs (wear/pack/buy)
   - Each tab has a text input + submit button
   - Display the recommended outfit or items

### **Phase 4: Feedback & History**

1. **Feedback API**
   - `POST /feedback`
     - Body: `interactionId`, `feedback` (thumbsUp or thumbsDown)
     - Update relevant `interactions` record

2. **History Endpoint**
   - `GET /history`
     - Return all `interactions` for user, sorted descending by timestamp

3. **UI for Feedback & History**
   - For each recommendation result, show thumbs-up/down
   - Provide a “History” link or tab to see past outfits

### **Phase 5: Final Integration & Testing**

1. **Integration Tests**
   - Ensure we can sign up, add items, get an outfit, rate it, and see it in history
2. **Clean Up & Deploy**
   - Prepare production environment
   - Deploy, test, fix any final issues

---

# 4. **Prompts for Code Generation (TDD Focus)**

Below is a series of prompts that you can feed into a code-generation LLM (e.g., GPT-4) to implement each piece step by step. Each prompt ends with instructions to **write tests** and **integrate** with the existing code to ensure no orphan code remains. 

Note: The exact text in these prompts can be tweaked to align with your code-generation environment. **Each prompt** is wrapped in ```text code blocks so you can copy-paste it cleanly.

---

## **Prompt 1: Project Initialization & CI/CD**

```text
You are an AI pair-programmer. We are building a new project called “Dorian MVP.” 

**Goal**: 
1. Create a minimal monorepo structure with a `backend` folder and a `frontend` folder.
2. Initialize each folder with a Node.js project setup.
3. Create a GitHub Actions workflow that runs tests (which we will create soon) on push/pull requests.
4. Ensure we can install dependencies in each subfolder and run lint/test steps.

**Steps**:
- Create `backend/package.json` and `frontend/package.json` with placeholders.
- Create a root `.github/workflows/ci.yml` GitHub Actions file that runs Node tests in both subfolders.
- Make sure to include a script in each package.json that runs `npm test` (though the test script can be a placeholder for now).
- After implementing, show the new file structure. 
- Provide example usage of `npm install` and `npm test` in both folders.

**Constraints**:
- Use best practices for Node project initialization.
- We’ll integrate real code/tests in subsequent prompts.

Now, please generate the code for this setup, including the CI workflow file, and walk through how to run it locally.
```

---

## **Prompt 2: DynamoDB Table Setup Scripts**

```text
We have a monorepo with `backend/` and `frontend/`. Focus on the backend now.

**Goal**:
1. Create scripts in the `backend` folder to define and create four DynamoDB tables: `users`, `wardrobeItems`, `interactions`, and `rateLimits`.
2. We’ll assume AWS credentials are configured in the environment for local or test usage.
3. Show how to create these tables using the AWS SDK for JavaScript (v3).
4. Include a script `createTables.js` that, when run, creates or updates the tables.
5. Write a couple of simple unit tests (using Jest or Mocha) to confirm the table creation logic can be called without error.

**Details**:
- `users` table has primary key: `userId` (string).
- `wardrobeItems` table has composite key: `userId` (partition), `itemId` (sort).
- `interactions` table has composite key: `userId` (partition), `interactionId` (sort).
- `rateLimits` table has composite key: `userId` (partition), `date` (sort).

**Constraints**:
- Code must be placed in `backend/` with relevant imports.
- Provide test instructions and sample usage.

Now generate the code for this step, ensuring to integrate with the existing `backend/package.json` for tests.
```

---

## **Prompt 3: Auth Skeleton (Stubbed) & Basic Server Setup**

```text
Continuing in the `backend/` folder. We will create a minimal Node/Express (or similar) server with stubbed authentication endpoints.

**Goal**:
1. Implement a small server (`app.js`) with Express that listens on a port (e.g., 3001).
2. Create two endpoints: `/auth/login` and `/auth/callback`.
   - For now, just return a static JSON response: `{ "user": "fakeUserId" }`.
3. Write a test (`auth.test.js`) verifying that hitting these endpoints returns the expected stubbed user.
4. Update `package.json` test script if needed to run these new tests.

**Constraints**:
- Keep it minimal, since real OAuth logic comes in a later step.
- The test should spin up the server in-memory (Supertest or similar) and check the response.

Now produce the code for:
- `app.js`
- `auth.test.js`
- Any changes to `package.json` needed
- Explanation of how to run and test the server.
```

---

## **Prompt 4: Frontend Initialization with React & Tailwind**

```text
Switching focus to `frontend/`. We will create a React app with Tailwind for styling.

**Goal**:
1. Use Create React App (or Vite) to initialize the React app in the `frontend/` folder.
2. Configure TailwindCSS:
   - Install tailwind and set up `tailwind.config.js`.
   - Ensure the default Tailwind directives are in `index.css` (or equivalent).
3. Include a simple home page with “Hello Dorian” text.
4. Provide a single test (e.g., using React Testing Library) that checks that the text “Hello Dorian” renders.

**Constraints**:
- Show `package.json` for the frontend and how to run the dev server (`npm start`) and tests (`npm test`).
- Use a minimal approach for now.

Now produce the code for the frontend’s initial setup, including the Tailwind configuration and a sample test.
```

---

## **Prompt 5: Implement Real OAuth in the Backend**

```text
Returning to `backend/`, we will replace our stubbed auth with real OAuth (e.g., Google).

**Goal**:
1. Use `passport` or a similar OAuth library to authenticate with Google.
2. On success, extract the user’s Google `sub` and store that in DynamoDB’s `users` table if it doesn’t exist.
3. Return a JWT or session-based cookie to the client (your choice, but show how).
4. Update tests: 
   - We can mock Google OAuth flow, or integrate a testing method. 
   - Ensure `users` table is updated with the new user.

**Constraints**:
- Must handle the callback route, extracting user info from Google.
- Minimal UI in frontend is acceptable for now; we only need the backend portion tested.

Now produce the code that integrates real OAuth with the existing `app.js`, modifies the `auth.test.js` to test the new flow, and ensures we create a user record if not existing. Provide instructions for local dev secrets (e.g., .env).
```

---

## **Prompt 6: Wardrobe Management Endpoints**

```text
Still in `backend/`. We’ll implement endpoints for adding and listing wardrobe items.

**Goal**:
1. `POST /wardrobe/add` 
   - Requires authenticated user (use the user ID from session/JWT).
   - Accept a JSON body with `description`.
   - Insert a new record into `wardrobeItems` with a generated `itemId`.
2. `GET /wardrobe`
   - Returns all wardrobe items for the authenticated user.
3. Tests:
   - Confirm that adding an item creates a record in the table.
   - Confirm that listing returns the items for that user.
   - Confirm items from one user do not show up for another user (test multi-user scenario).

Now produce the code, integrating with existing server structure (`app.js`). Provide updated test files (e.g., `wardrobe.test.js`). 
```

---

## **Prompt 7: Integrate Wardrobe UI (React)**

```text
Now we connect the `frontend/` to these new wardrobe endpoints.

**Goal**:
1. Add a simple page “Wardrobe” in React that:
   - Has a text input to add a new item.
   - Shows the list of existing items.
2. On load, call `GET /wardrobe` to display items.
3. On submit of the input, call `POST /wardrobe/add`, then refresh the list.
4. Write a test (using React Testing Library) that mocks the backend calls and verifies the flow.

**Constraints**:
- We can assume the user is already authenticated for now. 
- Must show how to configure the client to talk to `localhost:3001` or whichever port the backend is on.

Now produce the React code (new components/pages) and the test code. Show how to run the frontend dev server, and confirm the wardrobe flow is functional.
```

---

## **Prompt 8: LLM Integration & Rate Limiting**

```text
Back to the backend for the recommendation logic.

**Goal**:
1. Add environment variable `LLM_API_KEY`.
2. Create a new module `llmService.js` with a function `callLLM(prompt)` that calls GPT-4 (or any hosted LLM) and returns JSON.
3. Implement a rate-limiting middleware/function that checks `rateLimits` table:
   - If the user already made 10 requests today, return 429 or a custom error.
   - Otherwise increment the count.
4. Write tests (unit + integration) verifying the rate limit logic. 
5. Add a mock test for `callLLM` so we don’t call the real API in test.

Now provide the updated code for `llmService.js`, the rate-limiting logic, environment variable usage, and related tests.
```

---

## **Prompt 9: Recommendation Endpoints**

```text
We will create three endpoints: `/recommend/wear`, `/recommend/pack`, and `/recommend/buy`.

**Goal**:
1. Each endpoint:
   - Checks rate limit.
   - Loads the user’s wardrobe from DynamoDB.
   - Constructs a prompt for the LLM (slightly different for each mode).
   - Calls `callLLM`.
   - Parses the response, saves an interaction record in `interactions`.
   - Returns the recommended outfit/items to the client.
2. If the user has fewer than 3 items (arbitrary choice) in the wardrobe, return a fallback message instead.
3. Tests:
   - Mock LLM calls and check that each endpoint saves an interaction in `interactions`.
   - Confirm the fallback for too few items is returned.

Now produce the code in `recommendRoutes.js` (or integrated in `app.js`), plus tests (e.g., `recommend.test.js`).
```

---

## **Prompt 10: Frontend - Wear/Pack/Buy Tabs & Recommendation UI**

```text
In the `frontend/`, we will build the Recommendation interface.

**Goal**:
1. Create a new page with three tabs (Wear, Pack, Buy).
2. Each tab has:
   - A text input for user’s prompt (like “Weather is cold tomorrow” or “Weekend trip”).
   - A button to call the relevant endpoint (`/recommend/wear`, `/recommend/pack`, `/recommend/buy`).
3. Display the LLM’s structured result (e.g., top, bottom, shoes).
4. Basic error handling (show an alert if we get an error or fallback message).

**Constraints**:
- Reuse existing auth logic from the frontend.
- Write a test that mocks the recommendation calls and checks each tab’s UI.

Now produce the React code for this new page/component, the tab navigation, and the test code verifying it works. Provide instructions for accessing it from the main app.
```

---

## **Prompt 11: Feedback & History**

```text
We will add feedback submission and a history view.

**Goal**:
1. Feedback:
   - `POST /feedback` with `interactionId` and `feedback` (thumbsUp or thumbsDown).
   - Updates the record in `interactions`.
2. History:
   - `GET /history` to list a user’s interactions with the outfit response and feedback.
3. Frontend:
   - Display thumbs-up/down next to each recommendation result in the UI. On click, call `/feedback`.
   - Add a new “History” view that fetches `/history` and displays entries.
4. Tests:
   - Check that feedback is recorded in the backend.
   - Check that history displays the past outfits.

Now provide the code for the backend (`feedbackRoutes.js`, or integrated in `app.js`) and the frontend (components for feedback & history), plus the tests.
```

---

## **Prompt 12: Final Integration & Testing**

```text
We have all main features. Now we do a final pass to ensure everything is wired together and well-tested.

**Goal**:
1. Create an integration test (either in the backend or a separate test suite) that:
   - Logs in a test user (mocks OAuth).
   - Adds a wardrobe item.
   - Requests a “wear” recommendation.
   - Submits feedback.
   - Fetches history to confirm the interaction is recorded.
2. Review the code for any missing pieces or orphaned code.
3. Provide final deployment steps (how to deploy to AWS or Vercel).
4. Confirm all tests pass in GitHub Actions.

Now produce any final code updates needed, including an end-to-end integration test file, documentation updates, and instructions for deployment. 
```

---

# **Conclusion**

These prompts represent an incremental, test-driven journey from an empty monorepo to a fully functioning MVP of **Dorian**, the wardrobe assistant. Each step builds upon the last, ensuring that no code is left disconnected, and that testing is an integral part of the development process. 

Good luck, and happy coding!
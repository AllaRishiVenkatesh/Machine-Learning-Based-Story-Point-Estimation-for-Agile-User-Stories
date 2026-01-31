# SprintIQ: Machine Learning Based Agile Estimation
## Complete Project Documentation for Interviews

---

### 1. Problem Statement
**The Core Issue:** In Agile software development, "Sprint Planning" is critical but often flawed. Teams spend hours playing "Planning Poker," debating the complexity of user stories.
- **Subjectivity**: One developer says a task is a "3", another says "8".
- **Bias**: Senior developers might underestimate tasks, while juniors might overestimate.
- **Fatigue**: Long estimation meetings drain energy that could be used for coding.
- **Inconsistency**: Estimates vary wildly from sprint to sprint, making project velocity unpredictable.

### 2. The Solution: SprintIQ
**What it is:** An AI-powered decision support tool that analyzes the *text* of a user story and predicts its complexity (Story Points).
**How it helps:**
- **Objective Baseline**: Provides a data-driven "second opinion" to anchor discussions.
- **Speed**: Instantly estimates tasks, saving hours of meeting time.
- **Standardization**: Ensures consistent estimation criteria across the entire project lifespan.
- **Feedback Loop**: Learn from corrections to improve over time.

---

### 3. Technical Architecture & Tech Stack

#### **A. Backend (The Brain)**
*   **Python**: The core programming language chosen for its dominant ecosystem in AI/ML.
*   **FastAPI**: Used to build the high-performance REST API.
    *   *Why?* It is faster than Flask/Django for APIs, supports asynchronous processing (async/await), and auto-generates documentation (Swagger UI).
*   **Scikit-Learn**: The Machine Learning library used for the prediction model.
    *   *Algorithm*: **Random Forest Regressor**. We treat estimation as a regression problem (predicting a continuous value) which is then mapped to the nearest Fibonacci class.
    *   *Why Random Forest?* It handles non-linear relationships well, is robust against overfitting, and works great with tabular/text-derived features.
*   **Pandas & NumPy**: Used for data manipulation and numerical operations during preprocessing.

#### **B. Data Processing (The Logic)**
*   **Natural Language Processing (NLP)**:
    *   **TF-IDF Vectorization** (Term Frequency-Inverse Document Frequency): Converts raw text (the user story string) into numerical vectors that the model can understand. It highlights "important" words (like *database*, *API*, *encryption*) while ignoring common words (like *the*, *is*, *and*).
*   **Pipeline**: We built a `scikit-learn` Pipeline that chains the `TfidfVectorizer` and `RandomForestRegressor`. This ensures that any new text input goes through the exact same transformation steps as the training data.

#### **C. Frontend (The Face)**
*   **HTML5 & JavaScript**: Standard web technologies for structure and interactivity.
*   **Tailwind CSS**: A utility-first CSS framework.
    *   *Why?* Allows for rapid UI development, responsive design, and easy implementation of the modern "Dark Mode" aesthetic without writing thousands of lines of custom CSS.

#### **D. Data Storage**
*   **CSV / File-Based Store**:
    *   *Why?* For a student/demo project, a lightweight file store (CSV) is sufficient and avoids the complexity of setting up a full database server (PostgreSQL/MongoDB). It stores prediction history and feedback logs.

---

### 4. Key Interview Questions & Answers

**Q: How does the model actually "read" text?**
**A:** "I use TF-IDF vectorization. It counts how often words appear in a story but penalizes words that appear everywhere. This helps the model focus on technical keywords like 'authenticate' or 'migrate' which strongly correlate with complexity."

**Q: Why didn't you use a Deep Learning model like LSTM or BERT?**
**A:** "For this specific dataset size, Random Forest offers the best balance of performance and efficiency. Deep Learning models like BERT are resource-heavy and slow for real-time inference on a standard machine. Random Forest is fast, interpretable, and accurate enough for this use case."

**Q: How do you handle the Fibonacci scale (1, 2, 3, 5...)?**
**A:** "The model predicts a raw continuous number (e.g., 4.2). My post-processing logic acts as a 'classifier' that maps this raw number to the nearest valid Fibonacci point (in this case, 5). This ensures the output is always a valid Agile story point."

**Q: What happens if the model is wrong?**
**A:** "I implemented a Feedback Loop. The UI allows users to correct the estimate. This data is logged and can be used to re-train the model, allowing SprintIQ to get smarter and adapt to the specific team's estimation style over time."

**Q: How did you ensure the system is scalable?**
**A:** "The backend is stateless and container-ready. We use FastAPI which is built on Starlette and Uvicorn, capable of handling thousands of requests per second asynchronously. The frontend is decoupled, meaning the backend API can serve multiple clients (web, mobile, or CLI) simultaneously."

---

### 5. Project Flow (Step-by-Step)
1.  **Input**: User types: *"As an admin, I want to export monthly reports to PDF..."*
2.  **API Call**: Frontend sends this string to the `/predict` endpoint.
3.  **Preprocessing**: Backend cleans text (removes punctuation, lowercases) and Vectorizes it.
4.  **Inference**: The saved Model artifact (`model.joblib`) predicts a complexity score.
5.  **Mapping**: The score is snapped to the nearest Fibonacci number.
6.  **Response**: API returns `{ "points": 5, "confidence": "High" }`.
7.  **Display**: Frontend shows the result instantly.

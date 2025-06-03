## Part 1 of the project HOLBERTONSCHOOL - HBNB






















# 🏠 AirBnB Clone - Architecture Overview

This project is a simplified clone of the AirBnB platform, demonstrating a structured and layered architecture using object-oriented design principles and storage abstraction.

## 🔧 Technologies Used

- Language: **Python**
- Storage: **JSON File** or **MySQL Database**
- Architecture: **3-Layered Architecture**
- Version Control: **Git**

---

## 📐 System Architecture

The system is organized into **three main layers**:

1. **Presentation Layer**
2. **Business Logic Layer**
3. **Persistence Layer**


## 📦 Package Diagram - Software Architecture

![Package Diagram](./Package%20Diagram.png)




---

## 🏗️ Business Logic Layer - Class Diagram

![Class Diagram](./Class%20Diagram.png)


---

## 📒 Entity Descriptions

- **User**: Represents a user of the platform. Can be a regular user or an administrator. Users can register, update their profile, and be deleted. Each user can own multiple places and write multiple reviews.
- **Place**: Represents a property listed by a user. Contains details such as title, description, price, and location. Each place is owned by a user, can have multiple amenities, and can receive multiple reviews.
- **Review**: Represents a review left by a user for a place. Contains a rating and a comment. Each review is associated with one user and one place.
- **Amenity**: Represents an amenity that can be associated with places (e.g., Wi-Fi, Pool). Each amenity can be linked to multiple places.

### Relationships

- **User–Place**: A user can own multiple places.
- **Place–Review**: A place can have multiple reviews.
- **User–Review**: A user can write multiple reviews.
- **Place–Amenity**: A place can have multiple amenities.

---



---

## 📊 Sequence Diagrams for API Calls

This section illustrates the interaction flow between system layers (Presentation, Business Logic, Persistence) through four core API calls using sequence diagrams.

### 1️⃣ User Registration

**Description**:  
A user submits a registration form to create a new account. The request flows from the API layer to the business logic to validate and create the user, then stores it in the database.

**Sequence Flow**:
1. API receives sign-up request.
2. Validates and parses the input.
3. Business Logic creates a new `User` instance.
4. Persistence layer saves it to storage (DB or JSON).
5. Returns success or error response.

![User Registration Sequence](./Sequence%20Diagram/sign%20up.png)

---

### 2️⃣ Place Creation

**Description**:  
A registered user adds a new place listing to the system. This involves sending place details from the client through the API to the business logic, which validates and saves it via the storage engine.

**Sequence Flow**:
1. User sends POST request to create a place.
2. API validates the input.
3. Business Logic constructs a `Place` object.
4. Data saved via Persistence Layer.
5. Confirmation is sent back to the client.

![Place Creation Sequence](./Sequence%20Diagram/create%20place.png)

---

### 3️⃣ Review Submission

**Description**:  
A user submits a review for a listed place. The request passes through the API, triggers validation, creates a new `Review` object, and stores it in the database.

**Sequence Flow**:
1. API receives review data.
2. Checks that place and user exist.
3. Constructs a `Review` object in Business Logic.
4. Saves to database (Persistence Layer).
5. Returns result to user.

![Review Submission Sequence](./Sequence%20Diagram/submit%20review.png)

---

### 4️⃣ Fetching List of Places

**Description**:  
A user requests a filtered list of available places (e.g., by city, price, or amenities). The system queries the database and returns the matching results.

**Sequence Flow**:
1. API receives GET request with filters.
2. Business Logic processes filters.
3. Queries the Persistence Layer.
4. Retrieves and formats list of `Place` objects.
5. Sends response to user.

![List of Places Sequence](./Sequence%20Diagram/List%20of%20place.png)

---

## 📝 Notes

- Each diagram represents a **real-world flow** for a specific API call.
- The diagrams help clarify how the layers cooperate to fulfill requests.
- The interaction starts from the Presentation Layer, then to Business Logic, and ends in the Persistence Layer (with data storage/retrieval).

> 💡 These diagrams provide a clear understanding of how each API endpoint works under the hood, aiding debugging, onboarding, and documentation efforts.

---



## 👨‍💻 Authors

This project was created by:

- **Bader Alamri**  
- **Riyadh Alhamad**  
- **Mohammed Alqabas**

We collaborated on the design, implementation, and documentation of the HBNB application as part of the Holberton School curriculum. Each team member contributed to key system components, diagrams, and architectural decisions.

# CreditsDashboard

## Project Setup and Running Instructions

### Backend (API)

The backend is located in the `/api` directory.

#### Requirements
- Python 3.9 installed (if you see any issues with dependenies, it could be due to older version of Python)

#### Setup and Run

1. Navigate to the API directory:

   ```bash
   cd api

2. Run the Backend using the provided script

   ```bash
   ./run.sh

The script should activate a virtual environment + install the required dependencies.
You might need to run _chmod +x run.sh_ to ensure it is runnable.


### Frontend

The frontend is located in the `/frontend` directory.

#### Requirements
- Node.js (latest version 23 recommended)
- npm or yarn

#### Setup and Run

1. Navigate to the frontend directory:

   ```bash
   cd frontend

2. Install dependencies:

   ```bash
   yarn install

3. Start the app:

   ```bash
   yarn dev

## Decisions, Limitations and More

### Backend (API)

I don't tend to leave many comments in-code unless there is a need to explain something. When things are simple, I'd rather that code is self-explanatory, e.g. by breaking things into smaller functions and naming the function accordingly. That being said, please find here some insight on what code is where, which should help you review.

I decided to use Flask as it is the simplest Python server technology I am familiar with. The main file for our app is app.py which runs the server and provides the single endpoint. It also handles CORS. In the future, we can provide apispec with our project.
The code should have been in a /src parent directory, but forgot to add one and no point to refactor at this point, so please check following directories:
 - /models is where the models live, in our case Message and CreditCalculationResult, we can reuse these across the app as needed. 
 - /credits is where the implementation of this feature lives (CreditService does the main job and it uses the Calculator classes to count credits; I decided to introduce an abstract parent Calculator which can have different implementations, currently PromptCalculator and ReportCalculator; I thought this would make our code extendable for the future, plus it makes the abstraction clear and easy to understand. CreditCalculationResult model was needed so we can easily return both the credits used and the report name)
 - /tests is where unit tests would live, currently I have only tested the PromptCalculator in the interest of time (as this is the most critical component where errors could occur)

### Frontend (API)

I setup a simple React app via Vite. It serves a single component on the main page - CreditsDashboard. It is reponsible for fetching the data from the BE and passing it onto child components. They are rendered in a flexbox on the page:
- CreditsBarChart implements the chart. The simplest framework for that here was Recharts, so I just went with it. It worked pretty much off-the-shelf once the data was aggreagated. Only had to fix things like formatting.
- DashboardTable implements the table. I was considering what framework to use here as I don't like writing verbose HTML tables, it's not easy to follow at all. Plus, they don't have sorting etc included. Initially I went with Material UI's table as thought this was the simplest, but then realized only the paid version supports sorting of multiple columns at the same time. This was a mistake, and I should have researched it better. Ultimately, I switched to AGGrid which provides this functionality. It is currently configured to be able to sort the second column if you hold Ctrl. Another difficulty here was recent updates to the AGGrid APIs, which made me struggle initially with retrieving the sort state in order to implement the URL requirement. Finally, I think it all works :)

Obviously there is a lot we can add here, but we are limited by time:
- updates to the styles if we want to make the page feel our own, e.g. fit for Orbital's website
- I haven't added any tests here yet
- I like to have separation of concerns, ideally I would have components be presentational, and let logic be in hooks; for simplicity, I just implemented everything in one place here
- we can use React Query for working with the REST API
- we could add a spinner to indicate the data is loading as currently is't not a great user experience



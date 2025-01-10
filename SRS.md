# **PLACEHOLDER**
# System Requirement Specification (SRS)

## Introduction
### Purpose      
This document presents a detailed description of the **Acropora** financial planner web application. It explains the purpose of the software, features and functionalities, user interfaces, hardware constraints. This document is intended to be the reference for expectations for both the stakeholders and the developers of the system.

### Background
Young professionals have a hard time navigating personal finances due to the lack of knowledge and structure. While actively learning more about managing financial health and wealth-growing instruments, there is a lack of tools that put structure into their wealth. Professional financial planner often cost too much money compared to the amount of assets young professionals need to manage, and tools like Mint and CreditKarma apps are generally too commercialized leaving with abundance of distracting ads and credit card lures. 

Financially-concious professionals often rely on self-made Excel spreadsheets to track and plan their expenses, however that takes time and knowledge to develop and often result in similar spreadsheets. While spreadsheets are highly customizable, it lacks the ability to cross-analyze financial data. Even if the spreadsheets are adequately complex, they suffer slow responses and messy. Therefore, there is a need for a straight-forward wealth management tool, that is able to cross analyze the personal finance data. 

_Note_: **Acropora** is named after a genus of a fast-growing, stony branch corals exists in Indo-china Ocean.   

### Project Scope
This software will serve as a comprehensive personal financial planner for young professionals with simple wealth structure comprising of a few cashflow sources (W2, RSU, 1099, rentals, and investment income), basic investment strategies (equity markets, ETFs, mutual funds, ESPP), basic retirement strategies (401K, Traditional IRA, Roth IRA, automated savings, CDs), and common valuable properties (car, home, personal items). The planner's goal is to provide a structure to user's financial information that will facilitate understanding, analysis, and decision making.

We believe that making financial decision involve a mindset change. Daily status of your finance is helpful, but can at times be anxiety-driving and serve as a distraction. Therefore, the user experience of **Acropora** will be design such that Users are more focused on their financial goal tracking on a monthly basis. 

This planner will be designed to emphasize the ease of use and clarity of user's current and projected long-term net worth. Risk profile can be applied based on 3 scenarios: constant, bad-case, good-case. Second priority will be given toward features that help remind and guide the weekly or monthly cashflow and assets allocation. Additional tools such as credit card comparison, mortgage schedule, investment return calculator, paid-time off and hybrid days planner, and cost of living comparison will be given third priority. The data used by this software will be entered by the users. Streamlined forms or AI tools may be incorporated to simplify and streamline data entry. Personal data will be securedly stored in a relational database. The software will be built first for browser. Second phase will be developing for mobile app where data will be stored locally, with cloud backup. 

---

## Overall Description
### System Environment   
**Acropora** has two active actors and one cooperating system. The User accesses and updates the financial records and portfolios. Developer adds new financial objects that Users can pick up to their portfolios. 

### Product Functions
This section outlines the use case for each User, whereas Developer will only have one use case. Each use case contains task objective, description of actions, and constraints. These information will be used in planning epic and stories in [Scrum board](https://tree.taiga.io/project/techtana-personal-finance-planner).

### Users Characteristics
User is expected to be Internet literate and has a registered email account. Developer is expected to be familiar with javascript and git versioning for open-source repository.

#### User's Use Case
1. __Task Objective__: User signs up to create their personal account.
   1. __Description of Action__
      1. User clicks on `Sign Up` button.
      2. System asks User for Email address + Password + reCAPTCHA.
      3. User enter information on the form and click `Submit`
      4. System enters new account information into the login database. 
      5. System emails the User notifying that the account has been created.
2. __Task Objective__: User signs into their personal account which retrieves confidential information.   
   1. __Description of Action__
      1. User clicks on `Login` button.  
      2. System asks User for Email address + Password + reCAPTCHA.
      3. User enter information on the form and click `Submit`
      4. System relies on a mongo database to persist user and token data.
      5. System delivers JWT tokens for authentication without a call back to the central service.
      6. System loads `SideNav` bar.
      7. System displays `Overview` page.  
3. __Task Objective__: User finds an overview of their wealth
   1. __Description of Action__
      1. User signs in or click `Overview` button on `SideNav`.
      2. System displays a dashboard showing overview graphs, including:
         1. net worth over time
         2. status of financial goal (customizable)
         3. monthly cashflow over the year
         4. spending breakdown, income breakdown
4. __Task Objective__: User finds a breakdown of their wealth
   1. __Description of Action__
      1. User clicks `Overview` button on `SideNav`.
      2. System displays a dashboard showing overview graphs, including.

---

## Requirements Specification
### Interface Requirements
User will be able to access the web app as a single-page application (SPA) with HistoryAPI-compatible router. This will allow sensible navigation by browser users. 

#### User Interfaces
<img src="./img/signin_page.png" alt="signin_page" width="800"/>  
<img src="./img/signup_page.png" alt="signup_page" width="800"/>  
<img src="./img/overview_page.png" alt="overview_page" width="800"/>  
<img src="./img/budget_page.png" alt="budget_page" width="800"/>  

#### Database Requirements

#### Security Requirements
Users must have access only to their data. All forms must be encrypted to prevent JavaScript injection and unintended interaction with databases.

### Performance Requirements
Average response time on loading each page must not be longer than 10 seconds.

### Functional Requirements
Attribute of FinancialObject:
- Amount
  - Value (Initial value / Final value / Net amount)
  - Modifier (Amortization / Growth rate)
- Frequency
  - Interval (daily, weekly, biweekly, monthly, annual, every N days, )
  - End Period / Date
- Type of assets (Cash, asset, liability)
- Included in Analysis (Show/Hide)
- Nested objects (Show/Hide)

Actions:
  * Duplicate
  * Edit for all period
  * Edit for all periods, after a date
  * Edit for one period only

# Design Splitwise

## Customer User Journeys (CUJs)

* Add Expense
* Edit Expense
* Settle Expense
* Group Management for Group Expenses
* Add Comments in a particular Expense
* Activity Logs in a Group
* Viewing Payment Graph of a particular group

## Additional Functional Requirements

* Same as CUJs

## Non Functional Requirements

* ***Payment Graph Simplification*** to enusre minimum number of transactions
  * Optimized Approach - Calculating the exact minimum count of transactions needed
  * Approximate Approach - Fast Calculation of the minimum count of transactions needed

* ***Concurrency Support***
  
  If a particular user modifies the Payment Graph, and before completion of update another user tries to see the Payment Graph, what shall he/she see ?
  
  For example if userA updates a payment - UserA payed UserB 10$. So the Database must show amount owed by UserA is -10$ and amount owed by UserB is 10$. Now if in DB, only the update for UserA(-10$) has happened and UserA, tries to view the Payment Graph, he/she will see UserA(-10$) and UserB(0$). So, UserA will think, he should get 10$, but from no one. So, this is an inconsistent state of the system. The Consistent State is UserA(-10$) and UserB(10$). So, what shall be shown to UserA ?

  * An inconisistent state - UserA(-10$) and UserB(0$) ; OR
  * A stale state - UserA(0$) and UserB(0$)

  It makes much more sense to show a stale state, as UserA will think the state will be updated in some time.

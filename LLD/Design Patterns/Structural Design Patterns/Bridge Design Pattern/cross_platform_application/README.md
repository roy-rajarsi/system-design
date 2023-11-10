# BRIDGE Design Pattern

An Application can be a Web Backend or a Mobile Application. 
An Application is also associated with different types of responses - Response for Customers (general users) and Response for Admins. 
Instead of coupling these 2 dimensions of an application into one class, according to Bridge Design Pattern, lets delegate the "Response" dimension to a different class. Application class can reference Response Class instances

Need to add UML diagram
bitscramblr
===========
### turn pseudoanonymous bitcoin transactions into anonymous bitcoin transactions
Bitscramblr is an application that allows you to send Bitcoin anonymously. It differs from many mixing services in existence in that a transaction will not be sent until adequately sized inputs are available from another source. Basically what this means is: there is no path from a transaction's origin to its destination.
To illustrate, see a visualization of 5 transactions using **bitscramblr**:

![bitscramblr](http://www.elihickox.com/static/img/good_implementation.png)

Now compare that with a 5 transaction visualization from another comparable Bitcoin mixing service:

![other_mixer](http://www.elihickox.com/static/img/bad_implementation.png)

Notice how you can't trace a line from each transaction's origin to its respective destination? That's the beauty of **bitscramblr**, and it's what keeps **bitscramblr's** users completely anonymous.

meta
----
Distributed under the Apache 2 license with additional terms. See `LICENSE.txt` for more information.
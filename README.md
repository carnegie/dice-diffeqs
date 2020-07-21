# dice-diffeqs

This project is a version of DICE that is very close to the original version of DICE except that the it is written in the form of differential equations, except:
1. The time-integration is separated from the differential equations being advanced in time.
2. The times of decisions are independent of the time steps of the model.

This could was modeled on Nordhaus's code available here: http://www.econ.yale.edu/~nordhaus/homepage/homepage/DICE2016R-091916ap.gms

In addition to this, there are a number of optional enhancements such as ability to also choose to optimize on savings rate in addition to abatement amount.

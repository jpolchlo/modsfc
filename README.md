Simulation of Modular Stock/Flow Consistent Models
==================================================

A salty claim: The dominant paradigm of using equilibrium models to perform economic studies is questionable.  This is not the venue to adjudicate this claim, but it does raise the question: what is a better way to simulate economic activity?

An interesting replacement for equilibrium models is the forward simulation of behavioral equations that describe the localized choices of the agents in the system.  These might be difference or differential equations, but the result is a much richer vocabulary of descriptions and resulting dynamics; there may exist steady state solutions or the results may be chaotic.

The motivation for this package is to write macroeconomic models using this forward simulation strategy, and to specify those models in a modular way, where different sectors can be swapped in and out to test different hypotheses within similar frameworks.  The result should be faster turnaround times on models, greater flexibility for experimentation, and a generally more enjoyable modeling process.

The goal is to make the specification of behavior clearer by casting it as an aggregation of smaller choices based on a more limited set of signals.  For instance, the household sector may act as follows:
1. A wage announcement is received, and that value determines the number of labor hours households want to supply, the value of which is transmitted to the production sector.
2. The income that results from the use of the offered labor is received, as is a tax rate announced by government.  This yields a disposable income.  Disposable income and accumulated wealth combine to produce a total amount of consumption spending that is sent to the production sector.
3. The tax rate combines with income to generate a tax payment remitted to government.
4. Income net of taxation and spending accumulates to a stock of wealth.

In this description, each step is framed as a reaction to information received and may produce output signals/quantities which are consumed by other actors in the model.

We create a complete economic model by composing the behaviors of a set of actors with compatible communication protocols.  The complexity of an individual actor's behaviors is unbounded, but any model that obeys the same collection of received and sent signals can have compatible parts substituted in and out of the same framework.  For example, a more complex producer sector can be a drop-in replacement so long as it announces a wage, consumes labor, receives consumption expenditures, and pays an income.

This approach is in contrast to a more typical specification of a model as a large system of equations that becomes unruly to work with when even modest complexity is achieved.

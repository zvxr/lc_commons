# Lending Club Commons
Collects and stores loan information through Lending Club API over time.

Peer-to-peer loans is a billion dollar industry and an alternative investment opportunity. The
objective as a p2p loans investor is deceptively simple: yield a high return while mitigating risk.
The feedback while investing is quite marginal-- you spread your risk among a various loans in the
form of $25 notes, and collect payments every month. The loans will have an interest associated with
risk of the loan being defaulted on. As a p2p investor, it can be difficult to determine what loans
will have a good return on investment, given the risk of defaulting. It is especially hard to adapt
when each loan is either a 3 or 5 year investment.

Lending Club does provide an API in which many are encouraged to conduct automating the purchasing of
loans. As a billion dollar industry, one of the most common complaints is that the "good" loans are
snatched up quickly. With this in mind, __Lending Club Commons__ aims to provide a means of mining
the 'popularity' of loans, by storing snapshots of all available loans over time. There is a wealth
of variables that could be associated with the "quality" of a loan, such as length of employment or
revolving credit. Their value could be mapped against how quickly loans are satisfied over time
(one that is consumed over hours would be much preferred over one over 14 days). BUT-- this all
begins with collecting the data to be analyzed :).


# Technology



# Repository Layout
```
main/
    celery_tasks/
        app.py
        tasks/
        utils.py
    extractors/
    loaders/
    transformers/
        models/

```

## `celery_tasks/`
This will include Celery application and configuration.

## `extractors/`
Modules responsible for pulling data from external sources.

## `loaders/`
Modules responsible for loading data repository.

## `transformers/`
Task methods responsible for fetching data from external sources.

## `transformers/models/`
Classes for representing data.


# Testing
When running tests as a script, to resolve pythonpath the `-m` switch must be used from top-level
directory.

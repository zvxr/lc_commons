# Lending Club Commons Collects and stores loan information through Lending
Club API over time.

Peer-to-peer loans provides an alternative means of investing money. The
objective when investing is deceptively simple: invest in loans and collect
monthly payments, and mitigate risk of defaulting. The feedback while investing
is quite marginal-- you spread your risk among a various 3 or 5 year loans in
the form of $25 notes, collect payments every month. The loans will have an
interest associated with risk of the loan being defaulted on.

Lending Club does provide an API in which many are encouraged to conduct
automating the purchasing of loans. As a billion dollar industry, one of the
most common complaints is that the "good" loans are snatched up quickly. With
this in mind, __Lending Club Commons__ aims to provide a means of mining the
'popularity' of loans, by storing snapshots of all available loans over time.
There is a wealth of variables that could be associated with the "quality" of a
loan, such as length of employment or revolving credit. Their value could be
mapped against how quickly loans are satisfied over time (one that is consumed
over hours would be much preferred over one over 14 days). BUT-- this all
begins with collecting the data to be analyzed.


## Testing When running tests as a script, to resolve pythonpath the `-m`
switch must be used from top-level directory.

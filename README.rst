Kepler Aerospace REST-ful Services
==================================

The Kepler package consists of a set of REST-ful services intended to provide
common and accessible aerospace-related computational tasks and data access,
including TLE lookup, propagation, and access calculations. These services are
built on top of the *src* framework for scientific REST-ful computation. Each
top-level module within this package defines a different service, and each
service may support a number of operations and/or common data exchange models.

satcat
------

The *satcat* module defines a service for constructing, refreshing, and
querying a satellite catalog. This includes both satcat.Entry objects cached in
a refreshable copy of CelesTrak's satcat table, and direct TLE queries.
